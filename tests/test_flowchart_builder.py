import json
import os
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.abspath(".agents/skills/flowchart-builder/scripts"))
from flowchart_builder import render_architecture_diagram

class TestFlowchartBuilder(unittest.TestCase):
    def test_render_architecture_diagram(self):
        tmp_dir = tempfile.mkdtemp()
        res = render_architecture_diagram(output_dir=tmp_dir, fig_number=2, width_in=3.5, dpi=600)
        self.assertEqual(res["status"], "success")
        self.assertTrue(os.path.exists(res["png_file"]))
        self.assertTrue(os.path.exists(res["pdf_file"]))
        self.assertTrue(os.path.exists(res["mmd_file"]))
        self.assertIn("Fig. 2.", res["caption"])
