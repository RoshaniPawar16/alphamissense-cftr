"""
Build the AlphaMissense-annotated inventory and its derived tables.

Reproducible script version of notebooks/alphamissense.ipynb cells 8-9
(annotation), 11-12 (flagged unclassified), 15 (flagged with CFTR2
frequency), 17-19 (priority candidates; retracted selection, kept because
results/phase1/unique_variant_counts.csv counts it), 21-22 (varying clinical
consequence) and 30-36 (nonsense variants).

Added 2026-10-29 (docs/AUDIT_RECORD.md, Corrections 14). The per-transcript
allele-frequency lookup of cell 17 uses the fixed rule in scripts/hgvsp_names.py,
so a truncated HGVSp token no longer gives its frequency to a missense name.

Inputs : data/cftr2_results.csv (scripts/cftr2_scraper_analysis.py),
         data/cftr_alphamissense.tsv, data/cftr2_variants.xlsx,
         data/All_Variants_VEP.Gene.vcf
Outputs: data/cftr2_results_annotated.csv, data/flagged_unclassified.csv,
         data/flagged_prioritised.csv, data/priority_candidates.csv,
         data/varying_consequence_am.csv, data/nonsense_variants_cftr2.csv
         (written to --out-dir; default data/)

Usage:
    python scripts/build_annotated_tables.py [--inventory PATH] [--out-dir DIR] [--old-rule]
"""

import argparse
import os
import re
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hgvsp_names import name_from_hgvsp_field  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')
AA3TO1 = {'Ala': 'A', 'Arg': 'R', 'Asn': 'N', 'Asp': 'D', 'Cys': 'C', 'Glu': 'E', 'Gln': 'Q',
          'Gly': 'G', 'His': 'H', 'Ile': 'I', 'Leu': 'L', 'Lys': 'K', 'Met': 'M', 'Phe': 'F',
          'Pro': 'P', 'Ser': 'S', 'Thr': 'T', 'Trp': 'W', 'Tyr': 'Y', 'Val': 'V'}
CFTR2_COLUMNS = ['legacy_name', 'protein_name', 'cdna_name', 'alt_names', 'alleles_count',
                 'allele_frequency', 'determination_2024', 'determination_2026', 'change']
AF_INDEX = 34   # CSQ AF field (1000 Genomes Phase 3), notebook cell 17
CSQ_RE = re.compile(r'CSQ=([^;]+)')


def three_to_one(variant):
    """Convert Ser13Phe to S13F; None if either residue is not standard (cell 8)."""
    m = re.match(r'([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2})', variant)
    if not m or m.group(1) not in AA3TO1 or m.group(3) not in AA3TO1:
        return None
    return f"{AA3TO1[m.group(1)]}{m.group(2)}{AA3TO1[m.group(3)]}"


def vcf_af(fixed: bool) -> dict:
    """Largest AF per protein-change name across CSQ transcripts (cell 17)."""
    af = {}
    with open(os.path.join(DATA, 'All_Variants_VEP.Gene.vcf'), encoding='utf-8', errors='replace') as fh:
        for line in fh:
            if line.startswith('#'):
                continue
            m = CSQ_RE.search(line)
            if not m:
                continue
            for tx in m.group(1).split(','):
                f = tx.split('|')
                if len(f) <= AF_INDEX:
                    continue
                name = name_from_hgvsp_field(f[11], fixed=fixed)
                if not name or not f[AF_INDEX] or f[AF_INDEX] == '.':
                    continue
                try:
                    v = float(f[AF_INDEX])
                except ValueError:
                    continue
                if name not in af or v > af[name]:
                    af[name] = v
    return af


def build(inventory: str, out_dir: str, fixed: bool) -> None:
    """Write the annotated table and the five derived tables."""
    inv = pd.read_csv(inventory)
    result = inv.copy()
    result['am_variant'] = result['variant'].apply(three_to_one)
    am = pd.read_csv(os.path.join(DATA, 'cftr_alphamissense.tsv'), sep='\t')
    result = result.merge(am[['protein_variant', 'am_pathogenicity', 'am_class']],
                          left_on='am_variant', right_on='protein_variant', how='left'
                          ).drop(columns=['protein_variant'])
    result.to_csv(os.path.join(out_dir, 'cftr2_results_annotated.csv'), index=False)

    unmatched = result[result['determination_2026'].isna() & result['am_pathogenicity'].notna()]
    flagged = unmatched[unmatched['am_class'] == 'likely_pathogenic'].sort_values(
        'am_pathogenicity', ascending=False)
    flagged = flagged.drop_duplicates(subset=['am_variant']).sort_values('am_pathogenicity', ascending=False)
    flagged.to_csv(os.path.join(out_dir, 'flagged_unclassified.csv'), index=False)

    ff = result[result['determination_2026'].isna() & (result['am_class'] == 'likely_pathogenic')
                ].drop_duplicates(subset=['am_variant']).copy()
    ff['allele_frequency'] = pd.to_numeric(ff['allele_frequency'], errors='coerce')
    ff = ff.sort_values('allele_frequency', ascending=False)
    ff.to_csv(os.path.join(out_dir, 'flagged_prioritised.csv'), index=False)

    ff['vcf_af'] = ff['variant'].map(vcf_af(fixed))
    with_freq = ff[ff['vcf_af'].notna()].sort_values('vcf_af', ascending=False)
    priority = with_freq[['variant', 'am_variant', 'am_pathogenicity', 'vcf_af']].sort_values(
        'am_pathogenicity', ascending=False)
    priority.to_csv(os.path.join(out_dir, 'priority_candidates.csv'), index=False)

    varying = result[result['determination_2026'] == 'Varying clinical consequence']
    varying = varying.drop_duplicates(subset=['variant']).sort_values('am_pathogenicity', ascending=False)
    varying[['variant', 'am_pathogenicity', 'am_class']].to_csv(
        os.path.join(out_dir, 'varying_consequence_am.csv'), index=False)

    cftr2 = pd.read_excel(os.path.join(DATA, 'cftr2_variants.xlsx'), header=11)
    cftr2.columns = CFTR2_COLUMNS
    excluded = inv[inv['variant'].apply(three_to_one).isna()].copy()
    excluded['protein_name'] = excluded['protein_name'].str.replace('Ter', 'X')
    nonsense = excluded.drop(columns=['determination_2026'], errors='ignore').merge(
        cftr2[['protein_name', 'determination_2026']], on='protein_name', how='left')
    nonsense.to_csv(os.path.join(out_dir, 'nonsense_variants_cftr2.csv'), index=False)


def main() -> None:
    """Parse arguments and build."""
    ap = argparse.ArgumentParser()
    ap.add_argument('--inventory', default=os.path.join(DATA, 'cftr2_results.csv'))
    ap.add_argument('--out-dir', default=DATA)
    ap.add_argument('--old-rule', action='store_true')
    a = ap.parse_args()
    build(a.inventory, a.out_dir, fixed=not a.old_rule)
    print(f'wrote six tables to {a.out_dir}')


if __name__ == '__main__':
    main()
