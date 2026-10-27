# Open items from the Stage 1–5 pre-writing pass

**Compiled:** 2026-10-24 · **Branch:** paper-prep-2026-10

Every `[NOT IN REPO]` and `[CITATION NEEDED]` produced in this pass, with what
would resolve it. Nothing here blocks the Methods draft; several items block
submission.

---

## A. [NOT IN REPO] — unrecorded provenance

| # | Item | Where it appears | What resolves it |
|---|---|---|---|
| A1 | CFTR2 download date for the 30 January 2026 release | Table 1 row 1; Methods, variant inventory | The scraper notebook's execution date, a download log, or a dated note from whoever ran it. The spreadsheet header gives the release date, not the access date. |
| A2 | AlphaMissense dataset version string | Table 1 row 4 | The Zenodo record 8208688 version label as downloaded (the record is versioned). Recording the file checksum against a named Zenodo version would also settle it. |
| A3 | AlphaMissense download date | Table 1 row 4 | Same as A2: a dated download record. |
| A4 | CADD v1.7 REST query date | Table 1 row 5; Methods, comparator scores | A timestamp in `results/phase1/inputs_cadd_raw.json`, or a dated run log. The raw response file exists but carries no date field. |
| A5 | SpliceAI plugin version and model version | Table 1 row 6; Methods, SpliceAI scoring | The Ensembl VEP REST release that served the responses, which can be recovered by re-querying and recording the response headers. |
| A6 | SpliceAI query date | Table 1 row 6 | A dated run log for `scripts/fetch_comparator_scores.py` and `scripts/fix_spliceai_scores.py`. |
| A7 | gnomAD v4 query date | Table 1 row 9; Methods, screening set | A dated run record. No committed script performs this lookup at all, which is the larger half of the problem; see B1. |
| A8 | Day-level date of the genome-wide AlphaGenome recalibration run | Table 1 row 8; Methods, AlphaGenome scoring | A run log for `scripts/regenerate_quantiles_genomewide.py`. The filename pins the month only. |
| A9 | Exon or intron for each variant in the concordant set | Table 3, every row; `results/paper/concordant_set.csv` | A CFTR exon annotation for the analysis transcript, for example the Ensembl GTF for ENST00000003084.10 or the NM_000492.4 exon table, committed as a data file with a version and date. |
| A10 | Distance to the nearest splice site for each variant in the concordant set | Table 3, every row; `results/paper/concordant_set.csv` | The same annotation as A9, plus a small script computing the distance. The `dist_bp` column of `results/experimental_benchmark.csv` covers only the 23 minigene variants and has no generating script. |

## B. Reproducibility gaps found while building Stage 3

| # | Item | What resolves it |
|---|---|---|
| B1 | `results/gnomad_cftr_lookup.csv` has no generating script | A committed script that performs the gnomAD v4 lookup and writes the file, with the query date in a header comment or a provenance row. Until then the 291-of-1,278 figure rests on an orphaned file. |
| B2 | `results/experimental_benchmark.csv` has no generating script | A committed compilation script, or a provenance note recording how the 23 rows and the `dist_bp` column were produced. |
| B3 | The AlphaGenome quantile calibration used predates the 18 June 2026 genome-wide switch | Already handled by reporting both calibrations in `results/paper/ag_spliceai_2x2.csv` and `results/paper/concordant_set.csv`. No further action needed, but the manuscript must say which column each number comes from. |

## C. [CITATION NEEDED] — references the manuscript will need

None of these are missing facts; they are published works the Methods names
and the reference list does not yet hold. Vancouver style, per
`docs/paper/JOURNAL_RULES.md`.

| # | Work | Named in |
|---|---|---|
| C1 | AlphaMissense (Cheng et al., Science 2023) and its Zenodo dataset record 8208688 | Methods, AlphaMissense scores; Table 1 row 4 |
| C2 | AlphaGenome (Google DeepMind) — the citable release or preprint for v0.6.1 | Methods, AlphaGenome scoring; Table 1 rows 7 and 8 |
| C3 | SpliceAI (Jaganathan et al., Cell 2019) | Methods, SpliceAI scoring |
| C4 | CADD v1.7 (Kircher et al. and the current CADD release paper) | Methods, comparator scores |
| C5 | PolyPhen-2 (Adzhubei et al.) and SIFT (Ng and Henikoff) | Methods, comparator scores |
| C6 | Ensembl VEP (McLaren et al., Genome Biol 2016) | Methods, variant inventory |
| C7 | DeLong et al. 1988, and Sun and Xu, IEEE Signal Process Lett 2014;21(11):1389–1393 | Methods, paired comparison |
| C8 | CFTR2 (Sosnay et al. and the CFTR2 database citation) | Methods, variant inventory |
| C9 | gnomAD v4 (Chen et al. / the gnomAD v4 release paper) | Methods, screening set |
| C10 | Bergougnoux et al. 2023, J Cyst Fibros 22:515–524 | Methods, external validation |
| C11 | Zhang et al. 2025, Front Genet 16:1543623 | Methods, external validation |
| C12 | ClinVar (Landrum et al.) | Methods, variant inventory |
| C13 | bcftools / HTSlib 1.23.1 (Danecek et al., GigaScience 2021) | Methods, variant inventory |
| C14 | scikit-learn, SciPy, NumPy, pandas, Matplotlib | Methods, software |
| C15 | Pejaver et al. 2022, for the calibrated PP3 strength | Only if the ACMG side experiment enters the manuscript; it is not in the current message |

## D. Compliance items for submission

| # | Item | What resolves it |
|---|---|---|
| D1 | Data availability: four input files are not committed (`data/cftr2_results_annotated.csv`, `data/cftr_alphamissense.tsv`, `data/All_Variants_VEP.Gene.vcf`, `data/AlphaMissense_hg38.tsv.gz`) | Deposit the derived tables in a repository with a DOI, and state the redownload route for the three third-party sources. PLOS requires a persistent identifier, not a description. |
| D2 | Figure text below the 8 pt floor in Figs 1–3 | A layout pass; detailed per element in `docs/paper/FIGURES.md`. |
| D3 | Three main tables exceeds both comparable papers | A decision on whether Table 3 moves to supporting information. |
| D4 | Methods placement if it is to precede Results | One sentence in the cover letter, per the journal's "Manuscript Organization" section. |
