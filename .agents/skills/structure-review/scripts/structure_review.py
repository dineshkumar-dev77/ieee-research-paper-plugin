#!/usr/bin/env python3
"""Structure Review CLI.
Audits manuscript for all required IEEE paper sections.
"""
import argparse
import json
import os
import re
import sys

REQUIRED_SECTIONS = [
    {"name": "Abstract", "patterns": [r"\babstract\b"]},
    {"name": "Index Terms", "patterns": [r"\bindex\s+terms\b", r"\bkeywords\b"]},
    {"name": "I. Introduction", "patterns": [r"\b(?:i\.?\s+)?introduction\b"]},
    {"name": "II. Related Work", "patterns": [r"\b(?:ii\.?\s+)?related\s+work\b", r"\bbackground\b"]},
    {"name": "III. System Architecture and Methodology", "patterns": [r"\b(?:iii\.?\s+)?(?:system\s+architecture|methodology|system\s+model)\b"]},
    {"name": "IV. Experimental Results", "patterns": [r"\b(?:iv\.?\s+)?(?:experimental\s+results|experimental\s+evaluation|evaluation|performance\s+results)\b"]},
    {"name": "V. Conclusion", "patterns": [r"\b(?:v\.?\s+)?conclusion\b"]},
    {"name": "References", "patterns": [r"\breferences\b", r"\bbibliography\b"]}
]

def extract_text(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Manuscript not found: {path}")
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        import docx
        doc = docx.Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def review_structure(manuscript_path):
    text = extract_text(manuscript_path)
    lines = text.splitlines()

    found_sections = {}
    missing_sections = []

    for sec in REQUIRED_SECTIONS:
        sec_name = sec["name"]
        patterns = sec["patterns"]
        matched = False
        for idx, line in enumerate(lines, 1):
            stripped = line.strip().lower()
            # Headers e.g. # Abstract, ## I. Introduction, or plain section title
            for pat in patterns:
                if re.search(pat, stripped):
                    found_sections[sec_name] = {"line": idx, "heading": line.strip()}
                    matched = True
                    break
            if matched:
                break
        if not matched:
            missing_sections.append(sec_name)

    status = "PASS" if len(missing_sections) == 0 else "FAIL"
    report = {
        "manuscript": manuscript_path,
        "status": status,
        "required_count": len(REQUIRED_SECTIONS),
        "found_count": len(found_sections),
        "found_sections": found_sections,
        "missing_sections": missing_sections
    }
    return report

def main():
    parser = argparse.ArgumentParser(description="Audit manuscript structure for IEEE sections.")
    parser.add_argument("--manuscript", default="paper/manuscript.md", help="Path to manuscript")
    parser.add_argument("--output", default="paper/reports/structure_report.json", help="Path to output report")

    args = parser.parse_args()

    try:
        report = review_structure(args.manuscript)
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print(json.dumps(report, indent=2))
        if report["status"] != "PASS":
            print(f"[FAIL] Missing {len(report['missing_sections'])} required section(s): {report['missing_sections']}", file=sys.stderr)
            sys.exit(1)
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
