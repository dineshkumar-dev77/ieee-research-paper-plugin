#!/usr/bin/env python3
"""Front Matter Check CLI.
Audits Title, Abstract, and Index Terms in the manuscript.
Enforces:
- Abstract contains zero equations and zero [N] citations.
- Index Terms are sorted in strict alphabetical order.
Exits with code 1 on violation.
"""
import argparse
import json
import os
import re
import sys

def audit_front_matter(manuscript_path):
    if not os.path.exists(manuscript_path):
        raise FileNotFoundError(f"Manuscript not found: {manuscript_path}")

    with open(manuscript_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    errors = []

    # 1. Extract Title
    title = None
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break
    if not title:
        errors.append("Manuscript title (# ...) not found")

    # 2. Extract Abstract
    abstract_lines = []
    in_abstract = False
    for line in lines:
        stripped = line.strip()
        if re.search(r"^##\s+Abstract", stripped, re.IGNORECASE):
            in_abstract = True
            continue
        elif in_abstract and stripped.startswith("##"):
            break
        if in_abstract:
            abstract_lines.append(stripped)

    abstract_text = " ".join(abstract_lines).strip()
    if not abstract_text:
        errors.append("Abstract section (## Abstract) not found or empty")

    # Check for citations in Abstract
    if re.search(r"\[\s*\d+\s*\]", abstract_text):
        errors.append("Abstract contains citations (IEEE prohibits references in the Abstract)")

    # Check for equations or mathematical markup in Abstract
    if "$" in abstract_text or "\\" in abstract_text or re.search(r"[=<>]\s*\d", abstract_text):
        errors.append("Abstract contains equations or mathematical symbols (IEEE requires plain text Abstract)")

    # 3. Extract Index Terms
    # Look for "Index Terms-" or "Index Terms—" or "**Index Terms**—" or "## Index Terms"
    index_terms = []
    found_index_terms = False

    for line in lines:
        clean_l = line.replace("*", "").strip()
        m = re.search(r"(?:Index\s+Terms|Keywords)[:\s—\-]+(.*)", clean_l, re.IGNORECASE)
        if m:
            found_index_terms = True
            raw_terms = m.group(1).strip().rstrip(".")
            terms = [t.strip() for t in re.split(r"[,;]", raw_terms) if t.strip()]
            index_terms = terms
            break

    if not found_index_terms or not index_terms:
        errors.append("Index Terms section not found or contains no terms")
    else:
        # Check alphabetical sorting
        normalized = [t.lower() for t in index_terms]
        sorted_normalized = sorted(normalized)
        if normalized != sorted_normalized:
            errors.append(f"Index Terms are not in strict alphabetical order: {index_terms} (expected: {[t.title() for t in sorted_normalized]})")

    status = "PASS" if len(errors) == 0 else "FAIL"

    report = {
        "status": status,
        "manuscript": manuscript_path,
        "title": title,
        "abstract_length_words": len(abstract_text.split()),
        "index_terms": index_terms,
        "errors": errors
    }
    return report

def main():
    parser = argparse.ArgumentParser(description="Audit front matter (Title, Abstract, Index Terms).")
    parser.add_argument("--manuscript", default="paper/manuscript.md", help="Path to manuscript")
    parser.add_argument("--output", default="paper/reports/front_matter_report.json", help="Report output path")

    args = parser.parse_args()

    try:
        report = audit_front_matter(args.manuscript)
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print(json.dumps(report, indent=2))
        if report["status"] != "PASS":
            sys.exit(1)
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
