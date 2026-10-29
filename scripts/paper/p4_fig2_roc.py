#!/usr/bin/env python3
"""Figure 2: discrimination (A) and calibration (B) on the deduplicated benchmark.

Panel B added 2026-10-27: reliability diagram of AlphaMissense on the
deduplicated labelled variants (257 since 2026-10-29), drawn from results/paper/calibration_n259.csv,
with the AlphaMissense ambiguous band (0.34 to 0.564) shaded.

Stage 4 of the paper-prep task. Plots the receiver operating characteristic
curve of AlphaMissense, PolyPhen-2, CADD and SIFT on the 257 deduplicated
CFTR2-labelled variants that carry all four scores, with a bootstrap
confidence band around the AlphaMissense curve.

The band is a pointwise 95% percentile band over 2,000 bootstrap resamples
(seed 42), each curve interpolated onto a common false-positive-rate grid. It
is pointwise, not simultaneous, and is drawn only for AlphaMissense so the
four curves stay readable.

Reads : results/phase1/benchmark_cohort_dedup.csv
        results/paper/auc_ci.csv
        results/paper/calibration_n259.csv
Writes: figures/paper/Fig2.tif

Usage:
    python scripts/paper/p4_fig2_roc.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.metrics import roc_curve  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figstyle import (  # noqa: E402
    INK, MUTED, TOOL_COLOURS, TOOL_LINESTYLES, apply_style, recessive_axes, save_tiff,
)

ROOT = Path(__file__).resolve().parents[2]
COHORT = ROOT / "results" / "phase1" / "benchmark_cohort_dedup.csv"
CI = ROOT / "results" / "paper" / "auc_ci.csv"
CAL = ROOT / "results" / "paper" / "calibration_n259.csv"
FIG = ROOT / "figures" / "paper" / "Fig2.tif"

N_BOOT = 2000
SEED = 42
GRID = np.linspace(0.0, 1.0, 201)

COLUMNS = {
    "AlphaMissense": "am_pathogenicity",
    "PolyPhen-2": "polyphen_score",
    "CADD": "cadd_phred",
    "SIFT": "sift_score_inv",
}


def interp_roc(y: np.ndarray, s: np.ndarray) -> np.ndarray:
    """Return the ROC curve interpolated onto the shared FPR grid."""
    fpr, tpr, _ = roc_curve(y, s)
    return np.interp(GRID, fpr, tpr)


def main() -> None:
    """Render Fig2.tif."""
    df = pd.read_csv(COHORT)
    four = df[df["included"]].reset_index(drop=True)
    y = four["label"].to_numpy()
    ci = pd.read_csv(CI)
    ci = ci[ci["cohort"] == "four_tool_dedup"].set_index("tool")

    # Pointwise bootstrap band for AlphaMissense.
    rng = np.random.default_rng(SEED)
    s_am = four["am_pathogenicity"].to_numpy(dtype=float)
    curves = []
    for _ in range(N_BOOT):
        idx = rng.integers(0, len(y), size=len(y))
        yb = y[idx]
        if yb.min() == yb.max():
            continue
        curves.append(interp_roc(yb, s_am[idx]))
    band = np.vstack(curves)
    lo = np.percentile(band, 2.5, axis=0)
    hi = np.percentile(band, 97.5, axis=0)

    apply_style()
    fig, (ax, axb) = plt.subplots(1, 2, figsize=(7.5, 3.9),
                                  gridspec_kw={"width_ratios": [1, 1], "wspace": 0.32})

    ax.fill_between(GRID, lo, hi, color=TOOL_COLOURS["AlphaMissense"], alpha=0.16,
                    linewidth=0, zorder=1,
                    label="AlphaMissense 95% bootstrap band")
    ax.plot([0, 1], [0, 1], color=MUTED, linewidth=0.7, linestyle=(0, (2, 2)),
            zorder=1)

    for tool, col in COLUMNS.items():
        fpr, tpr, _ = roc_curve(y, four[col].to_numpy(dtype=float))
        row = ci.loc[tool]
        ax.plot(fpr, tpr, color=TOOL_COLOURS[tool], linestyle=TOOL_LINESTYLES[tool],
                linewidth=1.5, zorder=3,
                label=f"{tool}  {row['auc']:.3f} ({row['auc_ci_lo']:.2f}–{row['auc_ci_hi']:.2f})")

    recessive_axes(ax)
    ax.set_xlim(-0.01, 1.01)
    ax.set_ylim(-0.01, 1.01)
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate")
    ax.set_aspect("equal")
    leg = ax.legend(loc="lower right", frameon=True, framealpha=1.0,
                    edgecolor="#d9d9d9", fontsize=7, handlelength=2.4,
                    borderpad=0.5, labelspacing=0.4, title="AUC (95% CI)",
                    title_fontsize=7)
    leg.get_frame().set_linewidth(0.6)
    ax.text(-0.2, 1.04, "A", transform=ax.transAxes, fontsize=11,
            fontweight="bold", va="bottom")

    # Panel B: reliability diagram for AlphaMissense on every labelled variant (n = 257).
    cal = pd.read_csv(CAL)
    bins = cal[cal["bin"].astype(str).str.fullmatch(r"\d+")].copy()
    bins = bins[bins["n"] > 0]
    axb.axvspan(0.34, 0.564, color="#f2c14e", alpha=0.25, linewidth=0, zorder=0)
    axb.text(0.452, 0.04, "AlphaMissense\nambiguous", ha="center", va="bottom",
             fontsize=7, color=INK)
    axb.plot([0, 1], [0, 1], color=MUTED, linewidth=0.7, linestyle=(0, (2, 2)),
             zorder=1)
    sizes = 12 + 1.6 * bins["n"].to_numpy(dtype=float)
    axb.plot(bins["mean_predicted"], bins["observed_fraction_positive"],
             color=TOOL_COLOURS["AlphaMissense"], linewidth=1.0, zorder=2)
    axb.scatter(bins["mean_predicted"], bins["observed_fraction_positive"],
                s=sizes, color=TOOL_COLOURS["AlphaMissense"], edgecolor="white",
                linewidth=0.6, zorder=3)
    for n_ref in (5, 25, 136):
        axb.scatter([], [], s=12 + 1.6 * n_ref, color=TOOL_COLOURS["AlphaMissense"],
                    edgecolor="white", linewidth=0.6, label=f"{n_ref}")
    legb = axb.legend(loc="center right", title="Variants\nin bin", title_fontsize=7,
                      fontsize=7, frameon=False, labelspacing=1.1, borderpad=0.2,
                      handletextpad=0.8, bbox_to_anchor=(1.0, 0.5))
    recessive_axes(axb)
    axb.set_xlim(-0.01, 1.01)
    axb.set_ylim(-0.01, 1.06)
    axb.set_aspect("equal")
    axb.set_xlabel("Mean AlphaMissense score in bin")
    axb.set_ylabel("Fraction CF-causing in bin")
    axb.text(-0.2, 1.04, "B", transform=axb.transAxes, fontsize=11,
             fontweight="bold", va="bottom")

    fig.subplots_adjust(left=0.09, right=0.99, top=0.93, bottom=0.12)
    save_tiff(fig, FIG)
    plt.close(fig)


if __name__ == "__main__":
    main()
