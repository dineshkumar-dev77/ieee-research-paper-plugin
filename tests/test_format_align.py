import os
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.abspath(".agents/skills/format-align/scripts"))
from format_align import check_format_compliance

class TestFormatAlign(unittest.TestCase):
    def test_compliant_manuscript(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tf:
            tf.write("""
# IV. Experimental Evaluation
In this section we report empirical performance. As detailed in Table I and Fig. 1, our proposed method demonstrates superior performance. Later, Table II and Fig. 2 present ablation results.

**TABLE I**
*PERFORMANCE COMPARISON*
| Method | Value |

Fig. 1. Latency comparison across workloads.

**TABLE II**
*ABLATION ANALYSIS*
| Config | Value |

Fig. 2. Parameter sensitivity analysis.
""")
            path = tf.name

        rep = check_format_compliance(path)
        os.remove(path)
        self.assertEqual(rep["status"], "PASS")

    def test_guardrail3_simulated_label_violation(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tf:
            tf.write("""
# IV. Results
Our simulated results show reduced latency.
""")
            path = tf.name

        rep = check_format_compliance(path)
        os.remove(path)
        self.assertEqual(rep["status"], "FAIL")
        self.assertTrue(any("Guardrail 3" in e for e in rep["errors"]))
