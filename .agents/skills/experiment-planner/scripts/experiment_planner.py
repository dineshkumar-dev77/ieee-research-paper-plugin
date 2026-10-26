#!/usr/bin/env python3
"""Experiment Planner CLI.
Formulates research questions, metrics, baselines, sweeps, and seed configurations in paper/paper.json.
"""
import argparse
import json
import os
import sys

DEFAULT_PAPER_PLAN = {
    "title": "Adaptive Dynamic Scheduling for Heterogeneous Cloud Workloads",
    "domain": "cloud_task_scheduling",
    "research_questions": [
        {
            "id": "RQ1",
            "question": "How does Adaptive-DynaSched compare to heuristic baselines in makespan and latency?",
            "primary_metric": "makespan_sec",
            "methods": ["Adaptive-DynaSched", "Round-Robin", "Min-Min"]
        },
        {
            "id": "RQ2",
            "question": "What is the energy efficiency impact across heterogeneous cloud clusters?",
            "primary_metric": "energy_kwh",
            "methods": ["Adaptive-DynaSched", "Round-Robin", "Min-Min"]
        },
        {
            "id": "RQ3",
            "question": "How effectively does adaptive allocation maintain SLA guarantees under arrival variance?",
            "primary_metric": "sla_violation_pct",
            "methods": ["Adaptive-DynaSched", "Round-Robin", "Min-Min"]
        }
    ],
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
        {"name": "heterogeneous_cloud_1000_tasks", "task_count": 1000, "node_count": 16}
    ],
    "seeds": {
        "count": 10,
        "list": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    },
    "parameter_sweeps": {
        "task_arrival_rate": [1.0, 2.0, 5.0]
    },
    "ablations": [
        {"name": "No-DynamicAdjustment", "description": "Adaptive-DynaSched with static weights"}
    ]
}

def load_plan(path="paper/paper.json"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Plan file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_plan(path, data):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def validate_plan(data):
    required = ["research_questions", "methods", "metrics", "workloads", "seeds"]
    for r in required:
        if r not in data:
            return False, f"Missing required field: {r}"
    if not data["methods"].get("proposed"):
        return False, "Missing methods.proposed"
    if not isinstance(data["methods"].get("baselines"), list) or len(data["methods"]["baselines"]) < 1:
        return False, "At least one baseline required"
    seed_count = data["seeds"].get("count", 0)
    if seed_count < 1:
        return False, "Seed count must be at least 1"
    return True, "Valid"

def main():
    parser = argparse.ArgumentParser(description="Plan experiments in paper/paper.json.")
    parser.add_argument("--init", action="store_true", help="Initialize paper/paper.json with default plan")
    parser.add_argument("--config", default="paper/paper.json", help="Path to paper.json")
    parser.add_argument("--seeds", type=int, default=10, help="Number of seeds (default 10, recommended 10-30)")
    parser.add_argument("--proposed", help="Proposed method name")
    parser.add_argument("--baselines", nargs="+", help="Baseline method names")
    parser.add_argument("--validate", action="store_true", help="Validate plan schema")
    parser.add_argument("--output", help="Optional output path")

    args = parser.parse_args()

    try:
        if args.init:
            plan = dict(DEFAULT_PAPER_PLAN)
            if args.seeds:
                plan["seeds"] = {
                    "count": args.seeds,
                    "list": list(range(1, args.seeds + 1))
                }
            if args.proposed:
                plan["methods"]["proposed"] = args.proposed
            if args.baselines:
                plan["methods"]["baselines"] = args.baselines
            target = args.output if args.output else args.config
            save_plan(target, plan)
            print(json.dumps({"status": "initialized", "config": target, "seeds": plan["seeds"]["count"]}))
            sys.exit(0)

        data = load_plan(args.config)

        if args.validate:
            valid, msg = validate_plan(data)
            if not valid:
                print(json.dumps({"error": msg}), file=sys.stderr)
                sys.exit(1)
            print(json.dumps({"status": "valid", "config": args.config}))
            sys.exit(0)

        print(json.dumps(data, indent=2))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
