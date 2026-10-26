import json
import os
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.abspath(".agents/skills/experiment-planner/scripts"))
from experiment_planner import DEFAULT_PAPER_PLAN, validate_plan, save_plan, load_plan

class TestExperimentPlanner(unittest.TestCase):
    def test_default_plan_schema(self):
        valid, msg = validate_plan(DEFAULT_PAPER_PLAN)
        self.assertTrue(valid, msg)
        self.assertEqual(DEFAULT_PAPER_PLAN["seeds"]["count"], 10)
        self.assertEqual(DEFAULT_PAPER_PLAN["methods"]["proposed"], "Adaptive-DynaSched")
        self.assertIn("Round-Robin", DEFAULT_PAPER_PLAN["methods"]["baselines"])

    def test_save_and_load_plan(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            path = tf.name
        save_plan(path, DEFAULT_PAPER_PLAN)
        loaded = load_plan(path)
        self.assertEqual(loaded["title"], DEFAULT_PAPER_PLAN["title"])
        os.remove(path)
