import json
import os
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.abspath(".agents/skills/sim-validity-check/scripts"))
from sim_validity_check import audit_sim_validity

class TestSimValidityCheck(unittest.TestCase):
    def test_audit_phase1_runs(self):
        rep = audit_sim_validity("paper/runs", "paper/results.csv", min_seeds=10)
        self.assertEqual(rep["status"], "PASS")
        self.assertGreaterEqual(rep["runs_analyzed"], 30)
        for m, cnt in rep["seed_counts"].items():
            self.assertGreaterEqual(cnt, 10)
