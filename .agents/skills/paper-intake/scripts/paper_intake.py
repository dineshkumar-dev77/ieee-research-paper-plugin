#!/usr/bin/env python3
"""Paper Intake CLI.
Ingests author requirements or paper draft, filling missing parameters with
reproducible domain simulation defaults per Guardrail 7.
"""
import argparse
import json
import os
import sys

HISTORICAL_CLOUD_DEFAULTS = {
    "title": "Adaptive Dynamic Scheduling for Heterogeneous Cloud Workloads",
    "domain": "cloud_task_scheduling",
    "methods": {
        "proposed": "Adaptive-DynaSched",
        "baselines": ["Round-Robin", "Min-Min"]
    },
    "metrics": [
        {"name": "makespan_sec", "unit": "seconds", "direction": "lower_is_better"},
        {"name": "energy_kwh", "unit": "kWh", "direction": "lower_is_better"},
        {"name": "latency_ms", "unit": "ms", "direction": "lower_is_better"},
        {"name": "sla_violation_pct", "unit": "%", "direction": "lower_is_better"}
    ],
    "workloads": [
        {
            "name": "heterogeneous_cloud_1000_tasks",
            "task_count": 1000,
            "node_count": 16,
            "arrival_rate_lambda": 1.0,
            "instruction_range_mips": [500, 5000],
            "heterogeneity_classes": 3
        }
    ],
    "system_parameters": {
        "cluster_nodes": 16,
        "mips_profiles": [1500, 2500, 4000],
        "idle_power_w": [50.0, 75.0, 100.0],
        "peak_power_w": [180.0, 240.0, 320.0]
    },
    "seeds": {
        "count": 10,
        "list": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }
}

def fill_missing_parameters(existing_data):
    merged = dict(HISTORICAL_CLOUD_DEFAULTS)
    if not existing_data:
        return merged

    for key, val in existing_data.items():
        if isinstance(val, dict) and key in merged and isinstance(merged[key], dict):
            sub = dict(merged[key])
            sub.update(val)
            merged[key] = sub
        elif val:
            merged[key] = val
    return merged

def main():
    parser = argparse.ArgumentParser(description="Ingest paper specifications and fill missing fields.")
    parser.add_argument("--config", default="paper/paper.json", help="Path to paper.json")
    parser.add_argument("--domain", default="cloud_task_scheduling", help="Research domain")
    parser.add_argument("--input-json", help="Optional author input JSON file")
    parser.add_argument("--output", help="Optional output path")

    args = parser.parse_args()

    try:
        existing = {}
        if args.input_json and os.path.exists(args.input_json):
            with open(args.input_json, "r", encoding="utf-8") as f:
                existing = json.load(f)
        elif os.path.exists(args.config):
            with open(args.config, "r", encoding="utf-8") as f:
                existing = json.load(f)

        filled = fill_missing_parameters(existing)
        target = args.output if args.output else args.config
        os.makedirs(os.path.dirname(os.path.abspath(target)), exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            json.dump(filled, f, indent=2)

        print(json.dumps({
            "status": "success",
            "config": target,
            "domain": filled["domain"],
            "methods_count": 1 + len(filled["methods"]["baselines"]),
            "seeds_count": filled["seeds"]["count"]
        }, indent=2))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
