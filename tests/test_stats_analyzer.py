import csv
import json
import os
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.abspath(".agents/skills/stats-analyzer/scripts"))
from stats_analyzer import compute_stats_for_sample, welch_t_test, analyze_ledger

class TestStatsAnalyzer(unittest.TestCase):
    def test_compute_stats_sample(self):
        vals = [10.0, 12.0, 11.0, 13.0, 14.0]
        stats = compute_stats_for_sample(vals)
        self.assertEqual(stats["n"], 5)
        self.assertEqual(stats["mean"], 12.0)
        self.assertAlmostEqual(stats["std"], 1.581, places=2)
        self.assertLess(stats["ci95_low"], 12.0)
        self.assertGreater(stats["ci95_high"], 12.0)

    def test_welch_t_test(self):
        s1 = compute_stats_for_sample([10, 11, 12, 10, 11])
        s2 = compute_stats_for_sample([20, 21, 22, 20, 21])
        res = welch_t_test(s1, s2)
        self.assertLess(res["t_statistic"], 0)
        self.assertLess(res["p_value"], 0.05)
        self.assertNotEqual(res["cohens_d"], 0)
