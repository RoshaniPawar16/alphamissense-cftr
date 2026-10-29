"""
CFTR2 data processing — reproducible script version of notebooks/cftr2_scraper.ipynb.

Builds the variant inventory: every protein-change name in the ClinVar VCF,
joined to the CFTR2 spreadsheet by protein name. Reproduces notebook cells 2,
12 and 16. The Selenium download cells are not included; data/cftr2_variants.xlsx
must exist on disk.

Changed 2026-10-29 (docs/AUDIT_RECORD.md, Corrections 14):
  - Names come from scripts/hgvsp_names.py. A name counts only when the first
    HGVSp token on a VCF line is complete (p.Xxx123Yyy, nothing after it).
    The old rule also accepted the truncated prefix of frameshift and
    stop-loss tokens (p.Lys163ArgfsTer3 -> Lys163Arg).
  - The script now writes data/cftr2_results.csv, the file the rest of the
    pipeline reads, with the notebook's columns. The earlier version wrote
    results/phase1/cftr2_processed_labels.csv and assigned five column names
    to the nine-column spreadsheet, so it could not run.

Inputs : data/cftr2_variants.xlsx, data/All_Variants_VEP.Gene.vcf
Output : data/cftr2_results.csv  (or --out)

Usage:
    python scripts/cftr2_scraper_analysis.py [--old-rule] [--out PATH]
"""

import argparse
import logging
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hgvsp_names import name_from_line  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XLSX_PATH = os.path.join(ROOT, 'data', 'cftr2_variants.xlsx')
VCF_PATH = os.path.join(ROOT, 'data', 'All_Variants_VEP.Gene.vcf')
OUT_CSV = os.path.join(ROOT, 'data', 'cftr2_results.csv')

# Column names as in notebooks/cftr2_scraper.ipynb cell 12.
CFTR2_COLUMNS = ['legacy_name', 'protein_name', 'cdna_name', 'alt_names',
                 'alleles_count', 'allele_frequency', 'determination_2024',
                 'determination_2026', 'change']

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)


def extract_variants(vcf_path: str, fixed: bool) -> list[str]:
    """Return unique protein-change names in VCF order (notebook cell 2)."""
    seen, variants = set(), []
    with open(vcf_path, encoding='utf-8', errors='replace') as fh:
        for line in fh:
            if line.startswith('#'):
                continue
            name = name_from_line(line, fixed=fixed)
            if name and name not in seen:
                seen.add(name)
                variants.append(name)
    return variants


def build_inventory(fixed: bool = True) -> pd.DataFrame:
    """Join VCF names to CFTR2 by protein name (notebook cells 12 and 16)."""
    df = pd.read_excel(XLSX_PATH, header=11)
    df.columns = CFTR2_COLUMNS
    variants = extract_variants(VCF_PATH, fixed)
    vcf_df = pd.DataFrame({'variant': variants, 'protein_name': ['p.' + v for v in variants]})
    return vcf_df.merge(
        df[['protein_name', 'legacy_name', 'determination_2026', 'allele_frequency']],
        on='protein_name', how='left')


def main() -> None:
    """Build the inventory and write it."""
    ap = argparse.ArgumentParser()
    ap.add_argument('--old-rule', action='store_true',
                    help='replay the pre-2026-10-29 rule (reproduction check only)')
    ap.add_argument('--out', default=OUT_CSV)
    args = ap.parse_args()
    result = build_inventory(fixed=not args.old_rule)
    result.to_csv(args.out, index=False)
    log.info('Saved %s: %d rows, %d unique names, %d matched to CFTR2',
             args.out, len(result), result['variant'].nunique(),
             int(result['determination_2026'].notna().sum()))


if __name__ == '__main__':
    main()
