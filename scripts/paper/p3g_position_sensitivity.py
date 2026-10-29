#!/usr/bin/env python3
"""Position-level sensitivity checks for the splice agreement and the MSD2 test.

Several of the 1,278 AlphaMissense-ambiguous variants share a genomic position
(different alternate alleles at one base). Variants at one position are not
independent observations, so two results are repeated at position level:

(a) The AlphaGenome-SpliceAI 2x2 (gene-mask splice quantile > 0.95 against
    SpliceAI maximum delta > 0.2), keeping one variant per genomic position
    chosen at random. Repeated 500 times with numpy default_rng(42). Reports
    the median odds ratio, its 2.5th and 97.5th percentiles across draws, and
    the median and maximum two-sided Fisher p.
(b) The MSD2 Fisher test at position level: the genomic positions of the 18
    concordant variants against all positions of the 1,278, MSD2 against the
    other domains. Each position maps to one residue, so to one domain.

The odds ratio in (a) uses the same Woolf form as p3e (no zero-cell
correction is needed unless a cell is empty; if so, 0.5 is added to every
cell, and the count of such draws is reported).

Reads : results/alphagenome/alphagenome_full_cftr_results.csv
        results/comparator_scores.csv
        results/paper/concordant_set.csv
Writes: results/paper/position_sensitivity.csv

Usage:
    python scripts/paper/p3g_position_sensitivity.py
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact

ROOT = Path(__file__).resolve().parents[2]
AG = ROOT / "results/alphagenome/alphagenome_full_cftr_results.csv"
SCORES = ROOT / "results/comparator_scores.csv"
CONC = ROOT / "results/paper/concordant_set.csv"
OUT = ROOT / "results/paper/position_sensitivity.csv"

N_DRAWS = 500
SEED = 42
AG_THRESHOLD = 0.95
SAI_THRESHOLD = 0.2

# CFTR domain boundaries by residue, as in scripts/alphamissense_analysis.py:146.
DOMAINS = [("MSD1", 1, 394), ("NBD1", 395, 646), ("R-domain", 647, 835),
           ("MSD2", 836, 1172), ("NBD2", 1173, 1480)]
RESIDUE_RE = re.compile(r"^[A-Z](\d+)[A-Z]$")


def domain_of(protein_variant: str) -> str:
    """Map a single-letter protein change to its CFTR domain."""
    m = RESIDUE_RE.match(protein_variant)
    pos = int(m.group(1)) if m else -1
    for name, lo, hi in DOMAINS:
        if lo <= pos <= hi:
            return name
    return "unknown"


def odds_ratio(table: np.ndarray) -> tuple[float, bool]:
    """Return the odds ratio and whether a 0.5 zero-cell correction was applied."""
    a, b, c, d = table.ravel().astype(float)
    if min(a, b, c, d) == 0:
        a, b, c, d = a + 0.5, b + 0.5, c + 0.5, d + 0.5
        return (a * d) / (b * c), True
    return (a * d) / (b * c), False


def main() -> None:
    """Run both position-level checks and write position_sensitivity.csv."""
    ag = pd.read_csv(AG)
    sc = pd.read_csv(SCORES)[["variant_id", "SpliceAI_max_delta"]]
    m = ag.merge(sc, on="variant_id", how="left", validate="one_to_one")
    assert len(m) == 1278 and m["SpliceAI_max_delta"].notna().all()
    m["position"] = m["CHROM"].astype(str) + ":" + m["POS"].astype(str)
    m["ag_high"] = m["SPLICE_SITE_USAGE_quantile_max"] > AG_THRESHOLD
    m["sai_high"] = m["SpliceAI_max_delta"] > SAI_THRESHOLD
    n_positions = m["position"].nunique()

    # (a) One variant per position, 500 random draws.
    rng = np.random.default_rng(SEED)
    groups = [g.index.to_numpy() for _, g in m.groupby("position", sort=True)]
    ors, ps, n_corrected, a_cells = [], [], 0, []
    for _ in range(N_DRAWS):
        idx = np.array([g[rng.integers(len(g))] for g in groups])
        s = m.loc[idx]
        table = np.array([
            [int((s.ag_high & s.sai_high).sum()), int((s.ag_high & ~s.sai_high).sum())],
            [int((~s.ag_high & s.sai_high).sum()), int((~s.ag_high & ~s.sai_high).sum())],
        ])
        o, corrected = odds_ratio(table)
        n_corrected += corrected
        ors.append(o)
        ps.append(fisher_exact(table, alternative="two-sided")[1])
        a_cells.append(table[0, 0])
    ors, ps = np.asarray(ors), np.asarray(ps)

    # (b) MSD2 Fisher test at position level.
    conc = pd.read_csv(CONC)
    conc_ids = set(conc["variant_id_hg38"])
    m["domain"] = m["protein_variant"].map(domain_of)
    pos_dom = m.groupby("position")["domain"].agg(lambda x: x.iloc[0])
    pos_conc = m.groupby("position")["variant_id"].agg(lambda x: bool(set(x) & conc_ids))
    assert (m.groupby("position")["domain"].nunique() == 1).all(), "position spans domains"
    in_msd2 = pos_dom == "MSD2"
    t2 = np.array([
        [int((in_msd2 & pos_conc).sum()), int((in_msd2 & ~pos_conc).sum())],
        [int((~in_msd2 & pos_conc).sum()), int((~in_msd2 & ~pos_conc).sum())],
    ])
    or2, p2 = fisher_exact(t2, alternative="two-sided")

    rows = [
        {"analysis": "2x2_one_variant_per_position", "metric": "n_positions", "value": n_positions},
        {"analysis": "2x2_one_variant_per_position", "metric": "n_draws", "value": N_DRAWS},
        {"analysis": "2x2_one_variant_per_position", "metric": "seed", "value": SEED},
        {"analysis": "2x2_one_variant_per_position", "metric": "median_cell_a_both_high", "value": float(np.median(a_cells))},
        {"analysis": "2x2_one_variant_per_position", "metric": "median_odds_ratio", "value": round(float(np.median(ors)), 4)},
        {"analysis": "2x2_one_variant_per_position", "metric": "odds_ratio_p2.5", "value": round(float(np.percentile(ors, 2.5)), 4)},
        {"analysis": "2x2_one_variant_per_position", "metric": "odds_ratio_p97.5", "value": round(float(np.percentile(ors, 97.5)), 4)},
        {"analysis": "2x2_one_variant_per_position", "metric": "median_fisher_p", "value": f"{np.median(ps):.3e}"},
        {"analysis": "2x2_one_variant_per_position", "metric": "max_fisher_p", "value": f"{ps.max():.3e}"},
        {"analysis": "2x2_one_variant_per_position", "metric": "draws_with_zero_cell_correction", "value": n_corrected},
        {"analysis": "msd2_position_level", "metric": "n_positions_all", "value": n_positions},
        {"analysis": "msd2_position_level", "metric": "n_positions_concordant", "value": int(pos_conc.sum())},
        {"analysis": "msd2_position_level", "metric": "concordant_positions_in_msd2", "value": int(t2[0, 0])},
        {"analysis": "msd2_position_level", "metric": "all_positions_in_msd2", "value": int(in_msd2.sum())},
        {"analysis": "msd2_position_level", "metric": "fisher_odds_ratio", "value": round(float(or2), 4)},
        {"analysis": "msd2_position_level", "metric": "fisher_p_two_sided", "value": f"{p2:.3e}"},
    ]
    out = pd.DataFrame(rows)
    out["source_files"] = ("results/alphagenome/alphagenome_full_cftr_results.csv; "
                           "results/comparator_scores.csv; results/paper/concordant_set.csv")
    out.to_csv(OUT, index=False)
    print(out.drop(columns="source_files").to_string(index=False))
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
