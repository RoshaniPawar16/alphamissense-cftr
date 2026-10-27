# Two comparable papers — structure only

**Compiled:** 2026-10-24 · **Branch:** paper-prep-2026-10

What follows records how these two papers are built, not what they found. No
result of either paper is paraphrased. Both were read for one purpose: to see
what a reader of this literature expects a paper of this shape to contain.

**McDonald** — McDonald EF, et al. PLOS ONE 2024.
<https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0297560>

**Liu** — Liu et al. bioRxiv 2026, v2 full text.
<https://www.biorxiv.org/content/10.64898/2026.01.21.700828v2.full>

---

## Section headings, in order

| McDonald | Liu |
|---|---|
| Abstract | Abstract |
| Introduction | Introduction |
| Results and discussion (combined) | Methods |
| — I. AlphaMissense predictions of CFTR pathogenicity | — Definition of the AlphaGenome screening window for *RHD* regulation |
| — II. Cystic fibrosis pathogenicity correlated modestly with AlphaMissense predictions | — In silico prediction of non-coding variant effects using AlphaGenome |
| — III. AlphaMissense predicts CFTR function beyond folding and trafficking competency | — Selection algorithm for variant validation |
| — IV. AlphaMissense cannot predict CFTR variant theratype | — sgRNA cloning and plasmid preparation |
| Conclusion | — CRISPR-nCas9 cytosine base editing and DNA-level editing efficiency |
| Methods | — Quantification of *RHD* expression by qPCR |
| — Data curation and collection | — Flow cytometric analysis of surface *RHD* expression |
| — Filtering experimental data | Results |
| — Analysis | — AG defines predictable regions and a baseline expression reference |
| Supporting information | — Key regulatory signals enriched in promoter-proximal and intragenic regions |
| References | — Functional validation of AG-prioritized non-coding SNPs |
| | Discussion |
| | Acknowledgements |
| | Funder Information Declared |
| | Footnotes |
| | References |

**Reading.** The two sit at opposite ends of the ordering choice PLOS allows.
McDonald merges Results and Discussion and puts Methods last, which is the
PLOS Computational Biology default order. Liu puts Methods second, before
Results, which the guidelines permit with a cover-letter reason. Liu's
subsection titles are procedures; McDonald's are claims written as sentences.

---

## Figures and tables

| | McDonald | Liu |
|---|---|---|
| Main figures | 4 (Fig 1–4) | 8 (Figures 1–8) |
| Main tables | 1 (Table 1) | None in the full text |
| Supplementary figures | 7 (S1–S7) | Not determinable from the full-text page |
| Supplementary tables | 4 (S1–S4) | Not determinable from the full-text page |

**Reading.** Neither paper is table-heavy. McDonald carries one main table and
pushes the rest to supporting information; Liu carries none. Our current plan
of three main tables is above both. Table 3, the concordant set, is the one
most likely to belong in supporting information rather than the body.

---

## What the first figure shows

| McDonald | Liu |
|---|---|
| The average AlphaMissense score per residue mapped onto the CFTR structure (PDB 5UAK). | A genomic overview of the *RHD* locus with K562 chromatin tracks and the AlphaGenome-predicted baseline expression profile. |

**Reading.** Both open on the object of study rather than on a performance
metric: a protein structure in one case, a genome browser view in the other.
Neither opens with a study-flow diagram. Our planned Fig 1 is a flow diagram,
which is a reporting-standard choice rather than a field convention. It is
defensible here, because our cohort derivation is the part of this work most
easily misread, but it is a departure from both comparators.

---

## How the Methods describe data sources

| McDonald | Liu |
|---|---|
| No database version numbers and no access or download dates. Example phrasing: "ClinVar data was downloaded after searching for CFTR". Sources named include AlphaMissense, ESM, EVE, CFTR2.org and ClinVar. | No database version numbers and no access or download dates for the ENCODE tracks, gnomAD or other resources. The genome build is given as hg38. |
| Software named without versions: Python 3, Pandas, matplotlib, seaborn, SciPy. | AlphaGenome identified by release timing rather than a version string: a research preview released by Google DeepMind in July 2025. |

**Reading, and the decision it drives.** Neither comparator meets the
provenance standard this project has already set for itself. Both name their
sources without pinning them. That is the prevailing practice, and it is the
practice our audit record exists to reject. Our Methods will give a version
and a date for every dataset, or write [NOT IN REPO] where the repository does
not record one. This will make our Methods longer and more exposed than either
comparator's. That is the intended trade.

---

## How limitations are stated

| McDonald | Liu |
|---|---|
| No dedicated limitations subsection and no separate Discussion, because Results and Discussion are combined. Limitations appear inside Results section II and again in the Conclusion, which advises caution in interpreting the predictions. | No dedicated limitations section. Limitations appear in the Discussion as two consecutive paragraphs, one opening on several limitations despite the strengths and one on the scope of the base-editing validation. They cover cell-line choice, model dependence on training data, and validation of only a subset of prioritized variants. |

**Reading.** Neither uses a headed Limitations section; both fold the material
into running prose. For this manuscript the limitations are load-bearing
rather than decorative: the negative class is small, the quantile background
is miscalibrated for coding variants, and the only external validation set has
23 members with a known coverage gap. A headed subsection would carry them
better than a buried paragraph, even though neither comparator uses one.

---

## Reference counts

| McDonald | Liu |
|---|---|
| 52 numbered references. | 39 numbered references (last numbered entry is 39; the count assumes consecutive numbering from 1, as the list was read in two parts). |

---

## Summary of the decisions these two papers force

1. **Methods placement.** Both orders are acceptable to the journal. McDonald's
   order is the journal default. Choosing Liu's order costs a cover-letter
   sentence.
2. **Table count.** Three main tables exceeds both comparators. Table 3 is the
   candidate for supporting information.
3. **First figure.** Neither opens with a flow diagram. Ours will. The reason
   is specific to this cohort and should be stated rather than assumed.
4. **Provenance detail.** We will exceed both comparators, deliberately.
5. **Limitations.** Neither uses a headed subsection. We should, because ours
   change how the central claim must be read.
