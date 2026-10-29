#!/usr/bin/env python3
"""Three descriptive analyses that link the benchmark to the splice screen.

1. AlphaMissense class against CFTR2 label, on the 259 deduplicated labelled
   variants. Shows how many labelled variants fall in each AlphaMissense class
   and how many of those are CF-causing.

2. CFTR domain of the 1,278 AlphaMissense-ambiguous variants against the 18
   concordant variants, with a two-sided Fisher exact test for each domain
   (variants in that domain vs all others, concordant vs not concordant).

3. How the concordant set arises: SpliceAI and AlphaGenome counts on the
   1,278 at the concordant-set thresholds (SpliceAI > 0.5, AlphaGenome
   gene-mask splice quantile > 0.95, quantiles as served at the 2026-10-27
   rescore), and the number of SpliceAI zeros. Added 2026-10-29: how many of
   the 18 are in the ClinVar extract (exact nucleotide match in the VCF, and
   protein-change match in data/cftr2_results_annotated.csv) and how many have
   a gnomAD v4 allele frequency above zero.

Class boundaries are the published AlphaMissense thresholds: likely benign
below 0.34, ambiguous from 0.34 to 0.564, likely pathogenic above 0.564.
Domain boundaries are the residue ranges used in
scripts/paper/p3c_concordant_set.py.

Reads : results/phase1/benchmark_cohort_dedup.csv
        results/alphagenome/alphagenome_full_cftr_results.csv
        results/paper/concordant_set.csv
        results/comparator_scores.csv
        results/gnomad_cftr_lookup.csv
        data/All_Variants_VEP.Gene.vcf
        data/cftr2_results_annotated.csv
Writes: results/paper/am_class_by_label.csv
        results/paper/domain_distribution.csv
        results/paper/concordant_set_origin.csv

Usage:
    python scripts/paper/p3f_class_and_domain.py
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
from scipy.stats import fisher_exact

ROOT = Path(__file__).resolve().parents[2]
COHORT = ROOT / "results/phase1/benchmark_cohort_dedup.csv"
AG = ROOT / "results/alphagenome/alphagenome_full_cftr_results.csv"
CONC = ROOT / "results/paper/concordant_set.csv"
OUT_CLASS = ROOT / "results/paper/am_class_by_label.csv"
OUT_DOMAIN = ROOT / "results/paper/domain_distribution.csv"
SCORES = ROOT / "results/comparator_scores.csv"
OUT_ORIGIN = ROOT / "results/paper/concordant_set_origin.csv"
GNOMAD = ROOT / "results/gnomad_cftr_lookup.csv"
VCF = ROOT / "data/All_Variants_VEP.Gene.vcf"
ANNOT = ROOT / "data/cftr2_results_annotated.csv"

LB_MAX, LP_MIN = 0.34, 0.564
DOMAINS = [
    ("MSD1", 1, 394),
    ("NBD1", 395, 646),
    ("R-domain", 647, 835),
    ("MSD2", 836, 1172),
    ("NBD2", 1173, 1480),
]
RESIDUE_RE = re.compile(r"^[A-Z](\d+)[A-Z]$")


def am_class(score: float) -> str:
    if score < LB_MAX:
        return "likely_benign"
    if score > LP_MIN:
        return "likely_pathogenic"
    return "ambiguous"


def domain_of(protein_change: str) -> str:
    m = RESIDUE_RE.match(protein_change)
    if not m:
        raise ValueError(f"cannot parse residue from {protein_change!r}")
    residue = int(m.group(1))
    for name, lo, hi in DOMAINS:
        if lo <= residue <= hi:
            return name
    raise ValueError(f"residue {residue} outside CFTR domains")


def class_by_label() -> pd.DataFrame:
    d = pd.read_csv(COHORT)
    d["am_class"] = d["am_pathogenicity"].map(am_class)
    rows = []
    for cls in ("likely_benign", "ambiguous", "likely_pathogenic"):
        s = d[d["am_class"] == cls]
        rows.append({
            "am_class": cls,
            "n_labelled": len(s),
            "n_cf_causing": int(s["label"].sum()),
            "n_non_cf_causing": int((s["label"] == 0).sum()),
            "fraction_cf_causing": round(s["label"].mean(), 4) if len(s) else None,
            "mean_am_score": round(s["am_pathogenicity"].mean(), 4) if len(s) else None,
            "source_file": "results/phase1/benchmark_cohort_dedup.csv",
        })
    out = pd.DataFrame(rows)
    # Changed 2026-10-29: the benchmark size comes from the cohort file, not a constant.
    assert out["n_labelled"].sum() == len(d), "class counts must sum to the benchmark size"
    return out


def domain_distribution() -> pd.DataFrame:
    ag = pd.read_csv(AG)
    conc = pd.read_csv(CONC)
    assert len(ag) == 1278, f"expected 1,278 ambiguous variants, got {len(ag)}"
    assert len(conc) == 18, f"expected 18 concordant variants, got {len(conc)}"
    ag["domain"] = ag["protein_variant"].map(domain_of)
    conc_ids = set(conc["variant_id_hg38"])
    ag["concordant"] = ag["variant_id"].isin(conc_ids)
    assert ag["concordant"].sum() == 18, "every concordant variant must be in the 1,278"

    rows = []
    for name, lo, hi in DOMAINS:
        in_dom = ag["domain"] == name
        a = int((in_dom & ag["concordant"]).sum())
        b = int((in_dom & ~ag["concordant"]).sum())
        c = int((~in_dom & ag["concordant"]).sum())
        d_ = int((~in_dom & ~ag["concordant"]).sum())
        odds, p = fisher_exact([[a, b], [c, d_]], alternative="two-sided")
        rows.append({
            "domain": name,
            "residue_start": lo,
            "residue_end": hi,
            "n_ambiguous": int(in_dom.sum()),
            "pct_of_ambiguous": round(100 * in_dom.mean(), 1),
            "n_concordant": a,
            "pct_of_concordant": round(100 * a / 18, 1),
            "fisher_odds_ratio": round(odds, 3) if odds != float("inf") else "inf",
            "fisher_p_two_sided": float(f"{p:.3g}"),
            "source_files": "results/alphagenome/alphagenome_full_cftr_results.csv; "
                            "results/paper/concordant_set.csv",
        })
    return pd.DataFrame(rows)


def concordant_origin() -> pd.DataFrame:
    ag = pd.read_csv(AG)
    sc = pd.read_csv(SCORES)[["variant_id", "SpliceAI_max_delta"]]
    m = ag.merge(sc, on="variant_id", how="left", validate="one_to_one")
    assert len(m) == 1278 and m["SpliceAI_max_delta"].notna().all()
    sai = m["SpliceAI_max_delta"]
    agq = m["SPLICE_SITE_USAGE_quantile_max"]
    rows = [
        ("n_variants", len(m)),
        ("spliceai_gt_0.5", int((sai > 0.5).sum())),
        ("spliceai_gt_0.5_and_ag_q_gt_0.95", int(((sai > 0.5) & (agq > 0.95)).sum())),
        ("spliceai_gt_0.5_and_ag_q_le_0.95", int(((sai > 0.5) & (agq <= 0.95)).sum())),
        ("ag_q_gt_0.95", int((agq > 0.95).sum())),
        ("spliceai_gt_0.2", int((sai > 0.2).sum())),
        ("spliceai_exactly_0", int((sai == 0).sum())),
    ]
    dropped = m[(sai > 0.5) & (agq <= 0.95)]["protein_variant"].tolist()
    out = pd.DataFrame(rows, columns=["count_name", "value"])
    out["note"] = ""
    out.loc[out["count_name"] == "spliceai_gt_0.5_and_ag_q_le_0.95", "note"] = "; ".join(dropped)
    out["source_files"] = ("results/alphagenome/alphagenome_full_cftr_results.csv; "
                           "results/comparator_scores.csv")
    return pd.concat([out, concordant_presence()], ignore_index=True)


def vcf_variant_ids(path: Path) -> set[str]:
    """Return every chrom:pos:ref>alt in the ClinVar VCF, one per alternate allele."""
    ids: set[str] = set()
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            chrom, pos, _, ref, alts = line.split("\t", 5)[:5]
            for alt in alts.split(","):
                ids.add(f"chr{chrom.removeprefix('chr')}:{pos}:{ref}>{alt}")
    return ids


def concordant_presence() -> pd.DataFrame:
    """Count the 18 in the ClinVar extract and with a gnomAD v4 frequency above zero."""
    conc = pd.read_csv(CONC)
    assert len(conc) == 18, f"expected 18 concordant variants, got {len(conc)}"
    exact = conc[conc["variant_id_hg38"].isin(vcf_variant_ids(VCF))]
    annot = pd.read_csv(ANNOT)
    protein = conc[conc["protein_change"].isin(set(annot["am_variant"].dropna()))]
    protein_only = sorted(set(protein["protein_change"]) - set(exact["protein_change"]))
    gn = pd.read_csv(GNOMAD)
    with_af = set(gn.loc[gn["gnomad_max_af"] > 0, "variant_id_project"])
    af = conc[conc["variant_id_hg38"].isin(with_af)]
    rows = [
        {"count_name": "concordant_in_clinvar_vcf_exact_nucleotide", "value": len(exact),
         "note": "; ".join(exact["protein_change"]),
         "source_files": "results/paper/concordant_set.csv; data/All_Variants_VEP.Gene.vcf"},
        {"count_name": "concordant_in_cftr2_annotated_protein_change", "value": len(protein),
         "note": ("; ".join(protein["protein_change"])
                  + (f" | protein-change match only: {'; '.join(protein_only)}" if protein_only else "")),
         "source_files": "results/paper/concordant_set.csv; data/cftr2_results_annotated.csv"},
        {"count_name": "concordant_in_gnomad_v4_af_gt_0", "value": len(af),
         "note": "; ".join(af["protein_change"]),
         "source_files": "results/paper/concordant_set.csv; results/gnomad_cftr_lookup.csv"},
    ]
    return pd.DataFrame(rows)


def main() -> None:
    cls = class_by_label()
    cls.to_csv(OUT_CLASS, index=False)
    print(cls.to_string(index=False))
    dom = domain_distribution()
    dom.to_csv(OUT_DOMAIN, index=False)
    print(dom.drop(columns="source_files").to_string(index=False))
    origin = concordant_origin()
    origin.to_csv(OUT_ORIGIN, index=False)
    print(origin.drop(columns="source_files").to_string(index=False))


if __name__ == "__main__":
    main()
