#!/usr/bin/env python3
"""Centre-mask AlphaGenome scores for the 1,278 AlphaMissense-ambiguous variants.

Replaces the inline audit Check 15 run that produced the archived
results/alphagenome/rescore_centermask.csv (resolves OPEN_ITEMS B4). That run
matched results to variants by position only (OPEN_ITEMS E0). This script
matches on the full variant ID, chrom:pos:ref>alt, and stops if any variant
is missing.

Scorers, all CenterMaskScorer with aggregation DIFF_LOG2_SUM, as recorded in
audit/checks/CHECK_15_REPORT.md and docs/rescore_analysis.md:

  cm_splice_501   SPLICE_SITE_USAGE, width 501
  cm_splice_2001  SPLICE_SITE_USAGE, width 2001
  cm_rna_501      RNA_SEQ, width 501

Each value is the maximum absolute raw score across lung tracks
(UBERON:0002048), the same aggregation scripts/alphagenome_full_cftr.py uses.

cm_atac_501 is not rescored here. CenterMaskScorer(ATAC, 501, DIFF_LOG2_SUM)
is the SDK's recommended ATAC scorer, which scripts/alphagenome_full_cftr.py
already runs, so the column is copied from ATAC_raw_max in its output. In the
archived file cm_atac_501 also equals gm_atac_raw for every row.

The gm_* columns are copied from results/alphagenome/alphagenome_full_cftr_results.csv,
as in the archived file. The seven "priority" rows of the archived file are
not reproduced; that selection is retracted (docs/AUDIT_RECORD.md lines 84-85).
Every row has source = "full".

Reads : results/alphagenome/alphagenome_full_cftr_results.csv
        .env (ALPHAGENOME_API_KEY)
Writes: results/alphagenome/rescore_centermask.csv
        results/alphagenome/.rescore_centermask_checkpoint.csv (removed on success)

Refuses to run if the output already exists. Archive the old file first.

Usage:
    python scripts/paper/p2_alphagenome_centremask.py
"""

from __future__ import annotations

import logging
import os
import sys
import time
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path

import grpc
import numpy as np
import pandas as pd
from alphagenome.data import genome
from alphagenome.models import dna_client
from alphagenome.models import variant_scorers as vsl
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "results/alphagenome/alphagenome_full_cftr_results.csv"
OUT = ROOT / "results/alphagenome/rescore_centermask.csv"
CKPT = ROOT / "results/alphagenome/.rescore_centermask_checkpoint.csv"

ONTOLOGY = "UBERON:0002048"  # lung
BATCH_SIZE = 20
MAX_RETRIES = 5
BASE_BACKOFF = 10
HALF = dna_client.SEQUENCE_LENGTH_1MB // 2
N_EXPECTED = 1278

COLUMNS = [
    "variant_id", "protein_variant", "source", "pos", "ref", "alt",
    "cm_splice_501", "cm_splice_2001", "cm_atac_501", "cm_rna_501",
    "gm_splice_raw", "gm_splice_q", "gm_atac_raw", "gm_atac_q", "gm_rna_raw", "gm_rna_q",
]


def centre_mask(output: dna_client.OutputType, width: int) -> vsl.CenterMaskScorer:
    """Return a DIFF_LOG2_SUM centre-mask scorer for one output and width."""
    return vsl.CenterMaskScorer(
        requested_output=output, width=width,
        aggregation_type=vsl.AggregationType.DIFF_LOG2_SUM,
    )


SCORERS: dict[str, vsl.CenterMaskScorer] = {
    "cm_splice_501": centre_mask(dna_client.OutputType.SPLICE_SITE_USAGE, 501),
    "cm_splice_2001": centre_mask(dna_client.OutputType.SPLICE_SITE_USAGE, 2001),
    "cm_rna_501": centre_mask(dna_client.OutputType.RNA_SEQ, 501),
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("p2_centremask")


def score_batch(model, batch: pd.DataFrame) -> pd.DataFrame:
    """Score one batch with the three centre-mask scorers; return tidy rows."""
    variants = [
        genome.Variant(chromosome=r.CHROM, position=int(r.POS),
                       reference_bases=r.REF, alternate_bases=r.ALT)
        for r in batch.itertuples()
    ]
    intervals = [
        genome.Interval(chromosome=r.CHROM, start=int(r.POS) - HALF, end=int(r.POS) + HALF)
        for r in batch.itertuples()
    ]
    raw = model.score_variants(intervals=intervals, variants=variants,
                               variant_scorers=list(SCORERS.values()), progress_bar=False)
    return vsl.tidy_scores(raw)


def summarise(tidy: pd.DataFrame, batch: pd.DataFrame) -> pd.DataFrame:
    """Reduce tidy rows to one row per variant, matched on the full variant ID."""
    lung = tidy[tidy["ontology_curie"] == ONTOLOGY].copy()
    lung["_vid"] = lung["variant_id"].astype(str)
    lung["_scorer"] = lung["variant_scorer"].astype(str)
    rows = []
    for r in batch.itertuples():
        vdf = lung[lung["_vid"] == r.variant_id]
        if vdf.empty:
            raise RuntimeError(f"No AlphaGenome rows for {r.variant_id}")
        row = {"variant_id": r.variant_id}
        for col, scorer in SCORERS.items():
            sdf = vdf[vdf["_scorer"] == str(scorer)]
            if sdf.empty or sdf["raw_score"].isna().all():
                raise RuntimeError(f"No {col} score for {r.variant_id}")
            row[col] = float(sdf["raw_score"].abs().max())
        rows.append(row)
    return pd.DataFrame(rows)


def main() -> None:
    """Score all 1,278 variants and write rescore_centermask.csv."""
    if OUT.exists():
        sys.exit(f"ERROR: {OUT.relative_to(ROOT)} exists. Archive it before rescoring.")

    load_dotenv(ROOT / ".env")
    key = os.environ.get("ALPHAGENOME_API_KEY", "")
    if not key:
        sys.exit("ERROR: set ALPHAGENOME_API_KEY in .env")

    src = pd.read_csv(SRC)
    if len(src) != N_EXPECTED or src["variant_id"].nunique() != N_EXPECTED:
        sys.exit(f"ERROR: expected {N_EXPECTED} unique variants in {SRC.name}, got {len(src)}")

    done = pd.read_csv(CKPT) if CKPT.exists() else pd.DataFrame(columns=["variant_id"])
    todo = src[~src["variant_id"].isin(set(done["variant_id"]))].reset_index(drop=True)
    log.info("SDK alphagenome %s; %d to score, %d in checkpoint",
             metadata.version("alphagenome"), len(todo), len(done))

    model = dna_client.create(key)
    n_batches = (len(todo) + BATCH_SIZE - 1) // BATCH_SIZE
    for i, start in enumerate(range(0, len(todo), BATCH_SIZE), 1):
        batch = todo.iloc[start:start + BATCH_SIZE]
        backoff = BASE_BACKOFF
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                part = summarise(score_batch(model, batch), batch)
                part.to_csv(CKPT, mode="a", index=False,
                            header=not CKPT.exists() or CKPT.stat().st_size == 0)
                log.info("Batch %d/%d done", i, n_batches)
                break
            except (grpc.RpcError, RuntimeError, ConnectionError) as exc:
                log.warning("Batch %d attempt %d failed: %s", i, attempt, exc)
                if attempt == MAX_RETRIES:
                    sys.exit(f"ERROR: batch {i} failed {MAX_RETRIES} times; checkpoint kept")
                time.sleep(backoff)
                backoff = min(backoff * 2, 300)

    cm = pd.read_csv(CKPT).drop_duplicates(subset="variant_id")
    out = src.merge(cm, on="variant_id", how="left", validate="one_to_one")
    missing = out[list(SCORERS)].isna().any(axis=1).sum()
    if len(out) != N_EXPECTED or missing:
        sys.exit(f"ERROR: {missing} variants lack a centre-mask score; checkpoint kept")

    out = pd.DataFrame({
        "variant_id": out["variant_id"],
        "protein_variant": out["protein_variant"],
        "source": "full",
        "pos": out["POS"],
        "ref": out["REF"],
        "alt": out["ALT"],
        "cm_splice_501": out["cm_splice_501"],
        "cm_splice_2001": out["cm_splice_2001"],
        "cm_atac_501": out["ATAC_raw_max"],
        "cm_rna_501": out["cm_rna_501"],
        "gm_splice_raw": out["SPLICE_SITE_USAGE_raw_max"],
        "gm_splice_q": out["SPLICE_SITE_USAGE_quantile_max"],
        "gm_atac_raw": out["ATAC_raw_max"],
        "gm_atac_q": out["ATAC_quantile_max"],
        "gm_rna_raw": out["RNA_SEQ_raw_max"],
        "gm_rna_q": out["RNA_SEQ_quantile_max"],
    })[COLUMNS]
    out.to_csv(OUT, index=False)
    CKPT.unlink()
    log.info("Wrote %s (%d rows) at %s UTC", OUT.relative_to(ROOT), len(out),
             datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"))


if __name__ == "__main__":
    main()
