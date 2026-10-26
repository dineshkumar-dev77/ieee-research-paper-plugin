import os
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.abspath(".agents/skills/citation_check/scripts"))
from citation_check import parse_citations

class TestCitationCheck(unittest.TestCase):
    def test_sequential_citations_pass(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tf:
            tf.write("""# Title
## I. Introduction
Cloud computing is transformative [1], requiring task scheduling [2]. In [3], heuristic models are studied.

## References
[1] Ref 1.
[2] Ref 2.
[3] Ref 3.
""")
            path = tf.name

        rep = parse_citations(path)
        os.remove(path)
        self.assertEqual(rep["status"], "PASS")

    def test_out_of_order_citation_fails(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tf:
            tf.write("""# Title
## I. Introduction
First cite is [2], then later [1].

## References
[1] Ref 1.
[2] Ref 2.
""")
            path = tf.name

        rep = parse_citations(path)
        os.remove(path)
        self.assertEqual(rep["status"], "FAIL")
        self.assertTrue(any("Citation order violation" in e for e in rep["errors"]))
