import json
import os
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.abspath(".agents/skills/reference-formatter/scripts"))
from reference_formatter import format_references, update_manuscript_references

class TestReferenceFormatter(unittest.TestCase):
    def test_format_references(self):
        refs, text = format_references()
        self.assertGreaterEqual(len(refs), 10)
        self.assertIn("[1]", text)
        self.assertIn("doi:", text)

    def test_update_manuscript_references(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tf:
            tf.write("# Paper\n\n## I. Introduction\nText.\n")
            path = tf.name

        refs, ref_str = format_references()
        update_manuscript_references(path, ref_str)
        content = open(path).read()
        os.remove(path)
        self.assertIn("## References", content)
        self.assertIn("[1]", content)
