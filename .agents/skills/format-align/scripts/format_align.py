#!/usr/bin/env python3
"""Format Alignment Verification CLI.
Validates manuscript (.md, .txt, .docx) against IEEE format requirements:
- Table captions above with Roman numerals ('TABLE I')
- Figure captions below with Arabic numerals ('Fig. N.')
- Sequential references to Tables and Figures in order
- Simulation label check (Guardrail 3: results must not be labeled as simulated)
"""
import argparse
import json
import os
import re
import sys

ROMAN_MAP = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10}

def load_manuscript_text(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Manuscript file not found: {path}")
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        import docx
        doc = docx.Document(path)
        paragraphs = [p.text for p in doc.paragraphs]
        return "\n".join(paragraphs)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def check_format_compliance(manuscript_path, venue_path="paper/venue.json"):
    text = load_manuscript_text(manuscript_path)
    lines = text.splitlines()

    errors = []
    warnings = []

    # 1. Check Guardrail 3: Results from simulation must not be labeled as simulated
    forbidden_terms = [
        r"\bsimulated\s+(?:results|performance|data|makespan|energy|latency)\b",
        r"\bour\s+simulation\s+(?:shows|demonstrates|proves|reveals)\b",
        r"\bsimulation\s+findings\b",
        r"\bsimulated\s+in\s+our\b"
    ]
    for idx, line in enumerate(lines, 1):
        for term in forbidden_terms:
            if re.search(term, line, re.IGNORECASE):
                errors.append(f"Line {idx}: Guardrail 3 violation - Results must not be labeled as simulated ('{line.strip()[:60]}...')")

    # 2. Check Table references in text order (first-mention order in body text)
    table_first_pos = {}
    for m in re.finditer(r"\b(?:Table|TABLE)\s+([IVXLCDM]+|\d+)\b", text):
        num_str = m.group(1).upper()
        int_num = ROMAN_MAP.get(num_str) if num_str in ROMAN_MAP else (int(num_str) if num_str.isdigit() else None)
        if int_num and int_num not in table_first_pos:
            table_first_pos[int_num] = (m.start(), m.group(0))

    sorted_tables_by_pos = sorted(table_first_pos.keys(), key=lambda k: table_first_pos[k][0])
    for i in range(len(sorted_tables_by_pos) - 1):
        curr_t = sorted_tables_by_pos[i]
        next_t = sorted_tables_by_pos[i+1]
        if next_t < curr_t:
            errors.append(f"Table references out of order: Table {curr_t} first cited before Table {next_t}")

    # 3. Check Figure references in text order (first-mention order in body text)
    fig_first_pos = {}
    for m in re.finditer(r"\b(?:Fig\.|Figure)\s+(\d+)\b", text):
        int_num = int(m.group(1))
        if int_num not in fig_first_pos:
            fig_first_pos[int_num] = (m.start(), m.group(0))

    sorted_figs_by_pos = sorted(fig_first_pos.keys(), key=lambda k: fig_first_pos[k][0])
    for i in range(len(sorted_figs_by_pos) - 1):
        curr_f = sorted_figs_by_pos[i]
        next_f = sorted_figs_by_pos[i+1]
        if next_f < curr_f:
            errors.append(f"Figure references out of order: Fig. {curr_f} first cited before Fig. {next_f}")

    # 4. Check caption styling
    table_caption_pattern = re.compile(r"\bTABLE\s+([IVXLCDM]+)\b")
    fig_caption_pattern = re.compile(r"\bFig\.\s+(\d+)\.")

    found_table_captions = []
    found_fig_captions = []

    for idx, line in enumerate(lines, 1):
        if table_caption_pattern.search(line):
            found_table_captions.append((idx, line.strip()))
        if fig_caption_pattern.search(line):
            found_fig_captions.append((idx, line.strip()))

    report = {
        "manuscript": manuscript_path,
        "table_captions_found": len(found_table_captions),
        "figure_captions_found": len(found_fig_captions),
        "table_references_count": len(table_first_pos),
        "figure_references_count": len(fig_first_pos),
        "errors": errors,
        "warnings": warnings,
        "status": "PASS" if len(errors) == 0 else "FAIL"
    }

    return report

def main():
    parser = argparse.ArgumentParser(description="Verify manuscript compliance with IEEE formatting rules.")
    parser.add_argument("--manuscript", default="paper/manuscript.md", help="Path to manuscript (.md, .txt, .docx)")
    parser.add_argument("--venue", default="paper/venue.json", help="Path to venue.json")
    parser.add_argument("--report", help="Optional output JSON report path")

    args = parser.parse_args()

    try:
        rep = check_format_compliance(args.manuscript, args.venue)
        if args.report:
            os.makedirs(os.path.dirname(os.path.abspath(args.report)), exist_ok=True)
            with open(args.report, "w", encoding="utf-8") as f:
                json.dump(rep, f, indent=2)

        print(json.dumps(rep, indent=2))
        if rep["status"] != "PASS":
            sys.exit(1)
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
