#!/usr/bin/env python3
"""Numbers Check CLI.
Scans the manuscript for experimental numbers and verifies each against paper/results.csv.
Exits with code 1 if any experimental number is not verified in the ledger.
"""
import argparse
import csv
import json
import math
import os
import re
import sys

def extract_text_from_file(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Manuscript not found: {path}")
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        import docx
        doc = docx.Document(path)
        full_text = []
        for p in doc.paragraphs:
            full_text.append(p.text)
        for t in doc.tables:
            for row in t.rows:
                row_text = [cell.text.strip() for cell in row.cells]
                full_text.append(" | ".join(row_text))
        return "\n".join(full_text)
    else:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

def load_ledger_values(ledger_path):
    if not os.path.exists(ledger_path):
        raise FileNotFoundError(f"Ledger file not found: {ledger_path}")
    values = []
    with open(ledger_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_val = row.get("value", "")
            try:
                v = float(raw_val)
                values.append(v)
            except ValueError:
                pass
            raw_seed = row.get("seed", "")
            try:
                values.append(float(raw_seed))
            except ValueError:
                pass
    return values

def is_close_match(doc_val, ledger_values, tolerance=0.05):
    for lv in ledger_values:
        if math.isclose(doc_val, lv, abs_tol=tolerance):
            return True
        if lv != 0 and abs((doc_val - lv) / lv) < 0.015:
            return True
        for dec in (0, 1, 2, 3):
            if round(doc_val, dec) == round(lv, dec):
                if abs(doc_val - lv) < 0.2:
                    return True
    return False

def extract_candidate_numbers(text, section_filter=True):
    lines = text.splitlines()
    candidates = []
    
    in_eval_section = not section_filter
    eval_keywords = ["evaluation", "experimental results", "empirical results", "results", "performance characterization", "benchmark"]
    exit_keywords = ["related work", "conclusion", "references", "acknowledgments", "future work"]

    for line_idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        lower = stripped.lower()
        
        if section_filter:
            if lower.startswith("#") or lower.startswith("section") or re.match(r"^[ivxcdm]+\.", lower):
                if any(k in lower for k in eval_keywords):
                    in_eval_section = True
                elif any(k in lower for k in exit_keywords):
                    in_eval_section = False

        if not in_eval_section and not line.startswith("|") and not "TABLE" in line and not "Fig." in line:
            continue

        line_clean = re.sub(r"\[\s*\d+(?:\s*[,-]\s*\d+)*\s*\]", " ", line)
        line_clean = re.sub(r"\b(?:Fig\.|Figure|Table|TABLE)\s+[0-9IVXLCDM]+", " ", line_clean)
        line_clean = re.sub(r"\bSection\s+[0-9IVXLCDM]+(?:-[A-Z])?", " ", line_clean, flags=re.IGNORECASE)
        line_clean = re.sub(r"\b(19\d\d|20[0-3]\d)\b", " ", line_clean)
        line_clean = re.sub(r"^#+\s*", " ", line_clean)

        pattern = r"(?<![A-Za-z0-9_])([+-]?\d+(?:\.\d+)?)(%?)(?![A-Za-z0-9_])"
        for m in re.finditer(pattern, line_clean):
            raw_num_str = m.group(1)
            is_pct = m.group(2) == "%"
            try:
                val = float(raw_num_str)
                if not line.startswith("|") and val in (0.0, 1.0) and not is_pct and "." not in raw_num_str:
                    continue
                candidates.append({
                    "line_number": line_idx,
                    "text_line": line.strip()[:80],
                    "token": m.group(0),
                    "value": val,
                    "is_pct": is_pct
                })
            except ValueError:
                continue

    return candidates

def verify_manuscript(manuscript_path, ledger_path, tolerance=0.05, section_filter=True):
    text = extract_text_from_file(manuscript_path)
    ledger_vals = load_ledger_values(ledger_path)
    candidates = extract_candidate_numbers(text, section_filter=section_filter)

    if not candidates:
        candidates = extract_candidate_numbers(text, section_filter=False)

    unmatched = []
    matched = []

    for c in candidates:
        val = c["value"]
        if is_close_match(val, ledger_vals, tolerance=tolerance):
            matched.append(c)
        else:
            unmatched.append(c)

    return matched, unmatched

def main():
    parser = argparse.ArgumentParser(description="Scan manuscript for experimental numbers and check against results.csv.")
    parser.add_argument("--manuscript", default="paper/manuscript.md", help="Path to manuscript (.md, .txt, .docx)")
    parser.add_argument("--ledger", default="paper/results.csv", help="Path to results.csv")
    parser.add_argument("--tolerance", type=float, default=0.05, help="Matching tolerance")
    parser.add_argument("--all-sections", action="store_true", help="Scan entire document instead of evaluation section")
    parser.add_argument("--report", help="Optional output JSON report path")

    args = parser.parse_args()

    try:
        matched, unmatched = verify_manuscript(
            args.manuscript,
            args.ledger,
            tolerance=args.tolerance,
            section_filter=(not args.all_sections)
        )

        report = {
            "status": "PASS" if len(unmatched) == 0 else "FAIL",
            "manuscript": args.manuscript,
            "ledger": args.ledger,
            "matched_count": len(matched),
            "unmatched_count": len(unmatched),
            "unmatched_items": unmatched
        }

        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)

        if len(unmatched) > 0:
            print(f"[FAIL] Found {len(unmatched)} experimental number(s) in manuscript not present in {args.ledger}:", file=sys.stderr)
            for item in unmatched:
                print(f"  Line {item['line_number']}: \"{item['token']}\" in \"{item['text_line']}\"", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"[PASS] All {len(matched)} experimental numbers verified against ledger ({args.ledger}).")
            sys.exit(0)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
