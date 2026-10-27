# Comparator Analysis: AlphaGenome vs CADD v1.7 vs SpliceAI

**Dataset:** 1,278 ambiguous-class CFTR missense variants (AlphaMissense score 0.34–0.564)
**Genome build:** hg38  |  **Tissue:** Lung (UBERON:0002048)
**AlphaGenome version:** v0.6.1 (client SDK)  |  **CADD version:** v1.7 (GRCh38)  |  **SpliceAI version:** [NOT IN REPO] (precomputed scores via Ensembl VEP plugin; the API response does not return a version)

---

## 1. Score Availability

| Tool | Variants scored | Coverage |
|------|----------------|----------|
| AlphaGenome ATAC quantile   | 1,278 | 100% |
| AlphaGenome SPLICE quantile | 1,278 | 100% |
| CADD PHRED                  | 1,278 | 100% |
| SpliceAI max delta          | 1,278 | 100% |

---

## 2. Score Distributions

| Tool | n | Mean | p25 | p50 | p75 | p95 |
|------|---|------|-----|-----|-----|-----|
| CADD PHRED           | 1,278 | 24.5  | 23.1  | 24.9  | 26.4  | 28.6  |
| SpliceAI max delta   | 1,278 | 0.037 | 0.000 | 0.000 | 0.020 | 0.161 |
| AlphaGenome ATAC q   | 1,278 | 0.618 | 0.412 | 0.668 | 0.837 | 0.963 |
| AlphaGenome SPLICE q | 1,278 | 0.927 | 0.908 | 0.957 | 0.992 | 0.999 |

---

## 3. Classification Thresholds

| Tool | Threshold | Count | Fraction |
|------|-----------|------:|--------:|
| CADD PHRED ≥ 20 (top 1% most deleterious)   | ≥ 20  | 1,164 | 91.1% |
| CADD PHRED ≥ 30 (top 0.1%)                  | ≥ 30  |    40 |  3.1% |
| SpliceAI delta > 0.2 (potentially altering)  | > 0.2 |    52 |  4.1% |
| SpliceAI delta > 0.5 (high confidence)       | > 0.5 |    19 |  1.5% |
| AlphaGenome ATAC or SPLICE q > 0.95          | > 0.95|   778 | 60.9% |

**Note on CADD discrimination:** 91.1% of all 1,278 ambiguous variants have CADD PHRED ≥ 20. Because CADD flags nearly the entire class as deleterious, it cannot discriminate within the ambiguous group. The CADD < 20 threshold used to define the AlphaGenome rescue group therefore captures only the 8.9% of variants CADD considers genuinely low-impact.

---

## 4. Rescue Groups

### 4.1 AlphaGenome Rescue

**Definition:** (ATAC quantile > 0.95 OR SPLICE quantile > 0.95) AND CADD PHRED < 20 AND SpliceAI delta < 0.2

**Count: 58 variants** (4.5% of all 1,278)

> **Audit note.** The SPLICE quantile > 0.95 component of this definition clears 58.4% of the cohort by construction (coding variants ranked against a common-variant background). The 693 discordant count (SPLICE q > 0.95 AND SpliceAI < 0.2, strict) sits at 693 observed vs 713.7 expected under independence (2×2 χ²(1) = 32.4, p = 1.3 × 10⁻⁸; observed below expected; an earlier version stated "717 expected, χ² p = 0.20" which did not reproduce — see AUDIT_RECORD.md). The discordant group is significantly depleted, not at chance level; it cannot support a claim that AlphaGenome detects splice effects invisible to SpliceAI. The 58 rescue group inherits both limitations: the ATAC signal component is more interpretable, but the SPLICE component is not. These figures are retained for audit traceability; they are not interpreted as a validated candidate group.

These variants have an AlphaGenome ATAC or SPLICE quantile above 0.95 together with CADD PHRED below 20 and SpliceAI delta below 0.2. Per the audit note above, the group is retained as a count only and is not interpreted as a candidate set.

**Top 10 by ATAC quantile** (deduplicated by protein variant; multiple genomic variants encoding the same amino acid substitution are collapsed to the highest-scoring entry):

| Rank | Variant | AM Score | ATAC q | SPLICE q | CADD PHRED | SpliceAI |
|------|---------|:--------:|:------:|:--------:|:----------:|:--------:|
|  1 | F1413I | 0.487 | 0.999 | 0.996 | 19.2 | 0.000 |
|  2 | Q1411H | 0.357 | 0.999 | 0.960 |  9.2 | 0.000 |
|  3 | Q1412P | 0.548 | 0.995 | 0.960 | 17.1 | 0.000 |
|  4 | H950P  | 0.485 | 0.988 | 0.991 | 19.0 | 0.000 |
|  5 | H954P  | 0.367 | 0.985 | 0.992 | 19.6 | 0.000 |
|  6 | N965K  | 0.422 | 0.977 | 0.996 | 19.7 | 0.080 |
|  7 | I215F  | 0.477 | 0.963 | 0.940 | 18.1 | 0.000 |
|  8 | T940I  | 0.351 | 0.958 | 0.964 | 19.7 | 0.010 |
|  9 | G970C  | 0.491 | 0.933 | 1.000 | 19.8 | 0.860 |
| 10 | I1366L | 0.418 | 0.938 | 1.000 | 19.8 | 0.000 |

### 4.2 Multi-Tool Confirmed

**Definition:** AlphaGenome SPLICE quantile > 0.95 AND SpliceAI delta > 0.5

**Count: 18 variants**

Variants where both AlphaGenome and SpliceAI independently detect splice-altering effects. These are the highest-confidence splicing candidates — agreement between a DNA sequence model (SpliceAI) and a regulatory genomics model (AlphaGenome) strengthens the evidence for functional impact.

**Top 5 by SpliceAI delta:**

| Rank | Variant | AM Score | SPLICE q | SpliceAI delta | CADD PHRED |
|------|---------|----------|----------|----------------|------------|
| 1 | S1058G | 0.507 | 1.000 | 1.000 | 33.0 |
| 2 | A155G | 0.357 | 1.000 | 0.990 | 35.0 |
| 3 | I906S | 0.473 | 1.000 | 0.960 | 34.0 |
| 4 | G1047C | 0.342 | 1.000 | 0.960 | 34.0 |
| 5 | G970V | 0.440 | 0.999 | 0.950 | 27.9 |

### 4.3 Discordant: AlphaGenome High Splice, SpliceAI Low

**Definition:** AlphaGenome SPLICE quantile > 0.95 AND SpliceAI delta < 0.2

**Count: 693 variants** (54.2% of all 1,278)

This count is retained for traceability only. It is retracted as a finding: observed 693 against an independence expectation of 713.7 (2×2 χ²(1) = 32.4, p = 1.3 × 10⁻⁸; the group is depleted relative to independence; AUDIT_RECORD.md:82). It does not support a claim that AlphaGenome detects splice effects invisible to SpliceAI.

**Top 5 by AlphaGenome SPLICE quantile:**

| Rank | Variant | AM Score | AG SPLICE q | SpliceAI delta | CADD PHRED |
|------|---------|----------|-------------|----------------|------------|
| 1 | H620Q | 0.417 | 1.000 | 0.000 | 21.5 |
| 2 | A455G | 0.398 | 1.000 | 0.000 | 25.9 |
| 3 | W79C | 0.475 | 1.000 | 0.050 | 26.3 |
| 4 | I906N | 0.354 | 1.000 | 0.040 | 24.9 |
| 5 | I906T | 0.389 | 1.000 | 0.030 | 22.7 |

---

## 5. Tool Comparison Summary

| Feature | CADD v1.7 | SpliceAI (version [NOT IN REPO]) | AlphaGenome v0.6.1 |
|---------|-----------|---------------|-------------------|
| Score type | Conservation + functional annotation ensemble | Splice site delta score | Quantile score (RNA, ATAC, splice) |
| Mechanism captured | General deleteriousness | Canonical/cryptic splice sites | Regulatory, chromatin, splicing |
| Context window | Variant-level annotations | ±50 bp | 1 Mb genomic window |
| Tissue specificity | None (genome-wide) | None (gene-level) | Yes (lung UBERON:0002048) |
| Normalization | PHRED-scaled rank | Raw delta score | Quantile rank vs common variants (gnomAD v3, MAF > 0.01) |
| Captures ESE/ESS | No | No | Yes (via gene masking) |
| Captures chromatin effects | No | No | Yes (ATAC scorer) |

---

## 6. Interpretation

The discordant count (section 4.3) is not interpreted. The `GeneMaskSplicingScorer` returns a gene-body maximum set by the nearest canonical splice site rather than a variant-specific effect (AUDIT_RECORD.md:99-100), and its quantile ranks coding variants against a common-variant background (MAF > 0.01), which 58.4% of this cohort clears by construction. The 56 dual-mechanism variants identified in the earlier rescue analysis used the same scorer and the chromosome-22 calibration; they are retained as historical context and are not interpreted as a candidate set (docs/alphagenome_batch_report.md).

---

*Sources: CADD v1.7 GRCh38 via cadd.gs.washington.edu REST API. SpliceAI precomputed scores (version [NOT IN REPO]) via Ensembl VEP REST API (SpliceAI plugin). AlphaGenome v0.6.1 (client SDK) via Google DeepMind API. Analysis date: 2026-06-02. Corrected 2026-10-24: retracted interpretation of the 693 discordant group and of the 58 rescue group removed; SpliceAI version marked as not recorded.*