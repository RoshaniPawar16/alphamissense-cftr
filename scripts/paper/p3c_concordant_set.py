#!/usr/bin/env python3
"""Build the concordant set table under both definitions.

Stage 3c of the paper-prep task. Two definitions of "AlphaGenome and SpliceAI
agree" are applied to the 1,278 AlphaMissense-ambiguous CFTR missense variants:

  GM  gene-mask SPLICE quantile > 0.95 AND SpliceAI max delta > 0.5
  CM  centre-mask splice (501 bp window) in the top 5% of the 1,278
      AND SpliceAI max delta > 0.5

Every variant in the union of the two sets is emitted with one row per
variant. Columns that no file in this repository can fill are written as the
literal string [NOT IN REPO]; they are never left blank.

The gene-mask SPLICE quantile used is the chromosome-22-calibrated column from
the May 2026 scoring run, which is the column both published counts (18 and
13) were derived from. The genome-wide recalibrated quantile is carried
alongside it for comparison.

Reads : results/alphagenome/alphagenome_full_cftr_results.csv
        results/alphagenome/rescore_centermask.csv
        results/alphagenome/quantiles_genomewide_2026-08.csv
        results/comparator_scores.csv
        results/gnomad_cftr_lookup.csv
        results/experimental_benchmark.csv
        data/cftr2_results_annotated.csv
Writes: results/paper/concordant_set.csv

Usage:
    python scripts/paper/p3c_concordant_set.py
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "paper" / "concordant_set.csv"

MISSING = "[NOT IN REPO]"

# CFTR domain boundaries by residue, as used in scripts/alphamissense_analysis.py:146.
DOMAINS = [
    ("MSD1", 1, 394),
    ("NBD1", 395, 646),
    ("R-domain", 647, 835),
    ("MSD2", 836, 1172),
    ("NBD2", 1173, 1480),
]

RESIDUE_RE = re.compile(r"^[A-Z](\d+)[A-Z]$")

THREE_TO_ONE = {
    "Ala": "A", "Arg": "R", "Asn": "N", "Asp": "D", "Cys": "C", "Gln": "Q",
    "Glu": "E", "Gly": "G", "His": "H", "Ile": "I", "Leu": "L", "Lys": "K",
    "Met": "M", "Phe": "F", "Pro": "P", "Ser": "S", "Thr": "T", "Trp": "W",
    "Tyr": "Y", "Val": "V",
}
THREE_RE = re.compile(r"^([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2})")


def domain_of(protein_variant: str) -> str:
    """Map a single-letter protein change (e.g. R1070Q) to a CFTR domain."""
    m = RESIDUE_RE.match(protein_variant)
    if not m:
        return "unknown"
    pos = int(m.group(1))
    for name, lo, hi in DOMAINS:
        if lo <= pos <= hi:
            return name
    return "unknown"


def three_to_one(name: str) -> str:
    """Convert a three-letter protein change (Arg1070Gln) to one letter (R1070Q)."""
    m = THREE_RE.match(str(name))
    if not m:
        return ""
    ref, pos, alt = m.group(1), m.group(2), m.group(3)
    if ref not in THREE_TO_ONE or alt not in THREE_TO_ONE:
        return ""
    return f"{THREE_TO_ONE[ref]}{pos}{THREE_TO_ONE[alt]}"


def spliceai_type(row: pd.Series) -> str:
    """Name the SpliceAI delta channel that carries the maximum, or 'none'."""
    channels = {
        "AG": row["SpliceAI_DS_AG"],
        "AL": row["SpliceAI_DS_AL"],
        "DG": row["SpliceAI_DS_DG"],
        "DL": row["SpliceAI_DS_DL"],
    }
    top = max(channels.values())
    if top <= 0:
        return "none"
    return "+".join(sorted(k for k, v in channels.items() if v == top))


def main() -> None:
    """Assemble the union of the GM and CM concordant sets and write it out."""
    gm_src = pd.read_csv(ROOT / "results/alphagenome/alphagenome_full_cftr_results.csv")
    cm_src = pd.read_csv(ROOT / "results/alphagenome/rescore_centermask.csv")
    gw_src = pd.read_csv(ROOT / "results/alphagenome/quantiles_genomewide_2026-08.csv")
    comp = pd.read_csv(ROOT / "results/comparator_scores.csv")
    gnomad = pd.read_csv(ROOT / "results/gnomad_cftr_lookup.csv")
    expb = pd.read_csv(ROOT / "results/experimental_benchmark.csv")
    cftr2 = pd.read_csv(ROOT / "data/cftr2_results_annotated.csv")

    cm_full = cm_src[cm_src["source"] == "full"].copy()
    assert len(gm_src) == 1278 and len(cm_full) == 1278, "cohort size changed"

    base = gm_src.merge(
        comp[
            [
                "variant_id", "SpliceAI_max_delta", "SpliceAI_DS_AG",
                "SpliceAI_DS_AL", "SpliceAI_DS_DG", "SpliceAI_DS_DL", "CADD_PHRED",
            ]
        ],
        on="variant_id",
        how="left",
        validate="one_to_one",
    ).merge(
        cm_full[["variant_id", "cm_splice_501", "gm_splice_raw", "gm_splice_q"]],
        on="variant_id",
        how="left",
        validate="one_to_one",
    ).merge(
        gw_src[["variant_id", "new_SPLICE_SITE_USAGE_raw", "new_SPLICE_SITE_USAGE_quantile"]],
        on="variant_id",
        how="left",
        validate="one_to_one",
    ).merge(
        gnomad[["variant_id_project", "gnomad_max_af", "gnomad_variant_id"]].rename(
            columns={"variant_id_project": "variant_id"}
        ),
        on="variant_id",
        how="left",
        validate="one_to_one",
    )

    cm_threshold = float(cm_full["cm_splice_501"].quantile(0.95))
    in_gm = (base["SPLICE_SITE_USAGE_quantile_max"] > 0.95) & (base["SpliceAI_max_delta"] > 0.5)
    in_cm = (base["cm_splice_501"] > cm_threshold) & (base["SpliceAI_max_delta"] > 0.5)
    print(f"CM top-5% threshold on cm_splice_501: {cm_threshold:.6f} "
          f"({int((base['cm_splice_501'] > cm_threshold).sum())} variants above)")
    print(f"GM set n={int(in_gm.sum())}  CM set n={int(in_cm.sum())}  "
          f"union n={int((in_gm | in_cm).sum())}  intersection n={int((in_gm & in_cm).sum())}")

    sel = base[in_gm | in_cm].copy()
    sel["in_GM"] = in_gm[in_gm | in_cm].map({True: "yes", False: "no"})
    sel["in_CM"] = in_cm[in_gm | in_cm].map({True: "yes", False: "no"})

    # CFTR2 status, matched on the single-letter AlphaMissense variant name.
    cftr2_map = (
        cftr2.dropna(subset=["am_variant"])
        .drop_duplicates(subset=["am_variant"], keep="first")
        .set_index("am_variant")["determination_2026"]
    )

    # Membership in the minigene benchmark, matched via three-letter protein name.
    expb = expb.copy()
    expb["one_letter"] = expb["protein_name"].map(three_to_one)
    exp_map = (
        expb.dropna(subset=["one_letter"])
        .drop_duplicates(subset=["one_letter"], keep="first")
        .set_index("one_letter")["minigene_result"]
    )

    rows: list[dict[str, object]] = []
    for _, r in sel.iterrows():
        pv = r["protein_variant"]
        cftr2_status = cftr2_map.get(pv)
        if pd.isna(cftr2_status) or cftr2_status in (None, ""):
            cftr2_status = "no CFTR2 record"
        exp_hit = exp_map.get(pv)
        gmax = r["gnomad_max_af"]
        rows.append(
            {
                "protein_change": pv,
                "variant_id_hg38": r["variant_id"],
                "chrom": r["CHROM"],
                "pos_hg38": int(r["POS"]),
                "ref": r["REF"],
                "alt": r["ALT"],
                "cftr_domain": domain_of(pv),
                "exon_or_intron": MISSING,
                "distance_to_nearest_splice_site_bp": MISSING,
                "alphamissense_score": r["am_pathogenicity"],
                "alphamissense_class": r["am_class"],
                "ag_splice_raw_chr22run": r["SPLICE_SITE_USAGE_raw_max"],
                "ag_splice_quantile_chr22run": r["SPLICE_SITE_USAGE_quantile_max"],
                "ag_splice_raw_genomewide": r["new_SPLICE_SITE_USAGE_raw"],
                "ag_splice_quantile_genomewide": r["new_SPLICE_SITE_USAGE_quantile"],
                "ag_centermask_splice_501": r["cm_splice_501"],
                "spliceai_max_delta": r["SpliceAI_max_delta"],
                "spliceai_type": spliceai_type(r),
                "spliceai_ds_ag": r["SpliceAI_DS_AG"],
                "spliceai_ds_al": r["SpliceAI_DS_AL"],
                "spliceai_ds_dg": r["SpliceAI_DS_DG"],
                "spliceai_ds_dl": r["SpliceAI_DS_DL"],
                "cadd_phred": r["CADD_PHRED"],
                "gnomad_v4_max_af": (
                    "absent from gnomAD v4" if pd.isna(gmax) else gmax
                ),
                "cftr2_status": cftr2_status,
                "in_experimental_benchmark": (
                    "no" if exp_hit is None else f"yes ({exp_hit})"
                ),
                "in_GM": r["in_GM"],
                "in_CM": r["in_CM"],
            }
        )

    out = pd.DataFrame(rows).sort_values("pos_hg38").reset_index(drop=True)
    out.insert(0, "rank_by_position", range(1, len(out) + 1))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False)
    print(f"\nwrote {OUT.relative_to(ROOT)} ({len(out)} rows)")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
