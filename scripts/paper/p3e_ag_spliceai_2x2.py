#!/usr/bin/env python3
"""Independence check: AlphaGenome SPLICE against SpliceAI on the 1,278.

Stage 3e of the paper-prep task. Cross-tabulates AlphaGenome gene-mask SPLICE
quantile > 0.95 against SpliceAI max delta > 0.2 across the 1,278
AlphaMissense-ambiguous CFTR missense variants, with a chi-square test of
independence and an odds ratio with a 95% Woolf (log) confidence interval.

One calibration is reported: the quantile served by the AlphaGenome API at
the 2026-10-27 rescore with exact allele matching (OPEN_ITEMS E0). Changed
2026-10-27: the chromosome-22 row and the August genome-wide sensitivity row
were removed.

Reads : results/alphagenome/alphagenome_full_cftr_results.csv
        results/comparator_scores.csv
Writes: results/paper/ag_spliceai_2x2.csv

Usage:
    python scripts/paper/p3e_ag_spliceai_2x2.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "paper" / "ag_spliceai_2x2.csv"

AG_THRESHOLD = 0.95
SAI_THRESHOLD = 0.2


def two_by_two(ag_high: np.ndarray, sai_high: np.ndarray, label: str,
               column: str) -> dict[str, object]:
    """Chi-square and odds ratio for one AlphaGenome quantile column."""
    a = int((ag_high & sai_high).sum())      # AG high, SpliceAI high
    b = int((ag_high & ~sai_high).sum())     # AG high, SpliceAI low
    c = int((~ag_high & sai_high).sum())     # AG low,  SpliceAI high
    d = int((~ag_high & ~sai_high).sum())    # AG low,  SpliceAI low
    table = np.array([[a, b], [c, d]])

    chi2, p_chi2, dof, expected = stats.chi2_contingency(table, correction=False)
    chi2_yates, p_yates, _, _ = stats.chi2_contingency(table, correction=True)
    fisher_or, p_fisher = stats.fisher_exact(table)

    # Woolf odds ratio with Haldane-Anscombe 0.5 correction if any cell is zero.
    if min(a, b, c, d) == 0:
        aa, bb, cc, dd = a + 0.5, b + 0.5, c + 0.5, d + 0.5
        corrected = "yes (Haldane-Anscombe 0.5, a zero cell is present)"
    else:
        aa, bb, cc, dd = float(a), float(b), float(c), float(d)
        corrected = "no"
    or_point = (aa * dd) / (bb * cc)
    se_log = float(np.sqrt(1 / aa + 1 / bb + 1 / cc + 1 / dd))
    lo = float(np.exp(np.log(or_point) - 1.96 * se_log))
    hi = float(np.exp(np.log(or_point) + 1.96 * se_log))

    return {
        "quantile_calibration": label,
        "ag_quantile_column": column,
        "n": int(table.sum()),
        "ag_threshold": f"> {AG_THRESHOLD}",
        "spliceai_threshold": f"> {SAI_THRESHOLD}",
        "n_ag_high": a + b,
        "n_spliceai_high": a + c,
        "a_ag_high_sai_high": a,
        "b_ag_high_sai_low": b,
        "c_ag_low_sai_high": c,
        "d_ag_low_sai_low": d,
        "expected_a_under_independence": round(float(expected[0][0]), 2),
        "chi2": round(float(chi2), 4),
        "chi2_dof": int(dof),
        "chi2_p": f"{p_chi2:.3e}",
        "chi2_yates": round(float(chi2_yates), 4),
        "chi2_yates_p": f"{p_yates:.3e}",
        "fisher_p_two_sided": f"{p_fisher:.3e}",
        "odds_ratio": round(float(or_point), 4),
        "or_ci_lo": round(lo, 4),
        "or_ci_hi": round(hi, 4),
        "or_zero_cell_correction": corrected,
        "direction": (
            "observed above independence expectation"
            if a > expected[0][0]
            else "observed below independence expectation"
        ),
    }


def main() -> None:
    """Build the 2x2 table and write results/paper/ag_spliceai_2x2.csv."""
    ag = pd.read_csv(ROOT / "results/alphagenome/alphagenome_full_cftr_results.csv")
    comp = pd.read_csv(ROOT / "results/comparator_scores.csv")

    m = ag.merge(
        comp[["variant_id", "SpliceAI_max_delta"]], on="variant_id",
        how="left", validate="one_to_one",
    )
    assert len(m) == 1278 and m["SpliceAI_max_delta"].notna().all()
    assert m["SPLICE_SITE_USAGE_quantile_max"].notna().all()

    rows = [
        two_by_two(
            (m["SPLICE_SITE_USAGE_quantile_max"] > AG_THRESHOLD).to_numpy(),
            (m["SpliceAI_max_delta"] > SAI_THRESHOLD).to_numpy(),
            "AlphaGenome API calibration at the 2026-10-27 rescore (only calibration)",
            "SPLICE_SITE_USAGE_quantile_max",
        ),
    ]

    out = pd.DataFrame(rows)
    out["source_files"] = (
        "results/alphagenome/alphagenome_full_cftr_results.csv; "
        "results/comparator_scores.csv"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False)
    print(out.T.to_string())
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
