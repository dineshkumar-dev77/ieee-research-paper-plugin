import os
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.abspath(".agents/skills/front-matter-check/scripts"))
from front_matter_check import audit_front_matter

class TestFrontMatterCheck(unittest.TestCase):
    def test_valid_front_matter_passes(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tf:
            tf.write("""# Adaptive Dynamic Scheduling for Heterogeneous Cloud Workloads

## Abstract
Modern cloud datacenters require efficient task scheduling under fluctuating arrival rates and heterogeneous processor capabilities.

**Index Terms**—Cloud computing, Energy efficiency, Quality of service, Task scheduling.

## I. Introduction
Intro text.
""")
            path = tf.name

        rep = audit_front_matter(path)
        os.remove(path)
        self.assertEqual(rep["status"], "PASS")

    def test_abstract_with_citation_fails(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tf:
            tf.write("""# Title

## Abstract
This paper builds on prior methods [1].

**Index Terms**—Cloud computing, Task scheduling.
""")
            path = tf.name

        rep = audit_front_matter(path)
        os.remove(path)
        self.assertEqual(rep["status"], "FAIL")
        self.assertTrue(any("Abstract contains citations" in e for e in rep["errors"]))

    def test_unsorted_index_terms_fails(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tf:
            tf.write("""# Title

## Abstract
Valid plain text abstract.

**Index Terms**—Task scheduling, Cloud computing.
""")
            path = tf.name

        rep = audit_front_matter(path)
        os.remove(path)
        self.assertEqual(rep["status"], "FAIL")
        self.assertTrue(any("alphabetical order" in e for e in rep["errors"]))
