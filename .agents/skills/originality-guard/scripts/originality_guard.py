#!/usr/bin/env python3
"""Originality and N-Gram Overlap Guard."""

import argparse
import json
import os
import re
import sys

DEFAULT_PRIOR_ABSTRACTS = """Cloud computing has emerged as a dominant paradigm for hosting distributed services and compute-intensive workflows. Efficient task allocation across heterogeneous virtual machines requires balancing makespan and energy efficiency under service level agreements. Traditional scheduling heuristics, including Min-Min, Max-Min, and Round-Robin, exhibit structural limitations under high-concurrency bursty arrivals. Various heuristics incorporating genetic algorithms and dynamic programming have been proposed; however, scalability in real-time environments remains an active research challenge. Benchmarking methodologies must demonstrate rigorous statistical significance across independent trials."""

def tokenize(text):
    clean = re.sub(r'[^a-zA-Z0-9\s]', ' ', text.lower())
    return [w for w in clean.split() if len(w) > 1]

def get_ngrams(tokens, n):
    return set(tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1))

def audit_originality(manuscript_path, sources_dir, threshold=20.0):
    if not os.path.isfile(manuscript_path):
        raise FileNotFoundError(f"Manuscript not found: {manuscript_path}")

    os.makedirs(sources_dir, exist_ok=True)
    source_files = [os.path.join(sources_dir, f) for f in os.listdir(sources_dir) if os.path.isfile(os.path.join(sources_dir, f))]
    if not source_files:
        seed_path = os.path.join(sources_dir, "prior_abstracts.txt")
        with open(seed_path, "w", encoding="utf-8") as f:
            f.write(DEFAULT_PRIOR_ABSTRACTS.strip() + "\n")
        source_files = [seed_path]

    with open(manuscript_path, "r", encoding="utf-8") as f:
        manu_text = f.read()

    source_text = ""
    for sf in source_files:
        with open(sf, "r", encoding="utf-8", errors="ignore") as f:
            source_text += f.read() + " "

    manu_tokens = tokenize(manu_text)
    src_tokens = tokenize(source_text)

    manu_3 = get_ngrams(manu_tokens, 3)
    src_3 = get_ngrams(src_tokens, 3)
    overlap_3 = manu_3.intersection(src_3)
    sim_3 = (len(overlap_3) / len(manu_3) * 100) if manu_3 else 0.0

    manu_5 = get_ngrams(manu_tokens, 5)
    src_5 = get_ngrams(src_tokens, 5)
    overlap_5 = manu_5.intersection(src_5)
    sim_5 = (len(overlap_5) / len(manu_5) * 100) if manu_5 else 0.0

    overall_sim = round((sim_3 * 0.4 + sim_5 * 0.6), 2)
    passed = overall_sim <= threshold

    report = {
        "manuscript": manuscript_path,
        "sources_scanned": [os.path.basename(f) for f in source_files],
        "manuscript_token_count": len(manu_tokens),
        "source_token_count": len(src_tokens),
        "three_gram_overlap_count": len(overlap_3),
        "three_gram_similarity_pct": round(sim_3, 2),
        "five_gram_overlap_count": len(overlap_5),
        "five_gram_similarity_pct": round(sim_5, 2),
        "composite_similarity_pct": overall_sim,
        "threshold_pct": threshold,
        "status": "PASSED" if passed else "FAILED",
        "official_screening_notice": "Authors must run official IEEE CrossCheck / iThenticate screening prior to final submission."
    }
    return report, passed

def main():
    parser = argparse.ArgumentParser(description="Audit manuscript originality and n-gram overlap")
    parser.add_argument("--manuscript", default="paper/manuscript.md", help="Manuscript path")
    parser.add_argument("--sources", default="paper/sources", help="Sources directory")
    parser.add_argument("--output", default="paper/reports/originality_report.json", help="Output report JSON")
    parser.add_argument("--threshold", type=float, default=20.0, help="Allowable similarity threshold percentage")
    args = parser.parse_args()

    try:
        report, passed = audit_originality(args.manuscript, args.sources, args.threshold)
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        if not passed:
            print(f"[FAIL] Originality check failed: {report['composite_similarity_pct']}% exceeds threshold {args.threshold}%", file=sys.stderr)
            sys.exit(1)

        print(f"[PASS] Originality audit passed ({report['composite_similarity_pct']}% overlap). Report: {args.output}")
        sys.exit(0)
    except Exception as e:
        print(f"[FAIL] Originality guard error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
