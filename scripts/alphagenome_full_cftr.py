"""
AlphaGenome batch scoring for all 1,278 ambiguous-class CFTR missense variants.

Source: data/cftr_alphamissense.tsv, filtered to am_class == 'ambiguous'
Output: results/alphagenome/alphagenome_full_cftr_results.csv

Features:
  - Batches of BATCH_SIZE variants submitted via score_variants (parallel workers)
  - Checkpoint file: resumes from last completed batch if interrupted
  - Exponential backoff on rate-limit / transient errors
  - Progress reported to stdout

Run from project root:
    .venv/bin/python scripts/alphagenome_full_cftr.py

Estimated runtime: ~20-40 minutes depending on API load.
"""

import os
import sys
import time
import logging
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from alphagenome.data import genome
from alphagenome.models import dna_client
from alphagenome.models import variant_scorers as vsl
import grpc

# ── Config ────────────────────────────────────────────────────────────────────
ROOT        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH_SIZE  = 20          # MAX_VARIANT_SCORERS_PER_REQUEST = 20
MAX_RETRIES = 5
BASE_BACKOFF = 10         # seconds; doubles on each retry
HALF        = dna_client.SEQUENCE_LENGTH_1MB // 2

INPUT_TSV   = os.path.join(ROOT, 'data/cftr_alphamissense.tsv')
OUTPUT_CSV  = os.path.join(ROOT, 'results/alphagenome/alphagenome_full_cftr_results.csv')
CHECKPOINT  = os.path.join(ROOT, 'results/alphagenome/.alphagenome_full_cftr_checkpoint.csv')

SCORERS = [
    vsl.RECOMMENDED_VARIANT_SCORERS['RNA_SEQ'],
    vsl.RECOMMENDED_VARIANT_SCORERS['ATAC'],
    vsl.RECOMMENDED_VARIANT_SCORERS['SPLICE_SITE_USAGE'],
]
ONTOLOGY = 'UBERON:0002048'  # lung — tissue filter applied in post-processing

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

# ── Load API key ──────────────────────────────────────────────────────────────
load_dotenv(os.path.join(ROOT, '.env'))
API_KEY = os.environ.get('ALPHAGENOME_API_KEY', '')
if not API_KEY:
    sys.exit('ERROR: Set ALPHAGENOME_API_KEY in .env')

# ── Load variants ─────────────────────────────────────────────────────────────
log.info('Loading variants from %s', INPUT_TSV)
am = pd.read_csv(INPUT_TSV, sep='\t')
vus = am[am['am_class'] == 'ambiguous'].copy().reset_index(drop=True)
log.info('Ambiguous (VUS-equivalent) variants: %d', len(vus))

# ── Resume from checkpoint ────────────────────────────────────────────────────
completed_ids = set()
if os.path.exists(CHECKPOINT):
    ckpt = pd.read_csv(CHECKPOINT)
    completed_ids = set(ckpt['variant_id'].tolist())
    log.info('Resuming — %d variants already completed', len(completed_ids))

def variant_id(row):
    return f"{row['CHROM']}:{row['POS']}:{row['REF']}>{row['ALT']}"

vus['_vid'] = vus.apply(variant_id, axis=1)
remaining = vus[~vus['_vid'].isin(completed_ids)].reset_index(drop=True)
log.info('Remaining to score: %d', len(remaining))

if len(remaining) == 0:
    log.info('All variants already scored. Building final output.')

# ── Connect ───────────────────────────────────────────────────────────────────
log.info('Connecting to AlphaGenome API...')
model = dna_client.create(API_KEY)
log.info('Connected.')

# ── Batch scoring with retry ──────────────────────────────────────────────────
def score_batch(batch_df):
    """Score a batch of variants. Returns tidy DataFrame or raises on unrecoverable error."""
    variants = [
        genome.Variant(chromosome=r['CHROM'], position=int(r['POS']),
                       reference_bases=r['REF'], alternate_bases=r['ALT'])
        for _, r in batch_df.iterrows()
    ]
    intervals = [
        genome.Interval(chromosome=r['CHROM'],
                        start=int(r['POS']) - HALF,
                        end=int(r['POS']) + HALF)
        for _, r in batch_df.iterrows()
    ]
    raw = model.score_variants(
        intervals=intervals,
        variants=variants,
        variant_scorers=SCORERS,
        progress_bar=False,
    )
    return vsl.tidy_scores(raw)


def extract_lung_summary(tidy_df, batch_df):
    """Extract per-variant lung quantile scores from tidy DataFrame."""
    lung = tidy_df[tidy_df['ontology_curie'] == ONTOLOGY].copy()

    rows = []
    for _, r in batch_df.iterrows():
        vid = f"{r['CHROM']}:{r['POS']}:{r['REF']}>{r['ALT']}"
        # Match rows by position string in variant_id
        vdf = lung[lung['variant_id'].astype(str).str.contains(str(r['POS']), regex=False)]

        row = {
            'variant_id':       vid,
            'CHROM':            r['CHROM'],
            'POS':              r['POS'],
            'REF':              r['REF'],
            'ALT':              r['ALT'],
            'protein_variant':  r['protein_variant'],
            'am_pathogenicity': r['am_pathogenicity'],
            'am_class':         r['am_class'],
        }
        for otype in ['RNA_SEQ', 'ATAC', 'SPLICE_SITE_USAGE']:
            odf = vdf[vdf['output_type'] == otype]
            if len(odf) and 'quantile_score' in odf.columns and odf['quantile_score'].notna().any():
                row[f'{otype}_raw_max']      = float(odf['raw_score'].abs().max())
                row[f'{otype}_quantile_max'] = float(odf['quantile_score'].abs().max())
            else:
                row[f'{otype}_raw_max']      = np.nan
                row[f'{otype}_quantile_max'] = np.nan
        rows.append(row)
    return pd.DataFrame(rows)


# ── Main loop ─────────────────────────────────────────────────────────────────
n_batches = (len(remaining) + BATCH_SIZE - 1) // BATCH_SIZE
log.info('Processing %d variants in %d batches of %d', len(remaining), n_batches, BATCH_SIZE)

all_results = []
for batch_num, batch_start in enumerate(range(0, len(remaining), BATCH_SIZE), 1):
    batch = remaining.iloc[batch_start : batch_start + BATCH_SIZE]
    log.info('Batch %d/%d  (variants %d-%d)', batch_num, n_batches,
             batch_start + 1, min(batch_start + BATCH_SIZE, len(remaining)))

    backoff = BASE_BACKOFF
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            tidy = score_batch(batch)
            summary = extract_lung_summary(tidy, batch)
            all_results.append(summary)

            # Append to checkpoint
            summary.to_csv(CHECKPOINT, mode='a',
                           header=not os.path.exists(CHECKPOINT) or os.path.getsize(CHECKPOINT) == 0,
                           index=False)
            break

        except grpc.RpcError as e:
            code = e.code()
            if code in (grpc.StatusCode.RESOURCE_EXHAUSTED, grpc.StatusCode.UNAVAILABLE):
                log.warning('Rate limit / unavailable (attempt %d/%d). Sleeping %ds...',
                            attempt, MAX_RETRIES, backoff)
                time.sleep(backoff)
                backoff = min(backoff * 2, 300)
            elif code == grpc.StatusCode.INVALID_ARGUMENT:
                log.error('Invalid argument on batch %d — skipping: %s', batch_num, e.details())
                break
            else:
                log.error('gRPC error %s on batch %d (attempt %d): %s',
                          code, batch_num, attempt, e.details())
                if attempt == MAX_RETRIES:
                    log.error('Max retries reached — skipping batch %d', batch_num)
                time.sleep(backoff)
                backoff = min(backoff * 2, 300)

        except Exception as e:
            log.error('Unexpected error on batch %d (attempt %d): %s', batch_num, attempt, e)
            if attempt == MAX_RETRIES:
                log.error('Giving up on batch %d', batch_num)
            time.sleep(backoff)
            backoff = min(backoff * 2, 300)

# ── Consolidate ────────────────────────────────────────────────────────────────
log.info('Consolidating results...')

# Merge new results with any previously checkpointed results
if os.path.exists(CHECKPOINT):
    ckpt_df = pd.read_csv(CHECKPOINT)
    if all_results:
        new_df = pd.concat(all_results, ignore_index=True)
        final_df = pd.concat([ckpt_df, new_df], ignore_index=True)
    else:
        final_df = ckpt_df
else:
    final_df = pd.concat(all_results, ignore_index=True) if all_results else pd.DataFrame()

# Deduplicate (in case of partial reruns)
final_df = final_df.drop_duplicates(subset='variant_id').reset_index(drop=True)

# Sort by strongest ATAC quantile signal descending
if 'ATAC_quantile_max' in final_df.columns:
    final_df = final_df.sort_values('ATAC_quantile_max', ascending=False)

final_df.to_csv(OUTPUT_CSV, index=False)
log.info('Saved %d variant results to %s', len(final_df), OUTPUT_CSV)

# ── Summary ───────────────────────────────────────────────────────────────────
print('\n=== Summary ===')
print(f'Total variants scored: {len(final_df)}')
for col in ['RNA_SEQ_quantile_max', 'ATAC_quantile_max', 'SPLICE_SITE_USAGE_quantile_max']:
    if col in final_df.columns:
        print(f'{col}: mean={final_df[col].mean():.3f}  '
              f'p95={final_df[col].quantile(0.95):.3f}  '
              f'max={final_df[col].max():.3f}')

print('\nTop 10 by ATAC quantile:')
cols = ['protein_variant', 'am_pathogenicity', 'ATAC_quantile_max', 'SPLICE_SITE_USAGE_quantile_max', 'RNA_SEQ_quantile_max']
cols = [c for c in cols if c in final_df.columns]
print(final_df.head(10)[cols].to_string(index=False))

print(f'\nDone. Output: {OUTPUT_CSV}')
# Clean up checkpoint now that we have a final output
if os.path.exists(CHECKPOINT):
    os.remove(CHECKPOINT)
    log.info('Checkpoint removed.')
