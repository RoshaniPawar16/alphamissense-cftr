#!/usr/bin/env python3
"""Bootstrap 95% confidence intervals for AUC and average precision.

Stage 3a of the paper-prep task. Computes percentile bootstrap confidence
intervals (2,000 resamples, seed 42) for the four-tool benchmark on the
deduplicated CFTR2-labelled cohort (rows with all four scores) and for
AlphaMissense alone on the full deduplicated validation set. Since the
2026-10-29 extractor fix every labelled variant has all four scores, so both
sets are the same 257 variants.

Point estimates are recomputed here and are expected to reproduce
results/phase1/benchmark_metrics_dedup.csv and
results/phase1/am_validation_metrics.csv.

Reads : results/phase1/benchmark_cohort_dedup.csv
Writes: results/paper/auc_ci.csv

Usage:
    python scripts/paper/p3a_auc_ci.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score

ROOT = Path(__file__).resolve().parents[2]
COHORT = ROOT / "results" / "phase1" / "benchmark_cohort_dedup.csv"
OUT = ROOT / "results" / "paper" / "auc_ci.csv"

N_BOOT = 2000
SEED = 42

# column name -> tool label used in the output table
TOOLS: dict[str, str] = {
    "am_pathogenicity": "AlphaMissense",
    "cadd_phred": "CADD",
    "polyphen_score": "PolyPhen-2",
    "sift_score_inv": "SIFT",
}


def bootstrap_ci(
    y: np.ndarray, score: np.ndarray, n_boot: int, seed: int
) -> tuple[float, float, float, float, float, float, int]:
    """Return point and percentile-bootstrap CI for AUC and average precision.

    Resamples variant indices with replacement. Resamples that contain only
    one class are discarded and do not contribute to the percentile interval.

    Returns (auc, auc_lo, auc_hi, ap, ap_lo, ap_hi, n_valid_resamples).
    """
    auc = float(roc_auc_score(y, score))
    ap = float(average_precision_score(y, score))

    rng = np.random.default_rng(seed)
    n = len(y)
    aucs: list[float] = []
    aps: list[float] = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        y_b = y[idx]
        if y_b.min() == y_b.max():
            continue
        s_b = score[idx]
        aucs.append(roc_auc_score(y_b, s_b))
        aps.append(average_precision_score(y_b, s_b))

    a = np.asarray(aucs)
    p = np.asarray(aps)
    return (
        auc,
        float(np.percentile(a, 2.5)),
        float(np.percentile(a, 97.5)),
        ap,
        float(np.percentile(p, 2.5)),
        float(np.percentile(p, 97.5)),
        len(aucs),
    )


def main() -> None:
    """Compute bootstrap CIs for both cohorts and write results/paper/auc_ci.csv."""
    df = pd.read_csv(COHORT)

    rows: list[dict[str, object]] = []

    # Cohort 1: all four tools, rows flagged included by the cohort builder (257 since 2026-10-29).
    four = df[df["included"]].reset_index(drop=True)
    y4 = four["label"].to_numpy()
    for col, tool in TOOLS.items():
        s = four[col].to_numpy(dtype=float)
        auc, alo, ahi, ap, plo, phi, nv = bootstrap_ci(y4, s, N_BOOT, SEED)
        rows.append(
            {
                "cohort": "four_tool_dedup",
                "tool": tool,
                "n": len(four),
                "n_pos": int(y4.sum()),
                "n_neg": int((y4 == 0).sum()),
                "auc": round(auc, 6),
                "auc_ci_lo": round(alo, 6),
                "auc_ci_hi": round(ahi, 6),
                "ap": round(ap, 6),
                "ap_ci_lo": round(plo, 6),
                "ap_ci_hi": round(phi, 6),
                "n_boot": N_BOOT,
                "n_boot_valid": nv,
                "seed": SEED,
                "score_column": col,
                "source_file": "results/phase1/benchmark_cohort_dedup.csv",
            }
        )

    # Cohort 2: AlphaMissense on every labelled row (equal to cohort 1 since 2026-10-29).
    y259 = df["label"].to_numpy()
    s259 = df["am_pathogenicity"].to_numpy(dtype=float)
    auc, alo, ahi, ap, plo, phi, nv = bootstrap_ci(y259, s259, N_BOOT, SEED)
    rows.append(
        {
            "cohort": "am_validation_dedup",
            "tool": "AlphaMissense",
            "n": len(df),
            "n_pos": int(y259.sum()),
            "n_neg": int((y259 == 0).sum()),
            "auc": round(auc, 6),
            "auc_ci_lo": round(alo, 6),
            "auc_ci_hi": round(ahi, 6),
            "ap": round(ap, 6),
            "ap_ci_lo": round(plo, 6),
            "ap_ci_hi": round(phi, 6),
            "n_boot": N_BOOT,
            "n_boot_valid": nv,
            "seed": SEED,
            "score_column": "am_pathogenicity",
            "source_file": "results/phase1/benchmark_cohort_dedup.csv",
        }
    )

    out = pd.DataFrame(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False)
    print(out.to_string(index=False))
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
