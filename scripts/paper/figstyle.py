#!/usr/bin/env python3
"""Shared figure styling and saving for the paper figures.

Centralises the PLOS Computational Biology figure rules so each figure script
states only its own content:

  file format   TIFF ("File Format": TIFF or EPS only)
  width         <= 7.5 in / 2250 px at 300 dpi ("Dimensions")
  height        <= 8.75 in / 2625 px at 300 dpi ("Dimensions")
  resolution    300 dpi ("Resolution": 300-600 dpi)
  colour mode   RGB, 8 bit per channel ("Color Mode")
  text          Arial, 8-12 pt ("Text within Figures")
  no titles     figure number, title and caption stay out of the file
                ("Text within Figures")

Also exposes the categorical palette used across figures. It was checked with
the dataviz palette validator and passes all six checks in light mode: the
lightness band, the chroma floor, colour-vision-deficiency separation, the
normal-vision floor, and contrast against the chart surface.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402

# Fixed categorical order. Never cycled, never reassigned by rank.
TOOL_COLOURS: dict[str, str] = {
    "AlphaMissense": "#0072B2",
    "PolyPhen-2": "#D55E00",
    "CADD": "#009E73",
    "SIFT": "#7A5195",
}
# Secondary encoding so identity never rests on colour alone.
TOOL_LINESTYLES: dict[str, object] = {
    "AlphaMissense": "solid",
    "PolyPhen-2": (0, (5, 1.6)),
    "CADD": (0, (1.6, 1.4)),
    "SIFT": (0, (6, 1.5, 1.2, 1.5)),
}

INK = "#1a1a1a"
MUTED = "#6b6b6b"
GRID = "#d9d9d9"

MAX_WIDTH_IN = 7.5
MAX_HEIGHT_IN = 8.75
DPI = 300


def apply_style() -> None:
    """Set the rcParams every paper figure shares."""
    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 8.5,
            "axes.labelsize": 9,
            "axes.titlesize": 9,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 8,
            "axes.edgecolor": MUTED,
            "axes.linewidth": 0.7,
            "axes.labelcolor": INK,
            "text.color": INK,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "xtick.labelcolor": INK,
            "ytick.labelcolor": INK,
            "axes.grid": False,
            "grid.color": GRID,
            "grid.linewidth": 0.5,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
            "pdf.fonttype": 42,
        }
    )


def recessive_axes(ax) -> None:
    """Drop the top and right spines and put a faint grid behind the marks."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, color=GRID, linewidth=0.5)
    ax.set_axisbelow(True)


def save_tiff(fig, path: Path) -> tuple[int, int, str]:
    """Save a figure as an RGB TIFF at 300 dpi and verify it against the rules.

    Returns (width_px, height_px, mode) of the written file. Raises if the
    figure exceeds the journal's maximum dimensions.
    """
    w_in, h_in = fig.get_size_inches()
    if w_in > MAX_WIDTH_IN + 1e-6:
        raise ValueError(f"width {w_in:.2f} in exceeds the {MAX_WIDTH_IN} in maximum")
    if h_in > MAX_HEIGHT_IN + 1e-6:
        raise ValueError(f"height {h_in:.2f} in exceeds the {MAX_HEIGHT_IN} in maximum")

    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=DPI, format="tiff", facecolor="white",
                pil_kwargs={"compression": "tiff_lzw"})

    # matplotlib writes RGBA; the journal accepts RGB or grayscale only.
    with Image.open(path) as im:
        rgb = im.convert("RGB")
        rgb.save(path, format="TIFF", compression="tiff_lzw", dpi=(DPI, DPI))
    with Image.open(path) as im:
        size, mode = im.size, im.mode
    print(f"{path.name}: {size[0]}x{size[1]} px, {mode}, {DPI} dpi, "
          f"{path.stat().st_size / 1e6:.2f} MB")
    return size[0], size[1], mode
