#!/usr/bin/env python3
"""Citation Check CLI.
Verifies that all in-text citations appear in sequential numerical order ([1], [2], ...)
and that every in-text citation has a matching entry in References (and vice versa).
Exits with code 1 on orphan or out-of-order citations.
"""
import argparse
import json
import os
import re
import sys

def parse_citations(manuscript_path):
    if not os.path.exists(manuscript_path):
        raise FileNotFoundError(f"Manuscript not found: {manuscript_path}")

    with open(manuscript_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Separate body from References section
    parts = re.split(r"##\s+References", content, flags=re.IGNORECASE)
    body_text = parts[0]
    ref_text = parts[1] if len(parts) > 1 else ""

    # 1. Parse in-text citations from body
    # Matches [1], [2], [1, 2], [1]-[3]
    in_text_occurrences = []
    first_seen_pos = {}

    for m in re.finditer(r"\[(\s*\d+(?:\s*[,-]\s*\d+)*\s*)\]", body_text):
        raw_inside = m.group(1).strip()
        pos = m.start()
        # Parse ranges like 1-3 or lists like 1, 2
        nums = []
        if "-" in raw_inside:
            tokens = raw_inside.split("-")
            try:
                start_n, end_n = int(tokens[0]), int(tokens[1])
                nums.extend(list(range(start_n, end_n + 1)))
            except ValueError:
                pass
        else:
            tokens = raw_inside.split(",")
            for tok in tokens:
                try:
                    nums.append(int(tok.strip()))
                except ValueError:
                    pass

        for n in nums:
            in_text_occurrences.append((n, pos, m.group(0)))
            if n not in first_seen_pos:
                first_seen_pos[n] = pos

    # 2. Parse bibliography entries from references section
    ref_entries = set()
    for m in re.finditer(r"\[(\d+)\]", ref_text):
        ref_entries.add(int(m.group(1)))

    errors = []

    # 3. Check sequential order of first appearance
    first_seen_sorted = sorted(first_seen_pos.keys(), key=lambda k: first_seen_pos[k])
    expected_next = 1
    for n in first_seen_sorted:
        if n != expected_next:
            errors.append(f"Citation order violation: Citation [{n}] appeared before [{expected_next}]")
            break
        expected_next += 1

    # 4. Check matching between in-text and references
    in_text_set = set(first_seen_pos.keys())
    missing_in_refs = in_text_set - ref_entries
    if missing_in_refs:
        errors.append(f"Orphan in-text citation(s) missing in References section: {sorted(list(missing_in_refs))}")

    unused_refs = ref_entries - in_text_set
    if unused_refs:
        errors.append(f"Uncited reference(s) present in References section: {sorted(list(unused_refs))}")

    status = "PASS" if len(errors) == 0 else "FAIL"

    report = {
        "status": status,
        "manuscript": manuscript_path,
        "citations_found_count": len(in_text_set),
        "citations_sequence": first_seen_sorted,
        "references_count": len(ref_entries),
        "errors": errors
    }
    return report

def main():
    parser = argparse.ArgumentParser(description="Verify citation sequential ordering and completeness.")
    parser.add_argument("--manuscript", default="paper/manuscript.md", help="Path to manuscript")
    parser.add_argument("--output", default="paper/reports/citation_report.json", help="Report path")

    args = parser.parse_args()

    try:
        report = parse_citations(args.manuscript)
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
