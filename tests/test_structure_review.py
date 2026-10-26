import os
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.abspath(".agents/skills/structure-review/scripts"))
from structure_review import review_structure

class TestStructureReview(unittest.TestCase):
    def test_complete_manuscript_passes(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tf:
            tf.write("""
# Title
## Abstract
Summary.
**Index Terms**—Cloud computing, Scheduling.
## I. Introduction
Intro text.
## II. Related Work
Related text.
## III. System Architecture and Methodology
Architecture text.
## IV. Experimental Results
Results text.
## V. Conclusion
Conclusion text.
## References
[1] Author, Paper.
""")
            path = tf.name

        rep = review_structure(path)
        os.remove(path)
        self.assertEqual(rep["status"], "PASS")

    def test_missing_section_fails(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tf:
            tf.write("""
# Title
## Abstract
Summary.
## I. Introduction
Intro text.
""")
            path = tf.name

        rep = review_structure(path)
        os.remove(path)
        self.assertEqual(rep["status"], "FAIL")
        self.assertIn("References", rep["missing_sections"])
