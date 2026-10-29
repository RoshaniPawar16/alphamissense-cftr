#!/usr/bin/env python3
"""Recompute the benchmark without variants whose inventory name came only from a non-missense HGVSp.

Inputs are the existing benchmark cohort and the audit from
scripts/paper/p3h_inventory_audit.py. A variant is dropped when its short name
appears nowhere in the ClinVar VCF as a complete missense HGVSp token
(column a_name_only_from_nonmissense in benchmark_contamination_audit.csv).
Its CFTR2 label and AlphaMissense score still describe a genuine missense
change; it is dropped because it entered the inventory through a shortened
frameshift name, not through a ClinVar missense record.

Every statistic uses the same code path as the original:
  AUC and AP with bootstrap CI   scripts/paper/p3a_auc_ci.bootstrap_ci (2,000, seed 42)
  DeLong                         scripts/phase1_utils_delong.delong_test
  Calibration                    the ten equal-width bins and Brier score of p3b
  Class counts                   the AlphaMissense thresholds of p3f

A self-check first recomputes each statistic on the uncleaned cohort and
asserts it reproduces the committed file, so any difference in the _clean
files comes from the dropped variants alone.

Reads : results/phase1/benchmark_cohort_dedup.csv
        results/paper/benchmark_contamination_audit.csv
        results/paper/auc_ci.csv, results/phase1/delong_tests_dedup.csv,
        results/paper/calibration_n259.csv, results/paper/am_class_by_label.csv (self-check)
Writes: results/paper/auc_ci_clean.csv
        results/paper/delong_tests_clean.csv
        results/paper/calibration_clean.csv
        results/paper/am_class_by_label_clean.csv

Usage:
    python scripts/paper/p3i_benchmark_clean.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import brier_score_loss

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "paper"))
sys.path.insert(0, str(ROOT / "scripts"))
from p3a_auc_ci import N_BOOT, SEED, TOOLS, bootstrap_ci  # noqa: E402
from phase1_utils_delong import delong_test  # noqa: E402

COHORT = ROOT / "results/phase1/benchmark_cohort_dedup.csv"
AUDIT = ROOT / "results/paper/benchmark_contamination_audit.csv"
OUT = ROOT / "results/paper"
LB_MAX, LP_MIN = 0.34, 0.564
N_BINS = 10


def auc_rows(df: pd.DataFrame) -> pd.DataFrame:
    """AUC and AP with bootstrap CI: four tools on the included rows, AlphaMissense on all."""
    rows = []
    four = df[df["included"]].reset_index(drop=True)
    for col, tool in TOOLS.items():
        r = bootstrap_ci(four["label"].to_numpy(), four[col].to_numpy(dtype=float), N_BOOT, SEED)
        rows.append(("four_tool", tool, len(four), *r))
    r = bootstrap_ci(df["label"].to_numpy(), df["am_pathogenicity"].to_numpy(dtype=float), N_BOOT, SEED)
    rows.append(("am_validation", "AlphaMissense", len(df), *r))
    return pd.DataFrame(rows, columns=["cohort", "tool", "n", "auc", "auc_ci_lo", "auc_ci_hi",
                                       "ap", "ap_ci_lo", "ap_ci_hi", "n_boot_valid"]).round(6)


def delong_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Paired DeLong tests of each comparator against AlphaMissense on the included rows."""
    four = df[df["included"]]
    y = four["label"].to_numpy()
    am = four["am_pathogenicity"].to_numpy(dtype=float)
    rows = []
    for col, tool in [("polyphen_score", "PolyPhen"), ("cadd_phred", "CADD"), ("sift_score_inv", "SIFT")]:
        auc_a, auc_b, z, p = delong_test(y, am, four[col].to_numpy(dtype=float))
        rows.append(("AlphaMissense", tool, round(auc_a, 6), round(auc_b, 6), len(four), round(z, 4), round(p, 6)))
    return pd.DataFrame(rows, columns=["tool_a", "tool_b", "auc_a", "auc_b", "n", "z", "p"])


def calibration_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Ten equal-width reliability bins plus Brier scores, as in p3b."""
    y = df["label"].to_numpy(dtype=float)
    p = df["am_pathogenicity"].to_numpy(dtype=float)
    edges = np.linspace(0.0, 1.0, N_BINS + 1)
    idx = np.clip(np.digitize(p, edges[1:-1], right=False), 0, N_BINS - 1)
    rows = []
    for b in range(N_BINS):
        s = idx == b
        rows.append({"bin": b + 1, "bin_lo": round(edges[b], 2), "bin_hi": round(edges[b + 1], 2),
                     "n": int(s.sum()), "n_pos": int(y[s].sum()),
                     "mean_predicted": round(float(p[s].mean()), 6) if s.any() else None,
                     "observed_fraction_positive": round(float(y[s].mean()), 6) if s.any() else None})
    base = float(y.mean())
    ece = sum(abs(y[idx == b].mean() - p[idx == b].mean()) * (idx == b).sum()
              for b in range(N_BINS) if (idx == b).any()) / len(y)
    rows += [{"bin": "brier_score", "n": len(y), "observed_fraction_positive": round(float(brier_score_loss(y, p)), 6)},
             {"bin": "brier_score_base_rate_model", "n": len(y), "observed_fraction_positive": round(float(np.mean((y - base) ** 2)), 6)},
             {"bin": "expected_calibration_error", "n": len(y), "observed_fraction_positive": round(float(ece), 6)},
             {"bin": "base_rate", "n": len(y), "observed_fraction_positive": round(base, 6)}]
    return pd.DataFrame(rows)


def class_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Labelled variants by AlphaMissense class, as in p3f."""
    cls = np.where(df["am_pathogenicity"] < LB_MAX, "likely_benign",
                   np.where(df["am_pathogenicity"] > LP_MIN, "likely_pathogenic", "ambiguous"))
    rows = []
    for c in ("likely_benign", "ambiguous", "likely_pathogenic"):
        s = df[cls == c]
        rows.append({"am_class": c, "n_labelled": len(s), "n_cf_causing": int(s["label"].sum()),
                     "n_non_cf_causing": int((s["label"] == 0).sum())})
    return pd.DataFrame(rows)


def self_check(df: pd.DataFrame) -> None:
    """Assert that the uncleaned cohort reproduces the committed results."""
    a = auc_rows(df).set_index(["cohort", "tool"])
    ref = pd.read_csv(OUT / "auc_ci.csv")
    for r in ref.itertuples():
        key = ("four_tool" if r.cohort == "four_tool_dedup" else "am_validation", r.tool)
        assert abs(a.loc[key, "auc"] - r.auc) < 1e-6 and abs(a.loc[key, "auc_ci_lo"] - r.auc_ci_lo) < 1e-6, key
    d = delong_rows(df)
    dref = pd.read_csv(ROOT / "results/phase1/delong_tests_dedup.csv")
    assert np.allclose(d["z"].to_numpy(), dref["z"].to_numpy(), atol=1e-4)
    c = calibration_rows(df).set_index("bin")
    cref = pd.read_csv(OUT / "calibration_n259.csv").set_index("bin")
    assert abs(c.loc["brier_score", "observed_fraction_positive"]
               - float(cref.loc["brier_score", "observed_fraction_positive"])) < 1e-6
    k = class_rows(df).set_index("am_class")
    kref = pd.read_csv(OUT / "am_class_by_label.csv").set_index("am_class")
    assert (k["n_labelled"] == kref["n_labelled"]).all() and (k["n_cf_causing"] == kref["n_cf_causing"]).all()
    print("self-check: the uncleaned cohort reproduces auc_ci, delong_tests_dedup, calibration and class counts")


def main() -> None:
    """Drop the flagged variants, recompute, and write the _clean files."""
    cohort = pd.read_csv(COHORT)
    audit = pd.read_csv(AUDIT)
    drop = set(audit.loc[audit["a_name_only_from_nonmissense"], "variant"])
    self_check(cohort)
    clean = cohort[~cohort["variant"].isin(drop)].reset_index(drop=True)
    print(f"dropped {len(drop)}: {sorted(drop)}; {len(cohort)} -> {len(clean)} "
          f"({int(clean['included'].sum())} with all four scores)")

    note = f"dropped: {'; '.join(sorted(drop))}"
    for name, frame in [("auc_ci_clean", auc_rows(clean)), ("delong_tests_clean", delong_rows(clean)),
                        ("calibration_clean", calibration_rows(clean)),
                        ("am_class_by_label_clean", class_rows(clean))]:
        frame["note"] = note
        frame.to_csv(OUT / f"{name}.csv", index=False)
        print(f"\n{name}\n{frame.drop(columns='note').to_string(index=False)}")


if __name__ == "__main__":
    main()
