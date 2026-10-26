#!/usr/bin/env python3
"""Autonomous Benchmark Simulation Engine.
Implements reproducible simulation for cloud task-scheduling evaluation.
"""
import argparse
import hashlib
import json
import math
import os
import random
import sys
import time

class CloudNode:
    def __init__(self, node_id, mips, idle_power_w=80.0, peak_power_w=250.0):
        self.node_id = node_id
        self.mips = mips
        self.idle_power_w = idle_power_w
        self.peak_power_w = peak_power_w
        self.available_time = 0.0
        self.busy_time = 0.0

    def reset(self):
        self.available_time = 0.0
        self.busy_time = 0.0

class Task:
    def __init__(self, task_id, instructions, arrival_time, deadline):
        self.task_id = task_id
        self.instructions = instructions
        self.arrival_time = arrival_time
        self.deadline = deadline

def generate_workload(seed=42, task_count=1000, arrival_rate=1.0):
    rng = random.Random(seed)
    tasks = []
    curr_time = 0.0
    for i in range(task_count):
        inter_arrival = rng.expovariate(arrival_rate)
        curr_time += inter_arrival
        instructions = rng.uniform(500, 5000) * 1e6
        expected_exec_time = instructions / (2500 * 1e6)
        deadline = curr_time + expected_exec_time * rng.uniform(1.5, 3.5)
        tasks.append(Task(i, instructions, curr_time, deadline))
    return tasks

def create_nodes(node_count=16, seed=42):
    nodes = []
    for i in range(node_count):
        speed_category = i % 3
        if speed_category == 0:
            mips = 1500 * 1e6
            idle_p, peak_p = 50.0, 180.0
        elif speed_category == 1:
            mips = 2500 * 1e6
            idle_p, peak_p = 75.0, 240.0
        else:
            mips = 4000 * 1e6
            idle_p, peak_p = 100.0, 320.0
        nodes.append(CloudNode(i, mips, idle_p, peak_p))
    return nodes

def schedule_round_robin(tasks, nodes):
    latencies = []
    sla_violations = 0
    current_node_idx = 0

    for task in tasks:
        node = nodes[current_node_idx]
        current_node_idx = (current_node_idx + 1) % len(nodes)
        start_time = max(task.arrival_time, node.available_time)
        exec_duration = task.instructions / node.mips
        finish_time = start_time + exec_duration
        node.available_time = finish_time
        node.busy_time += exec_duration
        lat = finish_time - task.arrival_time
        latencies.append(lat)
        if finish_time > task.deadline:
            sla_violations += 1

    makespan = max(n.available_time for n in nodes)
    total_energy_kwh = sum(
        ((n.busy_time * n.peak_power_w) + ((makespan - n.busy_time) * n.idle_power_w)) / (3600.0 * 1000.0)
        for n in nodes
    )
    avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
    sla_pct = (sla_violations / len(tasks)) * 100.0 if tasks else 0.0

    return {
        "makespan_sec": round(makespan, 2),
        "energy_kwh": round(total_energy_kwh, 3),
        "latency_ms": round(avg_latency * 1000.0, 1),
        "sla_violation_pct": round(sla_pct, 2)
    }

def schedule_min_min(tasks, nodes):
    latencies = []
    sla_violations = 0
    sorted_tasks = sorted(tasks, key=lambda t: t.instructions)

    for task in sorted_tasks:
        best_node = None
        best_completion = float("inf")
        for node in nodes:
            start_time = max(task.arrival_time, node.available_time)
            finish_time = start_time + (task.instructions / node.mips)
            if finish_time < best_completion:
                best_completion = finish_time
                best_node = node
        start_time = max(task.arrival_time, best_node.available_time)
        exec_duration = task.instructions / best_node.mips
        finish_time = start_time + exec_duration
        best_node.available_time = finish_time
        best_node.busy_time += exec_duration
        lat = finish_time - task.arrival_time
        latencies.append(lat)
        if finish_time > task.deadline:
            sla_violations += 1

    makespan = max(n.available_time for n in nodes)
    total_energy_kwh = sum(
        ((n.busy_time * n.peak_power_w) + ((makespan - n.busy_time) * n.idle_power_w)) / (3600.0 * 1000.0)
        for n in nodes
    )
    avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
    sla_pct = (sla_violations / len(tasks)) * 100.0 if tasks else 0.0

    return {
        "makespan_sec": round(makespan, 2),
        "energy_kwh": round(total_energy_kwh, 3),
        "latency_ms": round(avg_latency * 1000.0, 1),
        "sla_violation_pct": round(sla_pct, 2)
    }

def schedule_adaptive_dynasched(tasks, nodes):
    latencies = []
    sla_violations = 0

    for task in tasks:
        best_node = None
        best_cost = float("inf")

        for node in nodes:
            start_time = max(task.arrival_time, node.available_time)
            exec_duration = task.instructions / node.mips
            finish_time = start_time + exec_duration
            
            l_cost = finish_time - task.arrival_time
            slack = task.deadline - finish_time
            urgency_penalty = 0.0 if slack >= 0 else abs(slack) * 4.0
            energy_penalty = (exec_duration * node.peak_power_w) / 1000.0
            
            total_cost = l_cost + urgency_penalty + (0.015 * energy_penalty)
            if total_cost < best_cost:
                best_cost = total_cost
                best_node = node

        start_time = max(task.arrival_time, best_node.available_time)
        exec_duration = task.instructions / best_node.mips
        finish_time = start_time + exec_duration
        best_node.available_time = finish_time
        best_node.busy_time += exec_duration
        lat = finish_time - task.arrival_time
        latencies.append(lat)
        if finish_time > task.deadline:
            sla_violations += 1

    makespan = max(n.available_time for n in nodes)
    total_energy_kwh = sum(
        ((n.busy_time * n.peak_power_w) + ((makespan - n.busy_time) * n.idle_power_w)) / (3600.0 * 1000.0)
        for n in nodes
    )
    avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
    sla_pct = (sla_violations / len(tasks)) * 100.0 if tasks else 0.0

    return {
        "makespan_sec": round(makespan, 2),
        "energy_kwh": round(total_energy_kwh, 3),
        "latency_ms": round(avg_latency * 1000.0, 1),
        "sla_violation_pct": round(sla_pct, 2)
    }

def run_simulation(method, seed=1, task_count=1000, node_count=16, arrival_rate=1.0):
    tasks = generate_workload(seed=seed, task_count=task_count, arrival_rate=arrival_rate)
    nodes = create_nodes(node_count=node_count, seed=seed)

    m = method.strip().lower().replace("_", "-")
    if m in ["adaptive-dynasched", "proposed"]:
        return schedule_adaptive_dynasched(tasks, nodes)
    elif m in ["round-robin", "rr"]:
        return schedule_round_robin(tasks, nodes)
    elif m in ["min-min", "minmin"]:
        return schedule_min_min(tasks, nodes)
    else:
        raise ValueError(f"Unknown simulation method: {method}")

def main():
    parser = argparse.ArgumentParser(description="Execute single benchmark run.")
    parser.add_argument("--method", required=True, help="Method name")
    parser.add_argument("--seed", type=int, default=1, help="Random seed")
    parser.add_argument("--tasks", type=int, default=1000, help="Task count")
    parser.add_argument("--nodes", type=int, default=16, help="Node count")
    parser.add_argument("--arrival-rate", type=float, default=1.0, help="Arrival rate")
    parser.add_argument("--output", help="Optional output JSON path")

    args = parser.parse_args()
    try:
        metrics = run_simulation(args.method, args.seed, args.tasks, args.nodes, args.arrival_rate)
        res = {
            "method": args.method,
            "seed": args.seed,
            "tasks": args.tasks,
            "nodes": args.nodes,
            "metrics": metrics
        }
        if args.output:
            os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(res, f, indent=2)
        print(json.dumps(res, indent=2))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
