import json
import os
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.abspath(".agents/skills/claims-check/scripts"))
from claims_check import extract_claims, check_claim_support

class TestClaimsCheck(unittest.TestCase):
    def test_extract_claims(self):
        text = "Our proposed scheduler achieves a 45.01% latency reduction and maintains makespan of 1011.42 seconds."
        claims = extract_claims(text)
        self.assertGreaterEqual(len(claims), 1)
        self.assertIn(45.01, claims[0]["extracted_numbers"])

    def test_claim_support_match(self):
        claim = {"extracted_numbers": [45.01, 1011.42]}
        evidence = {"ledger_values": [45.01, 1011.42, 0.370]}
        sup, unsup = check_claim_support(claim, evidence)
        self.assertTrue(sup)
        self.assertEqual(len(unsup), 0)

    def test_claim_support_unsupported(self):
        claim = {"extracted_numbers": [99.99]}
        evidence = {"ledger_values": [45.01, 1011.42]}
        sup, unsup = check_claim_support(claim, evidence)
        self.assertFalse(sup)
        self.assertIn(99.99, unsup)
