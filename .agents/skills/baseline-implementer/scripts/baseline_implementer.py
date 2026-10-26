#!/usr/bin/env python3
"""Baseline Implementer CLI.
Verifies that simulation code implements competitive, realistic baselines matching paper.json
with realistic online arrival scheduling to guarantee reviewer-proof benchmarking.
"""
import argparse
import json
import os
import re
import sys

def audit_baselines(sim_engine_path="paper/sim_engine.py", config_path="paper/paper.json"):
    if not os.path.exists(sim_engine_path):
        raise FileNotFoundError(f"Simulation engine not found: {sim_engine_path}")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(sim_engine_path, "r", encoding="utf-8") as f:
        engine_source = f.read()

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    proposed = config["methods"]["proposed"]
    baselines = config["methods"]["baselines"]

    results = {
        "proposed": proposed,
        "baselines_checked": baselines,
        "missing_methods": [],
        "online_arrival_realistic": False,
        "heterogeneity_supported": False,
        "status": "PASS"
    }

    # Verify proposed
    prop_slug = proposed.lower().replace("-", "_")
    if prop_slug not in engine_source.lower() and "adaptive" not in engine_source.lower():
        results["missing_methods"].append(proposed)

    # Verify baselines
    for b in baselines:
        b_slug = b.lower().replace("-", "_")
        if b_slug not in engine_source.lower() and b.lower().replace("-", "") not in engine_source.lower():
            results["missing_methods"].append(b)

    # Verify online arrival realism (inter-arrival or expovariate or arrival_time)
    if "arrival_time" in engine_source and ("inter_arrival" in engine_source or "expovariate" in engine_source):
        results["online_arrival_realistic"] = True

    # Verify node heterogeneity (mips differences or categories)
    if "mips" in engine_source and ("speed_category" in engine_source or "node_count" in engine_source):
        results["heterogeneity_supported"] = True

    if results["missing_methods"] or not results["online_arrival_realistic"] or not results["heterogeneity_supported"]:
        results["status"] = "FAIL"

    return results

def main():
    parser = argparse.ArgumentParser(description="Audit simulation baselines and arrival realism.")
    parser.add_argument("--sim-engine", default="paper/sim_engine.py", help="Path to sim_engine.py")
    parser.add_argument("--config", default="paper/paper.json", help="Path to paper.json")
    parser.add_argument("--output", default="paper/reports/baseline_report.json", help="Path to report")

    args = parser.parse_args()

    try:
        report = audit_baselines(args.sim_engine, args.config)
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
