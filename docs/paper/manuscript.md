# AlphaMissense outperforms three missense predictors on CFTR2-labelled variants, and two splice predictors agree on eighteen of its ambiguous calls

**Short title.** AlphaMissense benchmark and a concordant splice set in CFTR

---

# Authors

Roshani Pawar, Durjya Amonkar, Monika Gostic

---

# Abstract

Most missense variants in the cystic fibrosis transmembrane conductance regulator gene have no clinical classification, so a family given an unclassified result from newborn screening or carrier testing cannot be told what it means. We benchmarked AlphaMissense against CADD, PolyPhen-2 and SIFT on CFTR2-labelled missense variants, using bootstrap confidence intervals and a paired DeLong test. We measured how far AlphaMissense scores depart from calibrated probabilities. We then scored every variant that AlphaMissense left ambiguous with two splice predictors built on different principles, AlphaGenome and SpliceAI, and tested whether they agreed beyond chance. AlphaMissense separated CF-causing from Non CF-causing variants with an area under the receiver operating characteristic curve of 0.955 (95% confidence interval 0.912 to 0.988) on 259 unique labelled variants. On the 254 variants carrying all four scores it exceeded every comparator, with paired DeLong p = 0.0004 against PolyPhen-2, p = 0.0001 against CADD and p < 0.0001 against SIFT. Its scores were not calibrated probabilities: the Brier score was 0.053 against 0.111 for a model predicting only the base rate, and every score bin above 0.4 contained more CF-causing variants than its mean score predicted. Across 1,278 AlphaMissense-ambiguous variants, a high AlphaGenome splice quantile and a raised SpliceAI delta co-occurred more often than independence predicts (odds ratio 12.36, 95% confidence interval 3.83 to 39.86, p = 9.0 × 10⁻⁸). Eighteen variants met both predictors at the higher thresholds and form a candidate list for functional testing. The benchmark carried only 33 negative variants, and the only external functional comparison available had 23 members, too few to rank splice predictors.

---

# Author Summary

When newborn screening finds a change in the CFTR gene, the laboratory often cannot say whether that change causes cystic fibrosis. Most changes in this gene have never been seen in enough patients to be classified. The family is told only that the result is uncertain.

We asked how much help prediction software can offer. We tested AlphaMissense, which predicts whether a change to a protein is harmful, against the variants that the CFTR2 patient database has already classified. It did better than three older tools. We also found that its scores should not be read as probabilities, because it is too cautious through the middle of its range.

Many variants sit in a grey zone that AlphaMissense does not resolve. For those, we asked two separate programs whether the change disrupts the way the gene is spliced. The two programs agree with each other far more often than chance would produce, and eighteen variants are flagged by both.

We are not saying those eighteen variants cause cystic fibrosis. We did no laboratory work. We produced a short list that a laboratory could test.

---

# Introduction

Cystic fibrosis is caused by loss of function in the CFTR gene [1]. The CFTR2 database assigns CFTR variants to clinical categories such as CF-causing and Non CF-causing using clinical and functional evidence [2]. Its 30 January 2026 release reports 2,092 variants drawn from 122,935 patients. Variant archives hold many more CFTR changes than CFTR2 classifies [3]. Of the 2,665 missense changes with an AlphaMissense score, 259 carry a binary CFTR2 determination. A child whose newborn screening panel returns an unclassified CFTR change receives a result that cannot guide care. The guidelines laboratories apply to such results place computational prediction among their weakest categories of evidence [4].

Protein-level predictors score the effect of an amino acid substitution on the protein. SIFT scores conservation across homologues [5], PolyPhen-2 adds sequence and structural features [6], and CADD combines many annotations into a single deleteriousness score [7]. A comparison of nine predictors scored 779 CFTR missense variants and, on the 42 with clinical annotation, found none reliable [8]. AlphaMissense scores every possible human missense substitution using an adaptation of AlphaFold that combines structural context with evolutionary conservation and is fine-tuned on population frequency data [9,10]. A CFTR-specific benchmark of AlphaMissense reported fair classification performance with a high false positive rate, and found that the score cannot separate defects in protein expression from defects in channel function, and has limited use for predicting modulator response [11].

All of these tools score the protein consequence. None can represent a variant that disrupts splicing while leaving the encoded residue tolerable. Two models address splicing from different directions. SpliceAI predicts changes in splice donor and acceptor probability from local sequence [12]. AlphaGenome predicts several regulatory modalities, splice site usage among them, from a one-megabase window at base resolution, and reports each variant effect as a quantile against a background of common variants [13]. AlphaGenome has been applied to a single gene with wet-laboratory follow-up at a blood group locus [14]. We found no published application of AlphaGenome to CFTR [CITATION NEEDED: priority claim, requires a systematic literature search].

We benchmarked AlphaMissense against CADD, PolyPhen-2 and SIFT on CFTR2-labelled missense variants, measured how far its scores depart from calibrated probabilities, and scored every AlphaMissense-ambiguous CFTR missense variant with AlphaGenome and SpliceAI. AlphaMissense separated the CFTR2 labels with an area under the receiver operating characteristic curve of 0.955 (95% confidence interval 0.912 to 0.988, n = 259) and exceeded all three comparators, and its scores proved under-confident when read as probabilities. Among the variants it left ambiguous, the two splice predictors agreed beyond chance, and 18 AlphaMissense-ambiguous variants were flagged by both AlphaGenome and SpliceAI as a candidate set for functional testing.

---

# Results

## The benchmark set and the ambiguous set are separate variant sets

The benchmark set began with the CFTR region of a ClinVar release annotated with Ensembl VEP [15], which yielded 3,220 unique protein changes across 5,923 data lines. Of these, 2,909 converted to the single-letter notation AlphaMissense uses. The 311 that did not are 309 nonsense changes and 2 stop-loss changes, which AlphaMissense does not score. Merging scores left 2,665 protein changes with an AlphaMissense score. Of those, 259 carry a binary CFTR2 determination, 226 CF-causing and 33 Non CF-causing. Five of the 259 lack at least one comparator score, leaving 254 for the four-tool comparison, 221 CF-causing and 33 Non CF-causing.

The second set came from the AlphaMissense table of CFTR missense changes, which holds 9,721 scored single-nucleotide variants covering 8,597 unique protein changes. Filtering to the ambiguous class, a score between 0.34 and 0.564, gave 1,278 variants covering 1,100 unique protein changes. The two sets are not nested. Of the 1,278, 431 appear among the 3,220 protein changes, and the rest are missense changes the ClinVar extract does not contain. Of the 1,278, 291 carry a gnomAD v4 allele frequency above zero and 952 are absent from gnomAD v4. Fig 1 shows both chains with the count at each step. Table 1 lists every data source.

<!-- sources: `results/paper/fig1_flow_counts.csv`; `results/phase1/unique_variant_counts.csv`; `results/phase1/benchmark_metrics_dedup.csv`; `results/phase1/benchmark_cohort_dedup.csv`; `docs/paper/tables/Table1_data_sources.md` -->

**Fig 1. Derivation of the two variant sets analysed.** Flow of variants through both chains. The benchmark chain begins with 3,220 unique protein changes extracted from the CFTR region of a ClinVar VCF and narrows to 2,909 convertible to AlphaMissense notation, 2,665 carrying an AlphaMissense score, 259 carrying a binary CFTR2 label (226 CF-causing, 33 Non CF-causing), and 254 carrying CADD, PolyPhen-2 and SIFT scores as well (221 and 33). The screening chain begins with the AlphaMissense CFTR table of 9,721 scored single-nucleotide variants covering 8,597 unique protein changes, narrows to the 1,278 of ambiguous AlphaMissense class covering 1,100 unique protein changes, then to 778 with an AlphaGenome ATAC or SPLICE quantile above 0.95, then to 18 that also carry a SpliceAI maximum delta above 0.5 under the gene-mask definition, of which 13 also meet the centre-mask definition. The two chains are separate variant sets and are not nested: 431 of the 1,278 appear among the 3,220. Numbers to the right of the benchmark chain are the variants removed at each step.

**Table 1. Data sources.** Version, access or extraction date and record count for every dataset used in this work. The full table is held at `docs/paper/tables/Table1_data_sources.md`.

## AlphaMissense discriminates CFTR2 labels better than three comparators

On the 254 variants carrying all four scores, AlphaMissense reached an area under the receiver operating characteristic curve (AUC) of 0.9548 (95% confidence interval 0.9121 to 0.9880) and an average precision, the area under the precision-recall curve, of 0.9923 (0.9838 to 0.9983). The three comparators reached lower values on both measures (Table 2). On the full set of 259 unique labelled variants, which includes the five without a complete comparator record, AlphaMissense reached an AUC of 0.9549 (0.9119 to 0.9878) and an average precision of 0.9924 (0.9842 to 0.9983). Fig 2 shows the four curves.

The paired DeLong test [16,17] compared each comparator against AlphaMissense on the same variants. AlphaMissense exceeded PolyPhen-2 at Z = 3.5125, p = 0.000444, CADD at Z = 3.8341, p = 0.000126, and SIFT at Z = 6.2951, p < 0.0001. The bootstrap intervals in Table 2 are wide, and the AlphaMissense interval overlaps the PolyPhen-2 interval.

<!-- sources: `results/paper/auc_ci.csv`; `results/phase1/delong_tests_dedup.csv`; `results/phase1/benchmark_metrics_dedup.csv`; `docs/paper/tables/Table2_four_tool_benchmark.md` -->

**Table 2. Four-tool benchmark on CFTR2-labelled missense variants.** Discrimination against CFTR2 binary labels on the 254 deduplicated variants carrying all four scores (221 CF-causing, 33 Non CF-causing). Confidence intervals are percentile bootstrap, 2,000 resamples, seed 42. The DeLong column compares each tool against AlphaMissense on the same variants.

| Tool | AUC (95% CI) | Average precision (95% CI) | DeLong vs AlphaMissense |
|---|---|---|---|
| AlphaMissense | 0.9548 (0.9121–0.9880) | 0.9923 (0.9838–0.9983) | reference |
| PolyPhen-2 | 0.8109 (0.7215–0.8859) | 0.9560 (0.9239–0.9816) | Z = 3.5125, p = 0.000444 |
| CADD | 0.7489 (0.6257–0.8546) | 0.9328 (0.8872–0.9704) | Z = 3.8341, p = 0.000126 |
| SIFT | 0.6701 (0.5781–0.7644) | 0.9110 (0.8725–0.9457) | Z = 6.2951, p < 0.0001 |

**Fig 2. Receiver operating characteristic curves for four predictors.** ROC curves for AlphaMissense, PolyPhen-2, CADD and SIFT against CFTR2 binary labels on the 254 deduplicated variants carrying all four scores (221 CF-causing, 33 Non CF-causing). The shaded band is the pointwise 95% percentile bootstrap interval for the AlphaMissense curve over 2,000 resamples with seed 42, interpolated onto a common false-positive-rate grid; it is pointwise rather than simultaneous and is drawn for AlphaMissense only. Legend entries give each tool's area under the curve with its 95% bootstrap confidence interval. The diagonal marks chance performance. SIFT is plotted as 1 minus the SIFT score so that higher is more damaging for every curve.

## AlphaMissense scores are not calibrated probabilities

Read as probabilities, the scores were under-confident. The Brier score, the mean squared difference between the predicted score and the observed outcome, was 0.053 across the 259 labelled variants, against 0.111 for a model that predicts the base rate of 0.873 for every variant. The expected calibration error was 0.102. The mean predicted score of 0.793 sat below the observed positive fraction of 0.873.

Every score bin above 0.4 contained more CF-causing variants than its mean score predicted. The bin from 0.4 to 0.5 held 5 variants with a mean score of 0.465, all 5 of them CF-causing, a gap of 0.535. The bin from 0.5 to 0.6 held 10 variants with a mean score of 0.563 and 9 CF-causing, a gap of 0.337. The gap narrowed as the score rose, reaching 0.039 in the top bin, which held 136 variants with a mean score of 0.961 and all 136 CF-causing. Below 0.4, two bins held no CF-causing variants at all: 13 variants between 0.1 and 0.2, and 4 variants between 0.2 and 0.3.

<!-- sources: `results/paper/calibration_n259.csv` -->

## AlphaGenome and SpliceAI agree beyond chance on the ambiguous set

Across the 1,278 AlphaMissense-ambiguous variants, 747 carried an AlphaGenome gene-mask splice quantile above 0.95 and 52 carried a SpliceAI maximum delta above 0.2. A quantile is the rank of a variant effect within a background distribution, and the gene-mask scorer takes the largest change in splice-site probability at any junction in the CFTR gene body. Forty-nine variants met both criteria, against 30.39 expected under independence. The two criteria were associated: χ²(1) = 28.57, p = 9.0 × 10⁻⁸, Fisher's exact two-sided p = 4.3 × 10⁻⁹, and an odds ratio of 12.36 (95% confidence interval 3.83 to 39.86). Three variants carried a raised SpliceAI delta without clearing the AlphaGenome threshold, and 698 cleared the AlphaGenome threshold without a raised SpliceAI delta.

Repeating the test on the genome-wide quantile recalibration moved the marginal count to 800 of 1,278 and left the association in place: χ²(1) = 23.17, p = 1.5 × 10⁻⁶, odds ratio 10.33 (3.20 to 33.33).

<!-- sources: `results/paper/ag_spliceai_2x2.csv`; `results/alphagenome/alphagenome_full_cftr_results.csv`; `results/alphagenome/quantiles_genomewide_2026-08.csv`; `results/comparator_scores.csv` -->

## Eighteen variants form a concordant candidate set

Raising the threshold on both predictors gave a small set. The gene-mask definition, a gene-mask splice quantile above 0.95 together with a SpliceAI maximum delta above 0.5, returned 18 variants. The centre-mask definition returned 13. The centre-mask scorer restricts the comparison to a 501 bp window around the variant, and that definition takes a centre-mask splice score in the top 5% of the 1,278, an empirical threshold of 0.0828 exceeded by 64 variants, together with the same SpliceAI criterion. The 13 are a subset of the 18, so the union is 18. S1 Table lists all 18 with both memberships marked. Fig 3 places them against the rest of the 1,278.

The 18 fall in three CFTR domains: 5 in MSD1, 2 in NBD1 and 11 in MSD2. Their AlphaMissense scores span 0.3415 to 0.5491. Their SpliceAI deltas span 0.55 to 1.00, carried by donor loss in 7 variants, acceptor gain in 5, donor gain in 4 and acceptor loss in 2. Thirteen are absent from gnomAD v4, and the other five have a maximum allele frequency between 6.84 × 10⁻⁷ and 4.01 × 10⁻⁴.

No member of the set carries a CF-causing or Non CF-causing determination in CFTR2. Three carry the CFTR2 status "No interpretation available": H620Q, G1047C and K1060T. The other 15 have no CFTR2 record. One member, G970V, also appears in the minigene benchmark below, where it altered splicing. The other 17 have no experimental splicing result in the files used here.

<!-- sources: `results/paper/concordant_set.csv`; `results/paper/fig1_flow_counts.csv`; `results/alphagenome/rescore_centermask.csv`; `results/alphagenome/alphagenome_full_cftr_results.csv`; `results/comparator_scores.csv`; `docs/paper/tables/Table3_concordant_set.md` -->

**Fig 3. AlphaGenome splice quantile against SpliceAI delta.** One point per variant for all 1,278 AlphaMissense-ambiguous CFTR missense single-nucleotide variants. The horizontal axis is the AlphaGenome gene-mask SPLICE quantile from the May 2026 scoring run, plotted as −log10(1 − quantile) because the values crowd against 1.0; axis labels give the untransformed quantile. The vertical axis is the SpliceAI maximum delta across the four channels, on its native scale. Dashed lines mark the two thresholds defining the concordant set, quantile 0.95 and delta 0.5. Blue circles are the 13 variants meeting both the gene-mask and centre-mask definitions; orange squares are the 5 meeting the gene-mask definition only; all 18 are labelled with their protein change. Grey points are the remaining 1,260 variants.

## Confidence intervals on the minigene benchmark are about 0.30 wide

The only external functional comparison available is a 23-row benchmark of CFTR variants tested in a minigene splicing assay, a laboratory test of how a variant affects splicing. It holds 11 splice-altering variants and 12 that did not alter splicing, compiled from two studies [18,19]. On these labels the AlphaGenome gene-mask splice quantile reached an AUC of 0.856 (95% confidence interval 0.676 to 0.985) and the gene-mask raw score 0.860 (0.683 to 0.985). The intervals are about 0.30 wide for every scorer, and a single label change moves the estimate by about 0.008. At its 0.95 threshold the AlphaGenome quantile returned 10 true positives, 8 false positives, 1 false negative and 4 true negatives, giving sensitivity 0.909 and specificity 0.333.

SpliceAI returned a delta of exactly zero for 19 of the 23 rows. Its AUC on this benchmark was 0.432 (0.269 to 0.583). At thresholds of 0.2 and 0.5 it returned 1 true positive against 10 false negatives.

<!-- sources: `results/paper/minigene_benchmark.csv` -->

---

# Discussion

AlphaMissense separated CFTR2-labelled CF-causing from Non CF-causing missense variants with an AUC of 0.955 and exceeded CADD, PolyPhen-2 and SIFT on the same variants under a paired test, and its scores were under-confident when read as probabilities. Among the 1,278 variants it left ambiguous, AlphaGenome and SpliceAI agreed about which disrupt splicing more often than independence predicts, and 18 variants met both at the higher thresholds.

Our AlphaMissense result agrees in direction with the existing CFTR-specific benchmark and differs in magnitude [11]. That study used 169 CFTR2-classified missense variants and reported fair classification with a high false positive rate. We used every variant carrying a binary CFTR2 determination, deduplicated to 259 unique protein changes, and measured discrimination by AUC and average precision. The value we obtained, 0.955, is higher than the performance that study describes, and the two analyses differ in both variant selection and the measure reported. Both support the same conclusion, that AlphaMissense carries signal about CFTR variant pathogenicity. The proteome-wide evaluation of AlphaMissense reports high discrimination across genes [9], and the CFTR-specific value here is consistent with that report. Neither our analysis nor the earlier CFTR benchmark supports using the score to identify the mechanism by which a variant acts [11]. What our analysis adds is uncertainty and calibration. The confidence intervals show how much of the margin over PolyPhen-2 survives the small negative class. A laboratory using the score as computational evidence within an interpretation framework [4] should treat the published boundary at 0.564 as a decision threshold. The score at that point is not a probability of pathogenicity.

The ranking of the older tools matches the earlier CFTR-specific comparison [8]. That work scored 779 CFTR missense variants with nine predictors and found none reliable on the 42 with clinical annotation. SIFT and PolyPhen-2 sit at the bottom of our benchmark as well (Table 2). The difference is that AlphaMissense reaches a level none of the predictors in that comparison did.

The splice agreement extends AlphaGenome's reported behaviour to a new setting. The AlphaGenome paper evaluates regulatory and splicing prediction across the genome and reports variant effects as quantiles against a common-variant background [13]. A single-locus application with base-editing follow-up at the RHD locus found that prioritised non-coding variants changed expression [14]. Neither study applied the model to CFTR, and neither paired it with an independent splice predictor. Our analysis adds that pairing. The two predictors fail in different ways, because SpliceAI reads donor and acceptor probability from local sequence [12] while AlphaGenome scores splice site usage across a megabase window [13], so a variant flagged by both is less likely to reflect one model's systematic error. The association is strong and survives the change of quantile background, with the odds ratio moving from 12.36 to 10.33 and the p-value below 10⁻⁵ in both. Their independence is only partial, because both models are trained on overlapping genomic annotation.

The 18 concordant variants are a candidate list for functional testing. One of them, G970V, was reported as splice-altering in a minigene study of CFTR exonic variants [18], which shows the list contains at least one variant with a measured splicing effect. The other 17 carry no such measurement. Nothing in this analysis establishes that any of the 18 alters splicing in a cell, and nothing establishes that any of them causes disease. The size of the set also depends on two thresholds that we chose and that were not calibrated on CFTR.

## Limitations

The benchmark contains 33 Non CF-causing variants. Every discrimination interval in Table 2 is governed by that number. The labels are curated clinical calls, because CFTR2 assigns them from clinical and functional evidence [2]. Agreement with CFTR2 is therefore agreement with an expert synthesis. It is not agreement with an independent physical measurement.

Three properties of the splice analysis constrain it. The AlphaGenome quantile ranks a variant against common variants, which are mostly non-coding, so 747 of 1,278 coding variants clear the 0.95 threshold and the marginal rate carries no information about this gene. SpliceAI cannot serve as a negative control on this variant set: its default scoring distance is 50 nucleotides either side of the variant, and CFTR coding variants lie close to exon boundaries, so a zero may mean not assessed. The external minigene benchmark has 23 members, intervals about 0.30 wide, and 19 rows where SpliceAI returns zero, so it cannot rank the scorers.

Two further gaps concern the project record. We could not place any variant in an exon or give its distance to the nearest splice site, because no CFTR exon annotation exists in the project files; both columns read [NOT IN REPO] in S1 Table. Access dates are unrecorded for the CADD query, the SpliceAI query, the gnomAD v4 lookup and the AlphaMissense download, and the SpliceAI plugin and model versions are also unrecorded; each appears as [NOT IN REPO] in Table 1. The gnomAD lookup file has no generating script in the project, so the 291 and 952 counts rest on a file that cannot be regenerated as committed.

This work is computational throughout. We performed no experiment. No variant discussed here is claimed to cause cystic fibrosis.

## What validation would test

A minigene panel covering the 17 untested members of the concordant set would test the prediction directly. It would return the number of the 17 that alter splicing, measured against the 12 variants in the existing benchmark that did not. A high count would support using concordant splice prediction to select CFTR variants for laboratory work. A count near zero would show that agreement between two sequence models does not predict a measurable splicing effect.

## The gap this work addresses

Rare CFTR variants fall outside two established approaches. Genome-wide association studies of cystic fibrosis lung disease severity identify common modifier loci [20], and a variant seen in a handful of people contributes no association signal to such a study. Protein-level predictors reach every possible missense change but score only the protein consequence, and they return an ambiguous value for 1,278 CFTR missense variants. Splice prediction addresses part of what those two approaches miss. We conclude that AlphaMissense is the best of the four protein-level tools tested against CFTR2 labels, that its scores should not be read as probabilities, and that concordant AlphaGenome and SpliceAI predictions reduce 1,278 ambiguous variants to 18 that a laboratory can test.

---

# Materials and Methods

## Variant inventory and clinical labels

Variants were taken from the CFTR region of a ClinVar release whose VCF header records `##fileDate=2026-04-15` and `##source=ClinVar`. The region chr7:117,480,000 to 117,670,000 was extracted with bcftools 1.23.1 on 21 April 2026, normalised with `bcftools norm`, and annotated with Ensembl VEP v115.1 against the GRCh38.p14 cache carrying ClinVar 202502 annotations. The file is sites-only and carries no sample columns or patient-level data. Its global allele-frequency field holds the 1000 Genomes Phase 3 frequency. That field is not a gnomAD frequency. A protein-change regular expression applied to the CSQ annotation yielded 3,220 unique protein changes from 5,923 data lines. Clinical labels came from the CFTR2 database release of 30 January 2026, which reports 2,092 variants across 122,935 patients. The download date is [NOT IN REPO]; the earliest evidence of it in the project is a file modification time of 14 May 2026.

<!-- sources: `notebooks/cftr2_scraper.ipynb`; `scripts/cftr2_scraper_analysis.py`; `data/All_Variants_VEP.Gene.vcf`; `data/cftr2_variants.xlsx`; `data/cftr2_results.csv`; `results/phase1/unique_variant_counts.csv`; `audit/COHORT_PROVENANCE.md` -->

## AlphaMissense scores

AlphaMissense precomputed pathogenicity scores for hg38 were obtained from Zenodo record 8208688 and filtered to CFTR, UniProt P13569, transcript ENST00000003084.10, giving 9,721 single-nucleotide variants covering 8,597 unique protein changes. The dataset version string and the download date are [NOT IN REPO]. Three-letter protein-change names from the VCF were converted to the single-letter form AlphaMissense uses, which succeeded for 2,909 of the 3,220 protein changes. The 311 failures are 309 nonsense changes and 2 stop-loss changes, which AlphaMissense does not score. Merging scores into the labelled table left 2,665 protein changes with an AlphaMissense score. Each variant carries the published AlphaMissense class, with the likely-pathogenic boundary at 0.564 and the likely-benign boundary at 0.34.

<!-- sources: `notebooks/alphamissense.ipynb`; `scripts/alphamissense_analysis.py`; `data/cftr_alphamissense.tsv`; `data/cftr2_results_annotated.csv`; `results/phase1/unique_variant_counts.csv`; `results/phase1/SOURCE.md` -->

## Benchmark cohort and deduplication

The benchmark cohort was every protein change carrying both an AlphaMissense score and a binary CFTR2 determination of CF-causing or Non CF-causing. Merging on protein-variant name produced 292 rows for 259 unique variants, because one protein change can map to several nucleotide changes. Duplicated rows never differ in label or score. Rows were deduplicated keep-first on the protein-variant name, leaving 259 unique variants, 226 CF-causing and 33 Non CF-causing. Deduplication preceded every metric reported here. The earlier 292-row and 286-row cohorts are superseded and were not used.

<!-- sources: `scripts/phase1_build_cohort.py`; `results/phase1/benchmark_cohort_dedup.csv`; `results/phase1/unique_variant_counts.csv`; `docs/AUDIT_RECORD.md` -->

## Comparator scores

CADD PHRED scores came from the CADD v1.7 GRCh38 REST API endpoint `GRCh38-v1.7`; the query date is [NOT IN REPO]. SIFT and PolyPhen-2 scores were parsed from fields 31 and 32 of the CSQ annotation in the VEP-annotated VCF, so they are the VEP v115.1 versions of those predictors. SIFT scores run in the opposite direction to the other three and were inverted as one minus the score, so every predictor column reads higher-is-more-damaging. Five of the 259 unique validation variants lacked at least one comparator score and were excluded from the four-tool comparison, leaving 254 variants, 221 CF-causing and 33 Non CF-causing. Leu137Pro, Thr604Ile and Trp1098Cys returned no CADD v1.7 score. Trp496Gly and Gly622Val have no CADD, SIFT or PolyPhen-2 score.

<!-- sources: `scripts/phase1_fetch_cadd.py`; `scripts/fetch_comparator_scores.py`; `results/phase1/inputs_cadd_scores.csv`; `results/phase1/inputs_polyphen_sift.csv`; `results/phase1/benchmark_cohort_dedup.csv` -->

## Discrimination and its uncertainty

For each predictor we computed the area under the receiver operating characteristic curve and the average precision against the CFTR2 binary label, using `roc_auc_score` and `average_precision_score` from scikit-learn 1.9.0 on Python 3.13.1. Both measures are threshold-independent. Confidence intervals are percentile bootstrap intervals from 2,000 resamples of the variant list with replacement, drawn with `numpy.random.default_rng(42)`. Resamples containing a single class were discarded, and none occurred on either cohort. The same resample indices were applied to all four predictors within a draw. Intervals were computed for the four predictors on the 254-variant cohort and for AlphaMissense on the 259-variant cohort.

<!-- sources: `scripts/paper/p3a_auc_ci.py`; `results/paper/auc_ci.csv`; `results/phase1/benchmark_cohort_dedup.csv` -->

## Paired comparison between predictors

Each comparator's ROC curve was compared against AlphaMissense's on the same 254 variants with the DeLong test for two correlated ROC curves [16], implemented as the fast algorithm of Sun and Xu [17]. The test is paired across the same variants. Both the paired test and the bootstrap intervals are reported.

<!-- sources: `scripts/phase1_delong.py`; `scripts/phase1_utils_delong.py`; `results/phase1/delong_tests_dedup.csv` -->

## Calibration

AlphaMissense emits a score in the unit interval that is not trained to be a calibrated probability, so calibration was measured descriptively. The 259 unique validation variants were binned into ten equal-width bins across the unit interval by AlphaMissense score. For each bin we recorded the count, the mean predicted score and the observed fraction of CF-causing variants. We also computed the Brier score with scikit-learn's `brier_score_loss`, the Brier score of a model predicting the base rate for every variant, and the expected calibration error as the sample-weighted mean absolute gap between predicted and observed values across occupied bins.

<!-- sources: `scripts/paper/p3b_calibration.py`; `results/paper/calibration_n259.csv`; `results/phase1/benchmark_cohort_dedup.csv` -->

## The AlphaMissense-ambiguous screening set

The splicing analysis used every CFTR single-nucleotide variant whose AlphaMissense class is ambiguous, meaning a score between 0.34 and 0.564. Applied to the AlphaMissense CFTR table this gave 1,278 variants covering 1,100 unique protein changes. The set was drawn from the complete table of possible CFTR missense changes. It is not a subset of the ClinVar-derived inventory: 431 of the 1,278 appear among the 3,220 protein changes of the benchmark chain. Of the 1,278, 291 carry a gnomAD v4 allele frequency above zero and 952 are absent from gnomAD v4. The gnomAD query date is [NOT IN REPO] and no committed script performs the lookup. Most members carry no clinical submission of any kind, so the set is not a set of variants of uncertain significance in the clinical sense.

<!-- sources: `data/cftr_alphamissense.tsv`; `results/alphagenome/alphagenome_full_cftr_results.csv`; `results/gnomad_cftr_lookup.csv`; `results/paper/fig1_flow_counts.csv`; `audit/COHORT_PROVENANCE.md` -->

## AlphaGenome scoring

The 1,278 variants were scored with AlphaGenome v0.6.1 on 28 May 2026 across lung tracks, producing splice-site-usage, ATAC and RNA-seq outputs as a raw score and a quantile score. Two scorers were used. The gene-mask scorer returns the largest change in splice-site probability at any junction across the CFTR gene body, so for a coding variant its value depends partly on the distance to the nearest canonical splice site. The centre-mask scorer restricts the comparison to a 501 bp window centred on the variant. Quantile scores rank a variant against AlphaGenome's common-variant background, defined in the model documentation as variants above 1% minor allele frequency in any gnomAD v3 population [21]. That background is mostly non-coding, so rare coding variants in a heavily spliced gene routinely exceed its upper percentiles. The scoring run predates AlphaGenome's move from a chromosome-22 quantile background to a genome-wide one on 18 June 2026 [22]. Every quantile-based analysis is therefore reported on the chromosome-22 calibration and repeated on the genome-wide recalibration. The day-level date of the recalibration run is [NOT IN REPO].

<!-- sources: `scripts/alphagenome_full_cftr.py`; `scripts/regenerate_quantiles_genomewide.py`; `results/alphagenome/alphagenome_full_cftr_results.csv`; `results/alphagenome/rescore_centermask.csv`; `results/alphagenome/quantiles_genomewide_2026-08.csv`; `docs/AUDIT_RECORD.md`; `audit/PROVENANCE.md` -->

## SpliceAI scoring

SpliceAI delta scores for the same 1,278 variants were retrieved through the Ensembl VEP REST endpoint `https://rest.ensembl.org/vep/human/region` with the SpliceAI plugin [12], taking the maximum of the four channels: acceptor gain, acceptor loss, donor gain and donor loss. The plugin version, the SpliceAI model version and the query date are all [NOT IN REPO]. Variants returning a delta of exactly zero were re-queried to separate a genuine zero prediction from an absent record, and 766 were examined in that pass. Two properties of the score limit its use as a negative control. Its default scoring distance is 50 nucleotides either side of the variant, and CFTR coding variants lie close to exon boundaries, so a zero can mean not assessed. The precomputed score file also does not cover all exon-interior variants.

<!-- sources: `scripts/fetch_comparator_scores.py`; `scripts/fix_spliceai_scores.py`; `scripts/reclassify_spliceai_zeros.py`; `results/comparator_scores.csv`; `results/spliceai_zero_reclassification.csv`; `docs/AUDIT_RECORD.md` -->

## Agreement between AlphaGenome and SpliceAI

Agreement between the two splice predictors across the 1,278 variants was tested on a 2x2 table of AlphaGenome gene-mask SPLICE quantile above 0.95 against SpliceAI maximum delta above 0.2. The primary test was Pearson's chi-square test of independence without continuity correction, with the Yates-corrected chi-square and Fisher's exact test reported alongside it. All three come from `scipy.stats` in SciPy 1.17.1. The odds ratio is reported with a 95% Woolf interval computed on the log scale, with a Haldane-Anscombe correction of 0.5 applied if a cell is empty. The table was built twice, once on each quantile calibration.

<!-- sources: `scripts/paper/p3e_ag_spliceai_2x2.py`; `results/paper/ag_spliceai_2x2.csv`; `results/alphagenome/alphagenome_full_cftr_results.csv`; `results/alphagenome/quantiles_genomewide_2026-08.csv`; `results/comparator_scores.csv` -->

## Definition of the concordant set

Variants flagged by both splice predictors were assembled under two definitions, and both are reported. The gene-mask definition is a gene-mask SPLICE quantile above 0.95 together with a SpliceAI maximum delta above 0.5. The centre-mask definition is a centre-mask 501 bp splice score in the top 5% of the 1,278, an empirical threshold of 0.0828 that 64 variants exceed, together with the same SpliceAI criterion. For every variant in the union we recorded the protein change, hg38 position, reference and alternate allele, CFTR domain, AlphaMissense score, AlphaGenome splice raw and quantile scores under both calibrations, the centre-mask score, the SpliceAI maximum delta and the channel carrying it, CADD PHRED, gnomAD v4 maximum allele frequency, CFTR2 determination, and presence in the minigene benchmark. Domains were assigned from residue number using the CFTR domain boundaries used elsewhere in this project. Two columns could not be filled and are recorded as [NOT IN REPO] for every row: the exon or intron a variant falls in, and its distance to the nearest splice site. The project holds no CFTR exon annotation, and no script computes either quantity for this set.

<!-- sources: `scripts/paper/p3c_concordant_set.py`; `results/paper/concordant_set.csv`; `results/alphagenome/rescore_centermask.csv`; `results/alphagenome/alphagenome_full_cftr_results.csv`; `results/comparator_scores.csv`; `results/gnomad_cftr_lookup.csv`; `data/cftr2_results_annotated.csv`; `scripts/alphamissense_analysis.py` -->

## External validation against minigene assays

The external comparison used a 23-row benchmark compiled on 2 August 2026 from two minigene studies [18,19], covering 22 unique CFTR variants, of which 11 showed altered splicing and 12 did not. Glu403Asp contributes two rows as two distinct nucleotide changes. Coordinates are GRCh38, derived from NM_000492.4 HGVS notation through the Ensembl VEP REST API. Against these labels we scored the AlphaGenome gene-mask SPLICE quantile, the AlphaGenome gene-mask raw score and the SpliceAI maximum delta. We report AUC with percentile bootstrap intervals from 2,000 resamples at seed 42, and 2x2 contingency tables at SpliceAI 0.2, SpliceAI 0.5 and AlphaGenome quantile 0.95. SpliceAI returns a delta of exactly zero for 19 of the 23 rows.

<!-- sources: `scripts/paper/p3d_minigene_benchmark.py`; `results/paper/minigene_benchmark.csv`; `results/experimental_benchmark.csv`; `docs/experimental_benchmark.md` -->

## Software, figures and reproducibility

All analyses ran on Python 3.13.1 with NumPy 2.4.6, pandas 2.3.3, scikit-learn 1.9.0, SciPy 1.17.1 and Matplotlib 3.10.9. Every random procedure used seed 42 and `numpy.random.default_rng`. Analyses written for this manuscript were new scripts under `scripts/paper/` writing to `results/paper/`; no existing script or results file was modified. Figures were produced at 300 dpi as RGB TIFF files at most 7.5 inches wide, in Arial, with no figure number, title or caption inside the image file. The categorical colours were checked for colour-vision-deficiency separation and for contrast against the figure background, and each series also carries a line style or a marker shape.

<!-- sources: `scripts/paper/figstyle.py`; `scripts/paper/p4_fig1_flow.py`; `scripts/paper/p4_fig2_roc.py`; `scripts/paper/p4_fig3_scatter.py`; `scripts/paper/p4_tables.py`; `results/paper/fig1_flow_counts.csv` -->

---

# Data Availability Statement

All analysis code is available in the project Git repository on branch `main`, under `scripts/` and `scripts/paper/`. All derived results used in this manuscript are in that repository under `results/paper/`, `results/phase1/`, `results/alphagenome/` and `results/comparator_scores.csv`. A persistent identifier for an archived snapshot is [NOT IN REPO: repository DOI not yet minted].

Four input files are not committed to the repository: `data/AlphaMissense_hg38.tsv.gz`, `data/cftr_alphamissense.tsv`, `data/All_Variants_VEP.Gene.vcf` and `data/cftr2_results_annotated.csv`. The reason each is withheld is [NOT IN REPO: licence or file-size reason not recorded]. All four are reconstructible from public sources. AlphaMissense precomputed scores for hg38 are distributed through Zenodo record 8208688, and `data/cftr_alphamissense.tsv` is that file filtered to UniProt P13569 and transcript ENST00000003084.10. `data/All_Variants_VEP.Gene.vcf` is the ClinVar public VCF release dated 2026-04-15, restricted to chr7:117,480,000 to 117,670,000 with bcftools 1.23.1, normalised, and annotated with Ensembl VEP v115.1 against the GRCh38.p14 cache. `data/cftr2_results_annotated.csv` is the CFTR2 release of 30 January 2026, downloaded from cftr2.org, merged with the AlphaMissense scores above. CADD v1.7 scores are available from the CADD GRCh38 v1.7 REST service, SpliceAI deltas from the Ensembl VEP REST SpliceAI plugin, and allele frequencies from gnomAD v4. AlphaGenome v0.6.1 is accessed through its public API, and the scores used here are committed under `results/alphagenome/`.

---

# References

1. Elborn JS. Cystic fibrosis. Lancet. 2016;388(10059):2519-2531. doi:10.1016/S0140-6736(16)00576-6
2. Sosnay PR, Siklosi KR, Van Goor F, Kaniecki K, Yu H, Sharma N, et al. Defining the disease liability of variants in the cystic fibrosis transmembrane conductance regulator gene. Nat Genet. 2013;45(10):1160-1167. doi:10.1038/ng.2745
3. Landrum MJ, Chitipiralla S, Kaur K, Brown G, Chen C, Hart J, et al. ClinVar: updates to support classifications of both germline and somatic variants. Nucleic Acids Res. 2025;53(D1):D1313-D1321. doi:10.1093/nar/gkae1090
4. Richards S, Aziz N, Bale S, Bick D, Das S, Gastier-Foster J, et al. Standards and guidelines for the interpretation of sequence variants: a joint consensus recommendation of the American College of Medical Genetics and Genomics and the Association for Molecular Pathology. Genet Med. 2015;17(5):405-424. doi:10.1038/gim.2015.30
5. Ng PC, Henikoff S. SIFT: predicting amino acid changes that affect protein function. Nucleic Acids Res. 2003;31(13):3812-3814. doi:10.1093/nar/gkg509
6. Adzhubei IA, Schmidt S, Peshkin L, Ramensky VE, Gerasimova A, Bork P, et al. A method and server for predicting damaging missense mutations. Nat Methods. 2010;7(4):248-249. doi:10.1038/nmeth0410-248
7. Kircher M, Witten DM, Jain P, O'Roak BJ, Cooper GM, Shendure J. A general framework for estimating the relative pathogenicity of human genetic variants. Nat Genet. 2014;46(3):310-315. doi:10.1038/ng.2892
8. Michels M, Matte U, Fraga LR, Mancuso ACB, Ligabue-Braun R, Berneira EFR, et al. Determining the pathogenicity of CFTR missense variants: multiple comparisons of in silico predictors and variant annotation databases. Genet Mol Biol. 2019;42(3):560-570. doi:10.1590/1678-4685-GMB-2018-0148
9. Cheng J, Novati G, Pan J, Bycroft C, Žemgulytė A, Applebaum T, et al. Accurate proteome-wide missense variant effect prediction with AlphaMissense. Science. 2023;381(6664):eadg7492. doi:10.1126/science.adg7492
10. Jumper J, Evans R, Pritzel A, Green T, Figurnov M, Ronneberger O, et al. Highly accurate protein structure prediction with AlphaFold. Nature. 2021;596(7873):583-589. doi:10.1038/s41586-021-03819-2
11. McDonald EF, Oliver KE, Schlebach JP, Meiler J, Plate L. Benchmarking AlphaMissense pathogenicity predictions against cystic fibrosis variants. PLoS One. 2024;19(1):e0297560. doi:10.1371/journal.pone.0297560
12. Jaganathan K, Kyriazopoulou Panagiotopoulou S, McRae JF, Darbandi SF, Knowles D, Li YI, et al. Predicting splicing from primary sequence with deep learning. Cell. 2019;176(3):535-548.e24. doi:10.1016/j.cell.2018.12.015
13. Avsec Ž, Latysheva N, Cheng J, Novati G, Taylor KR, Ward T, et al. Advancing regulatory variant effect prediction with AlphaGenome. Nature. 2026;649(8099):1206-1218. doi:10.1038/s41586-025-10014-0
14. Liu M, Shen Z, Jeong YK, Yu N, Wu S-C, Wittig A, et al. AlphaGenome-enabled analysis of non-coding regulatory variants underlying RHD expression with wet-lab validation. bioRxiv [Preprint]. 2026. doi:10.64898/2026.01.21.700828
15. McLaren W, Gil L, Hunt SE, Riat HS, Ritchie GRS, Thormann A, et al. The Ensembl Variant Effect Predictor. Genome Biol. 2016;17:122. doi:10.1186/s13059-016-0974-4
16. DeLong ER, DeLong DM, Clarke-Pearson DL. Comparing the areas under two or more correlated receiver operating characteristic curves: a nonparametric approach. Biometrics. 1988;44(3):837-845. doi:10.2307/2531595
17. Sun X, Xu W. Fast implementation of DeLong's algorithm for comparing the areas under correlated receiver operating characteristic curves. IEEE Signal Process Lett. 2014;21(11):1389-1393. doi:10.1109/LSP.2014.2337313
18. Bergougnoux A, Billet A, Ka C, Heller M, Degrugillier F, Vuillaume ML, et al. The multi-faceted nature of 15 CFTR exonic variations: impact on their functional classification and perspectives for therapy. J Cyst Fibros. 2023;22(3):515-524. doi:10.1016/j.jcf.2022.12.003
19. Zhang B, Zhang Y, Zhang Y, Liu X, Zhang R, Wang Z, et al. Identified five variants in CFTR gene that alter RNA splicing by minigene assay. Front Genet. 2025;16:1543623. doi:10.3389/fgene.2025.1543623
20. Corvol H, Blackman SM, Boëlle PY, Gallins PJ, Pace RG, Stonebraker JR, et al. Genome-wide association meta-analysis identifies five modifier loci of lung disease severity in cystic fibrosis. Nat Commun. 2015;6:8382. doi:10.1038/ncomms9382
21. AlphaGenome documentation. Frequently asked questions [Internet]. Google DeepMind; [cited 2026 Oct 27]. Available from: https://www.alphagenomedocs.com/faqs.html
22. AlphaGenome team. Updating variant score quantiles [Internet]. AlphaGenome Community; 2026 Jun 11 [cited 2026 Oct 27]. Available from: https://www.alphagenomecommunity.com/t/updating-variant-score-quantiles/929

---

# Supporting information

**S1 Table. The concordant set.** Variants flagged by both AlphaGenome and SpliceAI among the 1,278 AlphaMissense-ambiguous CFTR missense single-nucleotide variants, under two definitions. The gene-mask definition is an AlphaGenome gene-mask splice quantile above 0.95 with a SpliceAI maximum delta above 0.5 (n = 18). The centre-mask definition is a centre-mask 501 bp splice score in the top 5% of the 1,278 with the same SpliceAI criterion (n = 13). The centre-mask set is a subset of the gene-mask set, so the union is 18. Columns give the protein change, hg38 position and alleles, CFTR domain, exon or intron, distance to the nearest splice site, AlphaMissense score, AlphaGenome splice raw and quantile scores, SpliceAI delta and the channel carrying it, gnomAD v4 maximum allele frequency, CFTR2 determination, presence in the minigene benchmark, and membership of each definition. The exon or intron and distance columns read [NOT IN REPO] in every row, because no CFTR exon annotation is held in the project files. Source table: `docs/paper/tables/Table3_concordant_set.md`; full column set: `results/paper/concordant_set.csv`.
