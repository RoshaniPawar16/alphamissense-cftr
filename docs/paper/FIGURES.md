# Figures — files, legends and compliance

**Compiled:** 2026-10-24 · **Branch:** paper-prep-2026-10

Captions follow the PLOS rules in `docs/paper/JOURNAL_RULES.md`: an Arabic
"Fig" label, a title of 15 words or fewer, then the legend. Captions belong in
the manuscript text at the point of first citation, never inside the figure
file. Each legend below states what is shown and the n, and nothing
interpretive.

| Figure | File | Generator | Size | Compliance |
|---|---|---|---|---|
| Fig 1 | `figures/paper/Fig1.tif` | `scripts/paper/p4_fig1_flow.py` | 2250 × 1980 px, RGB, 300 dpi, 0.36 MB | Meets the maximum width exactly; see the text-size deviation below |
| Fig 2 | `figures/paper/Fig2.tif` | `scripts/paper/p4_fig2_roc.py` | 1560 × 1500 px, RGB, 300 dpi, 0.23 MB | Compliant except the text-size deviation |
| Fig 3 | `figures/paper/Fig3.tif` | `scripts/paper/p4_fig3_scatter.py` | 1920 × 1380 px, RGB, 300 dpi, 0.23 MB | Compliant except the text-size deviation |
| Fig 4 | Not built | — | — | n does not permit it; see below |

---

## Fig 1

**Title.** Derivation of the two variant sets analysed.

**Legend.** Flow of variants through both chains of the study. The benchmark
chain begins with 3,220 unique protein changes extracted from the CFTR region
of a ClinVar VCF and narrows to 2,909 convertible to AlphaMissense notation,
2,665 carrying an AlphaMissense score, 259 carrying a binary CFTR2 label (226
CF-causing and 33 Non CF-causing), and 254 carrying CADD, PolyPhen-2 and SIFT
scores as well (221 CF-causing and 33 Non CF-causing). The screening chain
begins with the AlphaMissense CFTR table of 9,721 scored single-nucleotide
variants covering 8,597 unique protein changes, and narrows to the 1,278
variants of ambiguous AlphaMissense class covering 1,100 unique protein
changes, then to 778 with an AlphaGenome ATAC or SPLICE quantile above 0.95,
then to 18 that also carry a SpliceAI maximum delta above 0.5 under the
gene-mask definition, of which 13 also meet the centre-mask definition. The
two chains are separate variant sets and are not nested: 431 of the 1,278
appear among the 3,220. Numbers to the right of the benchmark chain are the
variants removed at each step. Every number is listed with its source file and
column in `results/paper/fig1_flow_counts.csv`.

---

## Fig 2

**Title.** Receiver operating characteristic curves for four predictors.

**Legend.** ROC curves for AlphaMissense, PolyPhen-2, CADD and SIFT against
CFTR2 binary labels on the 254 deduplicated variants carrying all four scores
(221 CF-causing, 33 Non CF-causing). The shaded band is the pointwise 95%
percentile bootstrap interval for the AlphaMissense curve over 2,000 resamples
with seed 42, interpolated onto a common false-positive-rate grid; it is
pointwise rather than simultaneous and is drawn for AlphaMissense only. Legend
entries give each tool's area under the curve with its 95% bootstrap
confidence interval from `results/paper/auc_ci.csv`. The diagonal marks chance
performance. SIFT is plotted as 1 minus the SIFT score so that higher is more
damaging for every curve.

---

## Fig 3

**Title.** AlphaGenome splice quantile against SpliceAI delta.

**Legend.** One point per variant for all 1,278 AlphaMissense-ambiguous CFTR
missense single-nucleotide variants. The horizontal axis is the AlphaGenome
gene-mask SPLICE quantile from the May 2026 scoring run, plotted as
−log10(1 − quantile) because the values crowd against 1.0; axis labels give the
untransformed quantile. The vertical axis is the SpliceAI maximum delta across
the four channels, on its native scale. Dashed lines mark the two thresholds
that define the concordant set, quantile 0.95 and delta 0.5. Blue circles are
the 13 variants meeting both the gene-mask and the centre-mask definition;
orange squares are the 5 meeting the gene-mask definition only; all 18 are
labelled with their protein change. Grey points are the remaining 1,260
variants. Scores are from
`results/alphagenome/alphagenome_full_cftr_results.csv` and
`results/comparator_scores.csv`; set membership is from
`results/paper/concordant_set.csv`.

---

## Fig 4 — not built

**n does not permit it.** The minigene benchmark has 23 rows, 11 positive and
12 negative, and a ROC figure drawn on it would imply a precision the data
cannot support. Two measurements from `results/paper/minigene_benchmark.csv`
make the case:

- The bootstrap confidence intervals on AUC span roughly 0.30 for all three
  scorers. The AlphaGenome gene-mask quantile gives 0.856 with an interval of
  0.676 to 0.985, and the raw gene-mask score gives 0.860 with an interval of
  0.683 to 0.985. Curves this uncertain cannot be visually compared.
- SpliceAI returns a delta of exactly 0 for 19 of the 23 rows. Its apparent
  AUC of 0.432 measures the coverage of a precomputed score file, not
  prediction, and plotting that curve beside the others would misrepresent it.

The 2x2 tables at each tool's operating point are the `operating_point_2x2`
rows of `results/paper/minigene_benchmark.csv`. They carry the same
information a figure would, without implying a smooth curve. If a visual is wanted later, a
dot plot of the three scores grouped by minigene label would be honest, since
it shows every one of the 23 observations and asserts no curve. It is not
built here.

---

## Compliance deviation to fix before submission

The journal requires text inside figures to be 8–12 point ("Text within
Figures"). Three annotation layers fall below the floor:

| Figure | Element | Current size |
|---|---|---|
| Fig 1 | Exclusion notes beside the benchmark chain, and the closing note on set overlap | 7.5 pt |
| Fig 2 | Legend entries | 7.6 pt |
| Fig 3 | Variant labels | 6.6 pt |
| Fig 3 | Legend entries and threshold labels | 7.0–7.4 pt |

All other text is within range. Raising these to 8 pt will require widening
Fig 2 and Fig 3, which have headroom: both are well under the 2250 px maximum
width. Fig 1 is already at the maximum width, so its notes will need to be
shortened or moved into the caption rather than enlarged in place. This is a
layout change, not a data change, and is left for the figure-finalisation
pass.
