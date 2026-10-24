"""
Unique-variant counts for Phase 1 sets (paper-prep, October 2026).

Why this exists:
  data/cftr2_results_annotated.csv is the product of a one-to-many merge of
  data/cftr2_results.csv (3,220 unique protein changes) onto
  data/cftr_alphamissense.tsv (9,721 rows; several genomic SNVs can encode the
  same protein change). Row counts from the annotated file therefore exceed
  unique-variant counts. Several documents reported row counts as variant
  counts (audit truth check, 2026-10-24). This script recounts every affected
  set as unique protein variants and records both numbers side by side.

Deduplication key: column `variant` (three-letter HGVS protein change without
the `p.` prefix, e.g. Ser13Phe). This is the key on which the original merge
was performed and the key used for the n=259 benchmark in
results/phase1/am_validation_metrics.csv. Keep-first is used where a
representative row is needed; counts do not depend on which duplicate is kept.

Inputs (must exist on disk):
  data/cftr2_results_annotated.csv
  data/nonsense_variants_cftr2.csv
  data/priority_candidates.csv
  data/varying_consequence_am.csv

Output:
  results/phase1/unique_variant_counts.csv
    columns: set_name, filter, unique_count, row_count, differs,
             dedup_key, source_file
"""

import os, csv, logging
from collections import Counter, OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANNOT_CSV    = os.path.join(ROOT, 'data', 'cftr2_results_annotated.csv')
NONSENSE_CSV = os.path.join(ROOT, 'data', 'nonsense_variants_cftr2.csv')
PRIORITY_CSV = os.path.join(ROOT, 'data', 'priority_candidates.csv')
VCC_CSV      = os.path.join(ROOT, 'data', 'varying_consequence_am.csv')
OUT_CSV      = os.path.join(ROOT, 'results', 'phase1', 'unique_variant_counts.csv')

DEDUP_KEY = 'variant'

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)


def read(path):
    with open(path, newline='') as f:
        return list(csv.DictReader(f))


def count(rows, key=DEDUP_KEY):
    """Return (unique_count, row_count) for a list of rows."""
    return len({r[key] for r in rows}), len(rows)


annotated = read(ANNOT_CSV)
nonsense  = read(NONSENSE_CSV)
priority  = read(PRIORITY_CSV)
vcc_file  = read(VCC_CSV)
log.info('annotated rows=%d  nonsense rows=%d  priority rows=%d  vcc rows=%d',
         len(annotated), len(nonsense), len(priority), len(vcc_file))

out = []


def add(set_name, flt, rows, source, key=DEDUP_KEY):
    u, n = count(rows, key)
    out.append(OrderedDict([
        ('set_name', set_name),
        ('filter', flt),
        ('unique_count', u),
        ('row_count', n),
        ('differs', 'YES' if u != n else 'no'),
        ('dedup_key', key),
        ('source_file', source),
    ]))
    log.info('%-45s unique=%5d rows=%5d %s', set_name, u, n, 'DIFFERS' if u != n else '')


A = 'data/cftr2_results_annotated.csv'

# ── Whole annotated table ────────────────────────────────────────────────────
add('annotated_table_all', 'all rows', annotated, A)
add('am_variant_converted', "am_variant != ''",
    [r for r in annotated if r.get('am_variant')], A)
add('am_variant_not_converted', "am_variant == ''",
    [r for r in annotated if not r.get('am_variant')], A)
add('am_scored_any_cftr2_status', "am_pathogenicity != ''",
    [r for r in annotated if r['am_pathogenicity']], A)

# ── CFTR2 determination categories (whole table) ────────────────────────────
for det in ['CF-causing', 'Non CF-causing', 'Varying clinical consequence',
            'No interpretation available']:
    add(f'cftr2_{det.replace(" ", "_")}', f"determination_2026 == '{det}'",
        [r for r in annotated if r['determination_2026'] == det], A)
add('cftr2_unclassified', "determination_2026 == ''",
    [r for r in annotated if not r['determination_2026']], A)

# ── Binary validation set ────────────────────────────────────────────────────
binary = [r for r in annotated
          if r['determination_2026'] in ('CF-causing', 'Non CF-causing')
          and r['am_pathogenicity']]
add('binary_validation_set', "determination in {CF-causing, Non CF-causing} and am_pathogenicity != ''",
    binary, A)
add('binary_validation_CF_causing', "as above, CF-causing",
    [r for r in binary if r['determination_2026'] == 'CF-causing'], A)
add('binary_validation_Non_CF_causing', "as above, Non CF-causing",
    [r for r in binary if r['determination_2026'] == 'Non CF-causing'], A)

# ── Unclassified (no CFTR2 determination) with AM score ─────────────────────
unclass = [r for r in annotated if not r['determination_2026'] and r['am_pathogenicity']]
add('unclassified_am_scored', "determination_2026 == '' and am_pathogenicity != ''", unclass, A)
for cls in ['likely_pathogenic', 'ambiguous', 'likely_benign']:
    add(f'unclassified_{cls}', f"as above, am_class == '{cls}'",
        [r for r in unclass if r['am_class'] == cls], A)

# ── Priority 7 (retracted selection; counts only) ───────────────────────────
add('unclassified_LP_with_vcf_AF_TGP', "rows of data/priority_candidates.csv",
    priority, 'data/priority_candidates.csv')

# ── VCC: annotated table vs the 72-row file ─────────────────────────────────
vcc_ann = [r for r in annotated if r['determination_2026'] == 'Varying clinical consequence']
add('vcc_in_annotated_table', "determination_2026 == 'Varying clinical consequence'", vcc_ann, A)
add('vcc_file', 'all rows', vcc_file, 'data/varying_consequence_am.csv')
for cls in ['likely_pathogenic', 'ambiguous', 'likely_benign']:
    add(f'vcc_file_{cls}', f"am_class == '{cls}'",
        [r for r in vcc_file if r['am_class'] == cls], 'data/varying_consequence_am.csv')

# ── Nonsense / stop-loss set (the 311 that failed three-to-one conversion) ──
N = 'data/nonsense_variants_cftr2.csv'
add('ter_set_all', 'all rows', nonsense, N)
add('ter_set_nonsense_Ter_suffix', "variant endswith 'Ter'",
    [r for r in nonsense if r['variant'].endswith('Ter')], N)
add('ter_set_stop_loss_Ter_prefix', "variant startswith 'Ter' (stop-loss)",
    [r for r in nonsense if r['variant'].startswith('Ter')], N)
add('ter_set_matched_cftr2', "determination_2026 != ''",
    [r for r in nonsense if r['determination_2026']], N)
for det in ['CF-causing', 'Varying clinical consequence', 'No interpretation available']:
    add(f'ter_set_{det.replace(" ", "_")}', f"determination_2026 == '{det}'",
        [r for r in nonsense if r['determination_2026'] == det], N)
add('ter_set_no_cftr2_record', "determination_2026 == ''",
    [r for r in nonsense if not r['determination_2026']], N)

# ── Save ─────────────────────────────────────────────────────────────────────
with open(OUT_CSV, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
    w.writeheader()
    w.writerows(out)
log.info('Saved %s (%d rows)', OUT_CSV, len(out))

print('\nSets where unique and row counts differ:')
for r in out:
    if r['differs'] == 'YES':
        print(f"  {r['set_name']:<40} unique={r['unique_count']:<5} rows={r['row_count']}")
