#!/usr/bin/env python3
"""Unit Tests for Phase 3 Skills."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class TestPhase3Skills(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_author_voice_burstiness_and_preservation(self):
        from importlib.machinery import SourceFileLoader
        av_path = os.path.join(ROOT_DIR, ".agents/skills/author-voice/scripts/author_voice.py")
        av = SourceFileLoader("author_voice", av_path).load_module()

        sample_dir = os.path.join(self.test_dir, "samples")
        profile = av.profile_samples(sample_dir)
        self.assertIn("burstiness_index", profile)
        self.assertGreater(profile["burstiness_index"], 0.0)

        manu_path = os.path.join(self.test_dir, "manuscript.md")
        with open(manu_path, "w", encoding="utf-8") as f:
            f.write("In this dynamic landscape, the results demonstrate that latency reached 45.01% with 0 SLA violations.\n")

        res = av.refine_manuscript(manu_path, apply_edits=True)
        self.assertGreaterEqual(res["edits_count"], 1)

        with open(manu_path, "r", encoding="utf-8") as f:
            new_text = f.read()
        self.assertIn("45.01%", new_text)
        self.assertIn("0", new_text)

    def test_ai_disclosure_audit_and_sync(self):
        from importlib.machinery import SourceFileLoader
        ad_path = os.path.join(ROOT_DIR, ".agents/skills/ai-disclosure/scripts/ai_disclosure.py")
        ad = SourceFileLoader("ai_disclosure", ad_path).load_module()

        log_path = os.path.join(self.test_dir, "ai_usage_log.json")
        ack_path = os.path.join(self.test_dir, "ai_acknowledgment.txt")
        manu_path = os.path.join(self.test_dir, "manuscript.md")

        log_data = {
            "sections_assisted": [
                {"section": "Section IV: Experimental Evaluation", "assistance_type": "Data analysis"},
                {"section": "Section V: Performance Analysis", "assistance_type": "Hypothesis testing"}
            ]
        }
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(log_data, f)

        with open(manu_path, "w", encoding="utf-8") as f:
            f.write("# Title\n## Introduction\nText\n## References\n[1] Ref\n")

        ad.sync_acknowledgment(log_path, ack_path, manu_path)
        self.assertTrue(os.path.isfile(ack_path))

        self.assertTrue(ad.audit_disclosure(log_path, ack_path, manu_path))

        with open(ack_path, "w", encoding="utf-8") as f:
            f.write("ACKNOWLEDGMENT\nNo sections were assisted.\n")
        self.assertFalse(ad.audit_disclosure(log_path, ack_path, manu_path))

    def test_reviewer_panel(self):
        from importlib.machinery import SourceFileLoader
        rp_path = os.path.join(ROOT_DIR, ".agents/skills/reviewer-panel/scripts/reviewer_panel.py")
        rp = SourceFileLoader("reviewer_panel", rp_path).load_module()

        manu_path = os.path.join(ROOT_DIR, "paper/manuscript.md")
        ledger_path = os.path.join(ROOT_DIR, "paper/results.csv")
        fig_dir = os.path.join(ROOT_DIR, "paper/figures")

        review = rp.audit_paper(manu_path, ledger_path, fig_dir)
        self.assertEqual(len(review["reviewers"]), 3)
        self.assertGreater(review["overall_score"], 7.0)

    def test_originality_guard(self):
        from importlib.machinery import SourceFileLoader
        og_path = os.path.join(ROOT_DIR, ".agents/skills/originality-guard/scripts/originality_guard.py")
        og = SourceFileLoader("originality_guard", og_path).load_module()

        manu_path = os.path.join(ROOT_DIR, "paper/manuscript.md")
        sources_dir = os.path.join(self.test_dir, "sources")

        report, passed = og.audit_originality(manu_path, sources_dir, threshold=30.0)
        self.assertTrue(passed)
        self.assertIn("composite_similarity_pct", report)
        self.assertIn("official_screening_notice", report)

    def test_permissions_register(self):
        from importlib.machinery import SourceFileLoader
        pr_path = os.path.join(ROOT_DIR, ".agents/skills/permissions-register/scripts/permissions_register.py")
        pr = SourceFileLoader("permissions_register", pr_path).load_module()

        reg = pr.build_permissions_register(
            os.path.join(ROOT_DIR, "paper/figures"),
            os.path.join(ROOT_DIR, "paper/tables"),
            os.path.join(ROOT_DIR, "paper/workloads.json")
        )
        self.assertGreater(reg["total_assets_registered"], 0)
        self.assertEqual(reg["compliance_status"], "ALL_ASSETS_CLEARED")

    def test_terminology_check(self):
        from importlib.machinery import SourceFileLoader
        tc_path = os.path.join(ROOT_DIR, ".agents/skills/terminology-check/scripts/terminology_check.py")
        tc = SourceFileLoader("terminology_check", tc_path).load_module()

        manu_path = os.path.join(ROOT_DIR, "paper/manuscript.md")
        report, passed = tc.audit_terminology(manu_path, strict=False)
        self.assertIn("acronyms_audited", report)
        self.assertIn("status", report)

    def test_rebuttal_generator(self):
        from importlib.machinery import SourceFileLoader
        rg_path = os.path.join(ROOT_DIR, ".agents/skills/rebuttal/scripts/rebuttal_generator.py")
        rg = SourceFileLoader("rebuttal_generator", rg_path).load_module()

        review_path = os.path.join(self.test_dir, "peer_review.json")
        with open(review_path, "w", encoding="utf-8") as f:
            json.dump({
                "recommendation": "Accept with Minor Revisions",
                "reviewers": [
                    {
                        "id": "Reviewer 1",
                        "focus": "Methodology",
                        "actionable_questions": ["How does the dispatch decision boundary adapt?"]
                    }
                ]
            }, f)

        let_path = os.path.join(self.test_dir, "letter.md")
        mat_path = os.path.join(self.test_dir, "matrix.json")

        matrix = rg.generate_rebuttal(review_path, os.path.join(ROOT_DIR, "paper/results.csv"), let_path, mat_path)
        self.assertTrue(os.path.isfile(let_path))
        self.assertTrue(os.path.isfile(mat_path))
        self.assertEqual(len(matrix["rebuttal_items"]), 1)

    def test_submission_package_docx_and_bundle(self):
        from importlib.machinery import SourceFileLoader
        sp_path = os.path.join(ROOT_DIR, ".agents/skills/submission-package/scripts/submission_package.py")
        sp = SourceFileLoader("submission_package", sp_path).load_module()

        test_md = os.path.join(self.test_dir, "doc.md")
        test_docx = os.path.join(self.test_dir, "doc.docx")
        with open(test_md, "w", encoding="utf-8") as f:
            f.write("# Title\nParagraph with 45.01% number.\n| Metric | Value |\n| Latency | 482.15 |\n")

        sp.convert_md_to_docx(test_md, test_docx)
        self.assertTrue(os.path.isfile(test_docx))

        bundle_dir = os.path.join(self.test_dir, "bundle")
        zip_path = os.path.join(self.test_dir, "bundle.zip")
        man_path = os.path.join(self.test_dir, "manifest.json")

        sp.bundle_submission(bundle_dir, zip_path, man_path, [{"check": "Mock", "passed": True}])
        self.assertTrue(os.path.isfile(zip_path))
        self.assertTrue(os.path.isfile(man_path))

if __name__ == "__main__":
    unittest.main()
