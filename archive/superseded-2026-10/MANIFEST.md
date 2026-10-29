# Archive: superseded files

**Archived:** 2026-10-27 · **Branch:** paper-prep-2026-10 · **Method:** `git mv` (history preserved; nothing deleted)

Files replaced by later work: the pre-deduplication 292-row and 286-row benchmark, the notebooks and figures built on it, earlier reports replaced by `docs/paper/manuscript.md`, an intermediate checkpoint, and a literature summary whose references are now verified in the manuscript. Each file keeps its original relative path under this folder.

References point to `docs/AUDIT_RECORD.md`, section "Corrections (2026-10)" (items 1–13).

Links to these files inside `audit/`, `docs/AUDIT_RECORD.md`, other archived files and all `.py` and `.ipynb` files were deliberately left unchanged so the audit trail reads as written. This manifest is the map from old path to new path.

| Path | Original location | Reason | Reference |
|---|---|---|---|
| `archive/superseded-2026-10/results/phase1/benchmark_cohort.csv` | `results/phase1/benchmark_cohort.csv` | 292-row cohort before deduplication; replaced by `benchmark_cohort_dedup.csv` | AUDIT_RECORD.md Corrections items 5 and 9 |
| `archive/superseded-2026-10/results/phase1/benchmark_metrics.csv` | `results/phase1/benchmark_metrics.csv` | 286-row four-tool metrics; replaced by `benchmark_metrics_dedup.csv` | AUDIT_RECORD.md Corrections items 9 and 13 |
| `archive/superseded-2026-10/results/phase1/delong_tests.csv` | `results/phase1/delong_tests.csv` | 286-row DeLong tests; replaced by `delong_tests_dedup.csv` | AUDIT_RECORD.md Corrections items 2 and 9 |
| `archive/superseded-2026-10/results/phase1/inputs_cftr2_labels.csv` | `results/phase1/inputs_cftr2_labels.csv` | 292-row label table before deduplication; read by nothing downstream | AUDIT_RECORD.md Corrections item 5 |
| `archive/superseded-2026-10/scripts/comparison_analysis.py` | `scripts/comparison_analysis.py` | Reads only the 286-row files | AUDIT_RECORD.md Corrections item 9 |
| `archive/superseded-2026-10/notebooks/comparison.ipynb` | `notebooks/comparison.ipynb` | Four-tool benchmark notebook; replaced by `phase1_benchmark.py` and `phase1_delong.py` | AUDIT_RECORD.md Corrections item 9 |
| `archive/superseded-2026-10/notebooks/ensemble.ipynb` | `notebooks/ensemble.ipynb` | Ensemble notebook; replaced by `phase1_ensemble_dedup.py`, now in `archive/side-analyses/` | AUDIT_RECORD.md Corrections item 9 |
| `archive/superseded-2026-10/figures/roc_4way.png` | `figures/roc_4way.png` | Output of `comparison.ipynb`, which predates deduplication; replaced by `figures/paper/Fig2.tif` | AUDIT_RECORD.md Corrections item 9 |
| `archive/superseded-2026-10/figures/pr_4way.png` | `figures/pr_4way.png` | Output of `comparison.ipynb` | AUDIT_RECORD.md Corrections item 9 |
| `archive/superseded-2026-10/figures/roc_comparison.png` | `figures/roc_comparison.png` | Output of `comparison.ipynb` | AUDIT_RECORD.md Corrections item 9 |
| `archive/superseded-2026-10/figures/ensemble_vs_am.png` | `figures/ensemble_vs_am.png` | Output of `ensemble.ipynb` | AUDIT_RECORD.md Corrections item 9 |
| `archive/superseded-2026-10/figures/ensemble_weights.png` | `figures/ensemble_weights.png` | Output of `ensemble.ipynb` | AUDIT_RECORD.md Corrections item 9 |
| `archive/superseded-2026-10/figures/calibration_plot.png` | `figures/calibration_plot.png` | Earlier calibration plot from `alphamissense.ipynb`; replaced by `results/paper/calibration_n259.csv` | None |
| `archive/superseded-2026-10/figures/summary_plot.png` | `figures/summary_plot.png` | Earlier summary plot from `alphamissense.ipynb` | None |
| `archive/superseded-2026-10/docs/REPORT.md` | `docs/REPORT.md` | Full project report; replaced by `docs/paper/manuscript.md` | AUDIT_RECORD.md Corrections items 9 and 13 |
| `archive/superseded-2026-10/docs/SUMMARY.md` | `docs/SUMMARY.md` | Short summary; replaced by `docs/paper/manuscript.md` | None |
| `archive/superseded-2026-10/docs/phase1_reproduction_report.md` | `docs/phase1_reproduction_report.md` | Reproduction of the 292-row and 286-row pipeline | AUDIT_RECORD.md Corrections items 8 and 9 |
| `archive/superseded-2026-10/results/.comparator_scores_checkpoint.csv` | `results/.comparator_scores_checkpoint.csv` | Intermediate checkpoint from `fetch_comparator_scores.py` | None |
| `archive/superseded-2026-10/docs/literature_review.md` | `docs/literature_review.md` | References are now verified in `docs/paper/manuscript.md`; the file contains summaries corrected in the 2026-10-27 fact check | None |
| `archive/superseded-2026-10/results/alphagenome/alphagenome_full_cftr_results.csv` | `results/alphagenome/alphagenome_full_cftr_results.csv` | Position-only matching; see OPEN_ITEMS E0. Archived 2026-10-27 before the rescore with exact allele matching. | `docs/paper/OPEN_ITEMS.md` E0 |
| `archive/superseded-2026-10/results/alphagenome/quantiles_genomewide_2026-08.csv` | `results/alphagenome/quantiles_genomewide_2026-08.csv` | Position-only matching; see OPEN_ITEMS E0. Archived 2026-10-27; the rescore uses the single calibration the API now serves. | `docs/paper/OPEN_ITEMS.md` E0 |
| `archive/superseded-2026-10/results/alphagenome/rescore_centermask.csv` | `results/alphagenome/rescore_centermask.csv` | Position-only matching; see OPEN_ITEMS E0. Archived 2026-10-27; replaced by the output of `scripts/paper/p2_alphagenome_centremask.py`. | `docs/paper/OPEN_ITEMS.md` E0 |
| `archive/superseded-2026-10/results/paper/concordant_set.csv` | `results/paper/concordant_set.csv` | Built from position-matched AlphaGenome scores with chromosome-22 and August columns; copied (not moved) 2026-10-27 before regeneration. Same 18 members. | `docs/paper/OPEN_ITEMS.md` E0 |
| `archive/superseded-2026-10/results/paper/ag_spliceai_2x2.csv` | `results/paper/ag_spliceai_2x2.csv` | Two-calibration 2x2 from position-matched scores; copied 2026-10-27 before regeneration | `docs/paper/OPEN_ITEMS.md` E0 |
| `archive/superseded-2026-10/results/paper/concordant_set_origin.csv` | `results/paper/concordant_set_origin.csv` | Counts from position-matched scores; copied 2026-10-27 before regeneration | `docs/paper/OPEN_ITEMS.md` E0 |
| `archive/superseded-2026-10/results/experimental_benchmark.csv` | `results/experimental_benchmark.csv` | Gene-mask splice scores from an earlier run with undocumented matching; moved 2026-10-29 before `scripts/paper/p2b_alphagenome_minigene.py` rescored `gm_splice_raw` and `gm_splice_q` with exact variant-ID matching. All other columns carried over unchanged. | `docs/paper/OPEN_ITEMS.md` E0 |
| `archive/superseded-2026-10/results/paper/minigene_benchmark.csv` | `results/paper/minigene_benchmark.csv` | Minigene AUCs from the earlier gene-mask scores; copied 2026-10-29 before `p3d` was rerun | `docs/paper/OPEN_ITEMS.md` E0 |
| `archive/superseded-2026-10/results/paper/fig1_flow_counts.csv` | `results/paper/fig1_flow_counts.csv` | Committed copy predated the current `p4_fig1_flow.py` (778 box replaced by SpliceAI > 0.5); copied 2026-10-27 before regeneration | None |

## Regeneration at the old path

Four scripts stay in place because they produce inputs to the paper. Re-running them will recreate some of the files above at their old paths as untracked files. Those copies are not part of the paper and should not be committed.

| Script (stays in place) | Recreates at the old path | When |
|---|---|---|
| `scripts/phase1_build_cohort.py` | `results/phase1/benchmark_cohort.csv`, `results/phase1/inputs_cftr2_labels.csv` | Every run |
| `scripts/phase1_benchmark.py` | `results/phase1/benchmark_metrics.csv` | When run without `--out` |
| `scripts/phase1_delong.py` | `results/phase1/delong_tests.csv` | When run without `--out` |
| `scripts/fetch_comparator_scores.py` | `results/.comparator_scores_checkpoint.csv` | Every run |

`notebooks/alphamissense.ipynb` also stays in place, because it produces `data/` inputs. Re-running it recreates `figures/calibration_plot.png` and `figures/summary_plot.png`.

The paper invocations of `phase1_benchmark.py` and `phase1_delong.py` pass `--cohort results/phase1/benchmark_cohort_dedup.csv` and the `_dedup` output paths (AUDIT_RECORD.md Corrections item 9). Their default input, `results/phase1/benchmark_cohort.csv`, now lives here, so running either script without arguments will fail unless `phase1_build_cohort.py` has run first.

## Running archived scripts and notebooks

The archived script and notebooks use paths relative to the repository root. They will not run from this folder without edits. They are kept as a record.

## Added 2026-10-29: extractor fix

Every file below was archived before the rebuild that followed the protein-name extractor fix (`scripts/hgvsp_names.py`). Files that came out byte-identical were moved back and are not listed. The untracked `data/` inputs (`cftr2_results.csv`, `cftr2_results_annotated.csv` and five derived tables) cannot be moved with `git mv`; their previous versions are kept locally in `data/superseded-2026-10/`, which is gitignored.

| Path | Original location | Reason | Reference |
|---|---|---|---|
| `archive/superseded-2026-10/2026-10-29-extractor-fix/docs/paper/tables/Table2_four_tool_benchmark.md` | `docs/paper/tables/Table2_four_tool_benchmark.md` | Built from the inventory produced by the old extractor (436 frameshift-derived missense names and 2 stop-loss names); regenerated 2026-10-29 with the fixed extractor (git mv) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/figures/paper/Fig1.tif` | `figures/paper/Fig1.tif` | Built from the inventory produced by the old extractor (436 frameshift-derived missense names and 2 stop-loss names); regenerated 2026-10-29 with the fixed extractor (git mv) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/figures/paper/Fig2.tif` | `figures/paper/Fig2.tif` | Built from the inventory produced by the old extractor (436 frameshift-derived missense names and 2 stop-loss names); regenerated 2026-10-29 with the fixed extractor (git mv) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/figures/paper/S1_Fig.tif` | `figures/paper/S1_Fig.tif` | Built from the inventory produced by the old extractor (436 frameshift-derived missense names and 2 stop-loss names); regenerated 2026-10-29 with the fixed extractor (git mv) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/figures/paper/preview/Fig1.png` | `figures/paper/preview/Fig1.png` | Built from the inventory produced by the old extractor (436 frameshift-derived missense names and 2 stop-loss names); regenerated 2026-10-29 with the fixed extractor (git mv) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/figures/paper/preview/Fig2.png` | `figures/paper/preview/Fig2.png` | Built from the inventory produced by the old extractor (436 frameshift-derived missense names and 2 stop-loss names); regenerated 2026-10-29 with the fixed extractor (git mv) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/figures/paper/preview/S1_Fig.png` | `figures/paper/preview/S1_Fig.png` | Built from the inventory produced by the old extractor (436 frameshift-derived missense names and 2 stop-loss names); regenerated 2026-10-29 with the fixed extractor (git mv) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/results/paper/am_class_by_label.csv` | `results/paper/am_class_by_label.csv` | Built from the inventory produced by the old extractor (436 frameshift-derived missense names and 2 stop-loss names); regenerated 2026-10-29 with the fixed extractor (git mv) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/results/paper/am_class_by_label_clean.csv` | `results/paper/am_class_by_label_clean.csv` | Built from the inventory produced by the old extractor (436 frameshift-derived missense names and 2 stop-loss names); regenerated 2026-10-29 with the fixed extractor (untracked before archiving) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/results/paper/auc_ci.csv` | `results/paper/auc_ci.csv` | Built from the inventory produced by the old extractor (436 frameshift-derived missense names and 2 stop-loss names); regenerated 2026-10-29 with the fixed extractor (git mv) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/results/paper/auc_ci_clean.csv` | `results/paper/auc_ci_clean.csv` | Built from the inventory produced by the old extractor (436 frameshift-derived missense names and 2 stop-loss names); regenerated 2026-10-29 with the fixed extractor (untracked before archiving) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/results/paper/benchmark_contamination_audit.csv` | `results/paper/benchmark_contamination_audit.csv` | Built from the inventory produced by the old extractor (436 frameshift-derived missense names and 2 stop-loss names); regenerated 2026-10-29 with the fixed extractor (untracked before archiving) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/results/paper/calibration_clean.csv` | `results/paper/calibration_clean.csv` | Built from the inventory produced by the old extractor (436 frameshift-derived missense names and 2 stop-loss names); regenerated 2026-10-29 with the fixed extractor (untracked before archiving) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/results/paper/calibration_n259.csv` | `results/paper/calibration_n259.csv` | Built from the inventory produced by the old extractor (436 frameshift-derived missense names and 2 stop-loss names); regenerated 2026-10-29 with the fixed extractor (git mv) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/results/paper/concordant_set_origin.csv` | `results/paper/concordant_set_origin.csv` | Built from the inventory produced by the old extractor (436 frameshift-derived missense names and 2 stop-loss names); regenerated 2026-10-29 with the fixed extractor (git mv) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/results/paper/delong_tests_clean.csv` | `results/paper/delong_tests_clean.csv` | Built from the inventory produced by the old extractor (436 frameshift-derived missense names and 2 stop-loss names); regenerated 2026-10-29 with the fixed extractor (untracked before archiving) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/results/paper/fig1_flow_counts.csv` | `results/paper/fig1_flow_counts.csv` | Built from the inventory produced by the old extractor (436 frameshift-derived missense names and 2 stop-loss names); regenerated 2026-10-29 with the fixed extractor (git mv) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/results/paper/inventory_audit_summary.csv` | `results/paper/inventory_audit_summary.csv` | Built from the inventory produced by the old extractor (436 frameshift-derived missense names and 2 stop-loss names); regenerated 2026-10-29 with the fixed extractor (untracked before archiving) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/results/paper/inventory_nonmissense_audit.csv` | `results/paper/inventory_nonmissense_audit.csv` | Built from the inventory produced by the old extractor (436 frameshift-derived missense names and 2 stop-loss names); regenerated 2026-10-29 with the fixed extractor (untracked before archiving) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/results/phase1/SOURCE.md` | `results/phase1/SOURCE.md` | Input checksums of the old annotated table; regenerated 2026-10-29 with the fixed extractor (git mv) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/results/phase1/am_validation_metrics.csv` | `results/phase1/am_validation_metrics.csv` | Built from the inventory produced by the old extractor (436 frameshift-derived missense names and 2 stop-loss names); regenerated 2026-10-29 with the fixed extractor (git mv) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/results/phase1/benchmark_cohort_dedup.csv` | `results/phase1/benchmark_cohort_dedup.csv` | 259-variant cohort including 2 frameshift-derived names; 5 lacked CADD; regenerated 2026-10-29 with the fixed extractor (git mv) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/results/phase1/benchmark_metrics_dedup.csv` | `results/phase1/benchmark_metrics_dedup.csv` | Built from the inventory produced by the old extractor (436 frameshift-derived missense names and 2 stop-loss names); regenerated 2026-10-29 with the fixed extractor (git mv) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/results/phase1/delong_tests_dedup.csv` | `results/phase1/delong_tests_dedup.csv` | Built from the inventory produced by the old extractor (436 frameshift-derived missense names and 2 stop-loss names); regenerated 2026-10-29 with the fixed extractor (git mv) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/results/phase1/inputs_cadd_raw.json` | `results/phase1/inputs_cadd_raw.json` | CADD responses; 5 benchmark names had frameshift coordinates and 2 names were frameshift-derived; regenerated 2026-10-29 with the fixed extractor (git mv) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/results/phase1/inputs_cadd_scores.csv` | `results/phase1/inputs_cadd_scores.csv` | CADD scores; same cause; regenerated 2026-10-29 with the fixed extractor (git mv) | `docs/AUDIT_RECORD.md` Corrections 14 |
| `archive/superseded-2026-10/2026-10-29-extractor-fix/results/phase1/unique_variant_counts.csv` | `results/phase1/unique_variant_counts.csv` | Counts on the 3,220-name inventory, 438 of whose names came from truncated HGVSp tokens; regenerated 2026-10-29 with the fixed extractor (git mv) | `docs/AUDIT_RECORD.md` Corrections 14 |
