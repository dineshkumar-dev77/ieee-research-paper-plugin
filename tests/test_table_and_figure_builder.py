import json
import csv
import os
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.abspath(".agents/skills/table-builder/scripts"))
from table_builder import generate_ieee_table

sys.path.insert(0, os.path.abspath(".agents/skills/figure-builder/scripts"))
from figure_builder import generate_ieee_figure

class TestTableAndFigureBuilder(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.ledger = os.path.join(self.tmp_dir, "results.csv")
        self.venue = os.path.join(self.tmp_dir, "venue.json")

        cols = ["run_id", "metric", "value", "method", "workload", "seed", "config_hash", "code_hash", "env", "timestamp", "source_file"]
        with open(self.ledger, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(cols)
            for m in ["Adaptive-DynaSched", "Round-Robin"]:
                for s in range(1, 4):
                    w.writerow([f"r_{m}_{s}", "makespan_sec", 10.0 if "Adaptive" in m else 15.0, m, "w1", s, "a", "b", "c", "d", "e"])
                    w.writerow([f"r_{m}_{s}", "energy_kwh", 1.2 if "Adaptive" in m else 1.8, m, "w1", s, "a", "b", "c", "d", "e"])
                    w.writerow([f"r_{m}_{s}", "latency_ms", 120.0 if "Adaptive" in m else 180.0, m, "w1", s, "a", "b", "c", "d", "e"])
                    w.writerow([f"r_{m}_{s}", "sla_violation_pct", 2.0 if "Adaptive" in m else 8.0, m, "w1", s, "a", "b", "c", "d", "e"])

        with open(self.venue, "w") as f:
            json.dump({
                "layout": {"single_column_width_in": 3.5, "double_column_width_in": 7.16},
                "graphics": {"min_dpi": 300}
            }, f)

    def test_table_generation(self):
        t_dir = os.path.join(self.tmp_dir, "tables")
        res = generate_ieee_table(self.ledger, self.venue, output_dir=t_dir, table_number=1)
        self.assertEqual(res["status"], "success")
        self.assertTrue(os.path.exists(res["md_file"]))
        self.assertTrue(os.path.exists(res["tex_file"]))
        md_text = open(res["md_file"]).read()
        self.assertIn("TABLE I", md_text)
        self.assertIn("Adaptive-DynaSched", md_text)

    def test_figure_generation(self):
        f_dir = os.path.join(self.tmp_dir, "figures")
        res = generate_ieee_figure(self.ledger, self.venue, output_dir=f_dir, fig_number=1)
        self.assertEqual(res["status"], "success")
        self.assertTrue(os.path.exists(res["png_file"]))
        self.assertTrue(os.path.exists(res["pdf_file"]))
        self.assertIn("Fig. 1.", res["caption"])
