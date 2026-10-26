#!/usr/bin/env python3
"""Terminology, Acronym, and Mathematical Notation Consistency Auditor."""

import argparse
import json
import os
import re
import sys

CANONICAL_METHODS = [
    ("Adaptive-DynaSched", [r"adaptive[\s_-]dynasched", r"adaptive\s+dynasched"]),
    ("Round-Robin", [r"round[\s_-]robin", r"roundrobin"]),
    ("Min-Min", [r"min[\s_-]min", r"minmin"])
]

KNOWN_ACRONYMS = {
    "SLA": "Service Level Agreement",
    "MIPS": "Million Instructions Per Second",
    "QoS": "Quality of Service",
    "DVFS": "Dynamic Voltage and Frequency Scaling",
    "HEFT": "Heterogeneous Earliest Finish Time"
}

STANDARD_SYMBOLS = [r"\mathcal{N}", r"\mathcal{T}", r"\mu_j", r"\tau_{i,j}"]

def audit_terminology(manuscript_path, strict=False):
    if not os.path.isfile(manuscript_path):
        raise FileNotFoundError(f"Manuscript not found: {manuscript_path}")

    with open(manuscript_path, "r", encoding="utf-8") as f:
        text = f.read()

    acronym_results = {}
    acronym_violations = []
    for acr, expansion in KNOWN_ACRONYMS.items():
        if acr in text:
            has_expansion = (expansion.lower() in text.lower())
            acronym_results[acr] = {
                "expansion": expansion,
                "defined": has_expansion
            }
            if not has_expansion:
                acronym_violations.append(f"Acronym '{acr}' is missing required expansion '{expansion}' on first use.")

    method_violations = []
    for canonical, patterns in CANONICAL_METHODS:
        for pat in patterns:
            matches = re.findall(pat, text, flags=re.IGNORECASE)
            for m in matches:
                if m != canonical and m.lower() != canonical.lower():
                    method_violations.append(f"Inconsistent method casing: '{m}' should be '{canonical}'")

    symbol_results = {}
    for sym in STANDARD_SYMBOLS:
        symbol_results[sym] = sym in text

    passed = (len(acronym_violations) == 0 and len(method_violations) == 0) if strict else True

    report = {
        "manuscript": manuscript_path,
        "acronyms_audited": acronym_results,
        "acronym_violations": acronym_violations,
        "method_naming_violations": method_violations,
        "mathematical_symbols_present": symbol_results,
        "status": "PASSED" if passed else "VIOLATIONS_DETECTED"
    }
    return report, passed

def main():
    parser = argparse.ArgumentParser(description="Terminology and Acronym Consistency Auditor")
    parser.add_argument("--manuscript", default="paper/manuscript.md", help="Manuscript path")
    parser.add_argument("--output", default="paper/reports/terminology_report.json", help="Output report JSON")
    parser.add_argument("--strict", action="store_true", help="Fail with exit code 1 if violations found")
    args = parser.parse_args()

    try:
        report, passed = audit_terminology(args.manuscript, strict=args.strict)
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        if not passed:
            print(f"[FAIL] Terminology violations detected under strict mode.", file=sys.stderr)
            sys.exit(1)

        print(f"[PASS] Terminology audit completed. Report: {args.output}")
        sys.exit(0)
    except Exception as e:
        print(f"[FAIL] Terminology check error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
