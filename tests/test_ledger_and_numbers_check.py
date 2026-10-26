import csv
import os
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.abspath(".agents/skills/results-ledger/scripts"))
from ledger_manager import init_ledger, validate_ledger, append_rows, REQUIRED_COLUMNS
from numbers_check import extract_candidate_numbers, is_close_match, verify_manuscript

class TestLedgerAndNumbersCheck(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.ledger_file = os.path.join(self.tmp_dir, "results.csv")
        self.manuscript_file = os.path.join(self.tmp_dir, "manuscript.md")

    def test_ledger_init_and_validate(self):
        init_ledger(self.ledger_file)
        valid, msg = validate_ledger(self.ledger_file)
        self.assertTrue(valid, msg)

    def test_append_and_query(self):
        init_ledger(self.ledger_file)
        row = {
            "run_id": "test_1",
            "metric": "makespan_sec",
            "value": 42.15,
            "method": "Adaptive-DynaSched",
            "workload": "test_w",
            "seed": 1,
            "config_hash": "abc",
            "code_hash": "def",
            "env": "test_env",
            "timestamp": "2026-10-25",
            "source_file": "test.json"
        }
        append_rows(self.ledger_file, [row])
        valid, msg = validate_ledger(self.ledger_file)
        self.assertTrue(valid)

    def test_numbers_check_pass_and_fail(self):
        init_ledger(self.ledger_file)
        append_rows(self.ledger_file, [{
            "run_id": "test_1",
            "metric": "makespan_sec",
            "value": 42.15,
            "method": "Adaptive-DynaSched",
            "workload": "test_w",
            "seed": 1,
            "config_hash": "abc",
            "code_hash": "def",
            "env": "test_env",
            "timestamp": "2026-10-25",
            "source_file": "test.json"
        }])

        # Valid manuscript
        valid_text = """
# IV. Experimental Results
Our evaluation demonstrates that Adaptive-DynaSched achieves an average makespan of 42.15 seconds.
"""
        with open(self.manuscript_file, "w") as f:
            f.write(valid_text)

        matched, unmatched = verify_manuscript(self.manuscript_file, self.ledger_file)
        self.assertEqual(len(unmatched), 0)
        self.assertEqual(len(matched), 1)

        # Invalid manuscript with tampered number 99.99
        invalid_text = """
# IV. Experimental Results
Our evaluation demonstrates that Adaptive-DynaSched achieves an average makespan of 99.99 seconds.
"""
        with open(self.manuscript_file, "w") as f:
            f.write(invalid_text)

        matched_inv, unmatched_inv = verify_manuscript(self.manuscript_file, self.ledger_file)
        self.assertEqual(len(unmatched_inv), 1)
        self.assertEqual(unmatched_inv[0]["value"], 99.99)
