import json
import os
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.abspath(".agents/skills/sim-runner/scripts"))
from sim_runner import run_smoke_test, run_experiment

class TestSimRunner(unittest.TestCase):
    def test_smoke_test(self):
        res = run_smoke_test("paper/sim_engine.py")
        self.assertTrue(res)

    def test_runner_execution_and_resume(self):
        tmp_dir = tempfile.mkdtemp()
        plan_file = os.path.join(tmp_dir, "paper.json")
        runs_dir = os.path.join(tmp_dir, "runs")
        ledger_file = os.path.join(tmp_dir, "results.csv")

        plan = {
            "methods": {"proposed": "Adaptive-DynaSched", "baselines": ["Round-Robin"]},
            "workloads": [{"name": "test_w", "task_count": 20, "node_count": 4}],
            "seeds": {"count": 2, "list": [1, 2]}
        }
        with open(plan_file, "w") as f:
            json.dump(plan, f)

        # Run 1
        res1 = run_experiment(
            config_path=plan_file,
            sim_engine_path="paper/sim_engine.py",
            runs_dir=runs_dir,
            ledger_path=ledger_file
        )
        self.assertEqual(res1["completed_runs"], 4)
        self.assertEqual(res1["resumed_runs"], 0)

        # Run 2 (resume should detect all existing runs)
        res2 = run_experiment(
            config_path=plan_file,
            sim_engine_path="paper/sim_engine.py",
            runs_dir=runs_dir,
            ledger_path=ledger_file
        )
        self.assertEqual(res2["completed_runs"], 0)
        self.assertEqual(res2["resumed_runs"], 4)
