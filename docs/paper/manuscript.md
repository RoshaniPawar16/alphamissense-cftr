# Title

**Preferred title.** Two splice predictors converge on eighteen AlphaMissense-ambiguous CFTR variants that protein-level scoring cannot resolve

**Short title.** AlphaMissense benchmark and a concordant splice candidate set in CFTR

**Alternative titles considered.** (a) AlphaMissense outperforms CADD, PolyPhen-2 and SIFT on CFTR2-labelled missense variants and leaves a grey zone that splice prediction narrows. (b) Benchmarking AlphaMissense on CFTR and prioritising its ambiguous calls with concordant AlphaGenome and SpliceAI splice predictions.

---

# Authors

[NOT IN REPO: author list]

# Affiliations

[NOT IN REPO: affiliations]

---

# Abstract

Most missense variants in the cystic fibrosis transmembrane conductance regulator gene have no clinical classification. A family given an unclassified result from newborn screening or carrier testing cannot be told what it means. We benchmarked AlphaMissense against CADD, PolyPhen-2 and SIFT on CFTR2-labelled missense variants, using bootstrap confidence intervals and a paired DeLong test on the variants that all four tools score. We measured whether AlphaMissense scores behave as calibrated probabilities. We then took the variants AlphaMissense leaves ambiguous and asked whether two splice predictors built on different principles, AlphaGenome and SpliceAI, agree about which of them disrupt splicing.

AlphaMissense separated CF-causing from Non CF-causing variants with an area under the receiver operating characteristic curve of 0.955 (95% confidence interval 0.912 to 0.988) on 259 unique labelled variants. On the 254 variants carrying all four scores it exceeded every comparator, with paired DeLong p = 0.0004 against PolyPhen-2, p = 0.0001 against CADD and p < 0.0001 against SIFT. Its scores are not calibrated probabilities. The Brier score was 0.053 against 0.111 for a model predicting only the base rate, and every score bin above 0.4 contained more CF-causing variants than its mean score predicted. Across 1,278 AlphaMissense-ambiguous variants, a high AlphaGenome splice quantile and a raised SpliceAI delta co-occurred far more often than independence predicts (odds ratio 12.36, 95% confidence interval 3.83 to 39.86, p = 9.0 × 10⁻⁸). Eighteen variants met both predictors at stricter thresholds.

Two methods built on different principles agree on a small, specific set of variants that protein-level scoring cannot resolve. That set is a prioritisation for laboratory work, not a classification. The benchmark carries only 33 negative variants, and the only external functional comparison available has 23 members, too few to rank splice predictors.

---

# Author Summary

When newborn screening finds a change in the CFTR gene, the laboratory often cannot say whether that change causes cystic fibrosis. Most changes in this gene have never been seen in enough patients to be classified. Families are left with an answer that is not an answer.

We asked how much help prediction software can offer. We tested AlphaMissense, which predicts whether a change to a protein is harmful, against the variants that the CFTR2 patient database has already classified. It did better than three older tools. We also found that its scores should not be read as probabilities, because it is systematically too cautious through the middle of its range.

Many variants sit in a grey zone that AlphaMissense does not resolve. For those, we asked two separate programs whether the change disrupts the way the gene is spliced. The two programs agree with each other far more often than chance would produce, and eighteen variants are flagged by both.

We are not saying those eighteen variants cause cystic fibrosis. We did no laboratory work. We produced a short list that a laboratory could now test.

---

# Introduction

Cystic fibrosis follows from loss of function in the CFTR gene [1]. The CFTR2 database assembles clinical and functional evidence to assign variants to categories such as CF-causing and Non CF-causing [2], and in its 30 January 2026 release it reports 2,092 variants drawn from 122,935 patients. That is a small fraction of what sequencing returns. Of 3,220 unique protein changes extracted from the CFTR region of a ClinVar release [CITATION NEEDED: Landrum et al.], only 259 carry a binary CFTR2 determination. The consequence falls on families. A child whose newborn screening panel returns a CFTR change with no classification receives a result that cannot be acted on, and the interpretation frameworks that laboratories apply [3] place computational evidence among the weakest categories they recognise.

Protein-level predictors try to fill that space by asking whether an amino acid substitution damages the protein. SIFT scores conservation across homologues [4], PolyPhen-2 adds structural and sequence features [5], and CADD integrates many annotations into a single deleteriousness score [6]. On CFTR specifically these tools performed poorly: an eight-predictor comparison across 779 CFTR missense variants found no tool reaching acceptable sensitivity and specificity at the same time [7]. AlphaMissense changed the available accuracy by scoring every possible human missense variant from a protein language model trained on evolutionary data and structural context [8, 9]. A CFTR-specific benchmark of AlphaMissense against clinical and functional data reported fair classification performance with a high false positive rate, and showed that the score does not distinguish misfolding from gating defects [10]. All of these tools share one limit. They score the protein consequence, so they are silent on a variant that acts by disrupting splicing while leaving the encoded residue tolerable.

Two models address that second mechanism from different directions. SpliceAI predicts changes in splice donor and acceptor probability directly from sequence [CITATION NEEDED: Jaganathan et al. 2019]. AlphaGenome predicts many regulatory modalities, splice site usage among them, from a one-megabase window at base resolution, and reports each variant effect as a quantile against a background of common variants [11]. AlphaGenome has been applied to a single gene with wet-laboratory follow-up in a blood group locus [12], but we found no published CFTR-specific application [CITATION NEEDED: priority claim, requires a systematic literature search]. The specific gap is narrow and testable. If a protein-level score leaves a variant ambiguous, do two independently built splice models agree about it, and does that agreement exceed chance?

We benchmarked AlphaMissense against CADD, PolyPhen-2 and SIFT on CFTR2-labelled missense variants with confidence intervals and a paired test, and we measured how far its scores depart from calibrated probabilities. We then scored every AlphaMissense-ambiguous CFTR missense variant with AlphaGenome and SpliceAI and tested whether the two agree beyond chance. AlphaMissense classifies CFTR2-labelled missense variants with high discrimination and outperforms CADD, PolyPhen-2 and SIFT; a small set of AlphaMissense-ambiguous variants is independently flagged for splicing disruption by AlphaGenome and SpliceAI and forms a candidate list for functional testing. This work is computational. No variant here is claimed to cause cystic fibrosis.

---

# Results

## The benchmark set and the ambiguous set are separate variant sets

Two variant sets support this work and they are not nested. The benchmark set begins with the CFTR region of a ClinVar release annotated with Ensembl VEP [13], from which 3,220 unique protein changes were extracted across 5,923 data lines. Of these, 2,909 converted to the single-letter notation AlphaMissense uses; the 311 that did not are 309 nonsense changes and 2 stop-loss changes, which AlphaMissense does not score. Merging scores left 2,665 protein changes with an AlphaMissense score, of which 259 carry a binary CFTR2 determination, 226 CF-causing and 33 Non CF-causing. Of those 259, five lack at least one comparator score, leaving 254 for the four-tool comparison, 221 CF-causing and 33 Non CF-causing.

The second set comes from the AlphaMissense table of CFTR missense changes, which holds 9,721 scored single-nucleotide variants covering 8,597 unique protein changes. Filtering to the ambiguous class, meaning a score between 0.34 and 0.564, gives 1,278 variants covering 1,100 unique protein changes. These 1,278 are not a subset of the benchmark chain: 431 of them appear among the 3,220 protein changes, and the remainder are missense changes that the ClinVar extract does not contain. Of the 1,278, 291 carry a gnomAD v4 allele frequency above zero and 952 are absent from gnomAD v4 entirely. Fig 1 shows both chains and the counts at each step. Table 1 lists every data source with its version and extraction date.

[`results/paper/fig1_flow_counts.csv`; `results/phase1/unique_variant_counts.csv`; `results/phase1/benchmark_metrics_dedup.csv`; `results/phase1/benchmark_cohort_dedup.csv`; `docs/paper/tables/Table1_data_sources.md`]

**Fig 1. Derivation of the two variant sets analysed.** Flow of variants through both chains. The benchmark chain begins with 3,220 unique protein changes extracted from the CFTR region of a ClinVar VCF and narrows to 2,909 convertible to AlphaMissense notation, 2,665 carrying an AlphaMissense score, 259 carrying a binary CFTR2 label (226 CF-causing, 33 Non CF-causing), and 254 carrying CADD, PolyPhen-2 and SIFT scores as well (221 and 33). The screening chain begins with the AlphaMissense CFTR table of 9,721 scored single-nucleotide variants covering 8,597 unique protein changes, narrows to the 1,278 of ambiguous AlphaMissense class covering 1,100 unique protein changes, then to 778 with an AlphaGenome ATAC or SPLICE quantile above 0.95, then to 18 that also carry a SpliceAI maximum delta above 0.5 under the gene-mask definition, of which 13 also meet the centre-mask definition. The two chains are separate variant sets and are not nested: 431 of the 1,278 appear among the 3,220. Numbers to the right of the benchmark chain are the variants removed at each step.

**Table 1. Data sources.** Full table with per-cell source citations is maintained at `docs/paper/tables/Table1_data_sources.md` and is reproduced in the submitted manuscript at this position.

## AlphaMissense discriminates CFTR2 labels better than three comparators

On the 254 variants carrying all four scores, AlphaMissense reached an area under the receiver operating characteristic curve of 0.9548 (95% confidence interval 0.9121 to 0.9880) and an average precision of 0.9923 (0.9838 to 0.9983). PolyPhen-2 reached 0.8109 (0.7215 to 0.8859), CADD 0.7489 (0.6257 to 0.8546) and SIFT 0.6701 (0.5781 to 0.7644). On the full set of 259 unique labelled variants, which includes the five without a complete comparator record, AlphaMissense reached 0.9549 (0.9119 to 0.9878) with an average precision of 0.9924 (0.9842 to 0.9983). Table 2 reports all four tools with intervals; Fig 2 shows the curves.

The paired DeLong test [14, 15] compares each comparator against AlphaMissense on the same variants. AlphaMissense exceeded PolyPhen-2 at Z = 3.5125, p = 0.000444, CADD at Z = 3.8341, p = 0.000126, and SIFT at Z = 6.2951, p < 0.0001. The bootstrap intervals in Table 2 are wide, and the AlphaMissense interval overlaps the PolyPhen-2 interval. That width follows from the 33 negative variants in the set: the interval of a discrimination statistic on this label distribution is governed by the smaller class. The DeLong test is paired across the same variants and does not share that limitation, which is why both are reported.

[`results/paper/auc_ci.csv`; `results/phase1/delong_tests_dedup.csv`; `results/phase1/benchmark_metrics_dedup.csv`; `docs/paper/tables/Table2_four_tool_benchmark.md`]

**Table 2. Four-tool benchmark on CFTR2-labelled missense variants.** Discrimination against CFTR2 binary labels on the 254 deduplicated variants carrying all four scores (221 CF-causing, 33 Non CF-causing). Confidence intervals are percentile bootstrap, 2,000 resamples, seed 42. The DeLong column compares each tool against AlphaMissense on the same variants.

| Tool | AUC (95% CI) | Average precision (95% CI) | DeLong vs AlphaMissense |
|---|---|---|---|
| AlphaMissense | 0.9548 (0.9121–0.9880) | 0.9923 (0.9838–0.9983) | reference |
| PolyPhen-2 | 0.8109 (0.7215–0.8859) | 0.9560 (0.9239–0.9816) | Z = 3.5125, p = 0.000444 |
| CADD | 0.7489 (0.6257–0.8546) | 0.9328 (0.8872–0.9704) | Z = 3.8341, p = 0.000126 |
| SIFT | 0.6701 (0.5781–0.7644) | 0.9110 (0.8725–0.9457) | Z = 6.2951, p < 0.0001 |

**Fig 2. Receiver operating characteristic curves for four predictors.** ROC curves for AlphaMissense, PolyPhen-2, CADD and SIFT against CFTR2 binary labels on the 254 deduplicated variants carrying all four scores (221 CF-causing, 33 Non CF-causing). The shaded band is the pointwise 95% percentile bootstrap interval for the AlphaMissense curve over 2,000 resamples with seed 42, interpolated onto a common false-positive-rate grid; it is pointwise rather than simultaneous and is drawn for AlphaMissense only. Legend entries give each tool's area under the curve with its 95% bootstrap confidence interval. The diagonal marks chance performance. SIFT is plotted as 1 minus the SIFT score so that higher is more damaging for every curve.

## AlphaMissense scores are not calibrated probabilities

Read as probabilities, the scores are under-confident. The Brier score across the 259 labelled variants was 0.053, against 0.111 for a model that predicts the base rate of 0.873 for every variant. The expected calibration error was 0.102, and the mean predicted score of 0.793 sits below the observed positive fraction of 0.873.

The departure is systematic rather than scattered. Every score bin above 0.4 contained more CF-causing variants than its mean score predicted. The bin from 0.4 to 0.5 held 5 variants with a mean score of 0.465, all 5 of them CF-causing, a gap of 0.535. The bin from 0.5 to 0.6 held 10 variants with a mean score of 0.563 and 9 CF-causing, a gap of 0.337. The gap narrows as the score rises, reaching 0.039 in the top bin, which held 136 variants with a mean score of 0.961 and all 136 CF-causing. Below 0.4 the direction reverses in the two bins that contain no positives at all: 13 variants between 0.1 and 0.2 and 4 variants between 0.2 and 0.3.

[`results/paper/calibration_n259.csv`]

## AlphaGenome and SpliceAI agree beyond chance on the ambiguous set

Across the 1,278 AlphaMissense-ambiguous variants, 747 carry an AlphaGenome gene-mask splice quantile above 0.95 and 52 carry a SpliceAI maximum delta above 0.2. Forty-nine variants meet both. Under independence the expected count in that cell is 30.39. The two criteria are associated: χ²(1) = 28.57, p = 9.0 × 10⁻⁸, with Fisher's exact two-sided p = 4.3 × 10⁻⁹ and an odds ratio of 12.36 (95% confidence interval 3.83 to 39.86). Three variants carry a raised SpliceAI delta without clearing the AlphaGenome threshold, and 698 clear the AlphaGenome threshold without a raised SpliceAI delta.

That 747 of 1,278 variants exceed the 0.95 quantile is a property of the comparison background rather than of this gene: AlphaGenome quantiles rank a variant against common variants above 1% minor allele frequency, which are predominantly non-coding, so rare coding variants in a heavily spliced gene routinely sit in the upper percentiles [11]. Repeating the test on the genome-wide quantile recalibration moves the marginal count to 800 of 1,278 and leaves the association in place: χ²(1) = 23.17, p = 1.5 × 10⁻⁶, odds ratio 10.33 (3.20 to 33.33).

[`results/paper/ag_spliceai_2x2.csv`; `results/alphagenome/alphagenome_full_cftr_results.csv`; `results/alphagenome/quantiles_genomewide_2026-08.csv`; `results/comparator_scores.csv`]

## Eighteen variants form a concordant candidate set

Applying stricter thresholds to both predictors gives a small set. The gene-mask definition, an AlphaGenome gene-mask splice quantile above 0.95 together with a SpliceAI maximum delta above 0.5, returns 18 variants. The centre-mask definition, a centre-mask 501 bp splice score in the top 5% of the 1,278 (an empirical threshold of 0.0828, exceeded by 64 variants) together with the same SpliceAI criterion, returns 13. The 13 are a subset of the 18, so the union is 18. S1 Table lists all 18 with both memberships marked, and Fig 3 places them against the rest of the 1,278.

The 18 are distributed across three CFTR domains: 5 in MSD1, 2 in NBD1 and 11 in MSD2. Their AlphaMissense scores span 0.3415 to 0.5491, which is the ambiguous band by construction. Their SpliceAI deltas span 0.55 to 1.00, carried by donor loss in 7 variants, acceptor gain in 5, donor gain in 4 and acceptor loss in 2. Thirteen are absent from gnomAD v4 and the remaining five have a maximum allele frequency between 6.84 × 10⁻⁷ and 4.01 × 10⁻⁴.

No member of the set carries a CF-causing or Non CF-causing determination in CFTR2. Three carry the CFTR2 status "No interpretation available", H620Q, G1047C and K1060T, and the other 15 have no CFTR2 record. One member, G970V, also appears in the minigene benchmark described below, where it is a confirmed splice-altering variant; the other 17 have no experimental splicing result in any file used here.

[`results/paper/concordant_set.csv`; `results/paper/fig1_flow_counts.csv`; `results/alphagenome/rescore_centermask.csv`; `results/alphagenome/alphagenome_full_cftr_results.csv`; `results/comparator_scores.csv`; `docs/paper/tables/Table3_concordant_set.md`]

**Fig 3. AlphaGenome splice quantile against SpliceAI delta.** One point per variant for all 1,278 AlphaMissense-ambiguous CFTR missense single-nucleotide variants. The horizontal axis is the AlphaGenome gene-mask SPLICE quantile from the May 2026 scoring run, plotted as −log10(1 − quantile) because the values crowd against 1.0; axis labels give the untransformed quantile. The vertical axis is the SpliceAI maximum delta across the four channels, on its native scale. Dashed lines mark the two thresholds defining the concordant set, quantile 0.95 and delta 0.5. Blue circles are the 13 variants meeting both the gene-mask and centre-mask definitions; orange squares are the 5 meeting the gene-mask definition only; all 18 are labelled with their protein change. Grey points are the remaining 1,260 variants.

## The minigene benchmark does not discriminate between scorers

The only external functional comparison available is a 23-row benchmark of CFTR variants tested by minigene assay, 11 splice-altering and 12 not, compiled from two studies [16, 17]. On these labels the AlphaGenome gene-mask splice quantile reached an area under the curve of 0.856 (95% confidence interval 0.676 to 0.985) and the gene-mask raw score 0.860 (0.683 to 0.985). The intervals are about 0.30 wide for every scorer, and a single label change moves the estimate by about 0.008. At its 0.95 threshold the AlphaGenome quantile returned 10 true positives, 8 false positives, 1 false negative and 4 true negatives, giving sensitivity 0.909 and specificity 0.333.

SpliceAI returned a delta of exactly zero for 21 of the 23 rows. Its area under the curve on this benchmark was 0.432 (0.269 to 0.583), and at thresholds of 0.2 and 0.5 it returned 1 true positive against 10 false negatives. These figures measure the coverage of a precomputed score file rather than prediction, because a zero in this setting can mean not assessed. No scorer can be ranked on 23 observations with these interval widths.

[`results/paper/minigene_benchmark.csv`]

---

# Discussion

Three findings carry this work. AlphaMissense separates CFTR2-labelled CF-causing from Non CF-causing missense variants with an area under the curve of 0.955 and exceeds CADD, PolyPhen-2 and SIFT on the same variants under a paired test. Its scores discriminate well but are not calibrated probabilities, running under-confident across the whole range above 0.4. Among the 1,278 variants it leaves ambiguous, AlphaGenome and SpliceAI agree about which disrupt splicing far more often than independence predicts, and 18 variants meet both at stricter thresholds.

The AlphaMissense result sits alongside the existing CFTR-specific benchmark [10] rather than contradicting it. That study reported fair classification against CFTR2 with a high false positive rate, using 169 variants selected for available clinical phenotype data. We used every variant carrying a binary CFTR2 determination, deduplicated to 259 unique protein changes so that a variant mapping to several nucleotide changes contributes once. The direction is the same in both: AlphaMissense carries real signal about CFTR variant pathogenicity, and it is better than the older tools it replaces. What we add is uncertainty and calibration. The confidence intervals show how much of the apparent margin over PolyPhen-2 survives the small negative class, and the calibration analysis shows that a score of 0.5 from this tool does not mean a coin flip. For a laboratory using the score as computational evidence within an interpretation framework [3], that second point matters more than the first. The published decision boundary at 0.564 is a threshold, not a probability, and treating it as one would understate risk through the middle of the range.

The 18 concordant variants are a list for functional testing and not a classification. Two things make the agreement worth acting on. The predictors are built on different principles: SpliceAI reads splice donor and acceptor probability from local sequence, while AlphaGenome predicts splice site usage as one modality among many across a megabase window [11]. They therefore fail in different ways, and a variant flagged by both is less likely to reflect a single model's systematic error. The association is also strong and survives the quantile recalibration, with an odds ratio of 12.36 falling to 10.33 and the p-value remaining below 10⁻⁵ in both. What the agreement does not establish is that any of these variants alters splicing in a cell, still less that it causes disease. Both tools are trained on overlapping genomic annotation, so their independence is partial. Agreement between two predictions is a prediction. Eighteen is also a small number set by two thresholds that we chose, and neither threshold was calibrated on CFTR.

## Limitations

The benchmark contains 33 Non CF-causing variants. Every discrimination interval in Table 2 is governed by that number, and no amount of resampling repairs it. The labels themselves are curated clinical calls rather than physical measurements: CFTR2 assigns them from clinical and functional evidence [2], so a tool that agrees with CFTR2 agrees with an expert synthesis, not with a ground truth independent of human judgement.

Three properties of the splice analysis constrain it. The AlphaGenome quantile ranks a variant against common variants, which are predominantly non-coding, so 747 of 1,278 coding variants clear the 0.95 threshold and the marginal rate carries no information about this gene. SpliceAI cannot serve as a negative control on this variant set, because its reporting window is plus or minus 50 nucleotides while every variant here lies within 500 bp of a CFTR splice site, so a zero may mean not assessed rather than assessed and negative. The external minigene benchmark has 23 members, intervals about 0.30 wide, and 21 rows where SpliceAI returns zero; it cannot rank the scorers and we do not use it to.

Two gaps are in the record rather than the analysis. We could not place any variant in an exon or give its distance to the nearest splice site, because no CFTR exon annotation exists in the project files; both columns read [NOT IN REPO] throughout S1 Table. Access dates are unrecorded for the CADD query, the SpliceAI query, the gnomAD v4 lookup and the AlphaMissense download, and the SpliceAI plugin and model versions are likewise unrecorded; each appears as [NOT IN REPO] in Table 1. The gnomAD lookup file also has no generating script in the project, so the 291 and 952 counts rest on a file that cannot be regenerated as committed.

This work is computational throughout. We performed no experiment. No variant discussed here is claimed to cause cystic fibrosis.

## What validation would look like

The concordant set is sized for a single minigene experiment. One of the 18, G970V, has already been tested by that assay and alters splicing [16], which shows the set is not empty of real effects but establishes nothing about the other 17. Those 17 are untested. A minigene panel covering them would return a count: how many of 17 alter splicing, against a background rate that the 12 negative variants in the existing benchmark help anchor. That number is the experiment this analysis is for. A result near zero would show that agreement between two sequence models does not survive contact with a cell, which is as informative as the alternative.

## The gap this work sits in

Rare CFTR variants fall between two methods that each miss them. Genome-wide association studies of cystic fibrosis severity find common modifier loci [CITATION NEEDED: Corvol et al. 2015], but a variant seen in a handful of people carries no association signal and cannot appear in that analysis. Protein-level predictors reach every possible missense change, including the rare ones, but score only the protein consequence and return an ambiguous value for a substantial set, 1,278 in CFTR. Splice prediction addresses part of what is missed, and the agreement reported here shows the two available tools converge on a specific small set rather than scattering. This is a filter, not a solution. It converts 1,278 variants that no one can act on into 18 that a laboratory can test, and the value of the filter is settled by that laboratory, not by the filter.

---

# Materials and Methods

> The section below is reproduced verbatim from `docs/paper/02_methods.md`, including its bracketed source lines. Those brackets are removed at submission.

## Variant inventory and clinical labels

Variants were taken from the CFTR region of a ClinVar release whose VCF header records `##fileDate=2026-04-15` and `##source=ClinVar`. The region chr7:117,480,000–117,670,000 was extracted with bcftools 1.23.1 on 21 April 2026, normalised with `bcftools norm`, and annotated with Ensembl VEP v115.1 against the GRCh38.p14 cache carrying ClinVar 202502 annotations. The file is sites-only and carries no sample columns or patient-level data. Its global allele-frequency field is the 1000 Genomes Phase 3 frequency, not a gnomAD frequency. A protein-change regular expression applied to the CSQ annotation yielded 3,220 unique protein changes from 5,923 data lines. Clinical labels came from the CFTR2 database release of 30 January 2026, which reports 2,092 variants across 122,935 patients; the date on which that release was downloaded is [NOT IN REPO], and the earliest evidence of it in this project is a file modification time of 14 May 2026.
[`scripts/cftr2_scraper_analysis.py`; `data/All_Variants_VEP.Gene.vcf`; `data/cftr2_variants.xlsx`; `data/cftr2_results.csv`; `results/phase1/unique_variant_counts.csv`; `audit/COHORT_PROVENANCE.md`]

## AlphaMissense scores

AlphaMissense precomputed pathogenicity scores for hg38 were obtained from Zenodo record 8208688 and filtered to CFTR, UniProt P13569, transcript ENST00000003084.10, giving 9,721 single-nucleotide variants covering 8,597 unique protein changes. The dataset version string and the download date are [NOT IN REPO]. Three-letter protein-change names from the VCF were converted to the single-letter form AlphaMissense uses, which succeeded for 2,909 of the 3,220 protein changes; the 311 failures are 309 nonsense changes and 2 stop-loss changes, which AlphaMissense does not score. Merging scores into the labelled table left 2,665 protein changes with an AlphaMissense score. Each variant carries the published AlphaMissense class, with the likely-pathogenic boundary at 0.564 and the likely-benign boundary at 0.34.
[`notebooks/alphamissense.ipynb`; `scripts/alphamissense_analysis.py`; `data/cftr_alphamissense.tsv`; `data/cftr2_results_annotated.csv`; `results/phase1/unique_variant_counts.csv`; `results/phase1/SOURCE.md`]

## Benchmark cohort and deduplication

The benchmark cohort is every protein change carrying both an AlphaMissense score and a binary CFTR2 determination of CF-causing or Non CF-causing. Merging on protein-variant name produced 292 rows for 259 unique variants, because one protein change can map to several nucleotide changes. Duplicated rows never differ in label or score. Rows were deduplicated keep-first on the protein-variant name, leaving 259 unique variants, 226 CF-causing and 33 Non CF-causing. Deduplication precedes every metric and every cross-validation fold assignment reported in this manuscript. The earlier 292-row and 286-row cohorts are superseded and are not used.
[`scripts/phase1_build_cohort.py`; `results/phase1/benchmark_cohort_dedup.csv`; `results/phase1/unique_variant_counts.csv`; `docs/AUDIT_RECORD.md`]

## Comparator scores

CADD PHRED scores came from the CADD v1.7 GRCh38 REST API endpoint `GRCh38-v1.7`; the query date is [NOT IN REPO]. SIFT and PolyPhen-2 scores were parsed from fields 31 and 32 of the CSQ annotation in the VEP-annotated VCF, so they carry the VEP v115.1 versions of those predictors rather than standalone releases. SIFT scores run in the opposite direction to the other three, so they were inverted as one minus the score; every predictor column therefore reads higher-is-more-damaging. Five of the 259 unique validation variants lack at least one comparator score and are excluded from any four-tool comparison, leaving 254 variants, 221 CF-causing and 33 Non CF-causing. Leu137Pro, Thr604Ile and Trp1098Cys returned no CADD v1.7 score; Trp496Gly and Gly622Val have no CADD, SIFT or PolyPhen-2 score.
[`scripts/phase1_fetch_cadd.py`; `scripts/fetch_comparator_scores.py`; `results/phase1/inputs_cadd_scores.csv`; `results/phase1/inputs_polyphen_sift.csv`; `results/phase1/benchmark_cohort_dedup.csv`]

## Discrimination and its uncertainty

For each predictor we computed the area under the receiver operating characteristic curve and the average precision against the CFTR2 binary label, using `roc_auc_score` and `average_precision_score` from scikit-learn 1.9.0 on Python 3.13.1. Both are threshold-independent, which matters here because the four predictors publish thresholds on different scales. Confidence intervals are percentile bootstrap intervals from 2,000 resamples of the variant list with replacement, drawn with `numpy.random.default_rng(42)`; resamples containing a single class were discarded, and none were on either cohort. The same resample indices are applied to all four predictors within a draw, so the intervals share their sampling variation. Intervals are reported for the four predictors on the 254-variant cohort and for AlphaMissense on the full 259-variant cohort.
[`scripts/paper/p3a_auc_ci.py`; `results/paper/auc_ci.csv`; `results/phase1/benchmark_cohort_dedup.csv`]

## Paired comparison between predictors

Each comparator's ROC curve was compared against AlphaMissense's on the same 254 variants with the DeLong test for two correlated ROC curves, implemented as the fast algorithm of Sun and Xu (2014). The test is paired, which is the appropriate form here because all four predictors score the same variants; it is reported alongside the bootstrap intervals rather than in place of them, since overlapping marginal intervals do not imply an absent paired difference.
[`scripts/phase1_delong.py`; `scripts/phase1_utils_delong.py`; `results/phase1/delong_tests_dedup.csv`]

## Calibration

AlphaMissense emits a score in the unit interval that is not trained to be a calibrated probability, so calibration was measured descriptively rather than tested. The 259 unique validation variants were binned into ten equal-width bins across the unit interval by AlphaMissense score. For each bin we recorded the count, the mean predicted score and the observed fraction of CF-causing variants. We also computed the Brier score with scikit-learn's `brier_score_loss`, the Brier score of a model predicting the base rate for every variant, and the expected calibration error as the sample-weighted mean absolute gap between predicted and observed values across occupied bins.
[`scripts/paper/p3b_calibration.py`; `results/paper/calibration_n259.csv`; `results/phase1/benchmark_cohort_dedup.csv`]

## The AlphaMissense-ambiguous screening set

A second variant set was assembled for the splicing analysis: every CFTR single-nucleotide variant whose AlphaMissense class is ambiguous, meaning a score between 0.34 and 0.564. Applied to the AlphaMissense CFTR table this gives 1,278 variants covering 1,100 unique protein changes. This set is drawn from the complete table of possible CFTR missense changes, not from the ClinVar-derived inventory, and the two sets are not nested: 431 of the 1,278 appear among the 3,220 protein changes of the benchmark chain. Of the 1,278, 291 carry a gnomAD v4 allele frequency above zero and 952 are absent from gnomAD v4 entirely; the gnomAD query date is [NOT IN REPO] and no committed script performs the lookup. The set is not a set of variants of uncertain significance in the clinical sense, because most carry no clinical submission of any kind.
[`data/cftr_alphamissense.tsv`; `results/alphagenome/alphagenome_full_cftr_results.csv`; `results/gnomad_cftr_lookup.csv`; `results/paper/fig1_flow_counts.csv`; `audit/COHORT_PROVENANCE.md`]

## AlphaGenome scoring

The 1,278 variants were scored with AlphaGenome v0.6.1 on 28 May 2026 across lung tracks, producing splice-site-usage, ATAC and RNA-seq outputs as a raw score and a quantile score. Two scorers were used and are kept distinct throughout. The gene-mask scorer returns the largest change in splice-site probability at any junction across the whole CFTR gene body, so for a coding variant its value is set partly by the distance to the nearest canonical splice site rather than by the variant's own effect. The centre-mask scorer restricts the comparison to a 501 bp window centred on the variant. Quantile scores rank a variant against AlphaGenome's common-variant background, defined as variants above 1% minor allele frequency in any gnomAD v3 population, and not against all human variation; because that background is predominantly non-coding, rare coding variants in a heavily spliced gene routinely exceed its upper percentiles. The scoring run predates AlphaGenome's 18 June 2026 move from a chromosome-22 quantile background to a genome-wide one, so every quantile-based analysis is reported on the original chromosome-22 calibration and repeated on the genome-wide recalibration as a sensitivity analysis; the day-level date of the recalibration run is [NOT IN REPO].
[`scripts/alphagenome_full_cftr.py`; `scripts/regenerate_quantiles_genomewide.py`; `results/alphagenome/alphagenome_full_cftr_results.csv`; `results/alphagenome/rescore_centermask.csv`; `results/alphagenome/quantiles_genomewide_2026-08.csv`; `docs/AUDIT_RECORD.md`; `audit/PROVENANCE.md`]

## SpliceAI scoring

SpliceAI delta scores for the same 1,278 variants were retrieved through the Ensembl VEP REST endpoint `https://rest.ensembl.org/vep/human/region` with the SpliceAI plugin, taking the maximum of the four channels: acceptor gain, acceptor loss, donor gain and donor loss. The plugin version, the SpliceAI model version and the query date are all [NOT IN REPO]. Variants returning a delta of exactly zero were re-queried to separate a genuine zero prediction from an absent record, and 766 were examined in that pass. Two properties of the score constrain its use as a negative control. Its reporting window is plus or minus 50 nucleotides, while every variant in this cohort lies within 500 bp of a CFTR splice site, so a zero can mean not assessed rather than assessed and negative. The precomputed score file also does not cover all exon-interior variants.
[`scripts/fetch_comparator_scores.py`; `scripts/fix_spliceai_scores.py`; `scripts/reclassify_spliceai_zeros.py`; `results/comparator_scores.csv`; `results/spliceai_zero_reclassification.csv`; `docs/AUDIT_RECORD.md`]

## Agreement between AlphaGenome and SpliceAI

Agreement between the two splice predictors across the 1,278 variants was tested on a 2x2 table of AlphaGenome gene-mask SPLICE quantile above 0.95 against SpliceAI maximum delta above 0.2, using Pearson's chi-square test of independence without continuity correction as the primary test, with the Yates-corrected chi-square and Fisher's exact test reported alongside it; all three come from `scipy.stats` in SciPy 1.17.1. The odds ratio is reported with a 95% Woolf interval computed on the log scale, with a Haldane-Anscombe correction of 0.5 applied only if a cell is empty. The table was built twice, once on each quantile calibration.
[`scripts/paper/p3e_ag_spliceai_2x2.py`; `results/paper/ag_spliceai_2x2.csv`; `results/alphagenome/alphagenome_full_cftr_results.csv`; `results/alphagenome/quantiles_genomewide_2026-08.csv`; `results/comparator_scores.csv`]

## Definition of the concordant set

Variants flagged independently by both splice predictors were assembled under two definitions, which are reported together rather than one being chosen. The gene-mask definition is an AlphaGenome gene-mask SPLICE quantile above 0.95 together with a SpliceAI maximum delta above 0.5. The centre-mask definition is a centre-mask 501 bp splice score in the top 5% of the 1,278, an empirical threshold of 0.0828 that 64 variants exceed, together with the same SpliceAI criterion. For every variant in the union we recorded the protein change, hg38 position, reference and alternate allele, CFTR domain, AlphaMissense score, AlphaGenome splice raw and quantile scores under both calibrations, the centre-mask score, the SpliceAI maximum delta and the channel carrying it, CADD PHRED, gnomAD v4 maximum allele frequency, CFTR2 determination, and whether the variant appears in the minigene benchmark. Domains were assigned from residue number using the CFTR domain boundaries already used in this project. Two requested columns could not be filled and are recorded as [NOT IN REPO] for every row: the exon or intron a variant falls in, and its distance to the nearest splice site. The repository holds no CFTR exon annotation in any form and no script computes either quantity for this cohort.
[`scripts/paper/p3c_concordant_set.py`; `results/paper/concordant_set.csv`; `results/alphagenome/rescore_centermask.csv`; `results/alphagenome/alphagenome_full_cftr_results.csv`; `results/comparator_scores.csv`; `results/gnomad_cftr_lookup.csv`; `data/cftr2_results_annotated.csv`; `scripts/alphamissense_analysis.py`]

## External validation against minigene assays

The only external functional comparison available is a 23-row benchmark compiled on 2 August 2026 from two minigene studies, Bergougnoux et al. 2023 and Zhang et al. 2025, covering 22 unique CFTR variants, of which 11 showed altered splicing and 12 did not. Glu403Asp contributes two rows as two distinct nucleotide changes. Coordinates are GRCh38, derived from NM_000492.4 HGVS notation through the Ensembl VEP REST API. Against these labels we scored the AlphaGenome gene-mask SPLICE quantile, the AlphaGenome gene-mask raw score, and the SpliceAI maximum delta, reporting AUC with percentile bootstrap intervals from 2,000 resamples at seed 42, and 2x2 contingency tables at SpliceAI 0.2, SpliceAI 0.5 and AlphaGenome quantile 0.95. The benchmark is too small to select a scorer, and it is reported with that limit attached rather than as a validation result: the bootstrap intervals span roughly 0.30 of AUC, and a single label change moves the estimate by about 0.008. SpliceAI returns a delta of exactly zero for 21 of the 23 rows, so its figures on this benchmark measure the coverage of a precomputed file as much as prediction.
[`scripts/paper/p3d_minigene_benchmark.py`; `results/paper/minigene_benchmark.csv`; `results/experimental_benchmark.csv`; `docs/experimental_benchmark.md`]

## Software, figures and reproducibility

All analyses ran on Python 3.13.1 with NumPy 2.4.6, pandas 2.3.3, scikit-learn 1.9.0, SciPy 1.17.1 and Matplotlib 3.10.9. Every random procedure uses seed 42 and `numpy.random.default_rng`. Analyses written for this manuscript are new scripts under `scripts/paper/` writing to `results/paper/`; no existing script or results file was modified. Figures were produced at 300 dpi as RGB TIFF files at most 7.5 inches wide, in Arial, with no figure number, title or caption inside the image file. The categorical colours used across figures were checked for colour-vision-deficiency separation and for contrast against the figure background, and each series also carries a non-colour encoding, a line style or a marker shape.
[`scripts/paper/figstyle.py`; `scripts/paper/p4_fig1_flow.py`; `scripts/paper/p4_fig2_roc.py`; `scripts/paper/p4_fig3_scatter.py`; `scripts/paper/p4_tables.py`; `results/paper/fig1_flow_counts.csv`]

---

# Acknowledgments

[NOT IN REPO: acknowledgments]

---

# Data Availability Statement

All analysis code is available in the project Git repository on branch `paper-prep-2026-10`, under `scripts/` and `scripts/paper/`. All derived results used in this manuscript are in that repository under `results/paper/`, `results/phase1/`, `results/alphagenome/` and `results/comparator_scores.csv`. A persistent identifier for an archived snapshot is [NOT IN REPO: repository DOI not yet minted].

Four input files are not committed to the repository: `data/AlphaMissense_hg38.tsv.gz`, `data/cftr_alphamissense.tsv`, `data/All_Variants_VEP.Gene.vcf` and `data/cftr2_results_annotated.csv`. The reason each is withheld is [NOT IN REPO: licence or file-size reason not recorded]. All four are reconstructible from public sources. AlphaMissense precomputed scores for hg38 are distributed through Zenodo record 8208688, and `data/cftr_alphamissense.tsv` is that file filtered to UniProt P13569 and transcript ENST00000003084.10. `data/All_Variants_VEP.Gene.vcf` is the ClinVar public VCF release dated 2026-04-15, restricted to chr7:117,480,000–117,670,000 with bcftools 1.23.1, normalised, and annotated with Ensembl VEP v115.1 against the GRCh38.p14 cache. `data/cftr2_results_annotated.csv` is the CFTR2 release of 30 January 2026, downloaded from cftr2.org, merged with the AlphaMissense scores above. CADD v1.7 scores are available from the CADD GRCh38 v1.7 REST service, SpliceAI deltas from the Ensembl VEP REST SpliceAI plugin, and allele frequencies from gnomAD v4. AlphaGenome v0.6.1 is accessed through its public API; the scores used here are committed under `results/alphagenome/`.

---

# References

1. Elborn JS. Cystic fibrosis. Lancet. 2016;388:2519–2531.
2. Sosnay PR, Siklosi KR, Van Goor F, Kaniecki K, Yu H, Sharma N, et al. Defining the disease liability of variants in the cystic fibrosis transmembrane conductance regulator gene. Nat Genet. 2013;45:1160–1167.
3. Richards S, Aziz N, Bale S, Bick D, Das S, Gastier-Foster J, et al. Standards and guidelines for the interpretation of sequence variants: a joint consensus recommendation of the American College of Medical Genetics and Genomics and the Association for Molecular Pathology. Genet Med. 2015;17:405–424.
4. Ng PC, Henikoff S. SIFT: predicting amino acid changes that affect protein function. Nucleic Acids Res. 2003;31:3812–3814.
5. Adzhubei IA, Schmidt S, Peshkin L, Ramensky VE, Gerasimova A, Bork P, et al. A method and server for predicting damaging missense mutations. Nat Methods. 2010;7:248–249.
6. Kircher M, Witten DM, Jain P, O'Roak BJ, Cooper GM, Shendure J. A general framework for estimating the relative pathogenicity of human genetic variants. Nat Genet. 2014;46:310–315.
7. Michels M, Matte U, Fraga LR, Mancuso ACBB, Ligabue-Braun R, Berneira EFR, et al. Determining the pathogenicity of CFTR missense variants: multiple comparisons of in silico predictors and variant annotation databases. Genet Mol Biol. 2019;42(3):560–570.
8. Cheng J, Novati G, Pan J, Bycroft C, Žemgulytė A, Applebaum T, et al. Accurate proteome-wide missense variant effect prediction with AlphaMissense. Science. 2023;381:eadg7492.
9. Jumper J, Evans R, Pritzel A, Green T, Figurnov M, Ronneberger O, et al. Highly accurate protein structure prediction with AlphaFold. Nature. 2021;596:583–589.
10. McDonald EF, Oliver KE, Schlebach JP, Meiler J, Plate L. Benchmarking AlphaMissense pathogenicity predictions against cystic fibrosis variants. PLOS ONE. 2024. PMID: 38271453.
11. Avsec Ž, Latysheva N, Cheng J, Novati G, Taylor KR, Ward T, et al. Advancing regulatory variant effect prediction with AlphaGenome. Nature. 2026;649(8099):1206–1218. doi:10.1038/s41586-025-10014-0
12. Liu M, Shen Z, Jeong YK, Yu N, Wu S-C, Wittig A, et al. AlphaGenome-enabled analysis of non-coding regulatory variants underlying RHD expression with wet-lab validation. bioRxiv. 2026;2026.01.21.700828.
13. McLaren W, Gil L, Hunt SE, Riat HS, Ritchie GRS, Thormann A, et al. The Ensembl Variant Effect Predictor. Genome Biol. 2016;17:122.
14. DeLong ER, DeLong DM, Clarke-Pearson DL. Comparing the areas under two or more correlated receiver operating characteristic curves: a nonparametric approach. Biometrics. 1988;44:837–845.
15. Sun X, Xu W. Fast implementation of DeLong's algorithm for comparing the areas under correlated receiver operating characteristic curves. IEEE Signal Process Lett. 2014;21(11):1389–1393.
16. Bergougnoux A, et al. J Cyst Fibros. 2023;22:515–524.
17. Zhang B, et al. Front Genet. 2025;16:1543623.

**Works flagged in the text as needing a citation, deliberately omitted from this list.** Landrum et al. (ClinVar); Jaganathan et al. 2019 (SpliceAI); Corvol et al. 2015 (CF modifier GWAS); the priority claim that no CFTR-specific AlphaGenome application exists. Full bibliographic details for these are not held in the project files, and none has been invented here. Reference 10 lacks volume and page numbers, and references 16 and 17 lack full author lists; PLOS requires the full DOI for every entry, so all three need completing before submission.

---

# Supporting information

**S1 Table. The concordant set.** Variants flagged by both AlphaGenome and SpliceAI among the 1,278 AlphaMissense-ambiguous CFTR missense single-nucleotide variants, under two definitions. The gene-mask definition is an AlphaGenome gene-mask splice quantile above 0.95 with a SpliceAI maximum delta above 0.5 (n = 18). The centre-mask definition is a centre-mask 501 bp splice score in the top 5% of the 1,278 with the same SpliceAI criterion (n = 13). The centre-mask set is a subset of the gene-mask set, so the union is 18. Columns give the protein change, hg38 position and alleles, CFTR domain, exon or intron, distance to the nearest splice site, AlphaMissense score, AlphaGenome splice raw and quantile scores, SpliceAI delta and the channel carrying it, gnomAD v4 maximum allele frequency, CFTR2 determination, presence in the minigene benchmark, and membership of each definition. The exon or intron and distance columns read [NOT IN REPO] in every row, because no CFTR exon annotation is held in the project files. Source table: `docs/paper/tables/Table3_concordant_set.md`; full column set: `results/paper/concordant_set.csv`.
