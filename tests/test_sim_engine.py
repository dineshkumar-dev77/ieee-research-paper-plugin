#!/usr/bin/env python3
"""Unit tests for benchmark simulation engine."""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath("paper"))
from sim_engine import run_simulation, generate_workload, create_nodes

class TestSimEngine(unittest.TestCase):
    def test_workload_generation_deterministic(self):
        w1 = generate_workload(seed=42, task_count=50)
        w2 = generate_workload(seed=42, task_count=50)
        self.assertEqual(len(w1), 50)
        self.assertEqual(w1[0].instructions, w2[0].instructions)
        self.assertEqual(w1[0].arrival_time, w2[0].arrival_time)

    def test_node_creation(self):
        nodes = create_nodes(node_count=8, seed=42)
        self.assertEqual(len(nodes), 8)
        self.assertTrue(all(n.mips > 0 for n in nodes))

    def test_adaptive_dynasched_execution(self):
        res = run_simulation("Adaptive-DynaSched", seed=1, task_count=50, node_count=4)
        self.assertIn("makespan_sec", res)
        self.assertIn("energy_kwh", res)
        self.assertIn("latency_ms", res)
        self.assertIn("sla_violation_pct", res)
        self.assertGreater(res["makespan_sec"], 0)

    def test_baseline_execution(self):
        res_rr = run_simulation("Round-Robin", seed=1, task_count=50, node_count=4)
        res_mm = run_simulation("Min-Min", seed=1, task_count=50, node_count=4)
        self.assertGreater(res_rr["makespan_sec"], 0)
        self.assertGreater(res_mm["makespan_sec"], 0)

    def test_invalid_method_raises(self):
        with self.assertRaises(ValueError):
            run_simulation("NonExistentMethod", seed=1)

if __name__ == "__main__":
    unittest.main()
