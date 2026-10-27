# Archive: retracted analyses

**Archived:** 2026-10-27 · **Branch:** paper-prep-2026-10 · **Method:** `git mv` (history preserved; nothing deleted)

Files whose findings were retracted in the 2026-07 integrity audit, or whose only purpose was to produce a retracted finding. Each file keeps its original relative path under this folder, so `results/rescue_analysis.csv` is now `archive/retracted-2026-07/results/rescue_analysis.csv`.

Retraction references point to `docs/AUDIT_RECORD.md`, section "What was retracted" (lines 79–91) and the list of documents still describing retracted findings (line 124).

Links to these files inside `audit/`, `docs/AUDIT_RECORD.md`, other archived files and all `.py` and `.ipynb` files were deliberately left unchanged so the audit trail reads as written. This manifest is the map from old path to new path.

| Path | Original location | Reason | Retraction reference |
|---|---|---|---|
| `archive/retracted-2026-07/results/alphagenome/alphagenome_batch_results.csv` | `results/alphagenome/alphagenome_batch_results.csv` | AlphaGenome scores for the seven priority variants | AUDIT_RECORD.md lines 84–85 (seven priority variants) |
| `archive/retracted-2026-07/results/alphagenome/alphagenome_quantile_scores_raw.csv` | `results/alphagenome/alphagenome_quantile_scores_raw.csv` | Per-track quantile scores for the seven priority variants | AUDIT_RECORD.md lines 84–85 |
| `archive/retracted-2026-07/scripts/alphagenome_batch.py` | `scripts/alphagenome_batch.py` | Generator for the seven-variant batch | AUDIT_RECORD.md lines 84–85 |
| `archive/retracted-2026-07/scripts/alphagenome_quantile_scores.py` | `scripts/alphagenome_quantile_scores.py` | Generator for the seven-variant quantile scores | AUDIT_RECORD.md lines 84–85 |
| `archive/retracted-2026-07/docs/alphagenome_batch_report.md` | `docs/alphagenome_batch_report.md` | Reports the seven priority variants, the rescue groups and "top X% of all human variants" wording | AUDIT_RECORD.md lines 84–85, 87–88 and 124 |
| `archive/retracted-2026-07/results/alphagenome/alphagenome_rescue_variants.csv` | `results/alphagenome/alphagenome_rescue_variants.csv` | Rescue groups (87 / 728 / 56); orphaned, no generating script; selected on quantile > 0.95, which AUDIT_RECORD.md shows clears most coding variants | No explicit retraction entry. Basis: AUDIT_RECORD.md lines 87–88 and 102–103 (quantile background); `quarantine/MANIFEST.md` (orphan status) |
| `archive/retracted-2026-07/results/rescue_analysis.csv` | `results/rescue_analysis.csv` | Contains the 693 discordant group and the rescue groups | AUDIT_RECORD.md lines 81–82 (693 discordant variants) |
| `archive/retracted-2026-07/results/threshold_sensitivity.csv` | `results/threshold_sensitivity.csv` | Threshold sweep of the discordant group | AUDIT_RECORD.md lines 81–82 and 124 |
| `archive/retracted-2026-07/docs/threshold_sensitivity.md` | `docs/threshold_sensitivity.md` | Discusses the 693 as a finding | AUDIT_RECORD.md line 124 |
| `archive/retracted-2026-07/docs/comparator_analysis_report.md` | `docs/comparator_analysis_report.md` | Presents the 693 discordant group as a finding | AUDIT_RECORD.md lines 81–82 and 124 |
| `archive/retracted-2026-07/docs/tool_association_analysis.md` | `docs/tool_association_analysis.md` | Discusses the 693 as a finding | AUDIT_RECORD.md line 124 |
| `archive/retracted-2026-07/docs/spliceai_coverage_analysis.md` | `docs/spliceai_coverage_analysis.md` | Discusses the 693 as a finding | AUDIT_RECORD.md line 124 |
| `archive/retracted-2026-07/scripts/write_comparator_report.py` | `scripts/write_comparator_report.py` | Generator of `comparator_analysis_report.md` | AUDIT_RECORD.md lines 81–82 |
| `archive/retracted-2026-07/docs/positive_control_analysis.md` | `docs/positive_control_analysis.md` | Twelve-variant positive control | AUDIT_RECORD.md lines 90–91 (twelve-variant positive control) |

## Regeneration at the old path

`scripts/build_comparator_analysis.py` stays in place because it produces `results/comparator_analysis.csv`, an input to the paper. It also writes `results/rescue_analysis.csv`. Re-running it will recreate that file at its old path as an untracked file. That copy is not part of the paper and should not be committed.

## Running archived scripts

The archived scripts compute the repository root from their own location. They will not run from this folder without editing their path constants. They are kept as a record, not as runnable code.
