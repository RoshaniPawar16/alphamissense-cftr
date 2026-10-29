#!/usr/bin/env python3
"""Audit the variant inventory for non-missense HGVSp shortened to missense names.

The inventory extractor (notebooks/cftr2_scraper.ipynb cell 2, reproduced in
scripts/cftr2_scraper_analysis.py) runs the regex p\\.([A-Z][a-z]{2}\\d+[A-Z][a-z]{2})
over each whole VCF line and keeps the first match. A frameshift such as
p.Lys163ArgfsTer3 therefore yields the short name Lys163Arg, which looks like
a missense change. The same first-match rule was used by
scripts/phase1_fetch_cadd.py to choose the coordinates sent to CADD.

This script replays the extractor on every VCF line, recovers the full HGVSp
token each short name came from, and classifies it:

  missense       token is exactly p.<Aaa><n><Bbb> with two standard residues
  non-missense   anything longer (fs, ext, del, ins, dup, delins, ...) or a
                 token with Ter that the regex shortened

A short name "looks like a missense change" when both residues are standard
amino acids (neither is Ter) and they differ.

Outputs
  results/paper/inventory_nonmissense_audit.csv   (A1: one row per VCF line
      whose first-match token is non-missense but whose short name looks like
      a missense change)
  results/paper/benchmark_contamination_audit.csv (A3: one row per benchmark
      variant, with its VCF provenance, its CFTR2 row and its CADD coordinates)
  results/paper/inventory_audit_summary.csv       (A1-A3 counts)

Reads : data/All_Variants_VEP.Gene.vcf
        data/cftr2_results_annotated.csv
        data/cftr2_variants.xlsx
        results/phase1/benchmark_cohort_dedup.csv
        results/phase1/inputs_cadd_raw.json

Usage:
    python scripts/paper/p3h_inventory_audit.py
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
VCF = ROOT / "data/All_Variants_VEP.Gene.vcf"
ANNOT = ROOT / "data/cftr2_results_annotated.csv"
XLSX = ROOT / "data/cftr2_variants.xlsx"
COHORT = ROOT / "results/phase1/benchmark_cohort_dedup.csv"
CADD_RAW = ROOT / "results/phase1/inputs_cadd_raw.json"
OUT_A1 = ROOT / "results/paper/inventory_nonmissense_audit.csv"
OUT_A3 = ROOT / "results/paper/benchmark_contamination_audit.csv"
OUT_SUM = ROOT / "results/paper/inventory_audit_summary.csv"

EXTRACT = re.compile(r"p\.([A-Z][a-z]{2}\d+[A-Z][a-z]{2})")   # the extractor, verbatim
NAME = re.compile(r"^([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2})$")
TOKEN_END = re.compile(r"[|,;\t\s]")
AA = {"Ala", "Arg", "Asn", "Asp", "Cys", "Gln", "Glu", "Gly", "His", "Ile", "Leu",
      "Lys", "Met", "Phe", "Pro", "Ser", "Thr", "Trp", "Tyr", "Val"}
SUBST = re.compile(r"^c\.\d+[ACGT]>[ACGT]$")


def looks_missense(name: str) -> bool:
    """True when a short name is two different standard residues around a position."""
    m = NAME.match(name)
    return bool(m) and m.group(1) in AA and m.group(3) in AA and m.group(1) != m.group(3)


def full_token(line: str, start: int) -> str:
    """Return the HGVSp token beginning at 'p.' up to the next field delimiter."""
    end = TOKEN_END.search(line, start)
    return line[start:end.start() if end else len(line)]


def consequence_of(line: str, start: int) -> str:
    """Return the CSQ Consequence of the transcript that holds the match, if any."""
    csq = line.find("CSQ=")
    if csq < 0 or start < csq:
        return ""
    seg_start = max(line.rfind(",", csq, start), csq + 3) + 1
    fields = line[seg_start:start].split("|")
    return fields[1] if len(fields) > 1 else ""


def exact_tokens_anywhere() -> set[str]:
    """Return every short name that appears anywhere in the VCF as a complete missense token."""
    names: set[str] = set()
    with open(VCF, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            for m in EXTRACT.finditer(line):
                if full_token(line, m.start()) == f"p.{m.group(1)}":
                    names.add(m.group(1))
    return names


def replay_vcf() -> pd.DataFrame:
    """Replay the extractor on every VCF data line; one row per line with a match."""
    rows = []
    with open(VCF, encoding="utf-8", errors="replace") as fh:
        for lineno, line in enumerate(fh, 1):
            if line.startswith("#"):
                continue
            m = EXTRACT.search(line)
            if not m:
                continue
            chrom, pos, vid, ref, alt = line.split("\t", 5)[:5]
            token = full_token(line, m.start())
            name = m.group(1)
            rows.append({
                "vcf_line": lineno, "chrom": chrom, "pos": int(pos), "clinvar_id": vid,
                "ref": ref, "alt": alt, "short_name": name, "hgvsp_token": token,
                "consequence": consequence_of(line, m.start()),
                "token_is_exact": token == f"p.{name}",
                "name_looks_missense": looks_missense(name),
            })
    return pd.DataFrame(rows)


def main() -> None:
    """Run A1 to A3 and write the three audit files."""
    lines = replay_vcf()
    annot = pd.read_csv(ANNOT)
    inv = set(annot["variant"].dropna())

    # A1: non-missense token, missense-looking short name.
    a1 = lines[~lines["token_is_exact"] & lines["name_looks_missense"]].copy()
    exact_names = set(lines.loc[lines["token_is_exact"], "short_name"])
    a1["name_also_has_exact_missense_line"] = a1["short_name"].isin(exact_names)
    a1["in_inventory_3220"] = a1["short_name"].isin(inv)
    first_line = lines.drop_duplicates("short_name", keep="first").set_index("short_name")["vcf_line"]
    a1["is_first_line_for_name"] = a1["vcf_line"].values == a1["short_name"].map(first_line).values

    # A2: unique names in the 3,220 that the extractor took from a non-missense token.
    from_nonmissense = set(a1["short_name"])
    only_nonmissense = from_nonmissense - exact_names
    anywhere = exact_tokens_anywhere()
    no_exact_anywhere = from_nonmissense - anywhere
    first_is_nonmissense = set(a1.loc[a1["is_first_line_for_name"], "short_name"])

    # A3: benchmark provenance.
    cohort = pd.read_csv(COHORT)
    x = pd.read_excel(XLSX, header=11)
    x.columns = ["legacy_name", "protein_name", "cdna_name", "alt_names", "n_alleles",
                 "allele_freq", "det_2024", "det_2026", "change"]
    x["protein_name"] = x["protein_name"].astype(str).str.strip()
    by_prot = x.groupby("protein_name")
    cadd = json.loads(CADD_RAW.read_text())
    line_tokens = defaultdict(set)
    for r in lines.itertuples():
        line_tokens[(str(r.pos), r.ref, r.alt)].add(r.hgvsp_token)

    rows = []
    for r in cohort.itertuples():
        name = r.variant
        sel = lines[lines["short_name"] == name]
        cf = by_prot.get_group(f"p.{name}") if f"p.{name}" in by_prot.groups else x.iloc[0:0]
        coord = (cadd.get(name) or {}).get("coord") or {}
        key = (str(coord.get("pos", "")), coord.get("ref", ""), coord.get("alt", ""))
        cadd_tokens = sorted(line_tokens.get(key, set()))
        rows.append({
            "variant": name,
            "determination_2026": r.determination_2026,
            "included_254": r.included,
            "vcf_lines_exact_missense": int(sel["token_is_exact"].sum()),
            "vcf_lines_nonmissense": int((~sel["token_is_exact"]).sum()),
            "a_name_only_from_nonmissense": name not in anywhere,
            "cftr2_rows": len(cf),
            "cftr2_cdna": "; ".join(cf["cdna_name"].astype(str)),
            "cftr2_det_2026": "; ".join(cf["det_2026"].astype(str)),
            # CFTR2 lists alternative nucleotide changes for one protein change
            # separated by "|"; every part must be a single-base substitution.
            "b_cftr2_row_is_this_missense": bool(len(cf)) and all(
                SUBST.match(part.strip())
                for cdna in cf["cdna_name"].astype(str) for part in cdna.split("|")),
            "cadd_query": f"{coord.get('pos','')}:{coord.get('ref','')}>{coord.get('alt','')}",
            "cadd_query_is_snv": len(coord.get("ref", "")) == 1 and len(coord.get("alt", "")) == 1,
            "cadd_query_line_tokens": "; ".join(cadd_tokens),
            "c_cadd_query_is_this_missense": f"p.{name}" in cadd_tokens,
        })
    a3 = pd.DataFrame(rows)

    a1.to_csv(OUT_A1, index=False)
    a3.to_csv(OUT_A3, index=False)

    affected = a3[a3["a_name_only_from_nonmissense"] | ~a3["b_cftr2_row_is_this_missense"]
                  | ~a3["c_cadd_query_is_this_missense"]]
    summary = [
        ("vcf_lines_with_extractor_match", len(lines)),
        ("A1_vcf_lines_nonmissense_token_missense_looking_name", len(a1)),
        ("A1_unique_short_names", a1["short_name"].nunique()),
        ("A2_inventory_unique_names", len(inv)),
        ("A2_names_with_any_nonmissense_source", len(from_nonmissense & inv)),
        ("A2_names_only_from_nonmissense_first_match", len(only_nonmissense & inv)),
        ("A2_names_with_no_exact_missense_token_anywhere_in_vcf", len(no_exact_anywhere & inv)),
        ("A2_inventory_unique_names_corrected", len(inv - no_exact_anywhere)),
        ("A2_names_whose_first_line_is_nonmissense", len(first_is_nonmissense & inv)),
        ("A3_benchmark_variants", len(a3)),
        ("A3a_name_only_from_nonmissense", int(a3["a_name_only_from_nonmissense"].sum())),
        ("A3b_cftr2_row_not_a_single_substitution", int((~a3["b_cftr2_row_is_this_missense"]).sum())),
        ("A3c_cadd_query_not_this_missense", int((~a3["c_cadd_query_is_this_missense"]).sum())),
        ("A3_any_affected", len(affected)),
        ("A3_any_affected_in_254", int(affected["included_254"].sum())),
    ]
    s = pd.DataFrame(summary, columns=["count_name", "value"])
    s["source_files"] = ("data/All_Variants_VEP.Gene.vcf; data/cftr2_results_annotated.csv; "
                         "data/cftr2_variants.xlsx; results/phase1/benchmark_cohort_dedup.csv; "
                         "results/phase1/inputs_cadd_raw.json")
    s.to_csv(OUT_SUM, index=False)
    print(s.drop(columns="source_files").to_string(index=False))
    print("\nA2 names with no exact missense token anywhere:", len(no_exact_anywhere & inv))
    print("\nA3 affected rows:")
    print(affected.drop(columns=["cadd_query_line_tokens"]).to_string(index=False) if len(affected) else "none")


if __name__ == "__main__":
    main()
