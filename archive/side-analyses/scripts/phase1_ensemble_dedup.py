"""
Ensemble (AlphaMissense + CADD + PolyPhen) on the deduplicated benchmark cohort.

Added 2026-10-24. This reproduces notebooks/ensemble.ipynb cell 9 exactly:

    pipe = Pipeline([("scaler", StandardScaler()),
                     ("clf", LogisticRegression(max_iter=1000, random_state=42))])
    cv   = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    ensemble_probs = cross_val_predict(pipe, X, y, cv=cv, method="predict_proba")[:, 1]

and cell 13 (pipe.fit(X, y) for the reported coefficients), but reads the
deduplicated cohort instead of re-fetching CADD from the API.

Difference from scripts/phase1_benchmark.py: the notebook fits StandardScaler
inside each CV fold (Pipeline); phase1_benchmark.py fits it once on the full
set before CV. Both are kept; this file records the notebook's form.

Input:  results/phase1/benchmark_cohort_dedup.csv (default; --cohort to override)
Output: results/phase1/ensemble_metrics_dedup.csv (default; --out to override)

Deduplication is asserted BEFORE StratifiedKFold is constructed: the script
exits with an error if any `variant` appears more than once among included rows.
"""

import os, csv, sys, logging, argparse
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score, average_precision_score

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('--cohort', default=os.path.join(ROOT, 'results', 'phase1', 'benchmark_cohort_dedup.csv'))
ap.add_argument('--out',    default=os.path.join(ROOT, 'results', 'phase1', 'ensemble_metrics_dedup.csv'))
args = ap.parse_args()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

with open(args.cohort) as f:
    rows = [r for r in csv.DictReader(f) if r['included'] == 'True']

# ── Assert deduplication precedes fold assignment ────────────────────────────
variants = [r['variant'] for r in rows]
dupes = {v for v in variants if variants.count(v) > 1}
if dupes:
    log.error('Input is not deduplicated: %d variants repeated (%s ...). Refusing to run.',
              len(dupes), sorted(dupes)[:5])
    sys.exit(1)
log.info('Input %s: %d included rows, %d unique variants (deduplicated before CV)',
         os.path.basename(args.cohort), len(rows), len(set(variants)))

y    = np.array([int(r['label']) for r in rows])
am   = np.array([float(r['am_pathogenicity']) for r in rows])
cadd = np.array([float(r['cadd_phred']) for r in rows])
pp   = np.array([float(r['polyphen_score']) for r in rows])
n, n_pos = len(y), int(y.sum())
n_neg = n - n_pos

# ── ensemble.ipynb cell 9 ────────────────────────────────────────────────────
features = ['am_pathogenicity', 'polyphen_score', 'cadd_score']
X = np.column_stack([am, pp, cadd])

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', LogisticRegression(max_iter=1000, random_state=42)),
])
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
ensemble_probs = cross_val_predict(pipe, X, y, cv=cv, method='predict_proba')[:, 1]

ensemble_auc = roc_auc_score(y, ensemble_probs)
ensemble_ap  = average_precision_score(y, ensemble_probs)
am_auc       = roc_auc_score(y, am)
am_ap        = average_precision_score(y, am)

# ── ensemble.ipynb cell 13 (full-data fit for coefficients) ──────────────────
pipe.fit(X, y)
coefs = dict(zip(features, pipe.named_steps['clf'].coef_[0]))

log.info('AlphaMissense alone  AUC=%.4f AP=%.4f', am_auc, am_ap)
log.info('Ensemble (CV)        AUC=%.4f AP=%.4f', ensemble_auc, ensemble_ap)
log.info('Coefficients: %s', {k: round(v, 4) for k, v in coefs.items()})

out_rows = [
    {'model': 'AlphaMissense_alone', 'auc': round(am_auc, 6), 'ap': round(am_ap, 6),
     'n': n, 'n_pos': n_pos, 'n_neg': n_neg,
     'note': 'raw am_pathogenicity, in-sample (no fitting)'},
    {'model': 'Ensemble_CV', 'auc': round(ensemble_auc, 6), 'ap': round(ensemble_ap, 6),
     'n': n, 'n_pos': n_pos, 'n_neg': n_neg,
     'note': ('ensemble.ipynb cell 9: Pipeline(StandardScaler, LogisticRegression(max_iter=1000, random_state=42)); '
              'StratifiedKFold(5, shuffle=True, random_state=42); cross_val_predict predict_proba; '
              'dedup asserted before fold assignment; '
              f"coef_am={coefs['am_pathogenicity']:.4f}_pp={coefs['polyphen_score']:.4f}_cadd={coefs['cadd_score']:.4f}")},
]
with open(args.out, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['model', 'auc', 'ap', 'n', 'n_pos', 'n_neg', 'note'])
    w.writeheader()
    w.writerows(out_rows)
log.info('Saved %s', args.out)
