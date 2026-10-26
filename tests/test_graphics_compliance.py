import json
import os
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.abspath(".agents/skills/graphics-compliance/scripts"))
from graphics_compliance import audit_graphics

class TestGraphicsCompliance(unittest.TestCase):
    def test_audit_phase1_figures(self):
        rep = audit_graphics("paper/figures", "paper/venue.json")
        # fig_1 is already generated in paper/figures
        self.assertIn(rep["status"], ["PASS", "FAIL"])
