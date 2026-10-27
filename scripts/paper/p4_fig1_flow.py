#!/usr/bin/env python3
"""S1 Fig: study flow for both variant chains (was Figure 1 before 2026-10-27).

Stage 4 of the paper-prep task. Draws the two provenance chains side by side:
the CFTR2-labelled benchmark chain and the AlphaMissense-ambiguous screening
chain. The two chains are drawn separately on purpose. They are not nested:
the 1,278 ambiguous variants are drawn from the full AlphaMissense CFTR table,
not from the 3,220 protein changes extracted from the ClinVar VCF, and only
431 variants are common to both.

Every number in the figure is recomputed here from a repository file and
written to results/paper/fig1_flow_counts.csv alongside the figure, so each
box can be traced to a file and column.

Output follows the PLOS Computational Biology figure rules: TIFF, 300 dpi,
RGB, 7.5 in maximum width, Arial 8-12 pt, no title inside the figure file.

Reads : results/phase1/unique_variant_counts.csv
        results/phase1/benchmark_metrics_dedup.csv
        results/phase1/benchmark_cohort_dedup.csv
        data/cftr_alphamissense.tsv
        data/cftr2_results_annotated.csv
        results/alphagenome/alphagenome_full_cftr_results.csv
        results/paper/concordant_set.csv
Writes: figures/paper/S1_Fig.tif
        results/paper/fig1_flow_counts.csv

Usage:
    python scripts/paper/p4_fig1_flow.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

import sys  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from figstyle import INK, MUTED, apply_style, save_tiff  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
FIG = ROOT / "figures" / "paper" / "S1_Fig.tif"
COUNTS = ROOT / "results" / "paper" / "fig1_flow_counts.csv"

BOX_EDGE = "#4a4a4a"
BOX_FACE = "#f2f2f2"
HILITE_FACE = "#dce8f2"


def collect_counts() -> tuple[dict[str, int], list[dict[str, object]]]:
    """Recompute every flow-diagram number and return it with its provenance."""
    uvc = pd.read_csv(ROOT / "results/phase1/unique_variant_counts.csv").set_index("set_name")
    bm = pd.read_csv(ROOT / "results/phase1/benchmark_metrics_dedup.csv")
    amt = pd.read_csv(ROOT / "data/cftr_alphamissense.tsv", sep="\t")
    ann = pd.read_csv(ROOT / "data/cftr2_results_annotated.csv")
    ag = pd.read_csv(ROOT / "results/alphagenome/alphagenome_full_cftr_results.csv")
    conc = pd.read_csv(ROOT / "results/paper/concordant_set.csv")

    amb = amt[amt["am_class"] == "ambiguous"]
    # 2026-10-27: the screening chain now shows how the concordant set arises
    # (SpliceAI > 0.5 first, then AlphaGenome splice quantile > 0.95). The old
    # "ATAC or SPLICE > 0.95" box (778) did not match the set definition.
    sai = ag.merge(pd.read_csv(ROOT / "results/comparator_scores.csv")[["variant_id", "SpliceAI_max_delta"]],
                   on="variant_id", how="left", validate="one_to_one")["SpliceAI_max_delta"]
    am_row = bm[bm["tool"] == "AlphaMissense"].iloc[0]

    c = {
        "vcf_protein_changes": int(uvc.loc["annotated_table_all", "unique_count"]),
        "convertible": int(uvc.loc["am_variant_converted", "unique_count"]),
        "not_convertible": int(uvc.loc["am_variant_not_converted", "unique_count"]),
        "nonsense": int(uvc.loc["ter_set_nonsense_Ter_suffix", "unique_count"]),
        "stoploss": int(uvc.loc["ter_set_stop_loss_Ter_prefix", "unique_count"]),
        "am_scored": int(uvc.loc["am_scored_any_cftr2_status", "unique_count"]),
        "binary": int(uvc.loc["binary_validation_set", "unique_count"]),
        "binary_pos": int(uvc.loc["binary_validation_CF_causing", "unique_count"]),
        "binary_neg": int(uvc.loc["binary_validation_Non_CF_causing", "unique_count"]),
        "four_tool": int(am_row["n"]),
        "four_tool_pos": int(am_row["n_pos"]),
        "four_tool_neg": int(am_row["n_neg"]),
        "am_table_rows": len(amt),
        "am_table_unique_protein": int(amt["protein_variant"].nunique()),
        "ambiguous_rows": len(amb),
        "ambiguous_unique_protein": int(amb["protein_variant"].nunique()),
        "spliceai_gt_0.5": int((sai > 0.5).sum()),
        "concordant_gm": int((conc["in_GM"] == "yes").sum()),
        "concordant_cm": int((conc["in_CM"] == "yes").sum()),
        "overlap_1278_with_3220": int(
            ag["protein_variant"].isin(set(ann["am_variant"].dropna())).sum()
        ),
    }

    prov = [
        ("vcf_protein_changes", "results/phase1/unique_variant_counts.csv", "annotated_table_all:unique_count"),
        ("convertible", "results/phase1/unique_variant_counts.csv", "am_variant_converted:unique_count"),
        ("not_convertible", "results/phase1/unique_variant_counts.csv", "am_variant_not_converted:unique_count"),
        ("nonsense", "results/phase1/unique_variant_counts.csv", "ter_set_nonsense_Ter_suffix:unique_count"),
        ("stoploss", "results/phase1/unique_variant_counts.csv", "ter_set_stop_loss_Ter_prefix:unique_count"),
        ("am_scored", "results/phase1/unique_variant_counts.csv", "am_scored_any_cftr2_status:unique_count"),
        ("binary", "results/phase1/unique_variant_counts.csv", "binary_validation_set:unique_count"),
        ("binary_pos", "results/phase1/unique_variant_counts.csv", "binary_validation_CF_causing:unique_count"),
        ("binary_neg", "results/phase1/unique_variant_counts.csv", "binary_validation_Non_CF_causing:unique_count"),
        ("four_tool", "results/phase1/benchmark_metrics_dedup.csv", "AlphaMissense:n"),
        ("four_tool_pos", "results/phase1/benchmark_metrics_dedup.csv", "AlphaMissense:n_pos"),
        ("four_tool_neg", "results/phase1/benchmark_metrics_dedup.csv", "AlphaMissense:n_neg"),
        ("am_table_rows", "data/cftr_alphamissense.tsv", "row count"),
        ("am_table_unique_protein", "data/cftr_alphamissense.tsv", "protein_variant:nunique"),
        ("ambiguous_rows", "data/cftr_alphamissense.tsv", "am_class=='ambiguous':row count"),
        ("ambiguous_unique_protein", "data/cftr_alphamissense.tsv", "am_class=='ambiguous':protein_variant:nunique"),
        ("spliceai_gt_0.5", "results/alphagenome/alphagenome_full_cftr_results.csv x "
         "results/comparator_scores.csv", "SpliceAI_max_delta>0.5"),
        ("concordant_gm", "results/paper/concordant_set.csv", "in_GM=='yes'"),
        ("concordant_cm", "results/paper/concordant_set.csv", "in_CM=='yes'"),
        ("overlap_1278_with_3220", "results/alphagenome/alphagenome_full_cftr_results.csv "
         "x data/cftr2_results_annotated.csv", "protein_variant in am_variant"),
    ]
    rows = [{"box_number": k, "value": c[k], "source_file": f, "source_locator": loc}
            for k, f, loc in prov]
    return c, rows


def box(ax, x: float, y: float, w: float, h: float, text: str, *,
        face: str = BOX_FACE, size: float = 8.5) -> None:
    """Draw one rounded flow box with centred text."""
    ax.add_patch(
        FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.0,rounding_size=0.12",
            linewidth=0.8, edgecolor=BOX_EDGE, facecolor=face,
        )
    )
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=size, color=INK, linespacing=1.45)


def arrow(ax, x: float, y0: float, y1: float) -> None:
    """Draw a vertical flow arrow between two boxes."""
    ax.add_patch(
        FancyArrowPatch((x, y0), (x, y1), arrowstyle="-|>", mutation_scale=9,
                        linewidth=0.8, color=BOX_EDGE, shrinkA=0, shrinkB=0)
    )


def side_note(ax, x: float, y: float, text: str) -> None:
    """Draw an exclusion note to the right of the main flow."""
    ax.text(x, y, text, ha="left", va="center", fontsize=7.5, color=MUTED,
            linespacing=1.4)


def main() -> None:
    """Render S1_Fig.tif and write the per-box provenance table."""
    c, prov_rows = collect_counts()

    apply_style()

    fig, ax = plt.subplots(figsize=(7.5, 6.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    lx, rx = 3, 54        # left and right column origins
    bw = 36               # box width
    bh = 9.5              # box height

    # Column headers (these name the chain, they are not the figure title).
    ax.text(lx + bw / 2, 97, "Benchmark chain", ha="center", fontsize=9.5,
            color=INK, fontweight="bold")
    ax.text(rx + bw / 2, 97, "Screening chain", ha="center", fontsize=9.5,
            color=INK, fontweight="bold")

    # ---- left chain -------------------------------------------------------
    ys = [83.5, 68.5, 53.5, 38.5, 23.5]
    left = [
        f"ClinVar CFTR-region VCF\n{c['vcf_protein_changes']:,} unique protein changes",
        f"{c['convertible']:,} convertible to\nAlphaMissense notation",
        f"{c['am_scored']:,} with an\nAlphaMissense score",
        (f"{c['binary']} with a binary CFTR2 label\n"
         f"({c['binary_pos']} CF-causing, {c['binary_neg']} Non CF-causing)"),
        (f"{c['four_tool']} with CADD, PolyPhen-2\nand SIFT scores as well\n"
         f"({c['four_tool_pos']} / {c['four_tool_neg']})"),
    ]
    for i, (y, txt) in enumerate(zip(ys, left)):
        box(ax, lx, y, bw, bh, txt, face=HILITE_FACE if i == len(ys) - 1 else BOX_FACE)
        if i:
            arrow(ax, lx + bw / 2, ys[i - 1], y + bh)

    side_note(ax, lx + bw + 1.5, 76,
              f"−{c['not_convertible']}\n{c['nonsense']} nonsense\n{c['stoploss']} stop-loss")
    side_note(ax, lx + bw + 1.5, 61.5,
              f"−{c['convertible'] - c['am_scored']:,}\nno AlphaMissense\nscore")
    side_note(ax, lx + bw + 1.5, 46.5,
              f"−{c['am_scored'] - c['binary']:,}\nno binary\nCFTR2 label")
    side_note(ax, lx + bw + 1.5, 32, "−5 no CADD\nv1.7 score")

    # ---- right chain ------------------------------------------------------
    rys = [83.5, 65.5, 47.5, 26.0]
    right = [
        (f"AlphaMissense CFTR table\n{c['am_table_rows']:,} scored SNVs\n"
         f"({c['am_table_unique_protein']:,} unique protein changes)"),
        (f"{c['ambiguous_rows']:,} AlphaMissense-ambiguous SNVs\n"
         f"({c['ambiguous_unique_protein']:,} unique protein changes)"),
        (f"{c['spliceai_gt_0.5']} with SpliceAI > 0.5"),
        (f"{c['concordant_gm']} also with AlphaGenome splice\n"
         f"quantile > 0.95; {c['concordant_cm']} also meet\n"
         f"the narrower 501-base definition"),
    ]
    heights = [12.0, 9.5, 9.5, 12.0]
    for i, (y, txt, h) in enumerate(zip(rys, right, heights)):
        box(ax, rx, y, bw, h, txt, face=HILITE_FACE if i == len(rys) - 1 else BOX_FACE)
        if i:
            arrow(ax, rx + bw / 2, rys[i - 1], y + h)

    # ---- note that the two chains are not nested --------------------------
    ax.plot([lx + bw / 2, lx + bw / 2, rx + bw / 2, rx + bw / 2],
            [15.5, 11.5, 11.5, 22.5], color=MUTED, linewidth=0.7,
            linestyle=(0, (3, 3)))
    ax.text(50, 8.2,
            f"The two chains are separate variant sets, not nested: "
            f"{c['overlap_1278_with_3220']} of the {c['ambiguous_rows']:,}\n"
            f"ambiguous SNVs also appear among the {c['vcf_protein_changes']:,} "
            f"protein changes of the benchmark chain.",
            ha="center", va="center", fontsize=7.5, color=MUTED, linespacing=1.5)

    fig.tight_layout(pad=0.3)
    save_tiff(fig, FIG)
    plt.close(fig)

    COUNTS.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(prov_rows).to_csv(COUNTS, index=False)
    print(pd.DataFrame(prov_rows).to_string(index=False))
    print(f"\nwrote {FIG.relative_to(ROOT)} and {COUNTS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
