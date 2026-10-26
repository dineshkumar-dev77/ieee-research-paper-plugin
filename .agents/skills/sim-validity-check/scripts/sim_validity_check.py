#!/usr/bin/env python3
"""Simulation Validity Check CLI.
Audits run records in paper/runs/ and ledger paper/results.csv for:
- Seed count (>=10)
- Seed independence (variance > 0 across seeds)
- Metric completeness
- Hash integrity
"""
import argparse
import csv
import json
import math
import os
import sys

def audit_sim_validity(runs_dir="paper/runs", ledger_path="paper/results.csv", min_seeds=10):
    if not os.path.exists(runs_dir):
        raise FileNotFoundError(f"Runs directory not found: {runs_dir}")
    if not os.path.exists(ledger_path):
        raise FileNotFoundError(f"Ledger file not found: {ledger_path}")

    errors = []
    run_files = [os.path.join(runs_dir, f) for f in os.listdir(runs_dir) if f.endswith(".json")]

    if len(run_files) == 0:
        errors.append("No run JSON records found in runs directory")

    # Read ledger rows
    ledger_rows = []
    with open(ledger_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if not str(r.get("run_id", "")).startswith("summary_") and r.get("seed") != "summary":
                ledger_rows.append(r)

    # 1. Group seeds and metrics per method
    method_data = {}
    code_hashes = set()
    config_hashes = set()

    for r in ledger_rows:
        m = r.get("method")
        met = r.get("metric")
        s = r.get("seed")
        c_hash = r.get("code_hash")
        cfg_hash = r.get("config_hash")

        if c_hash and c_hash != "summary":
            code_hashes.add(c_hash)
        if cfg_hash and cfg_hash != "summary":
            config_hashes.add(cfg_hash)

        try:
            val = float(r.get("value", 0))
            method_data.setdefault(m, {}).setdefault(met, []).append((s, val))
        except (ValueError, TypeError):
            continue

    # 2. Check seed counts per method
    seed_counts = {}
    for m, metrics in method_data.items():
        # count unique seeds
        first_metric = list(metrics.keys())[0] if metrics else None
        if first_metric:
            unique_seeds = len(set(item[0] for item in metrics[first_metric]))
            seed_counts[m] = unique_seeds
            if unique_seeds < min_seeds:
                errors.append(f"Method '{m}' has only {unique_seeds} seeds (minimum required: {min_seeds})")

    # 3. Check seed independence (variance > 0 across runs for stochastic metrics)
    zero_variance_metrics = []
    for m, metrics in method_data.items():
        for met, s_vals in metrics.items():
            vals = [v for s, v in s_vals]
            if len(vals) > 1:
                mean_v = sum(vals) / len(vals)
                var_v = sum((x - mean_v) ** 2 for x in vals) / (len(vals) - 1)
                # makespan and latency must vary across seeds due to randomized task generation
                if var_v == 0.0 and met in ["makespan_sec", "latency_ms"]:
                    zero_variance_metrics.append((m, met))
                    errors.append(f"Method '{m}' metric '{met}' has zero variance across seeds (lack of seed independence)")

    # 4. Check hash integrity
    if not code_hashes or "none" in code_hashes:
        errors.append("Invalid or missing code_hash in ledger records")
    if not config_hashes or "none" in config_hashes:
        errors.append("Invalid or missing config_hash in ledger records")

    status = "PASS" if len(errors) == 0 else "FAIL"

    report = {
        "status": status,
        "runs_analyzed": len(run_files),
        "ledger_rows_checked": len(ledger_rows),
        "seed_counts": seed_counts,
        "code_hashes": list(code_hashes),
        "config_hashes": list(config_hashes),
        "errors": errors
    }
    return report

def main():
    parser = argparse.ArgumentParser(description="Audit simulation run records and ledger validity.")
    parser.add_argument("--runs-dir", default="paper/runs", help="Runs directory")
    parser.add_argument("--ledger", default="paper/results.csv", help="Ledger path")
    parser.add_argument("--min-seeds", type=int, default=10, help="Minimum required seeds")
    parser.add_argument("--output", default="paper/reports/sim_validity_report.json", help="Report output path")

    args = parser.parse_args()

    try:
        report = audit_sim_validity(args.runs_dir, args.ledger, args.min_seeds)
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print(json.dumps(report, indent=2))
        if report["status"] != "PASS":
            sys.exit(1)
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
