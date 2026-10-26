#!/usr/bin/env python3
"""Claims Check CLI.
Extracts claims in Abstract, Introduction, and Conclusion and verifies backing evidence
in results.csv, table_1.json, and stats_summary.json.
"""
import argparse
import csv
import json
import math
import os
import re
import sys

def load_evidence(ledger_path, table_path, stats_path):
    evidence = {"ledger_values": [], "tables": {}, "stats": {}}
    if os.path.exists(ledger_path):
        with open(ledger_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                try:
                    evidence["ledger_values"].append(float(r["value"]))
                except (ValueError, TypeError):
                    pass
                try:
                    evidence["ledger_values"].append(float(r.get("seed", "")))
                except (ValueError, TypeError):
                    pass
    if os.path.exists(table_path):
        with open(table_path, "r", encoding="utf-8") as f:
            evidence["tables"] = json.load(f)
    if os.path.exists(stats_path):
        with open(stats_path, "r", encoding="utf-8") as f:
            evidence["stats"] = json.load(f)
    return evidence

def extract_section_text(text, section_keywords, end_keywords):
    lines = text.splitlines()
    in_sec = False
    sec_lines = []
    for line in lines:
        lower = line.strip().lower()
        if any(re.search(rf"\b{k}\b", lower) for k in section_keywords):
            in_sec = True
            continue
        elif in_sec and (line.startswith("#") or any(re.search(rf"\b{k}\b", lower) for k in end_keywords)):
            if lower.startswith("#") or line.startswith("##"):
                break
        if in_sec:
            sec_lines.append(line)
    return "\n".join(sec_lines)

def extract_claims(text):
    """Extract sentences containing quantitative statements (numbers, percentages, metrics)."""
    claims = []
    clean_text = re.sub(r"\b(?:Fig|Table|et al|e\.g|i\.e)\.", lambda m: m.group(0).replace(".", "§"), text)
    raw_sentences = re.split(r"(?<=[.!?])\s+", clean_text)
    sentences = [s.replace("§", ".") for s in raw_sentences]
    metric_terms = ["latency", "makespan", "energy", "sla", "reduction", "improvement", "violation", "speedup"]
    num_pattern = r"(\d+(?:\.\d+)?)\s*(%|ms|s|seconds|kwh)?"

    for s in sentences:
        s_clean = s.strip()
        lower = s_clean.lower()
        if any(m in lower for m in metric_terms) and re.search(r"\d+", s_clean):
            # Extract numbers
            numbers = []
            for match in re.finditer(num_pattern, s_clean):
                try:
                    numbers.append(float(match.group(1)))
                except ValueError:
                    pass
            if numbers:
                claims.append({
                    "sentence": s_clean,
                    "extracted_numbers": numbers
                })
    return claims

def check_claim_support(claim, evidence, tol=0.05):
    supported = True
    unsupported_nums = []
    for n in claim["extracted_numbers"]:
        # Match with ledger values
        match_found = False
        for lv in evidence["ledger_values"]:
            if math.isclose(n, lv, abs_tol=tol) or (lv != 0 and abs((n - lv) / lv) < 0.02):
                match_found = True
                break
        if not match_found:
            supported = False
            unsupported_nums.append(n)
    return supported, unsupported_nums

def audit_claims(manuscript_path, ledger_path, table_path, stats_path):
    with open(manuscript_path, "r", encoding="utf-8") as f:
        text = f.read()

    evidence = load_evidence(ledger_path, table_path, stats_path)

    sections_to_check = {
        "Abstract": extract_section_text(text, ["abstract"], ["introduction", "index terms"]),
        "Introduction": extract_section_text(text, ["introduction"], ["related work", "system architecture"]),
        "Conclusion": extract_section_text(text, ["conclusion"], ["references", "acknowledgment"])
    }

    report = {"manuscript": manuscript_path, "status": "PASS", "sections": {}, "unsupported_claims": []}

    for sec_name, sec_text in sections_to_check.items():
        claims = extract_claims(sec_text)
        checked_claims = []
        for c in claims:
            sup, unsup = check_claim_support(c, evidence)
            item = {
                "sentence": c["sentence"],
                "extracted_numbers": c["extracted_numbers"],
                "supported": sup,
                "unsupported_numbers": unsup
            }
            checked_claims.append(item)
            if not sup:
                report["unsupported_claims"].append({
                    "section": sec_name,
                    **item
                })
                report["status"] = "FAIL"

        report["sections"][sec_name] = {
            "claims_count": len(checked_claims),
            "claims": checked_claims
        }

    return report

def main():
    parser = argparse.ArgumentParser(description="Audit quantitative and qualitative claims against evidence.")
    parser.add_argument("--manuscript", default="paper/manuscript.md", help="Path to manuscript")
    parser.add_argument("--ledger", default="paper/results.csv", help="Path to ledger")
    parser.add_argument("--table", default="paper/tables/table_1.json", help="Path to table JSON")
    parser.add_argument("--stats", default="paper/reports/stats_summary.json", help="Path to stats JSON")
    parser.add_argument("--output", default="paper/reports/claims_report.json", help="Output path")

    args = parser.parse_args()

    try:
        rep = audit_claims(args.manuscript, args.ledger, args.table, args.stats)
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
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
