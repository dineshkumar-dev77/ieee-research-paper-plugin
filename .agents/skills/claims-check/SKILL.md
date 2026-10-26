---
name: claims-check
description: Verifies quantitative claims in Abstract, Introduction, and Conclusion against ledger.
---

# Purpose
Scans Abstract, Introduction, and Conclusion for quantitative and qualitative claims, mapping each number to backing records in `paper/results.csv`.

# When to use / not use
- **Use when**: Ensuring high-level narrative claims are backed by empirical evidence.
- **Do not use**: For in-depth Table and Figure scanning (handled by `numbers_check.py`).

# Inputs
- `paper/manuscript.md`: Paper manuscript.
- `paper/results.csv`: Results ledger.

# Outputs
- `paper/reports/claims_report.json`: Verification report of substantiated claims.

# Step-by-step method
1. Extract sentences from Abstract, Introduction, and Conclusion containing metrics.
2. Parse candidate numerical tokens (percentages, latency, makespan, energy).
3. Cross-reference against `paper/results.csv` and `paper/reports/stats_summary.json`.
4. Flag unsupported claims and exit with code 1 if unbacked claims exist.

# Rules
- Every quantitative claim must have an exact or rounded match in the ledger.
- Evade plagiarism and AI artifacts by phrasing empirical evidence clearly (Guardrail 5).

# Self-check list
- [ ] All claims in Abstract and Conclusion substantiated.
- [ ] Zero unsupported numbers reported.

# Failure modes
- Unsupported numerical claim triggers exit code 1.

# Definition of done
Claims report saved with status PASS and exit code 0.

# Example CLI Call
```bash
python3 .agents/skills/claims-check/scripts/claims_check.py --manuscript paper/manuscript.md
# Output: {"status": "PASS", "unsupported_claims": []}
```
