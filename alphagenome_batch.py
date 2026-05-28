"""
Batch AlphaGenome query for 7 unclassified CFTR variants.
Run with: .venv/bin/python alphagenome_batch.py
"""

import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from alphagenome.data import genome
from alphagenome.models import dna_client

load_dotenv()
API_KEY = os.environ.get('ALPHAGENOME_API_KEY', '')
if not API_KEY:
    raise RuntimeError("Set ALPHAGENOME_API_KEY in .env")

# All 7 unclassified CFTR variants — canonical SNV per protein change
VARIANTS = [
    dict(label='Leu49Pro',   protein='L49P',   chrom='chr7', pos=117_504_345, ref='T', alt='C', am=0.9757),
    dict(label='Arg104Gly',  protein='R104G',  chrom='chr7', pos=117_530_935, ref='A', alt='G', am=0.8448),
    dict(label='Pro355Leu',  protein='P355L',  chrom='chr7', pos=117_540_294, ref='C', alt='T', am=0.8580),
    dict(label='Phe650Leu',  protein='F650L',  chrom='chr7', pos=117_592_115, ref='T', alt='C', am=0.8455),
    dict(label='Leu986Pro',  protein='L986P',  chrom='chr7', pos=117_606_722, ref='T', alt='C', am=0.8685),
    dict(label='His1054Gln', protein='H1054Q', chrom='chr7', pos=117_611_603, ref='T', alt='G', am=0.9010),
    dict(label='Arg1097Cys', protein='R1097C', chrom='chr7', pos=117_611_730, ref='C', alt='T', am=0.6513),
]

ONTOLOGY_TERMS = ['UBERON:0002048']
REQUESTED_OUTPUTS = [
    dna_client.OutputType.RNA_SEQ,
    dna_client.OutputType.ATAC,
    dna_client.OutputType.SPLICE_SITE_USAGE,
]
HALF = dna_client.SEQUENCE_LENGTH_1MB // 2


def summarise(ref, alt, label):
    r = ref.values.astype(np.float32)
    a = alt.values.astype(np.float32)
    lfc = np.log2(a + 1e-8) - np.log2(r + 1e-8)
    return {
        f'{label}_mean_abs_log2fc': float(np.abs(lfc).mean()),
        f'{label}_max_abs_log2fc': float(np.abs(lfc).max()),
        f'{label}_bins_gt05':      int((np.abs(lfc) > 0.5).sum()),
    }


print(f"Connecting to AlphaGenome API...")
model = dna_client.create(API_KEY)
print("Connected.\n")

rows = []
for v in VARIANTS:
    print(f"→ {v['label']} ({v['protein']})  chr7:{v['pos']:,}  {v['ref']}>{v['alt']}")
    variant = genome.Variant(
        chromosome=v['chrom'],
        position=v['pos'],
        reference_bases=v['ref'],
        alternate_bases=v['alt'],
    )
    interval = genome.Interval(
        chromosome=v['chrom'],
        start=v['pos'] - HALF,
        end=v['pos'] + HALF,
    )
    try:
        outputs = model.predict_variant(
            interval=interval,
            variant=variant,
            ontology_terms=ONTOLOGY_TERMS,
            requested_outputs=REQUESTED_OUTPUTS,
        )
        row = {
            'Variant':  v['label'],
            'Protein':  v['protein'],
            'Position': f"chr7:{v['pos']:,}",
            'REF>ALT':  f"{v['ref']}>{v['alt']}",
            'AM_score': v['am'],
        }
        row.update(summarise(outputs.reference.rna_seq,          outputs.alternate.rna_seq,          'rna'))
        row.update(summarise(outputs.reference.atac,             outputs.alternate.atac,             'atac'))
        row.update(summarise(outputs.reference.splice_site_usage, outputs.alternate.splice_site_usage, 'splice'))
        rows.append(row)
        print(f"   RNA  mean|lfc|={row['rna_mean_abs_log2fc']:.4f}  max={row['rna_max_abs_log2fc']:.4f}  bins>{0.5}={row['rna_bins_gt05']}")
        print(f"   ATAC mean|lfc|={row['atac_mean_abs_log2fc']:.4f}  max={row['atac_max_abs_log2fc']:.4f}  bins>{0.5}={row['atac_bins_gt05']}")
        print(f"   SPL  mean|lfc|={row['splice_mean_abs_log2fc']:.4f}  max={row['splice_max_abs_log2fc']:.4f}  bins>{0.5}={row['splice_bins_gt05']}\n")
    except Exception as e:
        print(f"   ERROR: {e}\n")
        rows.append({'Variant': v['label'], 'Protein': v['protein'], 'AM_score': v['am'], 'error': str(e)})

df = pd.DataFrame(rows)
df.to_csv('alphagenome_batch_results.csv', index=False)
print("Raw results saved to alphagenome_batch_results.csv")

# ── Ranked summary tables ─────────────────────────────────────────────────────
clean = df[df.get('error', pd.Series([None]*len(df))).isna()].copy() if 'error' in df.columns else df.copy()

atac_ranked   = clean.sort_values('atac_max_abs_log2fc',   ascending=False)
splice_ranked = clean.sort_values('splice_max_abs_log2fc', ascending=False)

# ── Markdown report ───────────────────────────────────────────────────────────
md_lines = [
    "# AlphaGenome Batch Analysis: 7 Unclassified CFTR Variants",
    "",
    "**Model:** AlphaGenome v0.6.1  |  **Genome:** hg38  |  **Tissue:** Lung (UBERON:0002048)",
    "**Outputs:** RNA-seq, ATAC-seq, Splice site usage  |  **Window:** 1 Mb centred on variant",
    "",
    "---",
    "",
    "## Variants Queried",
    "",
    "| Variant | Protein | hg38 Position | REF>ALT | AlphaMissense |",
    "|---------|---------|---------------|---------|---------------|",
]
for v in VARIANTS:
    md_lines.append(f"| {v['label']} | {v['protein']} | chr7:{v['pos']:,} | {v['ref']}>{v['alt']} | {v['am']} |")

md_lines += [
    "",
    "---",
    "",
    "## Raw Results per Output Type",
    "",
    "### RNA-seq (Gene Expression)",
    "",
    "| Variant | Mean \\|log2FC\\| | Max \\|log2FC\\| | Bins >0.5 |",
    "|---------|----------------|----------------|-----------|",
]
for _, r in df.iterrows():
    if 'error' not in r or pd.isna(r.get('error')):
        md_lines.append(f"| {r['Variant']} | {r['rna_mean_abs_log2fc']:.4f} | {r['rna_max_abs_log2fc']:.4f} | {r['rna_bins_gt05']} |")

md_lines += [
    "",
    "### ATAC-seq (Chromatin Accessibility)",
    "",
    "| Variant | Mean \\|log2FC\\| | Max \\|log2FC\\| | Bins >0.5 |",
    "|---------|----------------|----------------|-----------|",
]
for _, r in df.iterrows():
    if 'error' not in r or pd.isna(r.get('error')):
        md_lines.append(f"| {r['Variant']} | {r['atac_mean_abs_log2fc']:.4f} | {r['atac_max_abs_log2fc']:.4f} | {r['atac_bins_gt05']} |")

md_lines += [
    "",
    "### Splice Site Usage",
    "",
    "| Variant | Mean \\|log2FC\\| | Max \\|log2FC\\| | Bins >0.5 |",
    "|---------|----------------|----------------|-----------|",
]
for _, r in df.iterrows():
    if 'error' not in r or pd.isna(r.get('error')):
        md_lines.append(f"| {r['Variant']} | {r['splice_mean_abs_log2fc']:.4f} | {r['splice_max_abs_log2fc']:.4f} | {r['splice_bins_gt05']} |")

md_lines += [
    "",
    "---",
    "",
    "## Ranked: Strongest ATAC-seq Signal",
    "",
    "Sorted by Max |log2FC| — chromatin accessibility changes that may indicate disrupted enhancers or regulatory elements.",
    "",
    "| Rank | Variant | AM Score | ATAC Max \\|log2FC\\| | ATAC Bins >0.5 | Regulatory flag |",
    "|------|---------|----------|---------------------|----------------|-----------------|",
]
for rank, (_, r) in enumerate(atac_ranked.iterrows(), 1):
    flag = "⚠️ strong regulatory signal" if r['atac_max_abs_log2fc'] > 5 else ("moderate" if r['atac_max_abs_log2fc'] > 1 else "low")
    md_lines.append(f"| {rank} | {r['Variant']} | {r['AM_score']} | {r['atac_max_abs_log2fc']:.3f} | {r['atac_bins_gt05']} | {flag} |")

md_lines += [
    "",
    "---",
    "",
    "## Ranked: Strongest Splice Site Signal",
    "",
    "Sorted by Max |log2FC| — variants most likely to disrupt splicing in ways AlphaMissense cannot detect.",
    "",
    "| Rank | Variant | AM Score | Splice Max \\|log2FC\\| | Splice Bins >0.5 | Splicing flag |",
    "|------|---------|----------|-----------------------|------------------|---------------|",
]
for rank, (_, r) in enumerate(splice_ranked.iterrows(), 1):
    flag = "⚠️ cryptic splice risk" if r['splice_max_abs_log2fc'] > 0.5 else "low"
    md_lines.append(f"| {rank} | {r['Variant']} | {r['AM_score']} | {r['splice_max_abs_log2fc']:.4f} | {r['splice_bins_gt05']} | {flag} |")

md_lines += [
    "",
    "---",
    "",
    "## Key Findings: What AlphaMissense Misses",
    "",
    "AlphaMissense scores protein-level pathogenicity only. AlphaGenome adds:",
    "",
    "- **ATAC-seq outliers**: variants predicted to remodel chromatin — may disrupt intronic enhancers, CTCF binding sites, or DHS peaks in airway epithelium even when the amino acid change itself is tolerated.",
    "- **Splice site usage shifts**: variants within or near exon boundaries that alter donor/acceptor strength, enabling cryptic exon inclusion or exon skipping — invisible to protein-sequence models.",
    "",
    "### Variants of highest interest (regulatory/splicing signal beyond protein effect):",
    "",
]

# Highlight top ATAC and top splice
top_atac = atac_ranked.iloc[0]
top_splice = splice_ranked.iloc[0]

md_lines += [
    f"- **{top_atac['Variant']}** — highest ATAC max |log2FC| = {top_atac['atac_max_abs_log2fc']:.3f}, "
    f"{top_atac['atac_bins_gt05']} bins >0.5. AlphaMissense score {top_atac['AM_score']} — "
    f"regulatory disruption may contribute independently of protein misfolding.",
    "",
    f"- **{top_splice['Variant']}** — highest splice site max |log2FC| = {top_splice['splice_max_abs_log2fc']:.4f}, "
    f"{top_splice['splice_bins_gt05']} bins >0.5. Possible cryptic splicing effect "
    f"that AlphaMissense (score {top_splice['AM_score']}) would not capture.",
    "",
]

# Special note on R1097C — lowest AM score, most likely to have non-protein mechanism
r1097c = df[df['Protein'] == 'R1097C'].iloc[0] if 'R1097C' in df['Protein'].values else None
if r1097c is not None and 'error' not in r1097c:
    md_lines += [
        f"- **Arg1097Cys** — lowest AlphaMissense score (0.6513, borderline likely pathogenic). "
        f"ATAC max |log2FC| = {r1097c['atac_max_abs_log2fc']:.3f}, splice max = {r1097c['splice_max_abs_log2fc']:.4f}. "
        f"If regulatory or splicing signal is elevated here, it provides a mechanistic explanation "
        f"that protein-level scoring alone cannot.",
        "",
    ]

md_lines += [
    "---",
    "",
    "*AlphaGenome v0.6.1 · hg38 · Lung UBERON:0002048 · 2026-05-28*",
]

report = "\n".join(md_lines)
with open('alphagenome_batch_report.md', 'w') as f:
    f.write(report)

print("\nMarkdown report saved to alphagenome_batch_report.md")
print("\n=== ATAC-seq ranking ===")
print(atac_ranked[['Variant','AM_score','atac_max_abs_log2fc','atac_bins_gt05']].to_string(index=False))
print("\n=== Splice site ranking ===")
print(splice_ranked[['Variant','AM_score','splice_max_abs_log2fc','splice_bins_gt05']].to_string(index=False))
