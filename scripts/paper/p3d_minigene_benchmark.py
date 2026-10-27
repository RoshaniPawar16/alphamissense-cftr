#!/usr/bin/env python3
"""Score splice predictors against minigene-validated CFTR variants.

Stage 3d of the paper-prep task. results/experimental_benchmark.csv holds 23
rows (11 minigene-positive, 12 minigene-negative) compiled from Bergougnoux
2023 and Zhang 2025. AlphaGenome gene-mask SPLICE (quantile and raw) and
SpliceAI are scored against those labels: AUC with percentile bootstrap CI
(2,000 resamples, seed 42) and 2x2 contingency tables at SpliceAI 0.2, SpliceAI
0.5 and AlphaGenome quantile 0.95.

n=23 is small. The bootstrap interval is reported so its width can be read
directly; it is not evidence that the point estimate is stable. A documented
coverage problem also applies to SpliceAI on this set: 21 of 23 rows carry a
SpliceAI delta of exactly 0, which the audit record attributes to precomputed
scores not covering exon-interior variants rather than to negative prediction.

Reads : results/experimental_benchmark.csv
Writes: results/paper/minigene_benchmark.csv

Usage:
    python scripts/paper/p3d_minigene_benchmark.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "results" / "experimental_benchmark.csv"
OUT = ROOT / "results" / "paper" / "minigene_benchmark.csv"

N_BOOT = 2000
SEED = 42

SCORERS: dict[str, str] = {
    "AlphaGenome SPLICE quantile (gene mask)": "gm_splice_q",
    "AlphaGenome SPLICE raw (gene mask)": "gm_splice_raw",
    "SpliceAI max delta": "spliceai_max_delta",
}

OPERATING_POINTS: list[tuple[str, str, float]] = [
    ("SpliceAI max delta", "spliceai_max_delta", 0.2),
    ("SpliceAI max delta", "spliceai_max_delta", 0.5),
    ("AlphaGenome SPLICE quantile (gene mask)", "gm_splice_q", 0.95),
]


def boot_auc(y: np.ndarray, s: np.ndarray) -> tuple[float, float, float, int]:
    """Point AUC plus percentile bootstrap CI; returns (auc, lo, hi, n_valid)."""
    auc = float(roc_auc_score(y, s))
    rng = np.random.default_rng(SEED)
    vals: list[float] = []
    for _ in range(N_BOOT):
        idx = rng.integers(0, len(y), size=len(y))
        yb = y[idx]
        if yb.min() == yb.max():
            continue
        vals.append(roc_auc_score(yb, s[idx]))
    a = np.asarray(vals)
    return auc, float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5)), len(vals)


def main() -> None:
    """Compute AUCs, bootstrap CIs and 2x2 tables on the minigene benchmark."""
    df = pd.read_csv(SRC)
    y = (df["minigene_result"] == "positive").to_numpy().astype(int)
    n_pos, n_neg = int(y.sum()), int((y == 0).sum())
    print(f"n={len(df)}  positive={n_pos}  negative={n_neg}")

    rows: list[dict[str, object]] = []

    for label, col in SCORERS.items():
        s = df[col].to_numpy(dtype=float)
        auc, lo, hi, nv = boot_auc(y, s)
        ap = float(average_precision_score(y, s))
        rows.append(
            {
                "analysis": "discrimination",
                "scorer": label,
                "score_column": col,
                "threshold": "",
                "n": len(df),
                "n_pos": n_pos,
                "n_neg": n_neg,
                "auc": round(auc, 6),
                "auc_ci_lo": round(lo, 6),
                "auc_ci_hi": round(hi, 6),
                "auc_ci_width": round(hi - lo, 6),
                "ap": round(ap, 6),
                "ap_baseline": round(n_pos / len(df), 6),
                "tp": "", "fp": "", "fn": "", "tn": "",
                "sensitivity": "", "specificity": "",
                "n_boot": N_BOOT,
                "n_boot_valid": nv,
                "seed": SEED,
                "note": "n=23; see stability note row",
            }
        )

    for label, col, thr in OPERATING_POINTS:
        pred = (df[col].to_numpy(dtype=float) > thr).astype(int)
        tp = int(((pred == 1) & (y == 1)).sum())
        fp = int(((pred == 1) & (y == 0)).sum())
        fn = int(((pred == 0) & (y == 1)).sum())
        tn = int(((pred == 0) & (y == 0)).sum())
        rows.append(
            {
                "analysis": "operating_point_2x2",
                "scorer": label,
                "score_column": col,
                "threshold": f"> {thr}",
                "n": len(df),
                "n_pos": n_pos,
                "n_neg": n_neg,
                "auc": "", "auc_ci_lo": "", "auc_ci_hi": "", "auc_ci_width": "",
                "ap": "", "ap_baseline": "",
                "tp": tp, "fp": fp, "fn": fn, "tn": tn,
                "sensitivity": round(tp / n_pos, 6),
                "specificity": round(tn / n_neg, 6),
                "n_boot": "", "n_boot_valid": "", "seed": "",
                "note": "",
            }
        )

    zero_sai = int((df["spliceai_max_delta"] == 0).sum())
    rows.append(
        {
            "analysis": "stability_note",
            "scorer": "all",
            "score_column": "",
            "threshold": "",
            "n": len(df),
            "n_pos": n_pos,
            "n_neg": n_neg,
            "auc": "", "auc_ci_lo": "", "auc_ci_hi": "", "auc_ci_width": "",
            "ap": "", "ap_baseline": "",
            "tp": "", "fp": "", "fn": "", "tn": "",
            "sensitivity": "", "specificity": "",
            "n_boot": N_BOOT, "n_boot_valid": "", "seed": SEED,
            "note": (
                f"n={len(df)} ({n_pos} positive, {n_neg} negative) is too small for a "
                "stable AUC: one label flip moves the estimate by roughly 1/(n_pos*n_neg) "
                f"= {1 / (n_pos * n_neg):.4f} per discordant pair and the bootstrap "
                "intervals below span a large part of the usable range. No scorer can be "
                f"selected on this benchmark. SpliceAI delta is exactly 0 for {zero_sai} "
                "of 23 rows, a precomputed-score coverage gap, so SpliceAI figures here "
                "measure coverage as much as prediction."
            ),
        }
    )

    out = pd.DataFrame(rows)
    out["source_file"] = "results/experimental_benchmark.csv"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False)
    print(out.drop(columns=["note", "source_file"]).to_string(index=False))
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
