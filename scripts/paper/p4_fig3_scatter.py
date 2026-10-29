#!/usr/bin/env python3
"""Figure 3: AlphaGenome SPLICE quantile against SpliceAI delta.

Stage 4 of the paper-prep task. One point per variant for all 1,278
AlphaMissense-ambiguous CFTR missense SNVs, with the concordant set
highlighted and the two thresholds that define it drawn as reference lines.

The x axis is the AlphaGenome gene-mask SPLICE quantile from the 2026-10-27
rescore with exact allele matching (results/alphagenome/SOURCE.md), on a
reversed logit-like scale: the values crowd against 1.0, so
the axis is plotted as -log10(1 - quantile) to make the upper tail readable.
The y axis is the SpliceAI maximum delta on its native 0-1 scale.

Reads : results/alphagenome/alphagenome_full_cftr_results.csv
        results/comparator_scores.csv
        results/paper/concordant_set.csv
Writes: figures/paper/Fig3.tif

Usage:
    python scripts/paper/p4_fig3_scatter.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.patheffects as pe  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figstyle import (  # noqa: E402
    INK, MUTED, apply_style, recessive_axes, save_tiff,
)

ROOT = Path(__file__).resolve().parents[2]
FIG = ROOT / "figures" / "paper" / "Fig3.tif"

BACKGROUND = "#9fb3c2"
GM_ONLY = "#D55E00"
CM_TOO = "#0072B2"

AG_THRESHOLD = 0.95
SAI_THRESHOLD = 0.5


def to_axis(q: np.ndarray) -> np.ndarray:
    """Map a quantile in [0, 1) to -log10(1 - q), clipped for display."""
    return -np.log10(np.clip(1.0 - q, 1e-6, None))


def label_concordant(fig, ax, points: pd.DataFrame) -> None:
    """Direct-label the concordant points without letting the labels collide.

    Labels are placed to the left of each marker, then pushed apart vertically
    in display space until every pair clears a minimum gap. A white outline
    keeps each label legible where it crosses a marker or grid line.
    """
    fig.canvas.draw()
    xs = to_axis(points["SPLICE_SITE_USAGE_quantile_max"].to_numpy(dtype=float))
    ys = points["SpliceAI_max_delta"].to_numpy(dtype=float)
    names = points["protein_variant"].tolist()

    disp = ax.transData.transform(np.column_stack([xs, ys]))
    order = np.argsort(-disp[:, 1])
    gap = 11.0
    lab_y = disp[:, 1].astype(float).copy()
    for a, b in zip(order[:-1], order[1:]):
        if lab_y[a] - lab_y[b] < gap:
            lab_y[b] = lab_y[a] - gap

    inv = ax.transData.inverted()
    for i, name in enumerate(names):
        tx, ty = inv.transform((disp[i, 0] - 13.0, lab_y[i]))
        ax.annotate(
            name,
            xy=(xs[i], ys[i]),
            xytext=(tx, ty),
            ha="right", va="center", fontsize=6.6, color=INK,
            path_effects=[pe.withStroke(linewidth=1.8, foreground="white")],
            arrowprops=dict(arrowstyle="-", linewidth=0.5, color=MUTED,
                            shrinkA=1.0, shrinkB=3.0),
            zorder=6,
        )


def main() -> None:
    """Render Fig3.tif."""
    ag = pd.read_csv(ROOT / "results/alphagenome/alphagenome_full_cftr_results.csv")
    comp = pd.read_csv(ROOT / "results/comparator_scores.csv")
    conc = pd.read_csv(ROOT / "results/paper/concordant_set.csv")

    m = ag.merge(comp[["variant_id", "SpliceAI_max_delta"]], on="variant_id",
                 how="left", validate="one_to_one")
    assert len(m) == 1278 and m["SpliceAI_max_delta"].notna().all()

    cm_ids = set(conc.loc[conc["in_CM"] == "yes", "variant_id_hg38"])
    gm_only_ids = set(conc.loc[conc["in_CM"] == "no", "variant_id_hg38"])
    is_cm = m["variant_id"].isin(cm_ids)
    is_gm_only = m["variant_id"].isin(gm_only_ids)
    rest = ~(is_cm | is_gm_only)

    x = to_axis(m["SPLICE_SITE_USAGE_quantile_max"].to_numpy(dtype=float))
    y = m["SpliceAI_max_delta"].to_numpy(dtype=float)

    apply_style()
    fig, ax = plt.subplots(figsize=(6.4, 4.6))

    ax.axvline(to_axis(np.array([AG_THRESHOLD]))[0], color=MUTED, linewidth=0.7,
               linestyle=(0, (4, 3)), zorder=1)
    ax.axhline(SAI_THRESHOLD, color=MUTED, linewidth=0.7, linestyle=(0, (4, 3)),
               zorder=1)

    ax.scatter(x[rest], y[rest], s=9, c=BACKGROUND, alpha=0.5, linewidths=0,
               zorder=2, label=f"Not concordant (n={int(rest.sum())})")
    ax.scatter(x[is_gm_only], y[is_gm_only], s=34, facecolor=GM_ONLY,
               edgecolor="white", linewidths=0.8, marker="s", zorder=4,
               label=f"Gene mask only (n={int(is_gm_only.sum())})")
    ax.scatter(x[is_cm], y[is_cm], s=40, facecolor=CM_TOO, edgecolor="white",
               linewidths=0.8, marker="o", zorder=5,
               label=f"Gene mask and centre mask (n={int(is_cm.sum())})")

    recessive_axes(ax)
    ticks = np.array([0.0, 0.9, 0.99, 0.999, 0.9999, 0.99999])
    ax.set_xticks(to_axis(ticks))
    ax.set_xticklabels(["0", "0.9", "0.99", "0.999", "0.9999", "0.99999"])
    ax.set_xlabel("AlphaGenome gene-mask SPLICE quantile")
    ax.set_ylabel("SpliceAI maximum delta")
    ax.set_ylim(-0.03, 1.05)

    ax.text(to_axis(np.array([AG_THRESHOLD]))[0] - 0.04, 0.30, "quantile 0.95",
            fontsize=7, color=MUTED, ha="right", va="center", rotation=90)
    ax.text(0.02, SAI_THRESHOLD + 0.02, "SpliceAI 0.5", fontsize=7, color=MUTED,
            ha="left", va="bottom")

    leg = ax.legend(loc="upper left", frameon=True, framealpha=1.0,
                    edgecolor="#d9d9d9", fontsize=7.4, borderpad=0.6,
                    labelspacing=0.45, handletextpad=0.5)
    leg.get_frame().set_linewidth(0.6)

    fig.tight_layout(pad=0.4)
    label_concordant(fig, ax, m[is_cm | is_gm_only])
    save_tiff(fig, FIG)
    plt.close(fig)


if __name__ == "__main__":
    main()
