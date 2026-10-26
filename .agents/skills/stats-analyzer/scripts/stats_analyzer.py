#!/usr/bin/env python3
"""Statistical Analyzer CLI.
Computes mean, std, 95% CI, Welch'''s t-test, Cohen'''s d from paper/results.csv
and appends summary metrics back to the ledger.
"""
import argparse
import csv
import json
import math
import os
import sys
import time

# Student t-distribution critical values for 95% two-sided CI (df: 1 to 30)
T_CRIT_95 = {
    1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571,
    6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
    11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131,
    16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086,
    21: 2.080, 22: 2.074, 23: 2.069, 24: 2.064, 25: 2.060,
    26: 2.056, 27: 2.052, 28: 2.048, 29: 2.045, 30: 2.042
}

def get_t_crit(df):
    int_df = max(1, int(round(df)))
    if int_df in T_CRIT_95:
        return T_CRIT_95[int_df]
    if int_df > 30:
        return 1.960
    return 2.262

def compute_t_pvalue(t_stat, df):
    """Approximate two-tailed p-value from t-statistic using normal/polynomial approximation."""
    x = abs(t_stat)
    # Hill (1970) / Abramowitz & Stegun approximation
    w = x / math.sqrt(df)
    z = (math.log(1.0 + w * w) * (df - 0.5) / 2.0)
    z = math.sqrt(2.0 * z) if z > 0 else 0.0
    # Complementary error function approximation for standard normal
    p_norm = 0.5 * math.erfc(z / math.sqrt(2.0))
    p_val = max(1e-6, min(1.0, 2.0 * p_norm))
    return p_val

def compute_stats_for_sample(values):
    n = len(values)
    if n == 0:
        return None
    mean = sum(values) / n
    if n > 1:
        var = sum((x - mean) ** 2 for x in values) / (n - 1)
        std = math.sqrt(var)
    else:
        var = 0.0
        std = 0.0

    se = std / math.sqrt(n) if n > 0 else 0.0
    t_val = get_t_crit(n - 1 if n > 1 else 1)
    ci95_low = mean - (t_val * se)
    ci95_high = mean + (t_val * se)

    return {
        "n": n,
        "mean": round(mean, 3),
        "std": round(std, 3),
        "se": round(se, 3),
        "ci95_low": round(ci95_low, 3),
        "ci95_high": round(ci95_high, 3),
        "raw_values": values
    }

def welch_t_test(s1, s2):
    """Welch'''s two-sample t-test (assumes unequal variances)."""
    n1, m1, v1 = s1["n"], s1["mean"], (s1["std"] ** 2)
    n2, m2, v2 = s2["n"], s2["mean"], (s2["std"] ** 2)

    se_diff = math.sqrt((v1 / n1) + (v2 / n2)) if (v1/n1 + v2/n2) > 0 else 1e-9
    t_stat = (m1 - m2) / se_diff

    # Welch-Satterthwaite df
    num = ((v1 / n1) + (v2 / n2)) ** 2
    den = (((v1 / n1) ** 2) / (n1 - 1)) + (((v2 / n2) ** 2) / (n2 - 1)) if n1 > 1 and n2 > 1 else 1.0
    df = num / den if den > 0 else 1.0

    p_val = compute_t_pvalue(t_stat, df)

    # Cohen'''s d
    pooled_var = (((n1 - 1) * v1) + ((n2 - 1) * v2)) / (n1 + n2 - 2) if (n1 + n2 - 2) > 0 else 1.0
    pooled_sd = math.sqrt(pooled_var) if pooled_var > 0 else 1e-9
    cohens_d = (m1 - m2) / pooled_sd

    return {
        "t_statistic": round(t_stat, 3),
        "df": round(df, 1),
        "p_value": round(p_val, 4),
        "cohens_d": round(cohens_d, 3)
    }

def analyze_ledger(ledger_path="paper/results.csv", append_to_ledger=True):
    if not os.path.exists(ledger_path):
        raise FileNotFoundError(f"Ledger file not found: {ledger_path}")

    # Read existing raw records (skip any existing summary rows)
    raw_rows = []
    with open(ledger_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if not str(r.get("run_id", "")).startswith("summary_") and r.get("seed") != "summary":
                raw_rows.append(r)

    # Group by (metric, workload, method)
    groups = {}
    for r in raw_rows:
        metric = r["metric"]
        workload = r["workload"]
        method = r["method"]
        try:
            val = float(r["value"])
        except ValueError:
            continue
        key = (metric, workload, method)
        groups.setdefault(key, []).append(val)

    summary_results = {}
    for (metric, workload, method), vals in groups.items():
        summary_results.setdefault((metric, workload), {})[method] = compute_stats_for_sample(vals)

    # Compute comparative significance against baselines
    comparisons = []
    for (metric, workload), method_dict in summary_results.items():
        proposed = None
        for m in method_dict:
            if "adaptive" in m.lower() or "proposed" in m.lower():
                proposed = m
                break
        if not proposed and len(method_dict) > 0:
            proposed = list(method_dict.keys())[0]

        for m, stats in method_dict.items():
            if m != proposed:
                test_res = welch_t_test(method_dict[proposed], stats)
                pct_improvement = ((stats["mean"] - method_dict[proposed]["mean"]) / stats["mean"]) * 100.0 if stats["mean"] != 0 else 0.0
                comparisons.append({
                    "metric": metric,
                    "workload": workload,
                    "proposed_method": proposed,
                    "baseline_method": m,
                    "pct_improvement": round(pct_improvement, 2),
                    **test_res
                })

    # Prepare summary rows to append back to ledger
    new_ledger_rows = []
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    for (metric, workload), method_dict in summary_results.items():
        for method, stats in method_dict.items():
            # Mean
            new_ledger_rows.append({
                "run_id": f"summary_{method}_{metric}_mean",
                "metric": f"{metric}_mean",
                "value": stats["mean"],
                "method": method,
                "workload": workload,
                "seed": "summary",
                "config_hash": "summary",
                "code_hash": "summary",
                "env": "stats-analyzer",
                "timestamp": timestamp,
                "source_file": "paper/reports/stats_summary.json"
            })
            # Std
            new_ledger_rows.append({
                "run_id": f"summary_{method}_{metric}_std",
                "metric": f"{metric}_std",
                "value": stats["std"],
                "method": method,
                "workload": workload,
                "seed": "summary",
                "config_hash": "summary",
                "code_hash": "summary",
                "env": "stats-analyzer",
                "timestamp": timestamp,
                "source_file": "paper/reports/stats_summary.json"
            })
            # CI95
            new_ledger_rows.append({
                "run_id": f"summary_{method}_{metric}_ci95_low",
                "metric": f"{metric}_ci95_low",
                "value": stats["ci95_low"],
                "method": method,
                "workload": workload,
                "seed": "summary",
                "config_hash": "summary",
                "code_hash": "summary",
                "env": "stats-analyzer",
                "timestamp": timestamp,
                "source_file": "paper/reports/stats_summary.json"
            })
            new_ledger_rows.append({
                "run_id": f"summary_{method}_{metric}_ci95_high",
                "metric": f"{metric}_ci95_high",
                "value": stats["ci95_high"],
                "method": method,
                "workload": workload,
                "seed": "summary",
                "config_hash": "summary",
                "code_hash": "summary",
                "env": "stats-analyzer",
                "timestamp": timestamp,
                "source_file": "paper/reports/stats_summary.json"
            })

    for comp in comparisons:
        new_ledger_rows.append({
            "run_id": f"summary_{comp['proposed_method']}_vs_{comp['baseline_method']}_{comp['metric']}_pct_improvement",
            "metric": f"{comp['metric']}_pct_improvement_vs_{comp['baseline_method']}",
            "value": comp["pct_improvement"],
            "method": comp['proposed_method'],
            "workload": comp["workload"],
            "seed": "summary",
            "config_hash": "summary",
            "code_hash": "summary",
            "env": "stats-analyzer",
            "timestamp": timestamp,
            "source_file": "paper/reports/stats_summary.json"
        })
        new_ledger_rows.append({
            "run_id": f"summary_{comp['proposed_method']}_vs_{comp['baseline_method']}_{comp['metric']}_p_val",
            "metric": f"{comp['metric']}_p_value_vs_{comp['baseline_method']}",
            "value": comp["p_value"],
            "method": comp['proposed_method'],
            "workload": comp["workload"],
            "seed": "summary",
            "config_hash": "summary",
            "code_hash": "summary",
            "env": "stats-analyzer",
            "timestamp": timestamp,
            "source_file": "paper/reports/stats_summary.json"
        })

    if append_to_ledger and new_ledger_rows:
        cols = ["run_id", "metric", "value", "method", "workload", "seed", "config_hash", "code_hash", "env", "timestamp", "source_file"]
        with open(ledger_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for r in new_ledger_rows:
                writer.writerow([r.get(c, "") for c in cols])

    # Build report object
    report = {
        "timestamp": timestamp,
        "metrics_analyzed": list(set(k[0] for k in summary_results.keys())),
        "workloads": list(set(k[1] for k in summary_results.keys())),
        "summaries": {f"{k[0]}::{k[1]}": v for k, v in summary_results.items()},
        "comparisons": comparisons,
        "summary_ledger_rows_added": len(new_ledger_rows)
    }

    return report

def main():
    parser = argparse.ArgumentParser(description="Analyze ledger statistics.")
    parser.add_argument("--ledger", default="paper/results.csv", help="Path to results.csv")
    parser.add_argument("--output", default="paper/reports/stats_summary.json", help="Path to output JSON")
    parser.add_argument("--no-append", action="store_true", help="Do not append summary rows to ledger")

    args = parser.parse_args()

    try:
        report = analyze_ledger(args.ledger, append_to_ledger=(not args.no_append))
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        # Markdown report
        md_path = os.path.splitext(args.output)[0] + ".md"
        with open(md_path, "w", encoding="utf-8") as mf:
            mf.write("# Statistical Analysis Report\n\n")
            mf.write(f"Analyzed on: {report['timestamp']}\n\n")
            for comp in report.get("comparisons", []):
                mf.write(f"- **{comp['metric']}**: {comp['proposed_method']} vs {comp['baseline_method']}: ")
                mf.write(f"Improvement = {comp['pct_improvement']}%, p-value = {comp['p_value']}, Cohen's d = {comp['cohens_d']}\n")

        print(json.dumps({
            "status": "success",
            "report_json": args.output,
            "report_md": md_path,
            "summary_rows_added": report["summary_ledger_rows_added"]
        }, indent=2))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
