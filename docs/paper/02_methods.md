# Materials and Methods

**Draft:** 2026-10-24 · **Branch:** paper-prep-2026-10 · Stage 5 of the
pre-writing task. Methods only. No Introduction, Results, Discussion or
Abstract. No result is stated here; every number below describes a dataset, a
threshold or a procedure, never an outcome.

Each paragraph ends with a bracketed list of the scripts and results files it
rests on. A dataset with no recorded version or date is marked [NOT IN REPO]
rather than given an inferred one.

---

## Variant inventory and clinical labels

Variants were taken from the CFTR region of a ClinVar release whose VCF header
records `##fileDate=2026-04-15` and `##source=ClinVar`. The region
chr7:117,480,000–117,670,000 was extracted with bcftools 1.23.1 on 21 April
2026, normalised with `bcftools norm`, and annotated with Ensembl VEP v115.1
against the GRCh38.p14 cache carrying ClinVar 202502 annotations. The file is
sites-only and carries no sample columns or patient-level data. Its global
allele-frequency field is the 1000 Genomes Phase 3 frequency, not a gnomAD
frequency. A protein-change regular expression applied to the CSQ annotation
yielded 3,220 unique protein changes from 5,923 data lines. Clinical labels
came from the CFTR2 database release of 30 January 2026, which reports 2,092
variants across 122,935 patients; the date on which that release was
downloaded is [NOT IN REPO], and the earliest evidence of it in this project
is a file modification time of 14 May 2026.
[`scripts/cftr2_scraper_analysis.py`; `data/All_Variants_VEP.Gene.vcf`;
`data/cftr2_variants.xlsx`; `data/cftr2_results.csv`;
`results/phase1/unique_variant_counts.csv`; `audit/COHORT_PROVENANCE.md`]

## AlphaMissense scores

AlphaMissense precomputed pathogenicity scores for hg38 were obtained from
Zenodo record 8208688 and filtered to CFTR, UniProt P13569, transcript
ENST00000003084.10, giving 9,721 single-nucleotide variants covering 8,597
unique protein changes. The dataset version string and the download date are
[NOT IN REPO]. Three-letter protein-change names from the VCF were converted
to the single-letter form AlphaMissense uses, which succeeded for 2,909 of the
3,220 protein changes; the 311 failures are 309 nonsense changes and 2
stop-loss changes, which AlphaMissense does not score. Merging scores into the
labelled table left 2,665 protein changes with an AlphaMissense score. Each
variant carries the published AlphaMissense class, with the likely-pathogenic
boundary at 0.564 and the likely-benign boundary at 0.34.
[`notebooks/alphamissense.ipynb`; `scripts/alphamissense_analysis.py`;
`data/cftr_alphamissense.tsv`; `data/cftr2_results_annotated.csv`;
`results/phase1/unique_variant_counts.csv`; `results/phase1/SOURCE.md`]

## Benchmark cohort and deduplication

The benchmark cohort is every protein change carrying both an AlphaMissense
score and a binary CFTR2 determination of CF-causing or Non CF-causing.
Merging on protein-variant name produced 292 rows for 259 unique variants,
because one protein change can map to several nucleotide changes. Duplicated
rows never differ in label or score. Rows were deduplicated keep-first on the
protein-variant name, leaving 259 unique variants, 226 CF-causing and 33 Non
CF-causing. Deduplication precedes every metric and every cross-validation
fold assignment reported in this manuscript. The earlier 292-row and 286-row
cohorts are superseded and are not used.
[`scripts/phase1_build_cohort.py`;
`results/phase1/benchmark_cohort_dedup.csv`;
`results/phase1/unique_variant_counts.csv`; `docs/AUDIT_RECORD.md`]

## Comparator scores

CADD PHRED scores came from the CADD v1.7 GRCh38 REST API endpoint
`GRCh38-v1.7`; the query date is [NOT IN REPO]. SIFT and PolyPhen-2 scores
were parsed from fields 31 and 32 of the CSQ annotation in the VEP-annotated
VCF, so they carry the VEP v115.1 versions of those predictors rather than
standalone releases. SIFT scores run in the opposite direction to the other
three, so they were inverted as one minus the score; every predictor column
therefore reads higher-is-more-damaging. Five of the 259 unique validation
variants lack at least one comparator score and are excluded from any
four-tool comparison, leaving 254 variants, 221 CF-causing and 33 Non
CF-causing. Leu137Pro, Thr604Ile and Trp1098Cys returned no CADD v1.7 score;
Trp496Gly and Gly622Val have no CADD, SIFT or PolyPhen-2 score.
[`scripts/phase1_fetch_cadd.py`; `scripts/fetch_comparator_scores.py`;
`results/phase1/inputs_cadd_scores.csv`;
`results/phase1/inputs_polyphen_sift.csv`;
`results/phase1/benchmark_cohort_dedup.csv`]

## Discrimination and its uncertainty

For each predictor we computed the area under the receiver operating
characteristic curve and the average precision against the CFTR2 binary label,
using `roc_auc_score` and `average_precision_score` from scikit-learn 1.9.0 on
Python 3.13.1. Both are threshold-independent, which matters here because the
four predictors publish thresholds on different scales. Confidence intervals
are percentile bootstrap intervals from 2,000 resamples of the variant list
with replacement, drawn with `numpy.random.default_rng(42)`; resamples
containing a single class were discarded, and none were on either cohort. The
same resample indices are applied to all four predictors within a draw, so the
intervals share their sampling variation. Intervals are reported for the four
predictors on the 254-variant cohort and for AlphaMissense on the full
259-variant cohort.
[`scripts/paper/p3a_auc_ci.py`; `results/paper/auc_ci.csv`;
`results/phase1/benchmark_cohort_dedup.csv`]

## Paired comparison between predictors

Each comparator's ROC curve was compared against AlphaMissense's on the same
254 variants with the DeLong test for two correlated ROC curves, implemented
as the fast algorithm of Sun and Xu (2014). The test is paired, which is the
appropriate form here because all four predictors score the same variants; it
is reported alongside the bootstrap intervals rather than in place of them,
since overlapping marginal intervals do not imply an absent paired difference.
[`scripts/phase1_delong.py`; `scripts/phase1_utils_delong.py`;
`results/phase1/delong_tests_dedup.csv`]

## Calibration

AlphaMissense emits a score in the unit interval that is not trained to be a
calibrated probability, so calibration was measured descriptively rather than
tested. The 259 unique validation variants were binned into ten equal-width
bins across the unit interval by AlphaMissense score. For each bin we recorded
the count, the mean predicted score and the observed fraction of CF-causing
variants. We also computed the Brier score with scikit-learn's
`brier_score_loss`, the Brier score of a model predicting the base rate for
every variant, and the expected calibration error as the sample-weighted mean
absolute gap between predicted and observed values across occupied bins.
[`scripts/paper/p3b_calibration.py`; `results/paper/calibration_n259.csv`;
`results/phase1/benchmark_cohort_dedup.csv`]

## The AlphaMissense-ambiguous screening set

A second variant set was assembled for the splicing analysis: every CFTR
single-nucleotide variant whose AlphaMissense class is ambiguous, meaning a
score between 0.34 and 0.564. Applied to the AlphaMissense CFTR table this
gives 1,278 variants covering 1,100 unique protein changes. This set is drawn
from the complete table of possible CFTR missense changes, not from the
ClinVar-derived inventory, and the two sets are not nested: 431 of the 1,278
appear among the 3,220 protein changes of the benchmark chain. Of the 1,278,
291 carry a gnomAD v4 allele frequency above zero and 952 are absent from
gnomAD v4 entirely; the gnomAD query date is [NOT IN REPO] and no committed
script performs the lookup. The set is not a set of variants of uncertain
significance in the clinical sense, because most carry no clinical submission
of any kind.
[`data/cftr_alphamissense.tsv`;
`results/alphagenome/alphagenome_full_cftr_results.csv`;
`results/gnomad_cftr_lookup.csv`; `results/paper/fig1_flow_counts.csv`;
`audit/COHORT_PROVENANCE.md`]

## AlphaGenome scoring

The 1,278 variants were scored with AlphaGenome v0.6.1 on 28 May 2026 across
lung tracks, producing splice-site-usage, ATAC and RNA-seq outputs as a raw
score and a quantile score. Two scorers were used and are kept distinct
throughout. The gene-mask scorer returns the largest change in splice-site
probability at any junction across the whole CFTR gene body, so for a coding
variant its value is set partly by the distance to the nearest canonical
splice site rather than by the variant's own effect. The centre-mask scorer
restricts the comparison to a 501 bp window centred on the variant. Quantile
scores rank a variant against AlphaGenome's common-variant background, defined
as variants above 1% minor allele frequency in any gnomAD v3 population, and
not against all human variation; because that background is predominantly
non-coding, rare coding variants in a heavily spliced gene routinely exceed
its upper percentiles. The scoring run predates AlphaGenome's 18 June 2026
move from a chromosome-22 quantile background to a genome-wide one, so every
quantile-based analysis is reported on the original chromosome-22 calibration
and repeated on the genome-wide recalibration as a sensitivity analysis; the
day-level date of the recalibration run is [NOT IN REPO].
[`scripts/alphagenome_full_cftr.py`;
`scripts/regenerate_quantiles_genomewide.py`;
`results/alphagenome/alphagenome_full_cftr_results.csv`;
`results/alphagenome/rescore_centermask.csv`;
`results/alphagenome/quantiles_genomewide_2026-08.csv`;
`docs/AUDIT_RECORD.md`; `audit/PROVENANCE.md`]

## SpliceAI scoring

SpliceAI delta scores for the same 1,278 variants were retrieved through the
Ensembl VEP REST endpoint `https://rest.ensembl.org/vep/human/region` with the
SpliceAI plugin, taking the maximum of the four channels: acceptor gain,
acceptor loss, donor gain and donor loss. The plugin version, the SpliceAI
model version and the query date are all [NOT IN REPO]. Variants returning a
delta of exactly zero were re-queried to separate a genuine zero prediction
from an absent record, and 766 were examined in that pass. Two properties of
the score constrain its use as a negative control. Its reporting window is
plus or minus 50 nucleotides, while every variant in this cohort lies within
500 bp of a CFTR splice site, so a zero can mean not assessed rather than
assessed and negative. The precomputed score file also does not cover all
exon-interior variants.
[`scripts/fetch_comparator_scores.py`; `scripts/fix_spliceai_scores.py`;
`scripts/reclassify_spliceai_zeros.py`; `results/comparator_scores.csv`;
`results/spliceai_zero_reclassification.csv`; `docs/AUDIT_RECORD.md`]

## Agreement between AlphaGenome and SpliceAI

Agreement between the two splice predictors across the 1,278 variants was
tested on a 2x2 table of AlphaGenome gene-mask SPLICE quantile above 0.95
against SpliceAI maximum delta above 0.2, using Pearson's chi-square test of
independence without continuity correction as the primary test, with the
Yates-corrected chi-square and Fisher's exact test reported alongside it; all
three come from `scipy.stats` in SciPy 1.17.1. The odds ratio is reported with
a 95% Woolf interval computed on the log scale, with a Haldane-Anscombe
correction of 0.5 applied only if a cell is empty. The table was built twice,
once on each quantile calibration.
[`scripts/paper/p3e_ag_spliceai_2x2.py`;
`results/paper/ag_spliceai_2x2.csv`;
`results/alphagenome/alphagenome_full_cftr_results.csv`;
`results/alphagenome/quantiles_genomewide_2026-08.csv`;
`results/comparator_scores.csv`]

## Definition of the concordant set

Variants flagged independently by both splice predictors were assembled under
two definitions, which are reported together rather than one being chosen. The
gene-mask definition is an AlphaGenome gene-mask SPLICE quantile above 0.95
together with a SpliceAI maximum delta above 0.5. The centre-mask definition
is a centre-mask 501 bp splice score in the top 5% of the 1,278, an empirical
threshold of 0.0828 that 64 variants exceed, together with the same SpliceAI
criterion. For every variant in the union we recorded the protein change, hg38
position, reference and alternate allele, CFTR domain, AlphaMissense score,
AlphaGenome splice raw and quantile scores under both calibrations, the
centre-mask score, the SpliceAI maximum delta and the channel carrying it,
CADD PHRED, gnomAD v4 maximum allele frequency, CFTR2 determination, and
whether the variant appears in the minigene benchmark. Domains were assigned
from residue number using the CFTR domain boundaries already used in this
project. Two requested columns could not be filled and are recorded as
[NOT IN REPO] for every row: the exon or intron a variant falls in, and its
distance to the nearest splice site. The repository holds no CFTR exon
annotation in any form and no script computes either quantity for this cohort.
[`scripts/paper/p3c_concordant_set.py`; `results/paper/concordant_set.csv`;
`results/alphagenome/rescore_centermask.csv`;
`results/alphagenome/alphagenome_full_cftr_results.csv`;
`results/comparator_scores.csv`; `results/gnomad_cftr_lookup.csv`;
`data/cftr2_results_annotated.csv`; `scripts/alphamissense_analysis.py`]

## External validation against minigene assays

The only external functional comparison available is a 23-row benchmark
compiled on 2 August 2026 from two minigene studies, Bergougnoux et al. 2023
and Zhang et al. 2025, covering 22 unique CFTR variants, of which 11 showed
altered splicing and 12 did not. Glu403Asp contributes two rows as two
distinct nucleotide changes. Coordinates are GRCh38, derived from NM_000492.4
HGVS notation through the Ensembl VEP REST API. Against these labels we scored
the AlphaGenome gene-mask SPLICE quantile, the AlphaGenome gene-mask raw
score, and the SpliceAI maximum delta, reporting AUC with percentile bootstrap
intervals from 2,000 resamples at seed 42, and 2x2 contingency tables at
SpliceAI 0.2, SpliceAI 0.5 and AlphaGenome quantile 0.95. The benchmark is too
small to select a scorer, and it is reported with that limit attached rather
than as a validation result: the bootstrap intervals span roughly 0.30 of AUC,
and a single label change moves the estimate by about 0.008. SpliceAI returns
a delta of exactly zero for 21 of the 23 rows, so its figures on this
benchmark measure the coverage of a precomputed file as much as prediction.
[`scripts/paper/p3d_minigene_benchmark.py`;
`results/paper/minigene_benchmark.csv`;
`results/experimental_benchmark.csv`; `docs/experimental_benchmark.md`]

## Software, figures and reproducibility

All analyses ran on Python 3.13.1 with NumPy 2.4.6, pandas 2.3.3,
scikit-learn 1.9.0, SciPy 1.17.1 and Matplotlib 3.10.9. Every random procedure
uses seed 42 and `numpy.random.default_rng`. Analyses written for this
manuscript are new scripts under `scripts/paper/` writing to
`results/paper/`; no existing script or results file was modified. Figures
were produced at 300 dpi as RGB TIFF files at most 7.5 inches wide, in Arial,
with no figure number, title or caption inside the image file. The categorical
colours used across figures were checked for colour-vision-deficiency
separation and for contrast against the figure background, and each series
also carries a non-colour encoding, a line style or a marker shape.
[`scripts/paper/figstyle.py`; `scripts/paper/p4_fig1_flow.py`;
`scripts/paper/p4_fig2_roc.py`; `scripts/paper/p4_fig3_scatter.py`;
`scripts/paper/p4_tables.py`; `results/paper/fig1_flow_counts.csv`]

---

## Items a Methods reviewer will ask for that this draft cannot supply

These are listed here so they are not mistaken for omissions. Each is an
unrecorded fact, not an undescribed procedure.

1. Access dates for CADD, SpliceAI, gnomAD v4 and the AlphaMissense download.
2. The SpliceAI plugin and model version behind the Ensembl REST responses.
3. The day-level date of the genome-wide AlphaGenome recalibration run.
4. A committed script that produces `results/gnomad_cftr_lookup.csv`.
5. An exon annotation for CFTR, without which no variant in this manuscript
   can be placed in an exon or given a distance to a splice site.
