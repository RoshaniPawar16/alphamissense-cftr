# Table 1. Data sources

Every dataset the manuscript rests on, with the version and the access or
extraction date as recorded in the repository. A cell reads **[NOT IN REPO]**
when no committed file records the value. Source citations follow the table as
prose, because PLOS Computational Biology does not permit footnotes anywhere
in the manuscript ("Footnotes").

| # | Source | Version / release | Access or extraction date | n | Used for |
|---|---|---|---|---|---|
| 1 | CFTR2 database (cftr2.org) | 30 January 2026 release | [NOT IN REPO] as a recorded access date; the spreadsheet was last modified 2026-05-14 | 2,092 variants; 122,935 patients | Clinical labels: CF-causing, Non CF-causing, Varying clinical consequence |
| 2 | ClinVar variant file, CFTR region | VCF `##fileDate=2026-04-15`, `##source=ClinVar` | Extracted 2026-04-21 14:08:57 with bcftools 1.23.1, region 7:117480000–117670000, then `bcftools norm` | 5,923 data lines → 3,220 unique protein changes | Variant inventory for the benchmark chain |
| 3 | Ensembl VEP annotation of source 2 | VEP v115.1, cache GRCh38.p14, ClinVar annotations 202502 | Same run as source 2 | 2,473 rows of parsed CSQ output | SIFT (CSQ field 31) and PolyPhen-2 (CSQ field 32) scores |
| 4 | AlphaMissense precomputed scores, hg38 | Zenodo record 8208688; dataset version string [NOT IN REPO] | [NOT IN REPO]; the CFTR-filtered extract was last modified 2026-05-14 | 9,721 CFTR SNVs; 8,597 unique protein changes; UniProt P13569; transcript ENST00000003084.10 | AlphaMissense pathogenicity score and class |
| 5 | CADD | v1.7, GRCh38 (REST endpoint `GRCh38-v1.7`) | [NOT IN REPO] | 292 rows fetched for the benchmark chain; 1,278 for the screening chain | CADD PHRED comparator score |
| 6 | SpliceAI, via the Ensembl VEP REST SpliceAI plugin | Plugin and model version [NOT IN REPO] | [NOT IN REPO] | 1,278 variants scored; 766 re-queried in the zero-score audit | SpliceAI delta scores (AG, AL, DG, DL) |
| 7 | AlphaGenome | SDK v0.6.1; calibration served on the scoring date | Scored 2026-10-27 (1,278 variants); minigene rows 2026-10-29 | 1,278 variants; 23 minigene rows | Gene-mask and centre-mask SPLICE, ATAC and RNA scores |
| 9 | gnomAD v4 | gnomad_r4, GRCh38, position-matched | [NOT IN REPO] | 1,278 looked up; 291 with allele frequency > 0; 952 absent | Population allele frequency for the concordant set |
| 10 | Minigene literature benchmark | Bergougnoux et al. 2023, J Cyst Fibros 22:515–524; Zhang et al. 2025, Front Genet 16:1543623 | Compiled 2026-08-02 | 23 rows; 22 unique variants; 11 positive, 12 negative | The only external functional validation in the manuscript |

## Cell sources

**Row 1.** Release date, patient count and variant count are rows 2, 3 and 4 of
the first sheet of `data/cftr2_variants.xlsx` ("Date: 30 January 2026";
"Number of patients in CFTR2: 122,935"; "Number of variants reported in CFTR2:
2,092"). The access date is unrecorded: `docs/AUDIT_RECORD.md` Corrections
(2026-10) item 3 states that no download log exists and that the evidence is
the spreadsheet header, the download URL in `notebooks/cftr2_scraper.ipynb`,
and the file modification time.

**Row 2.** All values read directly from the header of
`data/All_Variants_VEP.Gene.vcf`: `##fileDate`, `##source`,
`##bcftools_viewVersion`, and the `##bcftools_viewCommand` line, which carries
both the region and the timestamp. The data-line count is the number of
non-`#` lines in that file. The 3,220 figure is
`results/phase1/unique_variant_counts.csv`, row `annotated_table_all`, column
`unique_count`.

**Row 3.** `VEP="v115.1"`, `assembly="GRCh38.p14"` and `ClinVar="202502"` are
read from the VCF header. The CSQ field indices and the row count are
`results/phase1/SOURCE.md` and `results/phase1/inputs_polyphen_sift.csv`
(2,473 data rows).

**Row 4.** The Zenodo record number is `results/phase1/SOURCE.md`. The row,
protein-change, UniProt and transcript values are computed from
`data/cftr_alphamissense.tsv` and recorded in
`results/paper/fig1_flow_counts.csv`, rows `am_table_rows` and
`am_table_unique_protein`. No version string or download date is recorded
anywhere in the repository for the AlphaMissense release.

**Row 5.** Version and endpoint: `scripts/phase1_fetch_cadd.py` line 24 and
`scripts/fetch_comparator_scores.py` line 33, both naming
`GRCh38-v1.7`. Row counts: `results/phase1/inputs_cadd_scores.csv` (292 data
rows) and `results/comparator_scores.csv` (1,278 data rows). The scripts log no run date
and the raw response file `results/phase1/inputs_cadd_raw.json` carries no
timestamp field.

**Row 6.** Endpoint: `scripts/fetch_comparator_scores.py` line 34 and
`scripts/fix_spliceai_scores.py` line 21, both
`https://rest.ensembl.org/vep/human/region`. Counts:
`results/comparator_scores.csv` (1,278 data rows) and
`results/spliceai_zero_reclassification.csv` (766 data rows). Neither the plugin
version nor the SpliceAI model version is recorded.

**Row 7 (changed 2026-10-29; replaces the former rows 7 and 8).** SDK version,
run times and scorers: `results/alphagenome/SOURCE.md`, which records the
2026-10-27 rescore of `results/alphagenome/alphagenome_full_cftr_results.csv`
and `results/alphagenome/rescore_centermask.csv` (1,278 data rows each) with
exact allele matching (`docs/paper/OPEN_ITEMS.md` E0). The 23 minigene rows of
`results/experimental_benchmark.csv` were rescored on 2026-10-29 by
`scripts/paper/p2b_alphagenome_minigene.py`. The quantiles are those the
service returned on the scoring date; the API does not name its background.
The earlier May 2026 chromosome-22 run and the August 2026 genome-wide
recalibration are archived in `archive/superseded-2026-10/results/alphagenome/`.

**Row 9.** Version string and method: `audit/COHORT_PROVENANCE.md` line 65,
recording gnomAD v4 (gnomad_r4, GRCh38, position-matched), 291 of 1,278 with
allele frequency above zero and 952 absent. File:
`results/gnomad_cftr_lookup.csv`, 1,278 data rows, column `gnomad_max_af`
non-empty in 291 rows. No script in the repository generates this file and no
query date is recorded.

**Row 10.** Citations and composition: `docs/experimental_benchmark.md`, dated
2026-08-02, naming both papers and recording 11 positives and 12 negatives
across 23 rows and 22 unique variants (Glu403Asp appears twice as two distinct
nucleotide changes). File: `results/experimental_benchmark.csv`, 23 data rows,
column `minigene_result`.

## Notes on the dates

File modification times are weak evidence and are quoted only where the audit
record already relies on them, in row 1. Three files in this table share a
modification time of 2026-09-06 13:35, which indicates a bulk file operation
rather than three analysis runs, so modification times are not used as access
dates anywhere else in this table.

Seven of the ten rows carry at least one [NOT IN REPO] cell. Six of those are
access dates. A single provenance file recording the query date for CADD,
SpliceAI, gnomAD and the AlphaMissense download would clear five of them.
