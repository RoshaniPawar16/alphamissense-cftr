#!/usr/bin/env python3
"""Calibration of AlphaMissense scores against CFTR2 binary labels.

Stage 3b of the paper-prep task. Treats the AlphaMissense pathogenicity score
as a probability of the CF-causing class and measures how well it is
calibrated on the deduplicated validation set (257 variants since the
2026-10-29 extractor fix; the output filename keeps its earlier n259 label): ten equal-width
reliability bins over [0, 1] and the Brier score.

AlphaMissense is not trained to emit calibrated probabilities, so this is a
descriptive measurement, not a test of a stated claim.

Reads : results/phase1/benchmark_cohort_dedup.csv
Writes: results/paper/calibration_n259.csv

Usage:
    python scripts/paper/p3b_calibration.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import brier_score_loss

ROOT = Path(__file__).resolve().parents[2]
COHORT = ROOT / "results" / "phase1" / "benchmark_cohort_dedup.csv"
OUT = ROOT / "results" / "paper" / "calibration_n259.csv"

N_BINS = 10


def main() -> None:
    """Bin AlphaMissense scores, compute per-bin observed rates and the Brier score."""
    df = pd.read_csv(COHORT)
    y = df["label"].to_numpy(dtype=float)
    p = df["am_pathogenicity"].to_numpy(dtype=float)

    edges = np.linspace(0.0, 1.0, N_BINS + 1)
    # np.digitize with right=False puts p==1.0 in an overflow bin; fold it back.
    idx = np.clip(np.digitize(p, edges[1:-1], right=False), 0, N_BINS - 1)

    rows: list[dict[str, object]] = []
    for b in range(N_BINS):
        sel = idx == b
        n = int(sel.sum())
        row: dict[str, object] = {
            "bin": b + 1,
            "bin_lo": round(float(edges[b]), 2),
            "bin_hi": round(float(edges[b + 1]), 2),
            "n": n,
            "n_pos": int(y[sel].sum()) if n else 0,
            "mean_predicted": round(float(p[sel].mean()), 6) if n else "",
            "observed_fraction_positive": round(float(y[sel].mean()), 6) if n else "",
            "calibration_gap_obs_minus_pred": (
                round(float(y[sel].mean() - p[sel].mean()), 6) if n else ""
            ),
        }
        rows.append(row)

    brier = float(brier_score_loss(y, p))
    # Brier score of the no-skill model that always predicts the base rate.
    base = float(y.mean())
    brier_base = float(np.mean((y - base) ** 2))
    # Expected calibration error: sample-weighted mean absolute bin gap.
    gaps = [
        abs(float(y[idx == b].mean() - p[idx == b].mean())) * int((idx == b).sum())
        for b in range(N_BINS)
        if (idx == b).sum()
    ]
    ece = float(sum(gaps) / len(y))

    summary = [
        {"bin": "SUMMARY", "bin_lo": "", "bin_hi": "", "n": len(y),
         "n_pos": int(y.sum()), "mean_predicted": round(float(p.mean()), 6),
         "observed_fraction_positive": round(base, 6),
         "calibration_gap_obs_minus_pred": round(base - float(p.mean()), 6)},
        {"bin": "brier_score", "bin_lo": "", "bin_hi": "", "n": len(y), "n_pos": "",
         "mean_predicted": "", "observed_fraction_positive": round(brier, 6),
         "calibration_gap_obs_minus_pred": ""},
        {"bin": "brier_score_base_rate_model", "bin_lo": "", "bin_hi": "", "n": len(y),
         "n_pos": "", "mean_predicted": "",
         "observed_fraction_positive": round(brier_base, 6),
         "calibration_gap_obs_minus_pred": ""},
        {"bin": "expected_calibration_error", "bin_lo": "", "bin_hi": "", "n": len(y),
         "n_pos": "", "mean_predicted": "", "observed_fraction_positive": round(ece, 6),
         "calibration_gap_obs_minus_pred": ""},
    ]

    out = pd.DataFrame(rows + summary)
    out["source_file"] = "results/phase1/benchmark_cohort_dedup.csv"
    out["score_column"] = "am_pathogenicity"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False)
    print(out.to_string(index=False))
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
