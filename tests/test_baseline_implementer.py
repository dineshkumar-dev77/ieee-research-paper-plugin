import json
import os
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.abspath(".agents/skills/baseline-implementer/scripts"))
from baseline_implementer import audit_baselines

class TestBaselineImplementer(unittest.TestCase):
    def test_audit_actual_sim_engine(self):
        rep = audit_baselines("paper/sim_engine.py", "paper/paper.json")
        self.assertEqual(rep["status"], "PASS")
        self.assertTrue(rep["online_arrival_realistic"])
        self.assertTrue(rep["heterogeneity_supported"])
        self.assertEqual(len(rep["missing_methods"]), 0)
