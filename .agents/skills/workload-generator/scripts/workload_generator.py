#!/usr/bin/env python3
"""Workload Generator CLI.
Generates reproducible cloud benchmark workload metadata and parameter sweeps in paper/workloads.json.
"""
import argparse
import json
import math
import os
import random
import sys

def generate_workload_specs(task_count=1000, node_count=16, arrival_lambda=1.0, seed=42):
    rng = random.Random(seed)
    
    # Statistical parameters of the workload
    task_types = [
        {"tier": "Standard", "share": 0.6, "slack_factor_range": [2.0, 3.5]},
        {"tier": "High_Priority", "share": 0.3, "slack_factor_range": [1.2, 2.0]},
        {"tier": "Best_Effort", "share": 0.1, "slack_factor_range": [3.5, 5.0]}
    ]

    sweeps = [
        {"arrival_rate_lambda": 0.5, "intensity": "low"},
        {"arrival_rate_lambda": 1.0, "intensity": "nominal"},
        {"arrival_rate_lambda": 2.0, "intensity": "high"}
    ]

    workload_profile = {
        "workload_name": f"heterogeneous_cloud_{task_count}_tasks",
        "task_count": task_count,
        "node_count": node_count,
        "default_arrival_lambda": arrival_lambda,
        "instruction_distribution": {
            "type": "bounded_uniform",
            "min_mips": 500,
            "max_mips": 5000,
            "unit": "million_instructions"
        },
        "sla_tiers": task_types,
        "sweeps": sweeps,
        "cluster_heterogeneity": {
            "node_categories": [
                {"type": "General_Compute", "mips": 1500, "share": 0.375},
                {"type": "Compute_Optimized", "mips": 2500, "share": 0.375},
                {"type": "High_Performance", "mips": 4000, "share": 0.25}
            ]
        },
        "seed_reproducibility": {
            "base_seed": seed,
            "generator": "Mersenne_Twister_Python_random"
        }
    }

    return workload_profile

def main():
    parser = argparse.ArgumentParser(description="Generate benchmark workload profile and sweeps.")
    parser.add_argument("--tasks", type=int, default=1000, help="Task count")
    parser.add_argument("--nodes", type=int, default=16, help="Node count")
    parser.add_argument("--lambda-rate", type=float, default=1.0, help="Poisson arrival rate")
    parser.add_argument("--seed", type=int, default=42, help="Workload seed")
    parser.add_argument("--output", default="paper/workloads.json", help="Output path")

    args = parser.parse_args()

    try:
        specs = generate_workload_specs(args.tasks, args.nodes, args.lambda_rate, args.seed)
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(specs, f, indent=2)

        print(json.dumps({
            "status": "success",
            "workload_file": args.output,
            "task_count": specs["task_count"],
            "node_count": specs["node_count"],
            "sla_tiers": len(specs["sla_tiers"])
        }, indent=2))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
