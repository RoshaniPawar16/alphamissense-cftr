#!/usr/bin/env python3
"""Rescore the 23 minigene-benchmark rows with the gene-mask splice scorer.

The archived benchmark (archive/superseded-2026-10/results/experimental_benchmark.csv)
carries gene-mask splice scores from an earlier run whose matching and
aggregation are undocumented. This script rescores the same
23 rows with the scorer and aggregation of scripts/alphagenome_full_cftr.py:
GeneMaskSplicingScorer(SPLICE_SITE_USAGE), lung tracks (UBERON:0002048),
maximum absolute raw and quantile score across tracks, each result matched on
the full variant ID chrom:pos:ref>alt. Two pairs of rows share a genomic
position (E403D as c.1209G>T and c.1209G>C; G970V and G970D at c.2909), and
exact matching keeps their scores separate.

Only gm_splice_raw and gm_splice_q are replaced. Every other column, including
the centre-mask, SpliceAI, Pangolin and CADD columns, is copied unchanged from
the archived file. Row order and columns are preserved.

Reads : archive/superseded-2026-10/results/experimental_benchmark.csv
        .env (ALPHAGENOME_API_KEY)
Writes: results/experimental_benchmark.csv

Refuses to run if the output already exists.

Usage:
    python scripts/paper/p2b_alphagenome_minigene.py
"""

from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path

import pandas as pd
from alphagenome.data import genome
from alphagenome.models import dna_client
from alphagenome.models import variant_scorers as vsl
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "archive/superseded-2026-10/results/experimental_benchmark.csv"
OUT = ROOT / "results/experimental_benchmark.csv"
ONTOLOGY = "UBERON:0002048"
HALF = dna_client.SEQUENCE_LENGTH_1MB // 2
SCORER = vsl.RECOMMENDED_VARIANT_SCORERS["SPLICE_SITE_USAGE"]


def main() -> None:
    """Score the 23 rows and write the refreshed benchmark file."""
    if OUT.exists():
        sys.exit(f"ERROR: {OUT.relative_to(ROOT)} exists. Archive it before rescoring.")
    load_dotenv(ROOT / ".env")
    key = os.environ.get("ALPHAGENOME_API_KEY", "")
    if not key:
        sys.exit("ERROR: set ALPHAGENOME_API_KEY in .env")

    src = pd.read_csv(SRC)
    assert len(src) == 23 and src["variant_id"].nunique() == 23
    parsed = src["variant_id"].str.extract(r"^(chr7):(\d+):([ACGT]+)>([ACGT]+)$")
    assert parsed.notna().all().all(), "unexpected variant_id format"

    variants = [genome.Variant(chromosome=c, position=int(p), reference_bases=r, alternate_bases=a)
                for c, p, r, a in parsed.itertuples(index=False)]
    intervals = [genome.Interval(chromosome=c, start=int(p) - HALF, end=int(p) + HALF)
                 for c, p, _, _ in parsed.itertuples(index=False)]
    model = dna_client.create(key)
    tidy = vsl.tidy_scores(model.score_variants(intervals=intervals, variants=variants,
                                                variant_scorers=[SCORER], progress_bar=False))
    lung = tidy[tidy["ontology_curie"] == ONTOLOGY]
    lung = lung.assign(_vid=lung["variant_id"].astype(str))

    raw, q = [], []
    for vid in src["variant_id"]:
        v = lung[lung["_vid"] == vid]
        if v.empty or v["quantile_score"].isna().all():
            sys.exit(f"ERROR: no gene-mask score for {vid}")
        raw.append(float(v["raw_score"].abs().max()))
        q.append(float(v["quantile_score"].abs().max()))

    out = src.copy()
    out["gm_splice_raw"] = raw
    out["gm_splice_q"] = q
    out.to_csv(OUT, index=False)
    print(f"alphagenome {metadata.version('alphagenome')}; scored "
          f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC; wrote {OUT.relative_to(ROOT)}")
    cmp = src[["protein_name", "minigene_result", "gm_splice_raw", "gm_splice_q"]].rename(
        columns={"gm_splice_raw": "raw_old", "gm_splice_q": "q_old"})
    cmp["raw_new"], cmp["q_new"] = raw, q
    print(cmp.to_string(index=False, float_format=lambda x: f"{x:.4f}"))


if __name__ == "__main__":
    main()
