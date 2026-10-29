"""
Fetch CADD v1.7 PHRED scores for the 292 binary CFTR variants.

Saves raw API responses to results/phase1/inputs_cadd_raw.json (one JSON
object per variant, keyed by variant name) before parsing. Parsed scores
are written to results/phase1/inputs_cadd_scores.csv.

Run ONCE; re-running will overwrite both files.

Source: CADD v1.7 GRCh38 REST API — https://cadd.gs.washington.edu/api

Changed 2026-10-29 (docs/AUDIT_RECORD.md, Corrections 14):
  - Coordinates come from the VCF line whose first HGVSp token is the
    complete missense name (scripts/hgvsp_names.py). The old rule could take
    the coordinates of a frameshift whose truncated name matched.
  - --reuse PATH reads an earlier inputs_cadd_raw.json. A variant whose
    coordinates are unchanged and whose earlier query returned HTTP 200 keeps
    that response; only changed or new coordinates are queried. Every entry
    records query_date: the UTC date for a new query, or
    "not recorded (reused from earlier run)".
  - The script refuses to overwrite existing outputs; archive them first.
"""

import os, re, json, time, logging, sys, argparse
import csv
from datetime import datetime, timezone
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hgvsp_names import name_from_line  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR      = os.path.join(ROOT, 'results', 'phase1')
ANNOT_CSV    = os.path.join(ROOT, 'data', 'cftr2_results_annotated.csv')
VCF_PATH     = os.path.join(ROOT, 'data', 'All_Variants_VEP.Gene.vcf')
RAW_JSON     = os.path.join(ROOT, 'results', 'phase1', 'inputs_cadd_raw.json')
SCORES_CSV   = os.path.join(ROOT, 'results', 'phase1', 'inputs_cadd_scores.csv')

CADD_URL    = 'https://cadd.gs.washington.edu/api/v1.0/GRCh38-v1.7/{chrom}:{pos}_{ref}_{alt}'
REQUEST_DELAY = 0.35   # seconds between requests to respect rate limit

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

os.makedirs(OUT_DIR, exist_ok=True)

_ap = argparse.ArgumentParser()
_ap.add_argument('--reuse', help='earlier inputs_cadd_raw.json to reuse for unchanged coordinates')
_args = _ap.parse_args()
for _p in (RAW_JSON, SCORES_CSV):
    if os.path.exists(_p):
        sys.exit(f'ERROR: {_p} exists. Archive it before rerunning.')
previous = json.load(open(_args.reuse)) if _args.reuse else {}
TODAY = datetime.now(timezone.utc).strftime('%Y-%m-%d')
n_reused = n_queried = 0

# ── Load 292 binary variants ──────────────────────────────────────────────────
with open(ANNOT_CSV) as f:
    annotated = list(csv.DictReader(f))

binary = [r for r in annotated
          if r['determination_2026'] in ('CF-causing', 'Non CF-causing')
          and r['am_pathogenicity']]
log.info('Binary variants: %d', len(binary))

# ── Extract genomic coordinates from VCF ─────────────────────────────────────
coords = {}

with open(VCF_PATH, encoding='utf-8', errors='replace') as fh:
    for line in fh:
        if line.startswith('#'):
            continue
        parts = line.rstrip('\n').split('\t')
        if len(parts) < 5:
            continue
        chrom, pos, _, ref, alt = parts[0], parts[1], parts[2], parts[3], parts[4]
        name = name_from_line(line)
        if name and name not in coords:
            coords[name] = {'chrom': chrom, 'pos': pos, 'ref': ref, 'alt': alt}

log.info('VCF coordinates extracted: %d unique protein variants', len(coords))

# ── Fetch CADD scores ─────────────────────────────────────────────────────────
def fetch_cadd(chrom, pos, ref, alt):
    url = CADD_URL.format(chrom=chrom, pos=pos, ref=ref, alt=alt)
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            return resp.status_code, data
        return resp.status_code, []
    except Exception as e:
        return 0, {'error': str(e)}

raw_responses = {}
scores_out = []
no_coord = []
no_cadd = []

for i, row in enumerate(binary, 1):
    variant_name = row['variant']   # three-letter format: Ser13Phe
    # The VCF uses three-letter format matching cftr2_results_annotated.csv variant column
    coord = coords.get(variant_name)

    if coord is None:
        no_coord.append(variant_name)
        raw_responses[variant_name] = {'error': 'no_vcf_coordinate'}
        scores_out.append({'variant': variant_name,
                           'determination_2026': row['determination_2026'],
                           'am_pathogenicity': row['am_pathogenicity'],
                           'cadd_phred': '',
                           'exclusion_reason': 'no_vcf_coordinate'})
        continue

    prior = previous.get(variant_name) or {}
    if variant_name in raw_responses:
        status, data = raw_responses[variant_name]['status'], raw_responses[variant_name]['data']
    elif prior.get('coord') == coord and prior.get('status') == 200:
        status, data = prior['status'], prior['data']
        raw_responses[variant_name] = {'status': status, 'data': data, 'coord': coord,
                                        'query_date': prior.get('query_date',
                                                                'not recorded (reused from earlier run)')}
        n_reused += 1
    else:
        status, data = fetch_cadd(coord['chrom'], coord['pos'], coord['ref'], coord['alt'])
        raw_responses[variant_name] = {'status': status, 'data': data,
                                        'coord': coord, 'query_date': TODAY}
        n_queried += 1
        time.sleep(REQUEST_DELAY)

    phred = None
    if status == 200 and isinstance(data, list) and len(data) > 0:
        entry = data[0]
        if isinstance(entry, dict) and 'PHRED' in entry:
            phred = float(entry['PHRED'])

    if phred is None:
        no_cadd.append(variant_name)
        reason = f'cadd_api_no_score_http{status}'
    else:
        reason = ''

    scores_out.append({'variant': variant_name,
                       'determination_2026': row['determination_2026'],
                       'am_pathogenicity': row['am_pathogenicity'],
                       'cadd_phred': phred if phred is not None else '',
                       'exclusion_reason': reason})

    if i % 20 == 0:
        log.info('  %d / %d done', i, len(binary))

log.info('CADD fetch complete. Scored: %d / %d  No coord: %d  No score: %d  '
         'Reused: %d  Queried %s: %d',
         sum(1 for r in scores_out if r['cadd_phred'] != ''),
         len(binary), len(no_coord), len(no_cadd), n_reused, TODAY, n_queried)

# ── Save raw responses ─────────────────────────────────────────────────────────
with open(RAW_JSON, 'w') as f:
    json.dump(raw_responses, f, indent=2)
log.info('Raw responses saved to %s', RAW_JSON)

# ── Save parsed scores ─────────────────────────────────────────────────────────
with open(SCORES_CSV, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['variant', 'determination_2026',
                                           'am_pathogenicity', 'cadd_phred',
                                           'exclusion_reason'])
    writer.writeheader()
    writer.writerows(scores_out)
log.info('Parsed CADD scores saved to %s', SCORES_CSV)

if no_coord:
    log.warning('No VCF coordinate for: %s', no_coord)
if no_cadd:
    log.warning('No CADD score for: %s', no_cadd)
