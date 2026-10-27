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
