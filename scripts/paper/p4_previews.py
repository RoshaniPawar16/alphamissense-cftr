#!/usr/bin/env python3
"""PNG previews of the paper figures, for reading the manuscript on GitHub.

GitHub does not display TIFF files, so manuscript.md embeds these PNG copies.
The TIFF files remain the submission files.

Reads : figures/paper/*.tif
Writes: figures/paper/preview/*.png

Usage:
    python scripts/paper/p4_previews.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "figures/paper"
OUT = SRC / "preview"
MAX_WIDTH = 1600


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for tif in sorted(SRC.glob("*.tif")):
        with Image.open(tif) as im:
            im = im.convert("RGB")
            if im.width > MAX_WIDTH:
                im = im.resize((MAX_WIDTH, round(im.height * MAX_WIDTH / im.width)),
                               Image.LANCZOS)
            dest = OUT / f"{tif.stem}.png"
            im.save(dest, optimize=True)
            print(f"{dest.relative_to(ROOT)}: {im.width}x{im.height}")


if __name__ == "__main__":
    main()
