# CFTR Variant Pathogenicity Analysis

**Roshani Pawar**

---

## Problem

A VEP-annotated VCF contained 3,220 CFTR gene variants. The goal was to obtain clinical classifications from CFTR2, the authoritative database for cystic fibrosis variant pathogenicity, built from data across 122,935 patients.

656 variants matched CFTR2. The remaining 2,564 had no clinical label.

This is not a data quality issue. CFTR2 only includes variants seen in enough patients to characterise. Most variants in a real patient VCF are rare -- too rare to have been studied at scale in a CF cohort. The classification problem is: for each variant, does it cause cystic fibrosis or not?

---

## Method

**Step 1 -- Automated CFTR2 annotation**

A scraper extracted variant names from the VCF using HGVS protein notation and matched them against the CFTR2 database. 656 of 3,220 variants matched. This became the labelled dataset.

**Step 2 -- AlphaMissense as an independent signal**

AlphaMissense (Google DeepMind, 2023) assigns a pathogenicity score between 0 and 1 to every possible human missense variant. It was trained on protein structure and evolutionary data with no knowledge of CFTR2. That independence matters for validation.

The AlphaMissense hg38 dataset was filtered to CFTR variants (UniProt P13569), yielding 9,721 scored variants. VCF variant names were converted from three-letter amino acid format (Ser13Phe) to single-letter format (S13F) to match the AlphaMissense convention. 311 variants could not be converted -- these were nonsense and frameshift mutations outside AlphaMissense scope.

**Step 3 -- Validation**

AlphaMissense scores were validated against the 292 CFTR2-labelled variants that had both a binary classification (CF-causing or Non CF-causing) and an AlphaMissense score.

**Step 4 -- Benchmarking**

AlphaMissense was benchmarked against three standard predictors on the same 286 variants:
- CADD (Combined Annotation Dependent Depletion) via REST API
- PolyPhen-2 scores from the VCF CSQ field
- SIFT scores from the VCF CSQ field

**Step 5 -- Ensemble**

A logistic regression was trained on AlphaMissense + CADD + PolyPhen using stratified 5-fold cross-validation. The question: does combining predictors outperform AlphaMissense alone?

---

## Results

### Validation

| Metric | Value |
|---|---|
| Variants | 292 |
| AUC | 0.946 |
| Accuracy | 0.94 |
| CF-causing F1 | 0.96 |
| Non CF-causing F1 | 0.77 |

AlphaMissense agrees with CFTR2 ground truth at AUC 0.946. The weaker F1 on Non CF-causing reflects class imbalance -- 253 CF-causing vs 39 Non CF-causing. AUC is the more reliable metric here.

### Predictor comparison

| Predictor | AUC | Average Precision |
|---|---|---|
| AlphaMissense | 0.946 | 0.990 |
| PolyPhen | 0.826 | 0.959 |
| CADD | 0.776 | 0.939 |
| SIFT | 0.678 | 0.909 |

AlphaMissense leads on both metrics. The precision-recall curve is the more honest measure given the class imbalance -- ROC overstates performance in that setting. AlphaMissense outperforms the next best predictor (PolyPhen) by 12 AUC points and 3 AP points.

CADD's PR curve is jagged at low recall -- it makes confident wrong calls at high score thresholds. AlphaMissense maintains clean precision across the full recall range.

### Ensemble

| Model | AUC | Average Precision |
|---|---|---|
| AlphaMissense alone | 0.946 | 0.990 |
| Ensemble (AM + CADD + PolyPhen) | 0.927 | 0.983 |

The ensemble is worse. Feature weights after scaling: AlphaMissense +1.907, CADD +0.279, PolyPhen -0.117. The logistic regression learns to rely almost entirely on AlphaMissense and discount the others. This confirms that AlphaMissense already captures the information CADD and PolyPhen provide. Adding them introduces noise.

### Priority candidates

705 unclassified variants were flagged as likely pathogenic by AlphaMissense. Of those, 7 had gnomAD population frequency data in the VCF -- meaning they have been observed in the general population.

| Variant | AM score | Population AF | ClinVar |
|---|---|---|---|
| Leu49Pro | 0.976 | 0.0002 | Uncertain significance |
| His1054Gln | 0.901 | 0.0002 | Uncertain significance |
| Leu986Pro | 0.869 | 0.0004 | Conflicting classifications |
| Pro355Leu | 0.858 | 0.0002 | Uncertain significance |
| Phe650Leu | 0.846 | 0.0002 | Uncertain significance |
| Arg104Gly | 0.845 | 0.0002 | Uncertain significance |
| Arg1097Cys | 0.651 | 0.0002 | Conflicting classifications |

All 7 are unresolved in ClinVar. 5 are uncertain significance. 2 have conflicting classifications from different labs. AlphaMissense calls all 7 likely pathogenic. These are the strongest candidates for functional follow-up.

### Varying clinical consequence

72 variants in CFTR2 are classified as varying clinical consequence -- CFTR2 itself is uncertain about them. AlphaMissense scored all 72.

| AlphaMissense class | Count |
|---|---|
| likely_pathogenic | 41 |
| ambiguous | 19 |
| likely_benign | 12 |

41 of 72 are called likely pathogenic. The domain distribution is not random: 73% of the likely pathogenic calls fall in the membrane-spanning domains (MSD1 and MSD2), which form the chloride channel pore. The regulatory domain has zero -- it is intrinsically disordered and more tolerant of missense variation.

| Domain | Variants |
|---|---|
| MSD1 | 13 |
| NBD1 | 6 |
| R-domain | 0 |
| MSD2 | 17 |
| NBD2 | 5 |

Arg117His, a well-known mild variant associated with CBAVD rather than classic CF, scores 0.299 (likely benign). This matches clinical knowledge and validates the model's sensitivity to functional context.

### Nonsense variants

311 variants were nonsense mutations and outside AlphaMissense scope. Of those, 225 matched CFTR2 as CF-causing -- consistent with the expectation that premature stop codons truncate the protein and cause disease.

Two exceptions: Ser1455Ter and Gln1476Ter, which truncate only the last 25 and 4 residues of a 1,480 amino acid protein. Their classification as varying clinical consequence is biologically justified.

---

## Conclusion

AlphaMissense is a credible tool for prioritising unclassified CFTR variants. On a gene with a well-curated clinical database, it agrees with ground truth at AUC 0.946 and outperforms all three standard baselines. Combining it with CADD and PolyPhen in an ensemble does not improve performance -- the ensemble is worse, confirming AlphaMissense already captures what the others offer.

The 7 priority candidates are variants that are predicted pathogenic, observed in the general population, and unresolved by any clinical database. The domain clustering of uncertain variants points to the membrane-spanning domains as the structural locus of pathogenicity in CFTR.

---

## Limitations

- Validation set is imbalanced: 253 CF-causing vs 39 Non CF-causing.
- AlphaMissense covers missense variants only. Nonsense, frameshift, and splicing variants are outside its scope.
- Population frequency data was available for only 117 of 3,220 variants. Most are too rare for gnomAD.
- One VCF from one cohort. Findings should be validated on a larger dataset before clinical use.
- Ensemble cross-validation on 286 samples has high variance. The result is indicative, not definitive.

---

## Code

All code is available at [github.com/RoshaniPawar16/cftr2-scraper](https://github.com/RoshaniPawar16/cftr2-scraper).

| Notebook | Description |
|---|---|
| `cftr2_scraper.ipynb` | CFTR2 annotation pipeline |
| `alphamissense.ipynb` | AlphaMissense analysis |
| `comparison.ipynb` | 4-predictor benchmark |
| `ensemble.ipynb` | Ensemble model |
