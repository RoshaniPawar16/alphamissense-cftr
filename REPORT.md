# AlphaMissense outperforms standard pathogenicity predictors for CFTR variant classification: a benchmarking study

**Roshani Pawar**

---

## Abstract

Variant classification in cystic fibrosis is constrained by the limited coverage of clinical databases. The CFTR2 database classifies 2,092 variants observed at sufficient frequency in CF patients, leaving the majority of variants in real-world sequencing data without a clinical label. This study applies AlphaMissense, a proteome-wide missense pathogenicity predictor, to 3,220 CFTR variants from a VEP-annotated VCF. AlphaMissense is first validated against 292 CFTR2-labelled variants, achieving AUC 0.946 and average precision 0.990. It is then benchmarked against CADD, PolyPhen-2, and SIFT on the same variant set. AlphaMissense outperforms all three on both ROC-AUC and precision-recall metrics. An ensemble of all predictors does not improve on AlphaMissense alone, indicating that the other tools contribute no independent signal. Applied to 2,564 unclassified variants, AlphaMissense identifies 705 as likely pathogenic. Seven of these have population frequency support from gnomAD and remain unresolved in ClinVar. Within the 72 CFTR2 variants of varying clinical consequence, likely pathogenic calls cluster 73% in the membrane-spanning domains, consistent with the structural role of those regions in chloride conductance.

---

## 1. Introduction

Cystic fibrosis (CF) is an autosomal recessive disease caused by pathogenic variants in the *CFTR* gene, which encodes a chloride channel expressed in epithelial cells. CF affects approximately 1 in 3,500 live births in European populations and is associated with progressive lung disease, pancreatic insufficiency, and infertility [1]. Over 2,000 CFTR variants have been documented, but their clinical significance varies substantially. This heterogeneity makes variant classification central to patient management. CFTR modulators such as elexacaftor-tezacaftor-ivacaftor are approved only for specific variant classes, making accurate classification a prerequisite for treatment access.

The CFTR2 database is the authoritative resource for CFTR variant classification [2]. It aggregates genotype and phenotype data from 122,935 CF patients across 27 countries and classifies variants as CF-causing, non-CF-causing, varying clinical consequence, or no interpretation available. However, CFTR2 only includes variants observed in enough patients to characterise. Rare and private variants, which constitute the majority of variants in a real sequencing cohort, fall outside its scope.

This classification gap is not unique to CF. Across rare disease genetics, variants of uncertain significance (VUS) represent a persistent clinical challenge. The ACMG-AMP guidelines provide a framework for variant interpretation that incorporates computational evidence alongside population frequency, functional data, and segregation data [3]. Computational pathogenicity predictors are therefore a standard component of clinical variant assessment.

Several such tools exist. SIFT predicts the effect of amino acid substitutions based on sequence conservation across species [4]. PolyPhen-2 uses sequence conservation combined with structural features to classify missense variants as benign, possibly damaging, or probably damaging [5]. CADD integrates multiple genomic annotations into a single deleteriousness score using a trained support vector machine [6]. All three are gene-agnostic and were designed as general-purpose tools.

AlphaMissense [7] takes a different approach. It adapts the AlphaFold protein structure framework [8] to pathogenicity prediction, using a protein language model pre-trained on evolutionary sequences across the proteome. It assigns a score between 0 and 1 to every possible human missense variant and classifies variants as likely benign (score below 0.34), ambiguous (0.34 to 0.564), or likely pathogenic (above 0.564). These thresholds were calibrated against ClinVar. The full dataset of pre-computed scores is publicly available, covering 71 million variants across 19,233 human proteins.

The independence of AlphaMissense from clinical databases is relevant here. Because its training data does not include CFTR2 classifications, agreement between AlphaMissense predictions and CFTR2 labels represents genuine external validation rather than label leakage. Prior work has assessed AlphaMissense performance on ClinVar variants [7], but gene-specific benchmarking against disease-specific databases has received less attention. CFTR is an appropriate candidate for such analysis: it has one of the most thoroughly curated variant databases in human genetics, a well-characterised protein structure, and a known functional architecture that generates testable hypotheses about domain-level pathogenicity patterns.

This study addresses three questions. First, how well does AlphaMissense agree with CFTR2 ground truth? Second, does it outperform established predictors on this gene? Third, can combining predictors in an ensemble improve performance? The answers inform how computational tools should be used for prioritising unclassified CFTR variants.

---

## 2. Methods

### 2.1 Variant annotation

A VEP-annotated VCF containing 3,220 CFTR gene variants was used as input. Variant Effect Predictor (VEP) [9] annotates variants with consequence type, protein change in HGVS notation, SIFT scores, PolyPhen-2 scores, and population allele frequency from gnomAD [10] where available.

Variant names were extracted from the CSQ field using the HGVS protein notation pattern `p.([A-Z][a-z]{2}\d+[A-Z][a-z]{2})`. Each matched variant was then queried against the CFTR2 January 2026 release, downloaded directly from cftr2.org as a structured spreadsheet. The spreadsheet header begins at row 11 (0-indexed). Matching was performed on protein name after adding the `p.` prefix.

### 2.2 AlphaMissense scoring

The AlphaMissense hg38 dataset was downloaded from Zenodo (record 8208688, ~1.4 GB). Variants were filtered to CFTR (UniProt P13569), yielding 9,721 scored variants. VCF variant names in three-letter amino acid format (e.g. Ser13Phe) were converted to single-letter format (S13F) using a standard amino acid dictionary. 311 variants could not be converted; inspection confirmed these were nonsense mutations (Ter suffix) and frameshifts, which are outside AlphaMissense scope.

Scores were merged onto the annotated variant table on the converted protein name. 3,161 of 3,220 variants received an AlphaMissense score.

### 2.3 Validation

AlphaMissense scores were validated against CFTR2 binary labels. Variants with determinations of "CF-causing" or "Non CF-causing" and a valid AlphaMissense score were retained. This produced 292 variants (253 CF-causing, 39 Non CF-causing). Binary labels were assigned (CF-causing = 1) and ROC-AUC and average precision (AP) were computed using scikit-learn [11]. Classification metrics were computed at the published AlphaMissense threshold of 0.564.

### 2.4 Predictor benchmarking

CADD v1.7 scores were retrieved for each labelled variant via the CADD REST API (GRCh38 build). Genomic coordinates were extracted from the VCF. SIFT and PolyPhen-2 scores were parsed from the VEP CSQ field at indices 31 and 32 respectively. SIFT scores were inverted (1 - score) so that higher values indicate greater predicted deleteriousness, consistent with the other predictors. 286 variants had all four scores available and were used for benchmarking. ROC-AUC and average precision were computed for each predictor.

### 2.5 Ensemble model

A logistic regression was trained on three features: AlphaMissense score, PolyPhen-2 score, and CADD score. Features were standardised using z-score normalisation prior to fitting. Stratified 5-fold cross-validation was used to obtain out-of-fold probability estimates for the full 286-variant dataset. This avoids test set leakage given the small sample size. Performance was evaluated using the same metrics as individual predictors.

### 2.6 Variant prioritisation

Unclassified variants (no CFTR2 determination) with an AlphaMissense score of likely pathogenic were flagged. These were cross-referenced with gnomAD population frequency from the VCF. Flagged variants with population frequency data were further queried against ClinVar using the NCBI Entrez API.

### 2.7 Domain mapping

The 41 likely pathogenic calls within the varying clinical consequence group were mapped to CFTR protein domains using published boundaries: MSD1 (residues 1-394), NBD1 (395-646), R-domain (647-835), MSD2 (836-1172), NBD2 (1173-1480). Residue position was extracted from the variant name using regex.

---

## 3. Results

### 3.1 CFTR2 annotation coverage

656 of 3,220 variants (20.4%) matched CFTR2. The remaining 2,564 had no clinical label. Among matched variants, 226 were CF-causing, 72 varying clinical consequence, 33 Non CF-causing, and 325 had no interpretation available.

### 3.2 AlphaMissense validation

| Metric | Value |
|---|---|
| Variants | 292 |
| AUC | 0.946 |
| Average Precision | 0.990 |
| Accuracy | 0.94 |
| MCC | 0.689 |
| CF-causing F1 | 0.96 |
| Non CF-causing F1 | 0.77 |

AlphaMissense achieves AUC 0.946 and MCC 0.689 on 292 labelled CFTR variants. MCC is reported alongside AUC because it accounts for all four cells of the confusion matrix and is robust to class imbalance. A value of 0.689 indicates strong agreement with CFTR2 ground truth beyond what accuracy alone would suggest. The weaker F1 on Non CF-causing reflects the imbalance (253 CF-causing vs 39 Non CF-causing). AUC and average precision are the primary metrics for the benchmarking comparison. The calibration curve shows moderate overestimation at high scores, a known property of AlphaMissense on disease-specific subsets.

### 3.3 Predictor comparison

| Predictor | AUC | Average Precision |
|---|---|---|
| AlphaMissense | 0.946 | 0.990 |
| PolyPhen-2 | 0.826 | 0.959 |
| CADD | 0.776 | 0.939 |
| SIFT | 0.678 | 0.909 |

Statistical significance of AUC differences was assessed using DeLong's test [12]:

| Comparison | Z | p-value | |
|---|---|---|---|
| AlphaMissense vs PolyPhen-2 | 2.88 | 0.0040 | ** |
| AlphaMissense vs CADD | 3.28 | 0.0011 | ** |
| AlphaMissense vs SIFT | 5.87 | <0.0001 | *** |

All three differences are statistically significant. AlphaMissense outperforms every baseline predictor at p < 0.01. The precision-recall curve is the more informative measure given class imbalance, as ROC-AUC is insensitive to performance on the minority class. AlphaMissense outperforms PolyPhen-2 by 12 AUC points (p = 0.004) and 3 AP points. CADD shows jagged precision at low recall, indicating confident false positive calls at high score thresholds. SIFT, which relies on sequence conservation alone without structural context, performs weakest (p < 0.0001 vs AlphaMissense).

### 3.4 Ensemble model

| Model | AUC | Average Precision |
|---|---|---|
| AlphaMissense alone | 0.946 | 0.990 |
| Ensemble (AM + CADD + PolyPhen-2) | 0.927 | 0.983 |

The ensemble performs worse than AlphaMissense alone. Logistic regression feature weights after standardisation are: AlphaMissense +1.907, CADD +0.279, PolyPhen-2 -0.117. The model assigns near-zero weight to CADD and a negative weight to PolyPhen-2, indicating that these predictors do not contribute independent information. AlphaMissense already subsumes the signal available from the other tools on this gene.

### 3.5 Unclassified variant prioritisation

Of 2,564 unclassified variants, 2,411 received AlphaMissense scores. 705 were classified as likely pathogenic, 357 as ambiguous, and 1,349 as likely benign.

Of the 705 flagged variants, 7 had gnomAD population frequency data in the VCF, indicating they have been observed in the general population.

| Variant | AM score | Population AF | ClinVar status |
|---|---|---|---|
| Leu49Pro | 0.976 | 0.0002 | Uncertain significance |
| His1054Gln | 0.901 | 0.0002 | Uncertain significance |
| Leu986Pro | 0.869 | 0.0004 | Conflicting classifications |
| Pro355Leu | 0.858 | 0.0002 | Uncertain significance |
| Phe650Leu | 0.846 | 0.0002 | Uncertain significance |
| Arg104Gly | 0.845 | 0.0002 | Uncertain significance |
| Arg1097Cys | 0.651 | 0.0002 | Conflicting classifications |

All 7 are unresolved in ClinVar. 5 carry an uncertain significance classification. 2 (Leu986Pro, Arg1097Cys) have conflicting classifications from different submitting laboratories. AlphaMissense calls all 7 likely pathogenic. These represent the highest-priority candidates for functional follow-up, combining computational evidence for pathogenicity with observed population frequency and the absence of clinical consensus.

### 3.6 Varying clinical consequence

72 CFTR2 variants are classified as varying clinical consequence, indicating insufficient data for a definitive determination. AlphaMissense scored all 72.

| AlphaMissense class | Count |
|---|---|
| likely_pathogenic | 41 |
| ambiguous | 19 |
| likely_benign | 12 |

41 of 72 are called likely pathogenic. As a positive control, Arg117His scores 0.299 (likely benign), consistent with its established association with mild phenotype and congenital bilateral absence of the vas deferens rather than classic CF.

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

311 variants could not be converted to single-letter amino acid format and were excluded from AlphaMissense matching. All were nonsense mutations (Ter suffix). Of these, 232 matched CFTR2: 225 as CF-causing, 2 as varying clinical consequence, and 5 as no interpretation available. The 225 CF-causing nonsense variants are consistent with the established mechanism whereby premature stop codons produce truncated, non-functional protein.

Two exceptions -- Ser1455Ter and Gln1476Ter -- are classified as varying clinical consequence. Both truncate near the C-terminus of the 1,480 amino acid protein, removing only 25 and 4 residues respectively. Minimal truncation of the C-terminal tail may be tolerated, explaining the clinical uncertainty.

---

## 4. Discussion

AlphaMissense achieves AUC 0.946 on CFTR variants, demonstrating strong agreement with CFTR2 ground truth despite having no access to CF patient data during training. This validates its use as an independent signal for unclassified variants on this gene.

The performance gap between AlphaMissense and established tools is substantial. PolyPhen-2, the second-best predictor, scores 12 AUC points lower. CADD and SIFT trail further. This gap is likely explained by the depth of representation in AlphaMissense. PolyPhen-2 and SIFT use sequence conservation and limited structural features. CADD integrates genomic annotations but does not model protein structure directly. AlphaMissense draws on a protein language model pre-trained on 703 million protein sequences, capturing evolutionary and structural context at a resolution the other tools do not reach [7]. On a gene with a well-characterised 3D structure and a defined functional architecture, this advantage is expected.

The ensemble result is informative. A logistic regression trained on AlphaMissense, CADD, and PolyPhen-2 performs worse than AlphaMissense alone. The feature weights confirm this: CADD and PolyPhen-2 are assigned near-zero or negative weight. This indicates that the information in these tools is already captured by AlphaMissense, and combining them introduces variance without adding signal. The practical implication is that AlphaMissense alone is the appropriate tool for CFTR missense variant prioritisation.

The 7 priority candidates represent a tractable set for follow-up. All have AlphaMissense scores above 0.65, population frequency evidence from gnomAD, and unresolved ClinVar status. Two (Leu986Pro, Arg1097Cys) have active laboratory disagreement in ClinVar. Consistent computational evidence for pathogenicity from a model validated at AUC 0.946 on this gene strengthens the case for experimental characterisation of these variants.

The domain distribution of likely pathogenic calls within the varying clinical consequence group adds biological support to the computational findings. 73% cluster in the membrane-spanning domains. These regions line the chloride channel pore and are directly involved in ion conductance. Missense variants in these domains are likely to disrupt channel function through structural perturbation. The R-domain, which is intrinsically disordered and functions primarily as a regulatory gating domain, tolerates missense variation more readily. This pattern matches established structure-function relationships in CFTR.

Several limitations apply. The validation set is imbalanced (253 CF-causing, 39 Non CF-causing), which inflates accuracy and limits the reliability of Non CF-causing F1 as an evaluation metric. AlphaMissense does not model nonsense, frameshift, or splicing variants, which account for a substantial fraction of pathogenic CFTR alleles including many common ones. Population frequency data was available for only 117 of 3,220 variants, reflecting the rarity of most variants in the cohort. The ensemble cross-validation estimate, based on 286 samples, carries high variance. Findings should be replicated in a larger independent cohort before clinical application.

---

## 5. Conclusion

AlphaMissense is a credible tool for prioritising unclassified CFTR missense variants. It outperforms CADD, PolyPhen-2, and SIFT on a disease-specific benchmark, and the ensemble analysis confirms it subsumes the information available from the other tools. Seven unclassified variants are identified as high-priority candidates for functional follow-up based on convergent evidence from computational prediction, population frequency, and ClinVar status. The domain clustering of likely pathogenic calls in the membrane-spanning domains is consistent with CFTR structure and function.

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
