#!/usr/bin/env python3
"""Figure 1: the idea and the study design.

Panel A is a schematic of the two ways a single-nucleotide missense change in a
CFTR exon can act: through the amino acid it changes, which protein-level
predictors score, or through the splice site it disrupts, which splice
predictors score. It is a diagram, not data.

Panel B is the study design in two parts. The counts in panel B are read from
results files so the figure cannot drift from them.

Reads : results/paper/am_class_by_label.csv
        results/paper/concordant_set.csv
        results/phase1/benchmark_cohort_dedup.csv
        results/alphagenome/alphagenome_full_cftr_results.csv
Writes: figures/paper/Fig1.tif

Usage:
    python scripts/paper/p4_fig1_design.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figstyle import INK, MUTED, apply_style, save_tiff  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
CLASS = ROOT / "results/paper/am_class_by_label.csv"
CONC = ROOT / "results/paper/concordant_set.csv"
COHORT = ROOT / "results/phase1/benchmark_cohort_dedup.csv"
AG = ROOT / "results/alphagenome/alphagenome_full_cftr_results.csv"
FIG = ROOT / "figures/paper/Fig1.tif"

EXON = "#9ecae1"
EXON_EDGE = "#3d7fb0"
SKIP = "#D55E00"
PROT = "#0072B2"
BOX = "#f3f4f6"
FIND = "#e6f0f8"


def box(ax, x, y, w, h, text, face=BOX, bold=False, size=7.6):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.006,rounding_size=0.012",
                                facecolor=face, edgecolor=MUTED, linewidth=0.6))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size,
            color=INK, fontweight="bold" if bold else "normal", linespacing=1.3)


def arrow(ax, x0, y0, x1, y1, colour=MUTED):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=9,
                                 color=colour, linewidth=0.9))


def exon(ax, x, y, w, h, label=None, face=EXON):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=face, edgecolor=EXON_EDGE, linewidth=0.6))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=7, color=INK)


def panel_a(ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(0.0, 0.98, "A", fontsize=11, fontweight="bold", va="top")
    ax.text(0.04, 0.98, "Two ways a missense change in an exon can act",
            fontsize=8.5, va="top", color=INK)

    # Gene: three exons joined by intron lines; the variant sits near the end
    # of the middle exon, close to its splice donor site.
    gy, gh = 0.74, 0.08
    ax.plot([0.20, 0.80], [gy + gh / 2] * 2, color=MUTED, linewidth=1.0, zorder=0)
    exon(ax, 0.20, gy, 0.12, gh, "exon 1")
    exon(ax, 0.44, gy, 0.12, gh, "exon 2")
    exon(ax, 0.68, gy, 0.12, gh, "exon 3")
    vx = 0.545
    ax.plot([vx, vx], [gy - 0.015, gy + gh + 0.015], color=INK, linewidth=1.6)
    ax.text(vx, gy + gh + 0.03, "missense variant\nnear the splice site", ha="center",
            va="bottom", fontsize=7, color=INK)
    ax.text(0.17, gy + gh / 2, "gene", ha="right", va="center", fontsize=7, color=MUTED)

    # Left path: protein consequence.
    arrow(ax, 0.40, gy - 0.03, 0.25, 0.53, PROT)
    ax.text(0.04, 0.60, "Protein route", fontsize=7.8, color=PROT, fontweight="bold")
    my = 0.43
    for i, (x, lab) in enumerate([(0.05, "1"), (0.15, "2"), (0.25, "3")]):
        exon(ax, x, my, 0.10, 0.06, f"exon {lab}")
    ax.plot([0.24, 0.24], [my - 0.01, my + 0.07], color=INK, linewidth=1.4)
    ax.text(0.20, my - 0.04, "normal splicing; one amino acid changed",
            ha="center", va="top", fontsize=7, color=INK)
    box(ax, 0.03, 0.06, 0.34, 0.15,
        "Scored by protein-level predictors\nAlphaMissense, PolyPhen-2,\nSIFT, CADD",
        face="#e6f0f8")

    # Right path: splicing consequence.
    arrow(ax, 0.60, gy - 0.03, 0.75, 0.53, SKIP)
    ax.text(0.96, 0.60, "Splicing route", fontsize=7.8, color=SKIP, fontweight="bold", ha="right")
    exon(ax, 0.63, my, 0.10, 0.06, "exon 1")
    exon(ax, 0.73, my, 0.10, 0.06, "exon 3")
    ax.text(0.73, my - 0.04, "splice site weakened; for example, exon 2 skipped",
            ha="center", va="top", fontsize=7, color=INK)
    box(ax, 0.61, 0.06, 0.34, 0.15,
        "Scored by splice predictors\nSpliceAI, AlphaGenome\n(not seen by protein scores)",
        face="#fbe9df")


def panel_b(ax, n_lab, n_amb_lab, n_amb_cf, n_ambiguous, n_conc):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(0.0, 0.99, "B", fontsize=11, fontweight="bold", va="top")
    ax.text(0.04, 0.99, "Study design", fontsize=8.5, va="top", color=INK)

    w, h = 0.27, 0.27
    xs = (0.03, 0.365, 0.70)
    y1, y2 = 0.55, 0.08

    ax.text(0.03, 0.885, "Part 1. How well does AlphaMissense classify known CFTR variants?",
            fontsize=7.8, fontweight="bold", color=INK)
    box(ax, xs[0], y1, w, h, f"{n_lab} CFTR missense variants\nwith a CFTR2 label\n"
        "(CF-causing or\nnon-CF-causing)")
    box(ax, xs[1], y1, w, h, "Compare AlphaMissense with\nPolyPhen-2, CADD and SIFT;\n"
        "check whether its scores\nbehave as probabilities")
    box(ax, xs[2], y1, w, h, "AlphaMissense ranks best.\n"
        f"{n_amb_cf} of {n_amb_lab} labelled variants it\ncalls ambiguous are\nCF-causing",
        face=FIND)
    arrow(ax, xs[0] + w, y1 + h / 2, xs[1], y1 + h / 2)
    arrow(ax, xs[1] + w, y1 + h / 2, xs[2], y1 + h / 2)

    ax.text(0.03, 0.415, "Part 2. Among variants AlphaMissense calls ambiguous, which might act through splicing?",
            fontsize=7.8, fontweight="bold", color=INK)
    box(ax, xs[0], y2, w, h, f"{n_ambiguous:,} possible CFTR missense\nchanges that "
        "AlphaMissense\ncalls ambiguous")
    box(ax, xs[1], y2, w, h, "Score each with AlphaGenome\nand SpliceAI; test whether\n"
        "the two agree more than\nchance")
    box(ax, xs[2], y2, w, h, f"{n_conc} variants flagged by both.\nOne, G970V, already shown\n"
        "to alter splicing in\na minigene assay", face=FIND)
    arrow(ax, xs[0] + w, y2 + h / 2, xs[1], y2 + h / 2)
    arrow(ax, xs[1] + w, y2 + h / 2, xs[2], y2 + h / 2)



def main() -> None:
    cls = pd.read_csv(CLASS).set_index("am_class")
    cohort = pd.read_csv(COHORT)
    ag = pd.read_csv(AG)
    conc = pd.read_csv(CONC)
    n_lab = len(cohort)
    n_amb_lab = int(cls.loc["ambiguous", "n_labelled"])
    n_amb_cf = int(cls.loc["ambiguous", "n_cf_causing"])
    # Changed 2026-10-29: the benchmark size is read from the cohort file.
    assert n_lab == int(cls["n_labelled"].sum()) and len(ag) == 1278 and len(conc) == 18

    apply_style()
    fig = plt.figure(figsize=(7.5, 6.2))
    ax_a = fig.add_axes([0.0, 0.50, 1.0, 0.49])
    ax_b = fig.add_axes([0.0, 0.0, 1.0, 0.49])
    panel_a(ax_a)
    panel_b(ax_b, n_lab, n_amb_lab, n_amb_cf, len(ag), len(conc))
    save_tiff(fig, FIG)
    plt.close(fig)


if __name__ == "__main__":
    main()
