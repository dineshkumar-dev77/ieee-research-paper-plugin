#!/usr/bin/env python3
"""Simulation Runner CLI.
Runs smoke test, executes benchmark seeds, supports resume, saves records to paper/runs/,
and populates paper/results.csv.
"""
import argparse
import csv
import hashlib
import json
import os
import platform
import sys
import time

def compute_file_hash(path):
    if not os.path.exists(path):
        return "none"
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()[:12]

def run_smoke_test(sim_engine_path="paper/sim_engine.py"):
    sys.path.insert(0, os.path.dirname(os.path.abspath(sim_engine_path)))
    from sim_engine import run_simulation
    for m in ["Adaptive-DynaSched", "Round-Robin", "Min-Min"]:
        res = run_simulation(m, seed=999, task_count=20, node_count=4)
        if not res or "makespan_sec" not in res:
            raise RuntimeError(f"Smoke test failed for method: {m}")
    return True

def run_experiment(
    config_path="paper/paper.json",
    sim_engine_path="paper/sim_engine.py",
    runs_dir="paper/runs",
    ledger_path="paper/results.csv",
    force_rerun=False
):
    with open(config_path, "r", encoding="utf-8") as f:
        plan = json.load(f)

    sys.path.insert(0, os.path.dirname(os.path.abspath(sim_engine_path)))
    from sim_engine import run_simulation

    os.makedirs(runs_dir, exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(ledger_path)), exist_ok=True)

    code_hash = compute_file_hash(sim_engine_path)
    config_hash = compute_file_hash(config_path)
    env_str = f"Python {platform.python_version()} - {platform.system()} {platform.machine()}"

    methods = [plan["methods"]["proposed"]] + plan["methods"]["baselines"]
    workload = plan["workloads"][0]["name"] if plan.get("workloads") else "default_workload"
    task_count = plan["workloads"][0].get("task_count", 1000) if plan.get("workloads") else 1000
    node_count = plan["workloads"][0].get("node_count", 16) if plan.get("workloads") else 16
    seeds = plan["seeds"]["list"]

    # Initialize results.csv if not exists
    required_cols = ["run_id", "metric", "value", "method", "workload", "seed", "config_hash", "code_hash", "env", "timestamp", "source_file"]
    if not os.path.exists(ledger_path) or os.path.getsize(ledger_path) == 0:
        with open(ledger_path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(required_cols)

    # Check existing runs to support resume
    existing_run_ids = set()
    with open(ledger_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_run_ids.add((row.get("method"), row.get("seed"), row.get("workload")))

    completed_count = 0
    resumed_count = 0
    all_new_rows = []

    for method in methods:
        method_slug = method.lower().replace(" ", "_").replace("-", "_")
        for seed in seeds:
            run_key = (method, str(seed), workload)
            run_file_name = f"run_{method_slug}_s{seed}.json"
            run_file_path = os.path.join(runs_dir, run_file_name)

            if not force_rerun and (run_key in existing_run_ids or os.path.exists(run_file_path)):
                resumed_count += 1
                continue

            # Execute run
            t_start = time.time()
            metrics = run_simulation(
                method=method,
                seed=seed,
                task_count=task_count,
                node_count=node_count
            )
            t_elapsed = time.time() - t_start
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            run_id = f"run_{method_slug}_s{seed}_{int(t_start)}"
            record = {
                "run_id": run_id,
                "method": method,
                "seed": seed,
                "workload": workload,
                "task_count": task_count,
                "node_count": node_count,
                "metrics": metrics,
                "elapsed_sec": round(t_elapsed, 4),
                "timestamp": timestamp,
                "code_hash": code_hash,
                "config_hash": config_hash,
                "env": env_str
            }

            with open(run_file_path, "w", encoding="utf-8") as rf:
                json.dump(record, rf, indent=2)

            # Prepare ledger rows
            for m_name, m_val in metrics.items():
                row = [
                    run_id,
                    m_name,
                    m_val,
                    method,
                    workload,
                    seed,
                    config_hash,
                    code_hash,
                    env_str,
                    timestamp,
                    run_file_path
                ]
                all_new_rows.append(row)

            completed_count += 1

    if all_new_rows:
        with open(ledger_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for r in all_new_rows:
                writer.writerow(r)

    return {
        "status": "success",
        "completed_runs": completed_count,
        "resumed_runs": resumed_count,
        "total_planned": len(methods) * len(seeds),
        "ledger": ledger_path
    }

def main():
    parser = argparse.ArgumentParser(description="Execute experiments with smoke test and resume.")
    parser.add_argument("--smoke-test", action="store_true", help="Run smoke test first")
    parser.add_argument("--run-all", action="store_true", help="Run all planned seeds")
    parser.add_argument("--config", default="paper/paper.json", help="Path to paper.json")
    parser.add_argument("--sim-engine", default="paper/sim_engine.py", help="Path to sim_engine.py")
    parser.add_argument("--runs-dir", default="paper/runs", help="Directory to save run records")
    parser.add_argument("--ledger", default="paper/results.csv", help="Path to results.csv")
    parser.add_argument("--force-rerun", action="store_true", help="Force rerun even if records exist")

    args = parser.parse_args()

    try:
        if args.smoke_test:
            run_smoke_test(args.sim_engine)
            print(json.dumps({"smoke_test": "PASSED"}))
            if not args.run_all:
                sys.exit(0)

        res = run_experiment(
            config_path=args.config,
            sim_engine_path=args.sim_engine,
            runs_dir=args.runs_dir,
            ledger_path=args.ledger,
            force_rerun=args.force_rerun
        )
        print(json.dumps(res, indent=2))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
