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
| A4 | CADD v1.7 REST query date | Table 1 row 5; Methods, comparator scores | A timestamp in `results/phase1/inputs_cadd_raw.json`, or a dated run log. **Partly resolved 2026-10-29:** the file now carries a `query_date` field. Three queries (Leu137Pro, Thr604Ile, Trp1098Cys) are dated 2026-10-29. The other 254 responses were reused from the earlier run and their query date remains unrecorded. |
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
| B4 | `results/alphagenome/rescore_centermask.csv` has no generating script (produced inline in audit Check 15; described in `docs/rescore_analysis.md` and `audit/checks/CHECK_15_REPORT.md`) | **Resolved 2026-10-27.** `scripts/paper/p2_alphagenome_centremask.py` regenerates the file with exact allele matching; run record in `results/alphagenome/SOURCE.md`. |

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

## E. Added 2026-10-27 with the manuscript rewrite

| # | Item | What resolves it |
|---|---|---|
| E0 | **Blocking.** `scripts/alphagenome_full_cftr.py` and `scripts/regenerate_quantiles_genomewide.py` matched AlphaGenome results to variants by position only, so every allele at a multi-allelic position received the maximum score across alleles in its batch. 644 of the 1,278 variants sit at 306 multi-allelic positions; SPLICE raw scores are identical across alleles at 291 of them, and the 501-base centre-mask scores at 249. Eight of the 18 concordant variants are affected (R55T, R55I, H620Q, I906S, E1046V, S1058G, S1058C, L1156F). All AlphaGenome numbers in the manuscript (747, 49, the odds ratios, the 18 and 13, Fig 3, Fig 4, the domain test) are provisional. Both scripts now match on the full variant ID (fixed 2026-10-27). | **Resolved 2026-10-27.** The 1,278 were rescored with exact matching (`results/alphagenome/SOURCE.md`), the paper scripts rerun and the manuscript numbers updated; the concordant set and its 13-member subset were unchanged. The 23 minigene rows were rescored on 2026-10-29. |
| E1 | The 18 concordant variants are not mapped to exon boundaries (supersedes A9, A10). Only codon 970 is placed, from its two genomic positions. | A script that fetches the exon coordinates of ENST00000003084 from the Ensembl REST API, records the release, and writes the exon or intron and the distance to the nearest splice site for each of the 18. |
| E2 | The sentence "We found no published use of AlphaGenome on CFTR" rests on an informal web search. | A dated search of PubMed and bioRxiv for AlphaGenome AND CFTR, with the date and the number of hits recorded here. |
| E3 | Text in Figs 1, 2 and 4 goes down to 6.3 pt in places, below the PLOS 8 pt floor. | A layout pass before submission. |
| E4 | Figs 1, 2 and 4 were rendered in a session without Arial (fallback Liberation Sans). | Re-run `scripts/paper/p4_fig1_design.py`, `p4_fig2_roc.py`, `p4_fig4_domain_map.py`, `p4_fig1_flow.py` and `p4_previews.py` on a machine with Arial. |
| E5 | Domain enrichment of the 18 in MSD2 is reported with five uncorrected and Bonferroni-corrected Fisher tests on 18 variants. | Biological interpretation by Durjya Amonkar; consider whether exon structure explains it once E1 is done. |
| E6 | `results/alphagenome/l2diff_scores.csv` (Check 16) was probably produced with the same position-only matching as E0. The paper does not use it. | Rescore with exact matching if the file is ever used, or archive it. |
| E12 | The protein-name extractor shortened non-missense HGVSp tokens to missense-looking names (`p.Lys163ArgfsTer3` became `Lys163Arg`): 438 of 3,220 inventory names, 2 benchmark variants, and 5 CADD queries sent to frameshift coordinates. | **Resolved 2026-10-29.** Fixed at the source (`scripts/hgvsp_names.py`) and the pipeline rebuilt: 2,782 names; a benchmark of 257, all with four scores. See `docs/AUDIT_RECORD.md` Corrections 14. |
| E13 | The centre-mask columns of `results/experimental_benchmark.csv` (`cm_splice_501_dls`, `cm_splice_501_l2d`, `cm_splice_501_l2l`) were not rescored on 2026-10-29; only the gene-mask columns were. | Rescore them with exact variant matching if the centre-mask minigene results are ever reported. |
| E14 | Funding, Competing interests and Author contributions in `docs/paper/manuscript.md` have not been confirmed by every author, and the affiliations give no department. | Confirm all three statements with every author and add departments. |
| E15 | The minigene results for G970R, G970V, G970D and R55K were taken from `results/experimental_benchmark.csv` and the manuscript text, not checked against the source table. | Check Bergougnoux et al. 2023, Table 1, by eye for these four changes. |
