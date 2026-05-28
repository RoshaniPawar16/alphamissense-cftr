"""
Extract quantile scores for the 7 CFTR variants using AlphaGenome score_variants API.
Adds quantile_score columns to the existing batch results and updates the markdown report.
Run from project root: .venv/bin/python scripts/alphagenome_quantile_scores.py
"""

import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from alphagenome.data import genome
from alphagenome.models import dna_client
from alphagenome.models import variant_scorers as vsl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(ROOT, '.env'))
API_KEY = os.environ.get('ALPHAGENOME_API_KEY', '')
if not API_KEY:
    raise RuntimeError("Set ALPHAGENOME_API_KEY in .env")

VARIANTS_META = [
    dict(label='Leu49Pro',   protein='L49P',   chrom='chr7', pos=117_504_345, ref='T', alt='C', am=0.9757),
    dict(label='Arg104Gly',  protein='R104G',  chrom='chr7', pos=117_530_935, ref='A', alt='G', am=0.8448),
    dict(label='Pro355Leu',  protein='P355L',  chrom='chr7', pos=117_540_294, ref='C', alt='T', am=0.8580),
    dict(label='Phe650Leu',  protein='F650L',  chrom='chr7', pos=117_592_115, ref='T', alt='C', am=0.8455),
    dict(label='Leu986Pro',  protein='L986P',  chrom='chr7', pos=117_606_722, ref='T', alt='C', am=0.8685),
    dict(label='His1054Gln', protein='H1054Q', chrom='chr7', pos=117_611_603, ref='T', alt='G', am=0.9010),
    dict(label='Arg1097Cys', protein='R1097C', chrom='chr7', pos=117_611_730, ref='C', alt='T', am=0.6513),
]

ONTOLOGY_TERMS = ['UBERON:0002048']  # lung
HALF = dna_client.SEQUENCE_LENGTH_1MB // 2

SCORERS = [
    vsl.RECOMMENDED_VARIANT_SCORERS['RNA_SEQ'],
    vsl.RECOMMENDED_VARIANT_SCORERS['ATAC'],
    vsl.RECOMMENDED_VARIANT_SCORERS['SPLICE_SITE_USAGE'],
]

print("Connecting to AlphaGenome API...")
model = dna_client.create(API_KEY)
print("Connected.\n")

# Build variant + interval objects
variants = [
    genome.Variant(chromosome=v['chrom'], position=v['pos'],
                   reference_bases=v['ref'], alternate_bases=v['alt'])
    for v in VARIANTS_META
]
intervals = [
    genome.Interval(chromosome=v['chrom'], start=v['pos'] - HALF, end=v['pos'] + HALF)
    for v in VARIANTS_META
]

print(f"Scoring {len(variants)} variants with scorers: {[s.name for s in SCORERS]}")
print("(This may take 2-5 minutes...)\n")

raw_scores = model.score_variants(
    intervals=intervals,
    variants=variants,
    variant_scorers=SCORERS,
)

# Tidy into a DataFrame
scores_df = vsl.tidy_scores(raw_scores)
print("Score columns:", list(scores_df.columns))
print(f"Total rows: {len(scores_df)}\n")

# Filter to lung tracks only
lung_df = scores_df[scores_df['ontology_curie'] == 'UBERON:0002048'].copy()
print(f"Lung tracks: {len(lung_df)} rows\n")

# For each variant × output_type, take the track with the highest |quantile_score|
# (most impactful track per output type)
def best_quantile(group):
    if 'quantile_score' in group.columns and group['quantile_score'].notna().any():
        idx = group['quantile_score'].abs().idxmax()
        return group.loc[idx, 'quantile_score']
    return np.nan

def best_raw(group):
    idx = group['raw_score'].abs().idxmax()
    return group.loc[idx, 'raw_score']

# Parse variant_id back to our labels
def parse_label(variant_id):
    # variant_id may be a Variant object or a string like chr7:117504345:T>C
    vid = str(variant_id)
    for v in VARIANTS_META:
        if str(v['pos']) in vid:
            return v['label']
    return vid

lung_df['variant_label'] = lung_df['variant_id'].apply(parse_label)

summary_rows = []
for v in VARIANTS_META:
    vdf = lung_df[lung_df['variant_label'] == v['label']]
    row = {'Variant': v['label'], 'Protein': v['protein'], 'AM_score': v['am']}
    for otype in ['RNA_SEQ', 'ATAC', 'SPLICE_SITE_USAGE']:
        odf = vdf[vdf['output_type'] == otype]
        if len(odf) == 0:
            row[f'{otype}_raw']      = np.nan
            row[f'{otype}_quantile'] = np.nan
        else:
            row[f'{otype}_raw']      = float(odf['raw_score'].abs().max())
            row[f'{otype}_quantile'] = float(odf['quantile_score'].abs().max()) if 'quantile_score' in odf.columns and odf['quantile_score'].notna().any() else np.nan
    summary_rows.append(row)

quantile_df = pd.DataFrame(summary_rows)
print("Quantile score summary:")
print(quantile_df.to_string(index=False))

# ── Merge with existing batch results ─────────────────────────────────────────
existing = pd.read_csv(os.path.join(ROOT, 'results/alphagenome/alphagenome_batch_results.csv'))
merged = existing.merge(
    quantile_df[['Variant', 'RNA_SEQ_raw', 'RNA_SEQ_quantile',
                             'ATAC_raw',    'ATAC_quantile',
                             'SPLICE_SITE_USAGE_raw', 'SPLICE_SITE_USAGE_quantile']],
    on='Variant', how='left'
)
merged.to_csv(os.path.join(ROOT, 'results/alphagenome/alphagenome_batch_results.csv'), index=False)
print("\nUpdated results saved to results/alphagenome/alphagenome_batch_results.csv")

# ── Save full tidy scores ──────────────────────────────────────────────────────
lung_df.to_csv(os.path.join(ROOT, 'results/alphagenome/alphagenome_quantile_scores_raw.csv'), index=False)
print("Full tidy scores saved to results/alphagenome/alphagenome_quantile_scores_raw.csv")

# ── Build updated markdown report ─────────────────────────────────────────────
atac_ranked   = quantile_df.sort_values('ATAC_quantile',              ascending=False)
splice_ranked = quantile_df.sort_values('SPLICE_SITE_USAGE_quantile', ascending=False)

md = []
md += [
    "# AlphaGenome Batch Analysis: 7 Unclassified CFTR Variants",
    "",
    "**Model:** AlphaGenome v0.6.1  |  **Genome:** hg38  |  **Tissue:** Lung (UBERON:0002048)",
    "**Outputs scored:** RNA-seq (`GeneMaskLFCScorer`), ATAC-seq (`CenterMaskScorer` 501 bp), Splice site usage (`GeneMaskSplicingScorer`)",
    "**Window:** 1 Mb centred on variant  |  **Scores:** raw + quantile (normalised rank across all human variants)",
    "",
    "---",
    "",
    "## Variants",
    "",
    "| Variant | Protein | hg38 Position | REF>ALT | AlphaMissense |",
    "|---------|---------|---------------|---------|---------------|",
]
for v in VARIANTS_META:
    md.append(f"| {v['label']} | {v['protein']} | chr7:{v['pos']:,} | {v['ref']}>{v['alt']} | {v['am']} |")

md += [
    "",
    "---",
    "",
    "## Score Summary",
    "",
    "**Quantile score**: normalised rank of the variant effect relative to all human variants for that output type.  ",
    "A quantile of 0.99 means the variant's effect is larger than 99% of all scored variants — tissue-specific.",
    "",
    "| Variant | AM | RNA raw | RNA q | ATAC raw | ATAC q | Splice raw | Splice q |",
    "|---------|-----|---------|-------|----------|--------|------------|----------|",
]
for _, r in quantile_df.iterrows():
    md.append(
        f"| {r['Variant']} | {r['AM_score']} "
        f"| {r['RNA_SEQ_raw']:.4f} | {r['RNA_SEQ_quantile']:.3f} "
        f"| {r['ATAC_raw']:.4f} | {r['ATAC_quantile']:.3f} "
        f"| {r['SPLICE_SITE_USAGE_raw']:.4f} | {r['SPLICE_SITE_USAGE_quantile']:.3f} |"
    )

md += [
    "",
    "---",
    "",
    "## Ranked by ATAC Quantile Score",
    "",
    "| Rank | Variant | AM Score | ATAC Quantile | ATAC Raw | Bins >0.5 | Flag |",
    "|------|---------|----------|---------------|----------|-----------|------|",
]
prev_bins = dict(zip(existing['Variant'], existing.get('atac_bins_gt05', pd.Series(dtype=int))))
for rank, (_, r) in enumerate(atac_ranked.iterrows(), 1):
    flag = "🔴 top regulatory signal" if r['ATAC_quantile'] >= 0.95 else ("🟡 moderate" if r['ATAC_quantile'] >= 0.80 else "⚪ low")
    bins = prev_bins.get(r['Variant'], 'n/a')
    md.append(f"| {rank} | {r['Variant']} | {r['AM_score']} | {r['ATAC_quantile']:.3f} | {r['ATAC_raw']:.4f} | {bins} | {flag} |")

md += [
    "",
    "---",
    "",
    "## Ranked by Splice Quantile Score",
    "",
    "| Rank | Variant | AM Score | Splice Quantile | Splice Raw | Bins >0.5 | Flag |",
    "|------|---------|----------|-----------------|------------|-----------|------|",
]
prev_splice_bins = dict(zip(existing['Variant'], existing.get('splice_bins_gt05', pd.Series(dtype=int))))
for rank, (_, r) in enumerate(splice_ranked.iterrows(), 1):
    flag = "🔴 cryptic splice risk" if r['SPLICE_SITE_USAGE_quantile'] >= 0.95 else ("🟡 moderate" if r['SPLICE_SITE_USAGE_quantile'] >= 0.80 else "⚪ low")
    bins = prev_splice_bins.get(r['Variant'], 'n/a')
    md.append(f"| {rank} | {r['Variant']} | {r['AM_score']} | {r['SPLICE_SITE_USAGE_quantile']:.3f} | {r['SPLICE_SITE_USAGE_raw']:.4f} | {bins} | {flag} |")

md += [
    "",
    "---",
    "",
    "## Interpretation",
    "",
    "### What quantile scores add over raw log2FC",
    "",
    "Raw log2FC measures the absolute signal change at a locus. Quantile scores normalise this against the genome-wide distribution of variant effects for that output type, making scores comparable across output types and variants.",
    "",
    "- **Quantile ≥ 0.95**: variant effect is in the top 5% of all human variants for that tissue/output — strong evidence of functional impact beyond protein-level effect.",
    "- **Quantile 0.80–0.95**: notable but not extreme — warrants further investigation.",
    "- **Quantile < 0.80**: effect is within typical background variation.",
    "",
    "### What AlphaMissense misses",
    "",
    "AlphaMissense scores protein-level pathogenicity only. High quantile scores on ATAC or splice outputs identify variants with regulatory or splicing mechanisms that protein-sequence models cannot detect.",
    "",
]

top_atac   = atac_ranked.iloc[0]
top_splice = splice_ranked.iloc[0]
r1097c     = quantile_df[quantile_df['Protein'] == 'R1097C'].iloc[0]

md += [
    f"- **{top_atac['Variant']}** — ATAC quantile {top_atac['ATAC_quantile']:.3f}: strongest chromatin accessibility signal. "
    f"AlphaMissense {top_atac['AM_score']} — regulatory disruption may contribute independently of protein misfolding.",
    "",
    f"- **{top_splice['Variant']}** — Splice quantile {top_splice['SPLICE_SITE_USAGE_quantile']:.3f}: highest splicing impact. "
    f"AlphaMissense score {top_splice['AM_score']} captures protein effect but not this splicing mechanism.",
    "",
    f"- **Arg1097Cys** — lowest AlphaMissense score (0.6513). "
    f"ATAC quantile {r1097c['ATAC_quantile']:.3f}, splice quantile {r1097c['SPLICE_SITE_USAGE_quantile']:.3f}. "
    f"If either is elevated, it provides a regulatory/splicing explanation for pathogenicity that protein scoring alone does not.",
    "",
    "---",
    "",
    "*AlphaGenome v0.6.1 · hg38 · Lung UBERON:0002048 · 2026-05-28*",
]

report = "\n".join(md)
with open(os.path.join(ROOT, 'docs/alphagenome_batch_report.md'), 'w') as f:
    f.write(report)
print("\nUpdated markdown saved to docs/alphagenome_batch_report.md")

print("\n=== Final table ===")
print(quantile_df[['Variant','AM_score','RNA_SEQ_quantile','ATAC_quantile','SPLICE_SITE_USAGE_quantile']].to_string(index=False))
