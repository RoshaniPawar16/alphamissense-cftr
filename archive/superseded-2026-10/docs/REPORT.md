# AlphaMissense outperforms standard pathogenicity predictors for CFTR variant classification: a benchmarking study

**[author names omitted from working document]**

---

## Abstract

Variant classification in cystic fibrosis is constrained by the limited coverage of clinical databases. The CFTR2 database classifies 2,092 variants observed at sufficient frequency in CF patients, leaving the majority of variants submitted to ClinVar without a clinical label. This study applies AlphaMissense, a proteome-wide missense pathogenicity predictor, to 3,220 CFTR variants from a VEP-annotated ClinVar extract. AlphaMissense is first validated against 259 unique CFTR2-labelled variants, achieving AUC 0.9549 and average precision 0.9924. It is then benchmarked against CADD, PolyPhen-2, and SIFT on the 254 of those variants with all four scores. AlphaMissense outperforms all three on both ROC-AUC and precision-recall metrics. An ensemble of all predictors does not improve on AlphaMissense alone, indicating that the other tools contribute no independent signal. Applied to 2,564 unclassified variants, AlphaMissense identifies 546 unique variants (rows: 705) as likely pathogenic. Seven of these carry a 1000 Genomes Phase 3 allele-frequency entry in the VCF; this selection is retracted (AUDIT_RECORD.md:84-85). Within the 72 CFTR2 variants of varying clinical consequence, likely pathogenic calls cluster 73% in the membrane-spanning domains, consistent with the structural role of those regions in chloride conductance.

---

## 1. Introduction

Cystic fibrosis (CF) is an autosomal recessive disease caused by pathogenic variants in the *CFTR* gene, which encodes a chloride channel expressed in epithelial cells. CF affects approximately 1 in 3,500 live births in European populations and is associated with progressive lung disease, pancreatic insufficiency, and infertility [1]. Over 2,000 CFTR variants have been documented [CITATION NEEDED], but their clinical significance varies substantially. This heterogeneity makes variant classification central to patient management. CFTR modulators such as elexacaftor-tezacaftor-ivacaftor are approved only for specific variant classes, making accurate classification a prerequisite for treatment access.

### 1.1 Clinical variant databases and their limits

The CFTR2 database is the authoritative resource for CFTR variant classification [2]. In its original formulation, Sosnay et al. analysed 159 frequently occurring CFTR variants using genotype and phenotype data from 39,696 CF patients. Of those 159 variants, 127 met criteria for disease causation, 12 were classified as neutral, and 20 remained indeterminate due to insufficient evidence. The January 2026 release used in this study covers 2,092 variants across 122,935 patients. This represents significant expansion, but the fundamental constraint remains: CFTR2 only includes variants observed at sufficient frequency to characterise. Rare and novel variants, which constitute the majority of variants in ClinVar submissions for the CFTR locus, fall outside its scope by design. This is not a flaw in CFTR2. It is a property of any database that requires patient-level evidence.

The ACMG-AMP guidelines provide a framework for interpreting variants without clinical database coverage [3]. Computational evidence is one component of that framework, weighted alongside population frequency, functional assay data, and co-segregation. Computational predictors therefore do not replace clinical evidence but serve as a first-pass prioritisation signal for variants that lack it.

### 1.2 Existing computational predictors and their shortfalls

SIFT predicts the functional effect of amino acid substitutions using sequence conservation across homologous proteins [4]. A substitution at a conserved position is predicted to be deleterious. The method is simple and fast, but its accuracy depends entirely on the quality and diversity of the sequence alignment. Ng and Henikoff noted that closely related homologues increase false positive rates for neutral substitutions. SIFT has no knowledge of protein structure and cannot distinguish between positions that are conserved for structural reasons versus those conserved for catalytic ones.

PolyPhen-2 extends the conservation-based approach by incorporating structural features including solvent accessibility and whether the substitution falls in a functional domain [5]. It outperformed SIFT and other tools available at the time of publication. However, PolyPhen-2 is trained on the HumDiv and HumVar datasets, which are drawn from UniProt annotations of human disease mutations. These training labels are not equivalent to prospective clinical classifications. The tool is also restricted to missense variants where a sequence alignment can be constructed, which introduces missing data for rare variants with few homologues.

CADD integrates over 60 genomic annotations into a single deleteriousness score using a support vector machine trained on human-derived alleles versus simulated variants [6]. Kircher et al. pre-computed scores for all 8.6 billion possible human single-nucleotide variants. CADD is gene-agnostic and annotation-driven. It does not model protein structure directly and does not capture evolutionary context at the protein sequence level. Training on simulated variants rather than known pathogenic or benign variants is a methodological choice that may not reflect the biological distribution of real disease mutations.

All three tools share a common limitation: they were designed and evaluated as general-purpose tools across the full genome or proteome. Their performance on any specific gene is not guaranteed to match their reported average performance. Gene-specific benchmarking is necessary before applying them in a disease-specific context.

### 1.3 AlphaMissense

AlphaMissense adapts the AlphaFold protein structure framework [8] to pathogenicity prediction [7]. It uses a protein language model pre-trained on 703 million protein sequences from evolutionary data across the proteome, and fine-tunes it to predict whether a missense substitution is likely pathogenic. Pre-computed scores are available for 71 million variants across 19,233 human proteins. Variants are classified as likely benign (score below 0.34), ambiguous (0.34 to 0.564), or likely pathogenic (above 0.564), with thresholds calibrated against ClinVar. Cheng et al. reported AUC 0.940 on a balanced test set of 18,924 ClinVar variants across 999 proteins.

AlphaMissense has important limitations. Its training set includes ClinVar variants, which introduces a potential circularity when it is evaluated on ClinVar-derived benchmarks. Its published performance is a proteome-wide average; gene-level performance varies. A recent evaluation across neurological and neuromuscular disease genes found that AlphaMissense performed well on some genes (SCN4A, NF1) but showed low specificity on others (GRIN2A, RYR1), with an overall specificity of 41% on VUS despite sensitivity of 86% [13]. This gene-specific variability motivates disease-specific validation before clinical use. AlphaMissense also scores only missense variants. Nonsense, frameshift, and splicing variants are outside its scope, which limits its coverage of the CFTR variant spectrum.

### 1.4 This study

CFTR is an appropriate gene for evaluating AlphaMissense against an independent disease-specific database. CFTR2 is not derived from ClinVar, removing the circularity concern. CFTR has a well-characterised protein structure and a known domain architecture with distinct functional regions, enabling testable hypotheses about where pathogenic variants should cluster. The CFTR2 classification of 72 variants as varying clinical consequence provides a direct test case for whether AlphaMissense can resolve clinical uncertainty that the largest CF database cannot.

This study addresses three questions. First, how well does AlphaMissense agree with CFTR2 ground truth on an independent benchmark? Second, does it outperform SIFT, PolyPhen-2, and CADD on this gene, and are those differences statistically significant? Third, does combining predictors in an ensemble improve on AlphaMissense alone? The answers inform how computational tools should be applied when CFTR2 coverage is absent.

---

## 2. Methods

### 2.1 Variant annotation

The input was a ClinVar VCF (`##fileDate 2026-04-15`; header `##source=ClinVar`; sites-only, no sample columns) from which the CFTR region (chr7:117,480,000–117,670,000, GRCh38) was extracted on 21 April 2026 with bcftools (VCF header L79) and annotated with the Variant Effect Predictor (VEP) v115.1 cache carrying ClinVar 202502 annotations [9]. It contains 3,220 unique CFTR protein changes. VEP annotates variants with consequence type, protein change in HGVS notation, SIFT scores, PolyPhen-2 scores, and population allele frequency from 1000 Genomes Phase 3 (`AF_TGP`) where available. The VCF carries no gnomAD [10] frequencies.

Variant names were extracted from the CSQ field using the HGVS protein notation pattern `p.([A-Z][a-z]{2}\d+[A-Z][a-z]{2})`. Each matched variant was then queried against the CFTR2 January 2026 release, downloaded directly from cftr2.org as a structured spreadsheet. The spreadsheet header begins at row 11 (0-indexed). Matching was performed on protein name after adding the `p.` prefix.

### 2.2 AlphaMissense scoring

The AlphaMissense hg38 dataset was downloaded from Zenodo (record 8208688). Variants were filtered to CFTR (UniProt P13569), yielding 9,721 scored variants. VCF variant names in three-letter amino acid format (e.g. Ser13Phe) were converted to single-letter format (S13F) using a standard amino acid dictionary. 311 variants could not be converted: 309 are nonsense (Ter suffix) and 2 are stop-loss (Ter1481Tyr, Ter1481Trp), all outside AlphaMissense scope (`results/phase1/unique_variant_counts.csv`).

Scores were merged onto the annotated variant table on the converted protein name. Because several genomic variants encode the same protein change, this one-to-many merge produces duplicate rows (3,716 rows for 3,220 unique variants). 2,665 of 3,220 unique variants received an AlphaMissense score (rows: 3,161).

### 2.3 Validation

AlphaMissense scores were validated against CFTR2 binary labels. Variants with determinations of "CF-causing" or "Non CF-causing" and a valid AlphaMissense score were retained. After removing duplicate rows (keep-first by protein variant name), this produced 259 unique variants (226 CF-causing, 33 Non CF-causing; rows before deduplication: 292, 253/39). Binary labels were assigned (CF-causing = 1) and ROC-AUC and average precision (AP) were computed using scikit-learn [11]. Classification metrics were computed at the published AlphaMissense threshold of 0.564 (`results/phase1/am_validation_metrics.csv`).

### 2.4 Predictor benchmarking

CADD v1.7 scores were retrieved for each labelled variant via the CADD REST API (GRCh38 build). Genomic coordinates were extracted from the VCF. SIFT and PolyPhen-2 scores were parsed from the VEP CSQ field at indices 31 and 32 respectively. SIFT scores were inverted (1 - score) so that higher values indicate greater predicted deleteriousness, consistent with the other predictors. Of the 259 unique validation variants, five (Leu137Pro, Trp496Gly, Thr604Ile, Gly622Val, Trp1098Cys) returned no CADD v1.7 score; the remaining 254 unique variants had all four scores and were used for benchmarking (`results/phase1/benchmark_cohort_dedup.csv`, `results/phase1/benchmark_metrics_dedup.csv`). ROC-AUC and average precision were computed for each predictor.

### 2.5 Ensemble model

A logistic regression was trained on three features: AlphaMissense score, PolyPhen-2 score, and CADD score. Features were standardised using z-score normalisation prior to fitting. Stratified 5-fold cross-validation was used to obtain out-of-fold probability estimates for the 254 unique variants. Deduplication precedes fold assignment (`scripts/phase1_ensemble_dedup.py`; `results/phase1/ensemble_metrics_dedup.csv`). Performance was evaluated using the same metrics as individual predictors.

### 2.6 Variant prioritisation

Unclassified variants (no CFTR2 determination) with an AlphaMissense score of likely pathogenic were flagged. These were cross-referenced with the 1000 Genomes Phase 3 allele frequency (`AF_TGP`) in the VCF, which earlier versions of this document described as gnomAD. Flagged variants with an allele-frequency entry were further queried against ClinVar using the NCBI Entrez API.

### 2.7 Domain mapping

The 41 likely pathogenic calls within the varying clinical consequence group were mapped to CFTR protein domains using published boundaries [CITATION NEEDED]: MSD1 (residues 1-394), NBD1 (395-646), R-domain (647-835), MSD2 (836-1172), NBD2 (1173-1480). Residue position was extracted from the variant name using regex.

---

## 3. Results

### 3.1 CFTR2 annotation coverage

656 of 3,220 variants (20.4%) matched CFTR2. The remaining 2,564 had no clinical label. Among matched variants, 226 were CF-causing, 72 varying clinical consequence, 33 Non CF-causing, and 325 had no interpretation available.

### 3.2 AlphaMissense validation

| Metric | Value |
|---|---|
| Variants (unique) | 259 |
| AUC | 0.9549 |
| Average Precision | 0.9924 |
| Accuracy (threshold 0.564) | 0.927 |
| MCC (threshold 0.564) | 0.702 |
| CF-causing F1 (threshold 0.564) | 0.957 |
| Non CF-causing F1 (threshold 0.564) | 0.740 |

Source: `results/phase1/am_validation_metrics.csv`. AlphaMissense achieves AUC 0.9549 and MCC 0.702 (threshold 0.564) on 259 unique labelled CFTR variants. MCC is reported alongside AUC because it accounts for all four cells of the confusion matrix and is robust to class imbalance. A value of 0.702 indicates strong agreement with CFTR2 ground truth beyond what accuracy alone would suggest. The weaker F1 on Non CF-causing reflects the imbalance (226 CF-causing vs 33 Non CF-causing). AUC and average precision are the primary metrics for the benchmarking comparison. The calibration curve shows moderate overestimation at high scores, a known property of AlphaMissense on disease-specific subsets [CITATION NEEDED].

### 3.3 Predictor comparison

All values in this section are computed on the 254 unique variants with all four scores (221 CF-causing, 33 Non CF-causing; `results/phase1/benchmark_metrics_dedup.csv`, `results/phase1/delong_tests_dedup.csv`).

| Predictor | AUC | Average Precision |
|---|---|---|
| AlphaMissense | 0.955 | 0.992 |
| PolyPhen-2 | 0.811 | 0.956 |
| CADD | 0.749 | 0.933 |
| SIFT | 0.670 | 0.911 |

Statistical significance of AUC differences was assessed using DeLong's test [12], implemented with the covariance term (Sun and Xu 2014 algorithm; `scripts/phase1_utils_delong.py`):

| Comparison | Z | p-value | |
|---|---|---|---|
| AlphaMissense vs PolyPhen-2 | 3.51 | 0.0004 | *** |
| AlphaMissense vs CADD | 3.83 | 0.0001 | *** |
| AlphaMissense vs SIFT | 6.30 | <0.0001 | *** |

All three differences are statistically significant. AlphaMissense outperforms every baseline predictor at p < 0.001. The precision-recall curve is the more informative measure given class imbalance, as ROC-AUC is insensitive to performance on the minority class. AlphaMissense outperforms PolyPhen-2 by 14 AUC points (p = 0.0004) and 4 AP points. CADD shows jagged precision at low recall, indicating confident false positive calls at high score thresholds. SIFT, which relies on sequence conservation alone without structural context, performs weakest (p < 0.0001 vs AlphaMissense).

### 3.4 Ensemble model

Computed on the same 254 unique variants (`results/phase1/ensemble_metrics_dedup.csv`).

| Model | AUC | Average Precision |
|---|---|---|
| AlphaMissense alone | 0.955 | 0.992 |
| Ensemble (AM + CADD + PolyPhen-2) | 0.926 | 0.975 |

The ensemble performs worse than AlphaMissense alone. Logistic regression feature weights after standardisation are: AlphaMissense +2.113, CADD +0.008, PolyPhen-2 -0.049. The model assigns near-zero weight to CADD and a negative weight to PolyPhen-2, indicating that these predictors do not contribute independent information. AlphaMissense already subsumes the signal available from the other tools on this gene.

### 3.5 Unclassified variant prioritisation

Of 2,564 unclassified variants, 2,009 unique variants received AlphaMissense scores (rows: 2,411). 546 were classified as likely pathogenic (rows: 705), 277 as ambiguous (rows: 357), and 1,186 as likely benign (rows: 1,349) (`results/phase1/unique_variant_counts.csv`).

Of the 546 flagged variants, 7 had a 1000 Genomes Phase 3 allele-frequency entry (`AF_TGP`) in the VCF. All seven are singletons or doubletons in 2,504 individuals (AUDIT_RECORD.md:85).

| Variant | AM score | Population AF | ClinVar status |
|---|---|---|---|
| Leu49Pro | 0.976 | 0.0002 | Uncertain significance |
| His1054Gln | 0.901 | 0.0002 | Uncertain significance |
| Leu986Pro | 0.869 | 0.0004 | Conflicting classifications |
| Pro355Leu | 0.858 | 0.0002 | Uncertain significance |
| Phe650Leu | 0.846 | 0.0002 | Uncertain significance |
| Arg104Gly | 0.845 | 0.0002 | Uncertain significance |
| Arg1097Cys | 0.651 | 0.0002 | Conflicting classifications |

All 7 are unresolved in ClinVar. 5 carry an uncertain significance classification. 2 (Leu986Pro, Arg1097Cys) have conflicting classifications from different submitting laboratories. AlphaMissense calls all 7 likely pathogenic. The selection of these seven is retracted: it was made on 1000 Genomes Phase 3 allele frequency under the mistaken assumption that the field was gnomAD, and the selection has no basis in the data as originally described (AUDIT_RECORD.md:84-85). The table is retained for traceability only.

### 3.6 Varying clinical consequence

72 CFTR2 variants are classified as varying clinical consequence, indicating insufficient data for a definitive determination. AlphaMissense scored all 72.

| AlphaMissense class | Count |
|---|---|
| likely_pathogenic | 41 |
| ambiguous | 19 |
| likely_benign | 12 |

41 of 72 are called likely pathogenic. As a positive control, Arg117His scores 0.299 (likely benign), consistent with its established association with mild phenotype and congenital bilateral absence of the vas deferens rather than classic CF [CITATION NEEDED].

The 41 likely pathogenic variants show non-uniform domain distribution:

| Domain | Variants | Proportion |
|---|---|---|
| MSD1 | 13 | 32% |
| NBD1 | 6 | 15% |
| R-domain | 0 | 0% |
| MSD2 | 17 | 41% |
| NBD2 | 5 | 12% |

73% cluster in the membrane-spanning domains (MSD1 and MSD2), which form the chloride channel pore. The R-domain has zero likely pathogenic calls. The R-domain is intrinsically disordered and does not contribute directly to channel gating or ion conductance. This distribution is consistent with the structural role of each domain and provides biological coherence to the computational calls.

### 3.7 Nonsense variants

311 variants could not be converted to single-letter amino acid format and were excluded from AlphaMissense matching. 309 are nonsense mutations (Ter suffix) and 2 are stop-loss (Ter1481Tyr, Ter1481Trp). Of these, 222 unique variants matched CFTR2 (rows: 232): 215 as CF-causing (rows: 225), 2 as varying clinical consequence, and 5 as no interpretation available (`results/phase1/unique_variant_counts.csv`). The 215 CF-causing nonsense variants are consistent with the established mechanism whereby premature stop codons produce truncated, non-functional protein.

Two exceptions -- Ser1455Ter and Gln1476Ter -- are classified as varying clinical consequence. Both truncate near the C-terminus of the 1,480 amino acid protein [CITATION NEEDED], removing only 25 and 4 residues respectively. Minimal truncation of the C-terminal tail may be tolerated, explaining the clinical uncertainty.

---

## 4. Discussion

AlphaMissense achieves AUC 0.9549 on CFTR variants, demonstrating strong agreement with CFTR2 ground truth despite having no access to CF patient data during training. This validates its use as an independent signal for unclassified variants on this gene.

Cheng et al. reported AUC 0.940 for AlphaMissense on a balanced set of 18,924 ClinVar variants across 999 proteins [7]. The AUC of 0.9549 obtained here on CFTR-specific variants is consistent with that proteome-wide estimate and slightly exceeds it. This is notable for two reasons. First, the ClinVar benchmark used balanced classes, which is more favourable to AUC than our imbalanced set (226 CF-causing vs 33 Non CF-causing). The fact that we match or exceed their result under a harder evaluation condition suggests AlphaMissense performs at least as well on CFTR as on the average protein in its training distribution. Second, proteome-wide AUC estimates mask gene-level variation. A tool that achieves 0.940 on average may perform substantially worse on specific genes with unusual evolutionary profiles or structural properties. Gene-specific validation, as performed here, is therefore a necessary step before applying AlphaMissense in a disease-specific clinical context.

The performance gap between AlphaMissense and established tools is substantial. PolyPhen-2, the second-best predictor, scores 14 AUC points lower. CADD and SIFT trail further. This gap is likely explained by the depth of representation in AlphaMissense. PolyPhen-2 and SIFT use sequence conservation and limited structural features. CADD integrates genomic annotations but does not model protein structure directly. AlphaMissense draws on a protein language model pre-trained on 703 million protein sequences, capturing evolutionary and structural context at a resolution the other tools do not reach [7]. On a gene with a well-characterised 3D structure and a defined functional architecture, this advantage is expected.

The ensemble result is informative. A logistic regression trained on AlphaMissense, CADD, and PolyPhen-2 performs worse than AlphaMissense alone. The feature weights confirm this: CADD and PolyPhen-2 are assigned near-zero or negative weight. This indicates that the information in these tools is already captured by AlphaMissense, and combining them introduces variance without adding signal. The practical implication is that AlphaMissense alone is the appropriate tool for CFTR missense variant prioritisation.

The seven variants listed in section 3.5 are not presented as follow-up candidates. Their selection rested on a 1000 Genomes Phase 3 allele-frequency field that was mistaken for gnomAD; all seven are singletons or doubletons in 2,504 individuals, and the selection is retracted (AUDIT_RECORD.md:84-85).

The domain distribution of likely pathogenic calls within the varying clinical consequence group adds biological support to the computational findings. 73% cluster in the membrane-spanning domains. These regions line the chloride channel pore and are directly involved in ion conductance. Missense variants in these domains are likely to disrupt channel function through structural perturbation. The R-domain, which is intrinsically disordered and functions primarily as a regulatory gating domain, tolerates missense variation more readily. This pattern matches established structure-function relationships in CFTR.

Several limitations apply. The validation set is imbalanced (226 CF-causing, 33 Non CF-causing unique variants), which inflates accuracy and limits the reliability of Non CF-causing F1 as an evaluation metric. The comparator benchmark, DeLong tests and ensemble use the 254 unique variants with all four scores; the ensemble cross-validation estimate at this sample size carries high variance. AlphaMissense does not model nonsense, frameshift, or splicing variants, which account for a substantial fraction of pathogenic CFTR alleles including many common ones. Population frequency data was available for only 117 of 3,220 variants, reflecting the rarity of most variants in the cohort. The ensemble cross-validation estimate, based on 286 samples, carries high variance. Findings should be replicated in a larger independent cohort before clinical application.

---

## 5. Conclusion

AlphaMissense is a credible tool for prioritising unclassified CFTR missense variants. It outperforms CADD, PolyPhen-2, and SIFT on a disease-specific benchmark, and the ensemble analysis confirms it subsumes the information available from the other tools. The seven-variant priority set reported in earlier versions is retracted (AUDIT_RECORD.md:84-85). The domain clustering of likely pathogenic calls in the membrane-spanning domains is consistent with CFTR structure and function.

---

## References

[1] Elborn, J.S. Cystic fibrosis. *Lancet* 388, 2519-2531 (2016).

[2] Sosnay, P.R. et al. Defining the disease liability of variants in the cystic fibrosis transmembrane conductance regulator gene. *Nat Genet* 45, 1160-1167 (2013).

[3] Richards, S. et al. Standards and guidelines for the interpretation of sequence variants: a joint consensus recommendation of the American College of Medical Genetics and Genomics and the Association for Molecular Pathology. *Genet Med* 17, 405-424 (2015).

[4] Ng, P.C. and Henikoff, S. SIFT: predicting amino acid changes that affect protein function. *Nucleic Acids Res* 31, 3812-3814 (2003).

[5] Adzhubei, I.A. et al. A method and server for predicting damaging missense mutations. *Nat Methods* 7, 248-249 (2010).

[6] Kircher, M. et al. A general framework for estimating the relative pathogenicity of human genetic variants. *Nat Genet* 46, 310-315 (2014).

[7] Cheng, J. et al. Accurate proteome-wide missense variant effect prediction with AlphaMissense. *Science* 381, eadg7492 (2023).

[8] Jumper, J. et al. Highly accurate protein structure prediction with AlphaFold. *Nature* 596, 583-589 (2021).

[9] McLaren, W. et al. The Ensembl Variant Effect Predictor. *Genome Biol* 17, 122 (2016).

[10] Karczewski, K.J. et al. The mutational constraint spectrum quantified from variation in 141,456 humans. *Nature* 581, 434-443 (2020).

[11] Pedregosa, F. et al. Scikit-learn: machine learning in Python. *J Mach Learn Res* 12, 2825-2830 (2011).

[12] DeLong, E.R., DeLong, D.M. and Clarke-Pearson, D.L. Comparing the areas under two or more correlated receiver operating characteristic curves: a nonparametric approach. *Biometrics* 44, 837-845 (1988).

[13] Kopanos, C. et al. Comprehensive evaluation of AlphaMissense predictions by evidence quantification for variants of uncertain significance. *Front Genet* 15, 1487608 (2024).
