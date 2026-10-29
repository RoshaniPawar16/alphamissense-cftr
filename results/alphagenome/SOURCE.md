# AlphaGenome scores: run record

Rescored 2026-10-27 with exact allele matching (`docs/paper/OPEN_ITEMS.md` E0). The earlier files, which matched results by position only, are in `archive/superseded-2026-10/results/alphagenome/`.

| Output | Script | Run (UTC) | Rows | sha256 |
|---|---|---|---|---|
| `alphagenome_full_cftr_results.csv` | `scripts/alphagenome_full_cftr.py` | 2026-10-27 16:42:20 to 16:48:02 | 1,278 | `4a04c45e25047c1688d8da79988be70924a98895a13672a40a329e3e394394a1` |
| `rescore_centermask.csv` | `scripts/paper/p2_alphagenome_centremask.py` | 2026-10-27 17:53:56 to 17:58:54 | 1,278 | `adbeca83ac772fd6e88542ea139ee68d0663c512beac2a40ea9fb6e2deed2ccd` |

**Software.** alphagenome SDK 0.6.1, Python 3.13.1.

**Tracks.** Lung, UBERON:0002048. Each score is the maximum absolute value across lung tracks.

**Scorers.**
- `alphagenome_full_cftr_results.csv` uses the SDK's recommended scorers for RNA_SEQ (`GeneMaskLFCScorer`), ATAC (`CenterMaskScorer`, width 501, DIFF_LOG2_SUM) and SPLICE_SITE_USAGE (`GeneMaskSplicingScorer`).
- `rescore_centermask.csv` adds `CenterMaskScorer` with DIFF_LOG2_SUM for SPLICE_SITE_USAGE at widths 501 and 2001 and for RNA_SEQ at width 501. `cm_atac_501` is copied from ATAC in the first file, which uses the same scorer.

**Calibration.** Quantiles are the calibration the API served on 2026-10-27. Nothing returned by the API names the background it used. On the 634 variants at single-allele positions, these quantiles differ from the August 2026 genome-wide file (`archive/superseded-2026-10/results/alphagenome/quantiles_genomewide_2026-08.csv`): median absolute difference 0.0165, 95th percentile 0.318, maximum 0.727. Raw scores differ from the August run by at most 3 steps of 1/256. The calibration has changed since August, and the August file cannot be regenerated from today's API.

**Stability across runs (computed 2026-10-29 from the archived and current files, single-allele positions only, where the old position-only matching could not act).**
- Gene-mask splice raw against the May 2026 run (`archive/superseded-2026-10/results/alphagenome/alphagenome_full_cftr_results.csv`): 294 of 634 changed, by at most 3 steps of 1/256. The August comparison gives the same counts.
- Centre-mask 501-base splice score against the archived Check 15 file (`archive/superseded-2026-10/results/alphagenome/rescore_centermask.csv`):
  - On the 10 variants of the 2026-10-27 validation probe (random sample, `random_state=1`, of single-allele positions), the largest absolute difference was 0.0032 (2001-base 0.0033, ATAC 0.0032, RNA 0.0174).
  - On all 634 single-allele variants, the median difference was 0.0021 and the largest 0.0118; 6 exceed 0.01.

**Minigene rows.** `results/experimental_benchmark.csv` gene-mask columns were rescored on 2026-10-29 at 20:48 UTC by `scripts/paper/p2b_alphagenome_minigene.py` (SDK 0.6.1, the same scorer and tracks, 23 rows). sha256 `8c34a502ee1ed3f4aa0fd60819f9615f1c90632ca76e6fd73b53c28c7eeef889`.

**Rows.** The seven "priority" rows of the archived centre-mask file are not rescored; that selection is retracted (`docs/AUDIT_RECORD.md` lines 84-85).
