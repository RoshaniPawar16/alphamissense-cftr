# Archive: side analyses

**Archived:** 2026-10-27 · **Branch:** paper-prep-2026-10 · **Method:** `git mv` (history preserved; nothing deleted)

Analyses that were not retracted but are used by neither the manuscript (`docs/paper/manuscript.md`) nor the Option B GWAS work. Each file keeps its original relative path under this folder.

Links to these files inside `audit/`, `docs/AUDIT_RECORD.md`, other archived files and all `.py` and `.ipynb` files were deliberately left unchanged so the audit trail reads as written. This manifest is the map from old path to new path.

| Path | Original location | Reason | Retraction reference |
|---|---|---|---|
| `archive/side-analyses/results/acmg_llm/experiment_summary.json` | `results/acmg_llm/experiment_summary.json` | ACMG/AMP criteria via LLM; excluded from the paper | None |
| `archive/side-analyses/results/acmg_llm/experiment_summary_dedup.json` | `results/acmg_llm/experiment_summary_dedup.json` | As above, deduplicated run | None |
| `archive/side-analyses/results/acmg_llm/per_variant_log.jsonl` | `results/acmg_llm/per_variant_log.jsonl` | As above, per-variant log | None |
| `archive/side-analyses/scripts/acmg_llm_experiment.py` | `scripts/acmg_llm_experiment.py` | Generator of the ACMG/LLM results | None |
| `archive/side-analyses/results/codon_pairs_raw.csv` | `results/codon_pairs_raw.csv` | Synonymous codon-pair concordance analysis | None |
| `archive/side-analyses/results/codon_pairs_tracks/H620Q_splice_perbin.csv.gz` | `results/codon_pairs_tracks/H620Q_splice_perbin.csv.gz` | Per-bin splice tracks for H620Q; raw evidence for the Check 14b retraction | AUDIT_RECORD.md line 48 lists the codon-pair result as confirmed; the per-bin Check 14b finding was retracted in Check 15 (see `archive/audit-2026-07/MANIFEST.md`) |
| `archive/side-analyses/docs/synonymous_codon_analysis.md` | `docs/synonymous_codon_analysis.md` | Report of the codon-pair analysis | None |
| `archive/side-analyses/results/pangolin_scores.csv` | `results/pangolin_scores.csv` | Pangolin splice scores; not used in the paper | None |
| `archive/side-analyses/results/phase1/mcdonald_rebinarised.csv` | `results/phase1/mcdonald_rebinarised.csv` | Rebinarisation of the McDonald 2024 supplement; the paper compares with that study in prose only | None |
| `archive/side-analyses/results/phase1/ensemble_metrics_dedup.csv` | `results/phase1/ensemble_metrics_dedup.csv` | Ensemble model on n = 254; excluded from the paper | None |
| `archive/side-analyses/scripts/phase1_ensemble_dedup.py` | `scripts/phase1_ensemble_dedup.py` | Generator of the ensemble metrics | None |
| `archive/side-analyses/results/phase1/am_vcc_analysis.csv` | `results/phase1/am_vcc_analysis.csv` | Breakdown of variants with varying clinical consequence | None |
| `archive/side-analyses/results/phase1/am_domain_analysis.csv` | `results/phase1/am_domain_analysis.csv` | Domain distribution of likely-pathogenic calls with varying consequence | None |
| `archive/side-analyses/results/phase1/am_unclassified_counts.csv` | `results/phase1/am_unclassified_counts.csv` | AlphaMissense class counts in the unclassified set | None |
| `archive/side-analyses/figures/domain_distribution.png` | `figures/domain_distribution.png` | Figure for the domain analysis | None |
| `archive/side-analyses/figures/varying_consequence_plot.png` | `figures/varying_consequence_plot.png` | Figure for the varying-consequence analysis | None |
| `archive/side-analyses/results/alphagenome/alphagenome_cftr_f508i_summary.csv` | `results/alphagenome/alphagenome_cftr_f508i_summary.csv` | Single-variant F508I exploration | None |
| `archive/side-analyses/figures/alphagenome_cftr_f508i_atac.png` | `figures/alphagenome_cftr_f508i_atac.png` | F508I ATAC track figure | None |
| `archive/side-analyses/figures/alphagenome_cftr_f508i_rna.png` | `figures/alphagenome_cftr_f508i_rna.png` | F508I RNA track figure | None |
| `archive/side-analyses/figures/alphagenome_cftr_f508i_splice.png` | `figures/alphagenome_cftr_f508i_splice.png` | F508I splice track figure | None |
| `archive/side-analyses/notebooks/alphagenome_cftr.ipynb` | `notebooks/alphagenome_cftr.ipynb` | Notebook for the F508I exploration | None |
| `archive/side-analyses/docs/rescore_evaluation.md` | `docs/rescore_evaluation.md` | Gene-mask versus centre-mask scorer evaluation (audit Check 16 era) | None |
| `archive/side-analyses/docs/scorer_comparison.md` | `docs/scorer_comparison.md` | Comparison of centre-mask aggregation types (audit Check 19 era) | None |
| `archive/side-analyses/scripts/check20b_rescore.py` | `scripts/check20b_rescore.py` | One-off audit check of quantile recalibration on 20 variants | None |

## Regeneration at the old path

Two producers stay in place because they produce inputs to the paper:

- `scripts/alphamissense_analysis.py` recreates `results/phase1/am_vcc_analysis.csv`, `results/phase1/am_domain_analysis.csv` and `results/phase1/am_unclassified_counts.csv` at their old paths on every run.
- `notebooks/alphamissense.ipynb` recreates `figures/domain_distribution.png` and `figures/varying_consequence_plot.png` when re-run.

Those copies are untracked, are not part of the paper, and should not be committed.

## Files kept in place that relate to these analyses

`results/alphagenome/l2diff_scores.csv` stays at its original path by decision on 2026-10-27. It may be the undocumented source of the L2D columns in `results/experimental_benchmark.csv`, which is a paper input.

## Running archived scripts and notebooks

The archived scripts and notebook compute the repository root from their own location. They will not run from this folder without editing their path constants. They are kept as a record.
