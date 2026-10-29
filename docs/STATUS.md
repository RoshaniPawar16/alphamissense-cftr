# Project Status

**Branch:** main (audit work: tag audit-2026-07)  
**Last commit:** d4d1f10 (2026-08-19) — PP3 ClinGen SVI calibration  
**Status prepared:** 2026-08-28

---

## Audit note

The integrity audit (29 July – 2 August 2026) is recorded in `docs/AUDIT_RECORD.md`.
Ledger tallies (`audit/CLAIMS_LEDGER.csv`, 64 rows, column `a3_final_status`):
VERIFIED_ROUNDED 30, VERIFIED 24, CONTRADICTED 6, NOT_REPRODUCIBLE 4. An earlier
version of this note gave 41 verified / 9 corrected / 7 retracted / 6 no evidence;
those figures do not reproduce from the ledger (AUDIT_RECORD.md, Corrections 2026-10, item 1).

---

## Phase 1 — AlphaMissense benchmark on CFTR2 cohort (COMPLETE)

**Scripts:** `scripts/phase1_build_cohort.py`, `scripts/phase1_benchmark.py`,
`scripts/phase1_delong.py`, `scripts/phase1_fetch_cadd.py`

**Results:** `results/phase1/` — `archive/superseded-2026-10/results/phase1/inputs_cftr2_labels.csv` (293 rows),
inputs_cadd_scores.csv (290 data rows), inputs_polyphen_sift.csv (2,473 data rows),
am_validation_metrics.csv, `archive/superseded-2026-10/results/phase1/benchmark_cohort.csv` (292 rows) and
benchmark_cohort_dedup.csv (257 rows, keep-first on `variant`; rebuilt 2026-10-29),
`archive/superseded-2026-10/results/phase1/benchmark_metrics.csv` / `archive/superseded-2026-10/results/phase1/delong_tests.csv` (286 rows, superseded) and
benchmark_metrics_dedup.csv / delong_tests_dedup.csv / `archive/side-analyses/results/phase1/ensemble_metrics_dedup.csv`
(257 unique variants; rebuilt 2026-10-29)

**Verified numbers:**
> **Updated 2026-10-29** after the protein-name extractor fix (`docs/AUDIT_RECORD.md`, Corrections 14). The superseded 259/254 values are archived in `archive/superseded-2026-10/2026-10-29-extractor-fix/`.

- Cohort: 257 deduplicated CFTR2-labelled variants (224 CF-causing, 33 Non CF-causing), all with all four predictor scores.
  Source: `results/phase1/benchmark_cohort_dedup.csv`. The ACMG/LLM side experiment
  (`archive/side-analyses/results/acmg_llm/per_variant_log.jsonl`, 292 rows, 259 unique) used the earlier set.
- AM AUC 0.9550, AP 0.9924 on n=257. Source: `results/phase1/am_validation_metrics.csv`
- Four-tool comparison on the same n=257:
  AM 0.9550 / CADD 0.7499 / PolyPhen 0.8120 / SIFT 0.6707 AUC.
  Source: `results/phase1/benchmark_metrics_dedup.csv`
- DeLong (n=257) AM vs PolyPhen-2 Z=3.49 p=0.0005; vs CADD Z=3.82 p=0.0001;
  vs SIFT Z=6.29 p<0.0001. Source: `results/phase1/delong_tests_dedup.csv`.
  (Superseded n=254 values before the extractor fix: AUC 0.9548 / 0.7489 / 0.8109 / 0.6701; Z 3.51 / 3.83 / 6.30.)
  (Superseded n=286 values in `archive/superseded-2026-10/results/phase1/delong_tests.csv`: 3.32 / 0.0009; 3.56 / 0.0004; 6.78 / <0.0001.
  An earlier version of this note gave "Z=3.18 p=0.0015" for PolyPhen-2, which is in no results file.)

---

## AlphaGenome scoring — 1,278 CFTR variants (COMPLETE)

**Scripts:** `archive/retracted-2026-07/scripts/alphagenome_batch.py`, `scripts/alphagenome_full_cftr.py`,
`archive/retracted-2026-07/scripts/alphagenome_quantile_scores.py`, `scripts/regenerate_quantiles_genomewide.py`

**Results:** `results/alphagenome/` — l2diff_scores.csv (1278 data rows),
quantiles_genomewide_2026-08.csv (1278 rows), rescore_centermask.csv (1285 rows),
`archive/retracted-2026-07/results/alphagenome/alphagenome_rescue_variants.csv` (871 rows)

**Note:** All 1,278 variants in this pipeline are on chr7 (CFTR locus). This is the
primary cohort; the Option B modifier-loci analysis is a separate variant set.

**Key verified numbers (two definitions, corrected 2026-10-24):**
- CM definition: CM splice 501 in the top 5% of the 1,278 (threshold 0.0832, 64 variants)
  AND SpliceAI delta > 0.5 → **13** variants.
- GM definition: gene-mask SPLICE quantile > 0.95 AND SpliceAI delta > 0.5 → **18** variants.
Source: `results/alphagenome/rescore_centermask.csv` × `results/comparator_scores.csv`.
OR = 13.1–129 depending on definition (p < 0.001; AUDIT_RECORD.md:40). An earlier version
of this note attached the count 18 to the CM definition.

---

## PP3 calibration — ClinGen SVI (COMPLETE, 2026-08-19)

**Commit:** d4d1f10  
**Finding:** LP was unreachable under strict 5-criterion combining; adopting
Pejaver 2022 calibrated PP3 strength made LP reachable.  
Source: [NOT IN REPO] — no calibration analysis file exists under `results/phase1/`
(checked 2026-10-24); the finding rests on `archive/side-analyses/scripts/acmg_llm_experiment.py` and commit d4d1f10.

---

## Option B — GWAS modifier loci (ALL STAGES COMPLETE through B2c)

This is a separate analysis: AlphaGenome applied to five CF lung-disease severity
modifier loci from Corvol et al. (2015; Nat Commun 6:8382). The five modifier loci
are on chr3, chr5, chr6, chr11, and chrX — entirely separate from the 1,278 chr7/CFTR
variants above.

### B1 — hg19→hg38 liftover (COMPLETE, 2026-08-02)

**Scripts:** `scripts/b1_corvol_liftover.py`, `scripts/b1_extract_and_lift.py`

**Results:**
- `results/gwas_modifiers/B1_corvol_liftover.csv` — five lead-SNP positions hg19→hg38
- `results/gwas_modifiers/B1_lifted_hg38.csv.gz` — 49,930 clean SNVs across five loci
- `results/gwas_modifiers/B1_rejects.csv` — 206 liftover failures (chain gaps)
- `results/gwas_modifiers/B1_palindromic_strand_resolution.csv` — 72 palindromic GWS SNVs
- `results/gwas_modifiers/B1_gnomad_absent_nonsex_loci.csv` — 10 artefact exclusions
- `results/gwas_modifiers/B1_rescued_routeB_only.csv` — 2 route-B-rescued variants
- `results/gwas_modifiers/B1_REPORT.md` — full liftover report

**Input data:** `data/gwas/GWAS_results/gwasImpute2_hg19_SAKNORM_all_meta_fixed_chrPeaks1mb.txt`
(61,835 rows including chr16 extra locus; five-locus total 54,853 variants).
Provenance: `audit/gwas_provenance.md`.

**Key numbers:** 54,853 input variants → 49,930 clean SNVs → 558 GWS (p.fix < 5×10⁻⁸)
before artefact exclusion → 548 GWS taken forward after excluding 10 gnomAD-absent variants.

### B2 — AlphaGenome chromatin disruption scoring (COMPLETE, 2026-08-04)

**Scripts:** `scripts/b2_pilot.py`, `scripts/b2_score_full.py`

**Results:**
- `results/gwas_modifiers/B2_scored_variants.csv` — 574 variant-tissue pairs
- `results/gwas_modifiers/B2_splice_distances.csv` — splice distances
- `results/gwas_modifiers/B2_pilot_determinism.csv`, `B2_pilot_run1.csv`, `B2_pilot_run2.csv`

**Scorer:** CenterMaskScorer(ATAC, window=501, metric=L2_DIFF), AlphaGenome v0.6.1,
genomewide quantile calibration (post 2026-06-18). Run date: 2026-08-04.

**Tissue assignments:**
- Lung (UBERON:0002048): 3q29, 5p15, 11p13, Xq23
- Esophagus mucosa (UBERON:0006920): 3q29 secondary
- B lymphocytes (CL:0000236): 6p21 (HLA class II locus only)

**Key number:** 471 of 550 scored GWS variants (85.6%) lie beyond 500 bp of any
annotated exon boundary. Source: `results/gwas_modifiers/B2_splice_distances.csv`.

### B2b — DHS tiling scores (COMPLETE, 2026-08-04)

**Script:** `scripts/b2b_tiling.py`

**Results:** `results/gwas_modifiers/B2b_tiling_scores.csv`,
`results/gwas_modifiers/B2b_tiling_scores_PROVENANCE.md`

Source: 12 DHS elements from Stolzenburg et al. (2017; Nucleic Acids Res 45:8773).
Two luciferase-confirmed strong enhancers (chr11.2516, chr11.2521).

### B2c — control comparison (COMPLETE, 2026-08-05)

**Scripts:** `scripts/b2c_3q29_lung_rescore.py`, `scripts/b2c_control_comparison.py`

**Results:** `results/gwas_modifiers/B2c_summary.csv`,
`results/gwas_modifiers/B2c_3q29_lung_scores.csv`,
`results/gwas_modifiers/B2c_control_scores.csv`

**Finding (scope corrected 2026-10-24):** No elevated ATAC disruption at GWS variants
vs matched controls at the four loci present in `results/gwas_modifiers/B2c_summary.csv`:
5p15 (p = 0.0094), 6p21 (p = 0.073), 11p13 (p = 0.052), Xq23 (p = 0.70); two-sided
Mann–Whitney, uncorrected; all rank-biserial values negative.
**3q29 is not covered by any results file.** `scripts/b2c_control_comparison.py`
configures 3q29 for esophagus mucosa (UBERON:0006920); all 24 esophagus GWS rows in
`B2_scored_variants.csv` have an empty `ag_atac_l2d_raw`, so the script's
"insufficient data — skipping test" branch dropped 3q29 from the summary.
`scripts/b2c_3q29_lung_rescore.py` scores 24 lung controls
(`B2c_3q29_lung_scores.csv`) and prints a lung Mann–Whitney result to stdout only;
the 3q29 row in `docs/option_b_draft.md` Table 1 comes from that printout and is
[NOT IN REPO] as a results value.

### Results draft

`docs/option_b_draft.md` — complete methods and results draft, committed 2026-08-05.

---

## Not yet done (pending supervisor decision)

- **B3 variant compilation:** ClinVar + gnomAD variants within each modifier locus.
  Inclusion criteria TBD (ClinVar VUS only vs rare gnomAD vs both).
  Setup script: `scripts/gwas_loci.py` (coordinate registry, drafted 2026-08-28).
- **AlphaGenome scoring of B3 variants** — blocked on B3.
