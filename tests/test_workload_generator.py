import json
import os
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.abspath(".agents/skills/workload-generator/scripts"))
from workload_generator import generate_workload_specs

class TestWorkloadGenerator(unittest.TestCase):
    def test_generate_workload_specs(self):
        specs = generate_workload_specs(task_count=1000, node_count=16, arrival_lambda=1.0)
        self.assertEqual(specs["task_count"], 1000)
        self.assertEqual(specs["node_count"], 16)
        self.assertEqual(specs["default_arrival_lambda"], 1.0)
        self.assertGreaterEqual(len(specs["sweeps"]), 3)
