import json
import os
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.abspath(".agents/skills/paper-intake/scripts"))
from paper_intake import fill_missing_parameters, HISTORICAL_CLOUD_DEFAULTS

class TestPaperIntake(unittest.TestCase):
    def test_fill_missing_from_empty(self):
        filled = fill_missing_parameters({})
        self.assertEqual(filled["domain"], "cloud_task_scheduling")
        self.assertEqual(filled["seeds"]["count"], 10)
        self.assertIn("Adaptive-DynaSched", filled["methods"]["proposed"])

    def test_preserve_author_overrides(self):
        custom = {"title": "Custom Cloud Title", "seeds": {"count": 15, "list": list(range(1, 16))}}
        filled = fill_missing_parameters(custom)
        self.assertEqual(filled["title"], "Custom Cloud Title")
        self.assertEqual(filled["seeds"]["count"], 15)
        self.assertEqual(len(filled["seeds"]["list"]), 15)
