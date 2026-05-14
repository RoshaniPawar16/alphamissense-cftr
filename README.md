# AlphaMissense annotation for CFTR variants

## Why this exists

The CFTR2 pipeline matched 656 of 3,220 variants. 80% had no clinical classification.

CFTR2 only includes variants seen in enough patients to characterise. Most variants in a real VCF are rare. They exist in population databases but have never been studied at scale in CF patients. That is not a flaw. It is just the nature of rare variant data.

But it raises a question. What are those 2,564 variants?

AlphaMissense predicts pathogenicity for every possible human missense variant. It was built from protein structure and evolutionary data, not from CFTR2. That independence matters. If its predictions agree with CFTR2 on the variants we do have labels for, we can apply it to the ones we do not.

We checked that first. AUC 0.946 on 292 labelled CFTR variants. Good enough to use. We then ran it on the unclassified variants and found 705 predicted likely pathogenic with no clinical classification anywhere. We also looked at the 72 variants CFTR2 itself marks as uncertain. That turned out to be the most interesting part.

Requires `cftr2_results.csv` from `cftr2_scraper.ipynb`.

## What is AlphaMissense

AlphaMissense is a pathogenicity predictor from Google DeepMind. It assigns a score between 0 and 1 to every possible human missense variant. The scores are pre-computed and published as a downloadable dataset. No model needs to be run locally.

## What this does

1. Downloads the AlphaMissense hg38 dataset (~1.4 GB) and filters it to CFTR variants only (UniProt P13569)
2. Converts VCF variant names from three-letter amino acid format (`Ser13Phe`) to single-letter format (`S13F`) to match AlphaMissense convention
3. Merges scores into the CFTR2 results
4. Validates AlphaMissense predictions against CFTR2 ground truth
5. Flags unclassified variants predicted likely pathogenic
6. Cross-references flags with gnomAD population frequency from the VCF
7. Analyses the "varying clinical consequence" group

## Results

### Validation

| Metric | Value |
|---|---|
| Variants used | 292 |
| AUC | 0.946 |
| Accuracy | 0.94 |
| CF-causing F1 | 0.96 |
| Non CF-causing F1 | 0.77 |

AlphaMissense agrees with CFTR2 clinical classifications at AUC 0.946. The weaker F1 on Non CF-causing is expected. Only 39 such variants were available.

Note on class imbalance: 253 CF-causing vs 39 Non CF-causing. The overall accuracy is partly inflated by this. The AUC is the more reliable metric here.

### Unclassified variants

Of the 2,564 variants not in CFTR2, 2,411 had AlphaMissense scores.

| AlphaMissense class | Count |
|---|---|
| likely_benign | 1,349 |
| likely_pathogenic | 705 |
| ambiguous | 357 |

Of the 705 flagged, only 7 had gnomAD population frequency data in the VCF. Those are the highest-priority candidates: predicted pathogenic, observed in the general population, never classified by CFTR2.

We cross-referenced all 7 against ClinVar. Every one of them is unresolved.

| Variant | AM score | Population AF | ClinVar |
|---|---|---|---|
| Leu49Pro | 0.976 | 0.0002 | Uncertain significance |
| His1054Gln | 0.901 | 0.0002 | Uncertain significance |
| Leu986Pro | 0.869 | 0.0004 | Conflicting classifications |
| Pro355Leu | 0.858 | 0.0002 | Uncertain significance |
| Phe650Leu | 0.846 | 0.0002 | Uncertain significance |
| Arg104Gly | 0.845 | 0.0002 | Uncertain significance |
| Arg1097Cys | 0.651 | 0.0002 | Conflicting classifications |

5 are classified as uncertain significance. 2 have conflicting classifications, meaning different labs have actively disagreed. AlphaMissense calls all 7 likely pathogenic.

Leu986Pro and Arg1097Cys are the strongest candidates. Clinical disagreement already exists on both. AlphaMissense provides consistent computational evidence for pathogenicity. Arg1097Cys was last evaluated in ClinVar in February 2026.

These 7 variants are not in CFTR2, are observed in the general population, have no clinical consensus, and score high on a model validated at AUC 0.946 on this gene. They are candidates for functional follow-up.

The remaining 539 flagged variants are too rare to appear in gnomAD. They may be family-private mutations or sequencing artifacts.

### Varying clinical consequence

72 variants in CFTR2 are marked as "varying clinical consequence". CFTR2 has insufficient data to classify them cleanly. AlphaMissense scored all 72.

| AlphaMissense class | Count |
|---|---|
| likely_pathogenic | 41 |
| ambiguous | 19 |
| likely_benign | 12 |

41 of 72 are called likely pathogenic. CFTR2 is uncertain about them. The model is not. Asp979Ala scores 0.993 while CFTR2 still classifies it as varying. These are direct reclassification candidates.

Arg117His scores 0.299 (likely benign). This is consistent with clinical knowledge. R117H is associated with mild phenotypes and CBAVD rather than classic CF. That agreement is a meaningful sanity check on the model.

![AlphaMissense score distribution for varying clinical consequence variants](varying_consequence_plot.png)

The plot shows clear separation between classes. The ambiguous variants sit near the thresholds as expected. Val938Gly at ~0.6 is a borderline call worth noting.

## Limitations

- Class imbalance in the validation set. 253 CF-causing vs 39 Non CF-causing. Results should be interpreted with that in mind.
- 311 VCF variants could not be converted to single-letter format. These are likely non-missense variants (frameshifts, nonsense) and were excluded from AlphaMissense matching.
- Population frequency data was only available for 117 of 3,220 variants. Most are too rare for gnomAD.
- AlphaMissense does not model compound heterozygosity, splicing effects, or regulatory context.

## Files

| File | Description |
|---|---|
| `alphamissense.ipynb` | Experiment notebook |
| `AlphaMissense_hg38.tsv.gz` | Full AlphaMissense dataset. Not committed, ~1.4 GB. |
| `cftr_alphamissense.tsv` | CFTR-filtered scores. Not committed. |
| `cftr2_results_annotated.csv` | All variants with CFTR2 and AlphaMissense annotations. Not committed. |
| `flagged_unclassified.csv` | 705 unclassified variants predicted likely pathogenic. Not committed. |
| `priority_candidates.csv` | 7 high-priority variants with population frequency. Not committed. |
| `varying_consequence_am.csv` | 72 varying consequence variants with AlphaMissense scores. Not committed. |

## Dependencies

```
pandas
requests
scikit-learn
```
