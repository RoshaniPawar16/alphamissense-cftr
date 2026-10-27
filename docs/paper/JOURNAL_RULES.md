# PLOS Computational Biology — submission rules that bind this manuscript

**Compiled:** 2026-10-24 · **Branch:** paper-prep-2026-10

**Pages read**

- Submission guidelines — <https://journals.plos.org/ploscompbiol/s/submission-guidelines>
- Figures — <https://journals.plos.org/ploscompbiol/s/figures>

Every rule below names the page section it was taken from. Where neither page
states a rule, the entry reads **not stated**. Quotations are kept under 15
words throughout.

---

## 1. Length limits

| Item | Limit | Page section |
|---|---|---|
| Abstract | 300 words maximum; no citations; entered separately in the submission system | "Abstract" |
| Author Summary | 150–200 words | "Author Summary" |
| Body / full text | No limit. The page states there are no restrictions on word count, figures or supporting information | "Length" |
| Title | 200 characters | "Title" |
| Short title | 70 characters | "Title" |
| Software articles | Under 3,500 words excluding supplementary material (does not apply to this manuscript) | "Software Submissions" |

The absence of a body word limit is a real rule, not an omission: the page
says manuscripts may be any length but encourages concise presentation.

---

## 2. Required sections and their order

Section heading: **"Manuscript Organization"**

1. Title
2. Authors
3. Affiliations
4. Abstract
5. Author Summary
6. Introduction
7. Results
8. Discussion
9. Materials and Methods
10. Acknowledgments
11. References
12. Supporting information captions

Permitted departures, both stated under the same heading:

- Materials and Methods may be placed before Results or Discussion, if the
  reason is given in the cover letter.
- Results and Discussion may be combined into a single section.

Title, authors and affiliations must appear on the first page of the
manuscript file (section "Title page").

**Consequence for this project.** Methods is section 9 in the submitted order.
Drafting it first, as we are doing, is a drafting order, not a submission
order. If we want Methods to appear before Results in the final file, the
cover letter has to say why.

---

## 3. Author Summary — mandatory?

**Yes, for research articles.** Section heading: **"Author Summary"**. The page
states that all research article authors should include a non-technical
summary of 150–200 words, placed after the abstract. It must be written in the
first-person voice, be distinct from the abstract, and avoid acronyms and
complex terminology. Editors may revise it.

---

## 4. Figures

| Rule | Value | Page section |
|---|---|---|
| File format | TIFF or EPS only | "File Format" |
| LaTeX-generated vector EPS | Not accepted | "LaTeX" |
| Minimum width | 789 px at 300 dpi (6.68 cm / 2.63 in) | "Dimensions" |
| Maximum width | 2250 px at 300 dpi (19.05 cm / 7.5 in) | "Dimensions" |
| Maximum height | 2625 px at 300 dpi (22.23 cm / 8.75 in), excluding the caption | "Dimensions" |
| File size | 10 MB or less per figure | "File Size" |
| Resolution | 300–600 dpi; below 300 is blurred, above 600 may be resized | "Resolution" |
| Colour mode | RGB (8 bit per channel) or grayscale | "Color Mode" |
| Fonts inside figures | Arial, Times or Symbol only | "Text within Figures" |
| Text size inside figures | 8–12 point | "Text within Figures" |
| Text forbidden inside figure files | Author names, article title, figure number, title, caption | "Text within Figures" |
| Caption placement | In the manuscript text, immediately after the paragraph of first citation; never in the figure file | "Captions" |
| Caption label | Arabic numerals, abbreviated "Fig" (Fig 1) | "Captions" |
| Caption title | 15 words or fewer | "Captions" |
| Caption legend | Optional, directly after the title; figure credits in its last sentence | "Captions" |
| File naming | Numeric order matching the caption label and in-text citation (Fig1.tif) | "Figure Files" |
| Submission | One file per figure, separate from the manuscript | "Figure Files" |
| Number of figures | not stated | — |

A 20 MB ceiling applies to the raw blot and gel PDF under "Original images for
blots and gels". That section does not apply to this manuscript.

**Compliance of the figures built in Stage 4.** All are TIFF, RGB, 300 dpi,
Arial, 6.6–9.5 pt, under 0.5 MB, at most 2250 px wide and 1980 px high, with
no figure number or title inside the file. One deviation is flagged in the
figure list: some annotation text sits below the 8 pt floor and has to be
enlarged before submission.

---

## 5. Tables

| Rule | Value | Page section |
|---|---|---|
| Placement | Immediately after the first paragraph that cites the table | "Style and Format" |
| Submission | Inside the manuscript file, not as separate files | "Figures and Tables" |
| Citation order | Ascending numeric order at first appearance | "Figures and Tables" |
| Label and title | Label ("Table 1") plus a brief descriptive title, placed above the table | "Figures and Tables" |
| Legends and footnotes | Below the table | "Figures and Tables" |
| Footnotes elsewhere | Not permitted anywhere in the manuscript; move the content into the text or the reference list | "Footnotes" |
| Manuscript file format | DOC, DOCX, RTF or PDF | "File format" |
| Table-specific file format | not stated beyond the manuscript file format | — |

**Consequence for this project.** Tables 1–3 are drafted as markdown under
`docs/paper/tables/`. They must be pasted into the manuscript body at the
point of first citation before submission, not attached. The footnote ban
matters for Table 1 and Table 3: their per-cell source citations have to be
prose under the table, not footnote markers.

---

## 6. References

| Rule | Value | Page section |
|---|---|---|
| Style | Vancouver, as in the ICMJE sample references | "Reference style" |
| Journal name abbreviations | As in NCBI databases | "Reference style" |
| Numbering | Order of first appearance, cited in square brackets | "References" |
| Author list | First six authors, then "et al." | "References" |
| DOIs | Label plus the full DOI at the end of the reference; shortened DOIs and URLs are not accepted | "Formatting references" |
| Preprints | Citable if they carry a DOI or arXiv URL | "References" |
| Not citable | Unpublished or unavailable work, personal communications | "References" |
| Retracted work | May be discussed for historical context only if its retracted status is stated | "References" |
| Abstract citations | Not permitted | "Abstract" |

**Consequence for this project.** One of the two comparable papers, Liu et al.
2026, is a bioRxiv preprint with a DOI, so it is citable. The retracted-work
rule concerns the published literature and does not govern our own internal
corrections, but it sets the standard we are already following: anything
withdrawn is named as withdrawn.

---

## 7. Data and code availability

| Rule | Value | Page section |
|---|---|---|
| Underlying data | Must be available without restriction, rare exceptions aside | "Results" |
| Code | Code underlying the findings must also be available | "Results" |
| Statement required | A Data Availability Statement covering both data and code | "Data availability statement" |
| Statement contents | Names the repository and gives DOIs, accession numbers or other persistent identifiers | "Data availability statement" |
| Deposit location | A public repository, unless the data is already in the article | "Data reporting" |
| Code restrictions | Author-generated code must be public without access restrictions, unless legally or ethically restricted; a permanent repository with a DOI is strongly recommended | "Code reporting" |
| "Data not shown" | Not accepted | "Results" |

**Consequence for this project — the largest open compliance problem.** The
policy requires the underlying data to be public. Several inputs this analysis
rests on are not committed to the repository: `data/cftr2_results_annotated.csv`,
`data/cftr_alphamissense.tsv`, `data/All_Variants_VEP.Gene.vcf` and
`data/AlphaMissense_hg38.tsv.gz` are listed as not committed in the README file
table. The AlphaMissense dataset is redistributable from its own Zenodo record,
and the ClinVar and CFTR2 inputs are redownloadable from their sources, but a
persistent identifier has to be arranged for the derived tables before
submission. Nothing in Stage 3 or Stage 4 resolves this.

---

## 8. Rules checked for and not found on either page

- A maximum number of figures or tables — not stated.
- A per-figure panel-labelling convention (A, B, C) — not stated on these two
  pages.
- A statistical reporting checklist — not stated on these two pages.
- A specific requirement to report confidence intervals or exact p-values —
  not stated on these two pages.
