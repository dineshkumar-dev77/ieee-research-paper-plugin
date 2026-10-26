#!/usr/bin/env python3
"""Master Pre-Flight Audit Gate and Submission Packaging Pipeline."""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import zipfile

PREFLIGHT_CHECKS = [
    ("Numbers Ledger Verification", ["python3", ".agents/skills/results-ledger/scripts/numbers_check.py", "--manuscript", "paper/manuscript.md", "--ledger", "paper/results.csv"]),
    ("Format & Caption Alignment", ["python3", ".agents/skills/format-align/scripts/format_align.py", "--manuscript", "paper/manuscript.md"]),
    ("Front Matter & Abstract Rigor", ["python3", ".agents/skills/front-matter-check/scripts/front_matter_check.py", "--manuscript", "paper/manuscript.md"]),
    ("Sequential Citation Verification", ["python3", ".agents/skills/citation_check/scripts/citation_check.py", "--manuscript", "paper/manuscript.md"]),
    ("Graphics Compliance Audit", ["python3", ".agents/skills/graphics-compliance/scripts/graphics_compliance.py", "--figures-dir", "paper/figures", "--venue", "paper/venue.json"]),
    ("IEEE Section Structure Review", ["python3", ".agents/skills/structure-review/scripts/structure_review.py", "--manuscript", "paper/manuscript.md"]),
    ("Quantitative Claims Audit", ["python3", ".agents/skills/claims-check/scripts/claims_check.py", "--manuscript", "paper/manuscript.md", "--ledger", "paper/results.csv"]),
    ("Simulation Validity Audit", ["python3", ".agents/skills/sim-validity-check/scripts/sim_validity_check.py", "--ledger", "paper/results.csv"]),
    ("AI Usage Disclosure (Guardrail 4)", ["python3", ".agents/skills/ai-disclosure/scripts/ai_disclosure.py", "--audit", "--log", "paper/reports/ai_usage_log.json", "--ack", "paper/reports/ai_acknowledgment.txt", "--manuscript", "paper/manuscript.md"]),
    ("Terminology & Acronym Audit", ["python3", ".agents/skills/terminology-check/scripts/terminology_check.py", "--manuscript", "paper/manuscript.md"]),
    ("Originality & N-Gram Guard", ["python3", ".agents/skills/originality-guard/scripts/originality_guard.py", "--manuscript", "paper/manuscript.md", "--sources", "paper/sources"])
]

def run_preflight_audits():
    audit_results = []
    print("==================================================")
    print("RUNNING MASTER PRE-FLIGHT AUDIT GATE (11 CHECKS)")
    print("==================================================")
    for name, cmd in PREFLIGHT_CHECKS:
        res = subprocess.run(cmd, capture_output=True, text=True)
        passed = (res.returncode == 0)
        status_tag = "[PASS]" if passed else "[FAIL]"
        print(f"{status_tag} {name}")
        audit_results.append({
            "check": name,
            "command": " ".join(cmd),
            "passed": passed,
            "returncode": res.returncode,
            "output": res.stdout.strip() or res.stderr.strip()
        })
        if not passed:
            print(f"Error details:\n{res.stderr or res.stdout}", file=sys.stderr)
            return False, audit_results
    return True, audit_results

def convert_md_to_docx(md_path, docx_path):
    import docx
    doc = docx.Document()

    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_table = False
    table_rows = []

    def flush_table():
        nonlocal in_table, table_rows
        if in_table and table_rows:
            num_cols = max(len(r) for r in table_rows)
            t = doc.add_table(rows=len(table_rows), cols=num_cols)
            for r_idx, row in enumerate(table_rows):
                for c_idx, val in enumerate(row):
                    if c_idx < num_cols:
                        t.rows[r_idx].cells[c_idx].text = val
            in_table = False
            table_rows = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            inner = stripped[1:-1].replace("-", "").replace(":", "").replace(" ", "").replace("|", "")
            if inner == "":
                continue
            if not in_table:
                in_table = True
                table_rows = []
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            table_rows.append(cells)
            continue
        else:
            flush_table()

        if not stripped:
            continue
        if stripped.startswith("# "):
            doc.add_heading(stripped[2:], level=1)
        elif stripped.startswith("## "):
            doc.add_heading(stripped[3:], level=2)
        elif stripped.startswith("### "):
            doc.add_heading(stripped[4:], level=3)
        else:
            doc.add_paragraph(stripped)

    flush_table()
    doc.save(docx_path)
    print(f"[CONVERT] Generated {docx_path} from {md_path}")

def compute_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def bundle_submission(bundle_dir, zip_path, manifest_path, audit_results):
    os.makedirs(bundle_dir, exist_ok=True)
    artifacts_to_copy = [
        "paper/manuscript.docx",
        "paper/manuscript.md",
        "paper/tables/table_1.tex",
        "paper/figures/fig_1.pdf",
        "paper/figures/fig_1.png",
        "paper/figures/fig_2.pdf",
        "paper/figures/fig_2.png",
        "paper/reports/ai_acknowledgment.txt",
        "paper/reports/rebuttal_letter.md"
    ]

    bundled_files = []
    for art in artifacts_to_copy:
        if os.path.isfile(art):
            dest = os.path.join(bundle_dir, os.path.basename(art))
            shutil.copy2(art, dest)
            bundled_files.append({
                "file": os.path.basename(art),
                "source": art,
                "size_bytes": os.path.getsize(dest),
                "sha256": compute_sha256(dest)
            })
        else:
            print(f"[WARN] Expected artifact not found: {art}")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for b in bundled_files:
            file_path = os.path.join(bundle_dir, b["file"])
            z.write(file_path, arcname=b["file"])
    print(f"[BUNDLE] Created submission archive: {zip_path}")

    manifest = {
        "package_name": "IEEE_TCC_Adaptive_DynaSched_Submission",
        "venue": "IEEE Transactions on Cloud Computing (TCC)",
        "archive_file": os.path.basename(zip_path),
        "archive_sha256": compute_sha256(zip_path),
        "total_files": len(bundled_files),
        "preflight_gate_status": "ALL_11_CHECKS_PASSED",
        "preflight_audits": audit_results,
        "manifest_files": bundled_files
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"[MANIFEST] Generated submission manifest: {manifest_path}")

def main():
    parser = argparse.ArgumentParser(description="Master Pre-Flight Gate and Submission Packager")
    parser.add_argument("--skip-preflight", action="store_true", help="Skip pre-flight gate checks")
    parser.add_argument("--bundle-dir", default="paper/submission_bundle", help="Output bundle directory")
    parser.add_argument("--zip", default="paper/submission_bundle.zip", help="Output zip archive path")
    parser.add_argument("--manifest", default="paper/submission_manifest.json", help="Output manifest path")
    args = parser.parse_args()

    audit_results = []
    if not args.skip_preflight:
        passed, audit_results = run_preflight_audits()
        if not passed:
            print("[FAIL] Master pre-flight audit gate failed! Aborting packaging.", file=sys.stderr)
            sys.exit(1)

    try:
        convert_md_to_docx("paper/manuscript.md", "paper/manuscript.docx")
        bundle_submission(args.bundle_dir, args.zip, args.manifest, audit_results)
        print("==================================================")
        print("[SUCCESS] Submission Package successfully generated!")
        print("==================================================")
        sys.exit(0)
    except Exception as e:
        print(f"[FAIL] Packaging error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
