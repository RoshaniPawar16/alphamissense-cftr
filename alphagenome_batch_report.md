# AlphaGenome Batch Analysis: 7 Unclassified CFTR Variants

**Model:** AlphaGenome v0.6.1  |  **Genome:** hg38  |  **Tissue:** Lung (UBERON:0002048)
**Outputs:** RNA-seq, ATAC-seq, Splice site usage  |  **Window:** 1 Mb centred on variant

---

## Variants Queried

| Variant | Protein | hg38 Position | REF>ALT | AlphaMissense |
|---------|---------|---------------|---------|---------------|
| Leu49Pro | L49P | chr7:117,504,345 | T>C | 0.9757 |
| Arg104Gly | R104G | chr7:117,530,935 | A>G | 0.8448 |
| Pro355Leu | P355L | chr7:117,540,294 | C>T | 0.858 |
| Phe650Leu | F650L | chr7:117,592,115 | T>C | 0.8455 |
| Leu986Pro | L986P | chr7:117,606,722 | T>C | 0.8685 |
| His1054Gln | H1054Q | chr7:117,611,603 | T>G | 0.901 |
| Arg1097Cys | R1097C | chr7:117,611,730 | C>T | 0.6513 |

---

## Raw Results per Output Type

### RNA-seq (Gene Expression)

| Variant | Mean \|log2FC\| | Max \|log2FC\| | Bins >0.5 |
|---------|----------------|----------------|-----------|
| Leu49Pro | 0.0106 | 0.3527 | 0 |
| Arg104Gly | 0.0110 | 0.2519 | 0 |
| Pro355Leu | 0.0098 | 0.2553 | 0 |
| Phe650Leu | 0.0096 | 0.2441 | 0 |
| Leu986Pro | 0.0098 | 0.2553 | 0 |
| His1054Gln | 0.0098 | 0.4245 | 0 |
| Arg1097Cys | 0.0100 | 0.2533 | 0 |

### ATAC-seq (Chromatin Accessibility)

| Variant | Mean \|log2FC\| | Max \|log2FC\| | Bins >0.5 |
|---------|----------------|----------------|-----------|
| Leu49Pro | 0.0071 | 6.9406 | 13 |
| Arg104Gly | 0.0071 | 11.2490 | 13 |
| Pro355Leu | 0.0070 | 6.7811 | 10 |
| Phe650Leu | 0.0070 | 5.1427 | 18 |
| Leu986Pro | 0.0070 | 4.6793 | 9 |
| His1054Gln | 0.0071 | 13.3894 | 29 |
| Arg1097Cys | 0.0071 | 5.7603 | 16 |

### Splice Site Usage

| Variant | Mean \|log2FC\| | Max \|log2FC\| | Bins >0.5 |
|---------|----------------|----------------|-----------|
| Leu49Pro | 0.0113 | 1.5150 | 8 |
| Arg104Gly | 0.0112 | 1.2516 | 6 |
| Pro355Leu | 0.0108 | 0.6290 | 6 |
| Phe650Leu | 0.0107 | 0.9040 | 4 |
| Leu986Pro | 0.0108 | 1.2645 | 5 |
| His1054Gln | 0.0108 | 3.2423 | 39 |
| Arg1097Cys | 0.0110 | 0.6318 | 2 |

---

## Ranked: Strongest ATAC-seq Signal

Sorted by Max |log2FC| — chromatin accessibility changes that may indicate disrupted enhancers or regulatory elements.

| Rank | Variant | AM Score | ATAC Max \|log2FC\| | ATAC Bins >0.5 | Regulatory flag |
|------|---------|----------|---------------------|----------------|-----------------|
| 1 | His1054Gln | 0.901 | 13.389 | 29 | ⚠️ strong regulatory signal |
| 2 | Arg104Gly | 0.8448 | 11.249 | 13 | ⚠️ strong regulatory signal |
| 3 | Leu49Pro | 0.9757 | 6.941 | 13 | ⚠️ strong regulatory signal |
| 4 | Pro355Leu | 0.858 | 6.781 | 10 | ⚠️ strong regulatory signal |
| 5 | Arg1097Cys | 0.6513 | 5.760 | 16 | ⚠️ strong regulatory signal |
| 6 | Phe650Leu | 0.8455 | 5.143 | 18 | ⚠️ strong regulatory signal |
| 7 | Leu986Pro | 0.8685 | 4.679 | 9 | moderate |

---

## Ranked: Strongest Splice Site Signal

Sorted by Max |log2FC| — variants most likely to disrupt splicing in ways AlphaMissense cannot detect.

| Rank | Variant | AM Score | Splice Max \|log2FC\| | Splice Bins >0.5 | Splicing flag |
|------|---------|----------|-----------------------|------------------|---------------|
| 1 | His1054Gln | 0.901 | 3.2423 | 39 | ⚠️ cryptic splice risk |
| 2 | Leu49Pro | 0.9757 | 1.5150 | 8 | ⚠️ cryptic splice risk |
| 3 | Leu986Pro | 0.8685 | 1.2645 | 5 | ⚠️ cryptic splice risk |
| 4 | Arg104Gly | 0.8448 | 1.2516 | 6 | ⚠️ cryptic splice risk |
| 5 | Phe650Leu | 0.8455 | 0.9040 | 4 | ⚠️ cryptic splice risk |
| 6 | Arg1097Cys | 0.6513 | 0.6318 | 2 | ⚠️ cryptic splice risk |
| 7 | Pro355Leu | 0.858 | 0.6290 | 6 | ⚠️ cryptic splice risk |

---

## Key Findings: What AlphaMissense Misses

AlphaMissense scores protein-level pathogenicity only. AlphaGenome adds:

- **ATAC-seq outliers**: variants predicted to remodel chromatin — may disrupt intronic enhancers, CTCF binding sites, or DHS peaks in airway epithelium even when the amino acid change itself is tolerated.
- **Splice site usage shifts**: variants within or near exon boundaries that alter donor/acceptor strength, enabling cryptic exon inclusion or exon skipping — invisible to protein-sequence models.

### Variants of highest interest (regulatory/splicing signal beyond protein effect):

- **His1054Gln** — highest ATAC max |log2FC| = 13.389, 29 bins >0.5. AlphaMissense score 0.901 — regulatory disruption may contribute independently of protein misfolding.

- **His1054Gln** — highest splice site max |log2FC| = 3.2423, 39 bins >0.5. Possible cryptic splicing effect that AlphaMissense (score 0.901) would not capture.

- **Arg1097Cys** — lowest AlphaMissense score (0.6513, borderline likely pathogenic). ATAC max |log2FC| = 5.760, splice max = 0.6318. If regulatory or splicing signal is elevated here, it provides a mechanistic explanation that protein-level scoring alone cannot.

---

*AlphaGenome v0.6.1 · hg38 · Lung UBERON:0002048 · 2026-05-28*