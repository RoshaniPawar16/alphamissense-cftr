# cftr2_scraper

A friend had a VEP-annotated CFTR VCF and needed each variant annotated with its CFTR2 clinical classification. This notebook documents the full process, including the dead ends.

## Background

Cystic fibrosis is caused by pathogenic variants in the *CFTR* gene. CFTR2 is the authoritative clinical database for variant classification. It is maintained by Johns Hopkins, the CF Foundation, and the Hospital for Sick Children. As of January 2026, it holds data from ~122,935 patients across 2,092 variants. Classification determines treatment eligibility. CFTR modulators are approved for specific variant classes only.

## What we tried first

The first approach was scraping cftr2.org directly using BeautifulSoup and then Selenium. The site serves variant data through JavaScript. Neither approach returned usable results.

The CFTR2 mutations history page lists downloadable xlsx files with the full variant classification history. We downloaded the January 2026 release directly.

## Parsing the spreadsheet

The xlsx file has 10 rows of metadata above the actual data. Finding the correct header row took a few attempts. Row 11 (0-indexed) was correct.

## The naming problem

VEP annotates variants using three-letter amino acid codes without a prefix (e.g. `Ser13Phe`). CFTR2 uses HGVS protein format with a `p.` prefix (e.g. `p.Ser13Phe`). The first match returned 0 results. Once we identified the mismatch and added the prefix, 656 of 3,220 variants matched.

## Results (Jan 2026 CFTR2 release)

| Determination | Count |
|---|---|
| CF-causing | 226 |
| Varying clinical consequence | 72 |
| Non CF-causing | 33 |
| No interpretation available | 325 |
| Matched subtotal | 656 |
| Not in CFTR2 | 2,564 |
| Total VCF variants | 3,220 |

80% of variants are absent from CFTR2. This is expected. CFTR2 only curates variants with sufficient patient observations. Most variants in a VEP-annotated VCF are rare or private.

## Limitations

- CFTR2 is not exhaustive. Rare and novel variants will always fall outside it.
- Matching is on protein name only. Two variants with different cDNA changes but the same protein effect are treated as one.
- The spreadsheet URL is hardcoded to the Jan 2026 release. It needs manual updating when a new version is published.
- CFTR2 also classifies variant combinations (compound heterozygosity). This notebook handles single variants only.

## Files

| File | Description |
|---|---|
| `cftr2_scraper.ipynb` | Main notebook |
| `All_Variants_VEP.Gene.vcf` | Input VCF, VEP-annotated, CFTR gene. Not included, private data. |
| `cftr2_variants.xlsx` | CFTR2 spreadsheet from cftr2.org. Not committed, re-downloaded on run. |
| `cftr2_results.csv` | Output. One row per variant with CFTR2 determination. Not committed. |

## Usage

Run all cells in `cftr2_scraper.ipynb`.

## Dependencies

```
pandas
openpyxl
requests
beautifulsoup4
selenium
```
