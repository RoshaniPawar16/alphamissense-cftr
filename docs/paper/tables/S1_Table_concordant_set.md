# S1 Table. The concordant set

Variants flagged by both AlphaGenome and SpliceAI among the 1,278
AlphaMissense-ambiguous CFTR missense SNVs. Two definitions are reported.
GM: AlphaGenome gene-mask SPLICE quantile > 0.95 and SpliceAI maximum delta
> 0.5 (n = 18). CM: AlphaGenome centre-mask splice score in the top 5% of
the 1,278 and SpliceAI maximum delta > 0.5 (n = 13). The CM set is a subset
of the GM set, so the union is 18 variants. Rows are ordered by genomic
position.

| Protein change | Position (hg38) | Domain | Exon / intron | Distance to splice site (bp) | AlphaMissense | AlphaGenome SPLICE raw | AlphaGenome SPLICE quantile | SpliceAI delta | SpliceAI type | gnomAD v4 max AF | CFTR2 status | In minigene benchmark | GM | CM |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R55T | 117,504,363 G>C | MSD1 | [NOT IN REPO] | [NOT IN REPO] | 0.5030 | 0.3516 | 0.999860 | 0.62 | DL | absent from gnomAD v4 | no CFTR2 record | no | yes | yes |
| R55I | 117,504,363 G>T | MSD1 | [NOT IN REPO] | [NOT IN REPO] | 0.4688 | 0.7256 | 0.999965 | 0.77 | DL | absent from gnomAD v4 | no CFTR2 record | no | yes | yes |
| A155G | 117,531,089 C>G | MSD1 | [NOT IN REPO] | [NOT IN REPO] | 0.3573 | 0.7616 | 0.999974 | 0.99 | DG | absent from gnomAD v4 | no CFTR2 record | no | yes | yes |
| K163R | 117,531,113 A>G | MSD1 | [NOT IN REPO] | [NOT IN REPO] | 0.4000 | 0.6080 | 0.999946 | 0.74 | DL | absent from gnomAD v4 | no CFTR2 record | no | yes | yes |
| L214V | 117,535,308 C>G | MSD1 | [NOT IN REPO] | [NOT IN REPO] | 0.3424 | 0.0156 | 0.974892 | 0.64 | DG | 7.52e-06 | no CFTR2 record | no | yes | – |
| K464R | 117,548,822 A>G | NBD1 | [NOT IN REPO] | [NOT IN REPO] | 0.5491 | 0.7791 | 0.999978 | 0.68 | DL | absent from gnomAD v4 | no CFTR2 record | no | yes | yes |
| H620Q | 117,592,027 T>G | NBD1 | [NOT IN REPO] | [NOT IN REPO] | 0.4167 | 0.6210 | 0.999950 | 0.73 | AG | absent from gnomAD v4 | No interpretation available | no | yes | – |
| I906S | 117,603,591 T>G | MSD2 | [NOT IN REPO] | [NOT IN REPO] | 0.4729 | 0.3789 | 0.999870 | 0.96 | DG | 6.84e-07 | no CFTR2 record | no | yes | yes |
| G970C | 117,603,782 G>T | MSD2 | [NOT IN REPO] | [NOT IN REPO] | 0.4905 | 0.7616 | 0.999974 | 0.86 | DL | absent from gnomAD v4 | no CFTR2 record | no | yes | yes |
| G970V | 117,606,674 G>T | MSD2 | [NOT IN REPO] | [NOT IN REPO] | 0.4400 | 0.1875 | 0.999663 | 0.95 | AL | absent from gnomAD v4 | no CFTR2 record | yes (positive) | yes | yes |
| E1046V | 117,610,667 A>T | MSD2 | [NOT IN REPO] | [NOT IN REPO] | 0.3702 | 0.2383 | 0.999760 | 0.67 | DG | 1.37e-06 | no CFTR2 record | no | yes | yes |
| G1047C | 117,610,669 G>T | MSD2 | [NOT IN REPO] | [NOT IN REPO] | 0.3415 | 0.5293 | 0.999927 | 0.96 | DL | absent from gnomAD v4 | No interpretation available | no | yes | yes |
| P1050L | 117,611,590 C>T | MSD2 | [NOT IN REPO] | [NOT IN REPO] | 0.4886 | 0.7576 | 0.999973 | 0.81 | AG | absent from gnomAD v4 | no CFTR2 record | no | yes | yes |
| S1058G | 117,611,613 A>G | MSD2 | [NOT IN REPO] | [NOT IN REPO] | 0.5075 | 0.8007 | 0.999982 | 1.00 | AG | absent from gnomAD v4 | no CFTR2 record | no | yes | – |
| S1058C | 117,611,613 A>T | MSD2 | [NOT IN REPO] | [NOT IN REPO] | 0.4728 | 0.0664 | 0.998506 | 0.55 | AG | absent from gnomAD v4 | no CFTR2 record | no | yes | – |
| K1060T | 117,611,620 A>C | MSD2 | [NOT IN REPO] | [NOT IN REPO] | 0.4693 | 0.0898 | 0.999005 | 0.66 | AG | absent from gnomAD v4 | No interpretation available | no | yes | – |
| G1123V | 117,614,613 G>T | MSD2 | [NOT IN REPO] | [NOT IN REPO] | 0.4466 | 0.5215 | 0.999924 | 0.77 | AL | 6.91e-07 | no CFTR2 record | no | yes | yes |
| L1156F | 117,614,713 G>T | MSD2 | [NOT IN REPO] | [NOT IN REPO] | 0.3913 | 0.2383 | 0.999760 | 0.71 | DL | 4.01e-04 | no CFTR2 record | no | yes | yes |

**Cell sources.** Protein change, position, reference and alternate allele,
AlphaGenome SPLICE raw and quantile: `results/alphagenome/alphagenome_full_cftr_results.csv`.
Centre-mask splice score: `results/alphagenome/rescore_centermask.csv`, column
`cm_splice_501`. SpliceAI delta and the four channel scores:
`results/comparator_scores.csv`, columns `SpliceAI_max_delta`,
`SpliceAI_DS_AG`, `SpliceAI_DS_AL`, `SpliceAI_DS_DG`, `SpliceAI_DS_DL`.
AlphaMissense score: `results/alphagenome/alphagenome_full_cftr_results.csv`,
column `am_pathogenicity`. gnomAD v4 maximum allele frequency:
`results/gnomad_cftr_lookup.csv`, column `gnomad_max_af`; "absent from gnomAD v4"
means the lookup returned no record. CFTR2 status:
`data/cftr2_results_annotated.csv`, column `determination_2026`, matched on
`am_variant`. Minigene membership: `results/experimental_benchmark.csv`,
column `minigene_result`. Domain: residue number against the CFTR domain
boundaries used in `scripts/alphamissense_analysis.py` line 146.
Full table with every column: `results/paper/concordant_set.csv`.

**[NOT IN REPO] columns.** Exon or intron and distance to the nearest splice site
cannot be filled: the repository holds no CFTR exon-boundary annotation, no GTF
and no BED file, and no script computes either quantity for this cohort. The
`dist_bp` column of `results/experimental_benchmark.csv` covers only the 23
minigene variants and has no generating script.

Generated by `scripts/paper/p4_tables.py`.
