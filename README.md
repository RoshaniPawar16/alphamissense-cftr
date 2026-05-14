# cftr2_scraper

Annotates CFTR variants from a VEP-annotated VCF with clinical classifications from the CFTR2 database.

---

## Background

Cystic fibrosis is caused by pathogenic variants in the *CFTR* gene. Not every variant is equally damaging — or damaging at all. CFTR2 is the authoritative clinical database for variant classification. It is maintained by Johns Hopkins, the CF Foundation, and the Hospital for Sick Children. As of January 2026, it holds data from ~122,935 patients across 2,092 reported variants.

Classification determines treatment eligibility — CFTR modulators are approved for specific variant classes, not all CFTR mutations.

---

## What this does

A VEP-annotated VCF contains thousands of CFTR variants. This script maps each one to its CFTR2 determination.

Steps:
1. Parse protein-level variant names from the VCF using regex (e.g. `Ser13Phe`)
2. Download the official CFTR2 classification spreadsheet from cftr2.org
3. Translate VCF naming to HGVS protein format (`Ser13Phe` → `p.Ser13Phe`) to match CFTR2's convention
4. Left-join VCF variants against CFTR2 on protein name
5. Output a CSV with each variant's CFTR2 determination and allele frequency

---

## The naming problem

VEP outputs three-letter amino acid codes without a prefix (e.g. `Ser13Phe`).  
CFTR2 uses HGVS protein nomenclature with a `p.` prefix (e.g. `p.Ser13Phe`).  
Matching on legacy names (e.g. `F508del`) fails entirely — different convention.

---

## Results (Jan 2026 CFTR2 release)

| Determination | Count |
|---|---|
| CF-causing | 226 |
| Varying clinical consequence | 72 |
| Non CF-causing | 33 |
| No interpretation available | 325 |
| **Matched subtotal** | **656** |
| Not in CFTR2 | 2,564 |
| **Total VCF variants** | **3,220** |

80% of variants are absent from CFTR2. This is expected. CFTR2 only curates variants with sufficient patient observations. Most variants in a VEP-annotated VCF are rare or private — they exist in the literature or population databases but have never been characterised at scale.

---

## Limitations

- **Coverage gap.** CFTR2 is not exhaustive. Rare and novel variants will always fall outside it.
- **Protein-name matching only.** Two variants with different cDNA changes but identical protein effect are treated as the same. This is a reasonable simplification but not always correct.
- **Snapshot.** CFTR2 updates a few times a year. The spreadsheet URL is hardcoded to the Jan 2026 release. It needs manual updating.
- **No compound heterozygosity.** CFTR2 also classifies variant *combinations*. This script only handles single variants.

---

## Files

| File | Description |
|---|---|
| `cftr2_scraper.ipynb` | Main notebook |
| `All_Variants_VEP.Gene.vcf` | Input VCF (VEP-annotated, CFTR gene) — **not included, private data** |
| `cftr2_variants.xlsx` | CFTR2 spreadsheet downloaded from cftr2.org — not committed, re-downloaded on run |
| `cftr2_results.csv` | Output — one row per variant with determination — not committed |

---

## Usage

Run all cells in `cftr2_scraper.ipynb`.

---

## Dependencies

```
pandas
openpyxl
requests
```
