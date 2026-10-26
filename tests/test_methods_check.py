import os
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.abspath(".agents/skills/methods-check/scripts"))
from methods_check import audit_section_iii, enrich_section_iii

class TestMethodsCheck(unittest.TestCase):
    def test_enrich_and_audit(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tf:
            tf.write("""# Title
## I. Introduction
Intro.
## III. System Architecture and Methodology
Basic architecture.
## IV. Experimental Results
Results.
""")
            path = tf.name

        # Initial audit should fail because equations are missing
        rep1 = audit_section_iii(path)
        self.assertEqual(rep1["status"], "FAIL")

        # Enrich Section III
        enrich_section_iii(path)

        # Re-audit should pass
        rep2 = audit_section_iii(path)
        os.remove(path)
        self.assertEqual(rep2["status"], "PASS")
