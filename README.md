# AlphaMissense annotation for CFTR variants

## Why this exists

The CFTR2 pipeline matched 656 of 3,220 variants. 80% had no clinical classification.

CFTR2 only includes variants seen in enough patients to characterise. Most variants in a real VCF are rare. They exist in population databases but have never been studied at scale in CF patients. That is not a flaw. It is just the nature of rare variant data.

But it raises a question. What are those 2,564 variants?

AlphaMissense predicts pathogenicity for every possible human missense variant. It was built from protein structure and evolutionary data, not from CFTR2. That independence matters. If its predictions agree with CFTR2 on the variants we do have labels for, we can apply it to the ones we do not.

We checked that first. AUC 0.946 on 292 labelled CFTR variants. Good enough to use. We then ran it on the unclassified variants and found 705 predicted likely pathogenic with no clinical classification anywhere. Those are the ones worth looking at.

Requires `cftr2_results.csv` from `cftr2_scraper.ipynb`.

## What is AlphaMissense

AlphaMissense is a pathogenicity predictor from Google DeepMind. It assigns a score between 0 and 1 to every possible human missense variant. The scores are pre-computed and published as a downloadable dataset. No model needs to be run locally.

## What this does

1. Downloads the AlphaMissense hg38 dataset (~1.4 GB) and filters it to CFTR variants only (UniProt P13569)
2. Converts VCF variant names from three-letter amino acid format (`Ser13Phe`) to single-letter format (`S13F`) to match AlphaMissense convention
3. Merges scores into the CFTR2 results
4. Validates AlphaMissense predictions against CFTR2 classifications on 292 variants with ground truth labels
5. Flags unclassified variants that AlphaMissense calls likely pathogenic

## Results

**Validation against CFTR2 ground truth**

| Metric | Value |
|---|---|
| Variants used | 292 |
| AUC | 0.946 |
| Accuracy | 0.94 |
| CF-causing F1 | 0.96 |
| Non CF-causing F1 | 0.77 |

AUC of 0.946 means AlphaMissense scores strongly agree with CFTR2 clinical classifications on this gene. The weaker performance on Non CF-causing is expected. Only 39 such variants were available for evaluation.

**Unclassified variants**

Of the 2,564 variants not in CFTR2, 2,411 had AlphaMissense scores. Of those:

| AlphaMissense class | Count |
|---|---|
| likely_benign | 1,349 |
| likely_pathogenic | 705 |
| ambiguous | 357 |

705 variants have no CFTR2 classification but are predicted likely pathogenic. These are candidates for further investigation. Saved to `flagged_unclassified.csv`.

## Files

| File | Description |
|---|---|
| `alphamissense.ipynb` | Experiment notebook |
| `AlphaMissense_hg38.tsv.gz` | Full AlphaMissense dataset. Not committed, ~1.4 GB. |
| `cftr_alphamissense.tsv` | CFTR-filtered scores. Not committed. |
| `cftr2_results_annotated.csv` | All variants with CFTR2 and AlphaMissense annotations. Not committed. |
| `flagged_unclassified.csv` | 705 unclassified variants predicted likely pathogenic. Not committed. |

## Dependencies

```
pandas
requests
scikit-learn
```
