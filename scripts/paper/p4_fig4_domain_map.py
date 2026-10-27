#!/usr/bin/env python3
"""Figure 4: where the 18 concordant variants sit on the CFTR protein.

Panel A: the CFTR protein from residue 1 to 1480 with its five domains, the
density of the 1,278 AlphaMissense-ambiguous variants along it (grey
histogram, 20-residue bins), and one stem per concordant variant. G970V, the
one member with a minigene result, is drawn as a filled black diamond.

Panel B: share of the 1,278 ambiguous variants and share of the 18 concordant
variants in each domain, from results/paper/domain_distribution.csv.

Reads : results/alphagenome/alphagenome_full_cftr_results.csv
        results/paper/concordant_set.csv
        results/paper/domain_distribution.csv
Writes: figures/paper/Fig4.tif

Usage:
    python scripts/paper/p4_fig4_domain_map.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figstyle import INK, MUTED, apply_style, recessive_axes, save_tiff  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
AG = ROOT / "results/alphagenome/alphagenome_full_cftr_results.csv"
CONC = ROOT / "results/paper/concordant_set.csv"
DOMAIN = ROOT / "results/paper/domain_distribution.csv"
FIG = ROOT / "figures/paper/Fig4.tif"

PROTEIN_LEN = 1480
DOMAIN_COLOURS = {
    "MSD1": "#9ecae1",
    "NBD1": "#c7e9c0",
    "R-domain": "#e0e0e0",
    "MSD2": "#9ecae1",
    "NBD2": "#c7e9c0",
}
STEM = "#0072B2"
RESIDUE_RE = re.compile(r"^[A-Z](\d+)[A-Z]$")

# Label heights for the stems, chosen so labels in the 1046 to 1060 cluster
# and at shared residues do not overlap. Keyed by protein change.
LABEL_LEVEL = {
    "R55T": 1, "R55I": 2, "A155G": 3, "K163R": 2, "L214V": 1,
    "K464R": 1, "H620Q": 1,
    "I906S": 1, "G970V": 1, "G970C": 2, "E1046V": 5, "G1047C": 4,
    "P1050L": 3, "S1058G": 4, "S1058C": 5, "K1060T": 6,
    "G1123V": 2, "L1156F": 1,
}
# Labels drawn to the left of their stem; all others go to the right.
LABEL_LEFT = {"I906S", "E1046V", "G1047C"}


def residue(change: str) -> int:
    m = RESIDUE_RE.match(change)
    if not m:
        raise ValueError(change)
    return int(m.group(1))


def main() -> None:
    ag = pd.read_csv(AG)
    conc = pd.read_csv(CONC)
    dom = pd.read_csv(DOMAIN)
    assert len(ag) == 1278 and len(conc) == 18

    ag_res = ag["protein_variant"].map(residue).to_numpy()
    conc = conc.assign(residue=conc["protein_change"].map(residue))
    missing = set(conc["protein_change"]) - set(LABEL_LEVEL)
    assert not missing, f"no label level for {missing}"

    apply_style()
    fig = plt.figure(figsize=(7.5, 5.2))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.55, 1.0], hspace=0.42)
    ax = fig.add_subplot(gs[0])
    axb = fig.add_subplot(gs[1])

    # Panel A: density of the 1,278 as a background histogram.
    bins = np.arange(0, PROTEIN_LEN + 20, 20)
    counts, edges = np.histogram(ag_res, bins=bins)
    scale = 1.0 / counts.max()
    ax.bar(edges[:-1], counts * scale * 0.9, width=20, align="edge",
           color="#cfd5db", linewidth=0, zorder=1)

    # Protein bar with domains.
    bar_y, bar_h = -0.32, 0.18
    for _, r in dom.iterrows():
        ax.add_patch(plt.Rectangle((r["residue_start"], bar_y),
                                   r["residue_end"] - r["residue_start"] + 1, bar_h,
                                   facecolor=DOMAIN_COLOURS[r["domain"]],
                                   edgecolor=MUTED, linewidth=0.5, zorder=2))
        ax.text((r["residue_start"] + r["residue_end"]) / 2, bar_y + bar_h / 2,
                r["domain"], ha="center", va="center", fontsize=7.5, color=INK, zorder=3)

    # Stems for the 18 concordant variants.
    for _, r in conc.iterrows():
        level = LABEL_LEVEL[r["protein_change"]]
        top = 0.98 + 0.13 * (level - 1)
        is_lab = str(r["in_experimental_benchmark"]).startswith("yes")
        ax.plot([r["residue"], r["residue"]], [bar_y + bar_h, top],
                color=STEM, linewidth=0.7, zorder=3)
        ax.scatter([r["residue"]], [top], s=26 if is_lab else 16,
                   marker="D" if is_lab else "o",
                   color=INK if is_lab else STEM, edgecolor="white",
                   linewidth=0.5, zorder=4)
        left = r["protein_change"] in LABEL_LEFT
        ax.text(r["residue"] + (-9 if left else 9), top, r["protein_change"],
                fontsize=6.6, va="center", ha="right" if left else "left",
                color=INK, zorder=5,
                fontweight="bold" if is_lab else "normal")

    ax.set_xlim(-5, PROTEIN_LEN + 60)
    ax.set_ylim(-0.4, 1.78)
    ax.set_yticks([])
    for side in ("left", "top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_xticks([1, 200, 400, 600, 800, 1000, 1200, 1480])
    ax.tick_params(axis="x", length=0, pad=-2)
    ax.set_xlabel("CFTR residue")
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    handles = [
        Line2D([], [], marker="o", linestyle="none", markersize=4.5, color=STEM,
               label="Concordant variant (18)"),
        Line2D([], [], marker="D", linestyle="none", markersize=5, color=INK,
               label="Splice-altering in a published minigene assay"),
        Patch(facecolor="#cfd5db", label="Density of the 1,278 ambiguous variants"),
    ]
    ax.legend(handles=handles, loc="upper left", frameon=False, fontsize=7,
              bbox_to_anchor=(0.27, 1.0), handletextpad=0.6, borderaxespad=0)
    ax.text(-0.05, 1.0, "A", transform=ax.transAxes, fontsize=11,
            fontweight="bold", va="top")

    # Panel B: share per domain.
    x = np.arange(len(dom))
    w = 0.38
    axb.bar(x - w / 2, dom["pct_of_ambiguous"], width=w, color="#cfd5db",
            edgecolor=MUTED, linewidth=0.5, label="1,278 ambiguous variants")
    axb.bar(x + w / 2, dom["pct_of_concordant"], width=w, color=STEM,
            label="18 concordant variants")
    for i, r in dom.iterrows():
        axb.text(i - w / 2, r["pct_of_ambiguous"] + 1.5, f"{r['n_ambiguous']}",
                 ha="center", fontsize=6.6, color=MUTED)
        axb.text(i + w / 2, r["pct_of_concordant"] + 1.5, f"{r['n_concordant']}",
                 ha="center", fontsize=6.6, color=INK)
    axb.set_xticks(x)
    axb.set_xticklabels(dom["domain"])
    axb.set_ylabel("Share of variants (%)")
    axb.set_ylim(0, 72)
    recessive_axes(axb)
    axb.grid(axis="x", visible=False)
    axb.legend(loc="upper left", frameon=False, fontsize=7)
    axb.text(-0.05, 1.04, "B", transform=axb.transAxes, fontsize=11,
             fontweight="bold", va="bottom")

    fig.subplots_adjust(left=0.08, right=0.98, top=0.97, bottom=0.08)
    save_tiff(fig, FIG)
    plt.close(fig)


if __name__ == "__main__":
    main()
