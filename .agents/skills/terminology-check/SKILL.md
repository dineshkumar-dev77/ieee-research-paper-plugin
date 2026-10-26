---
name: terminology-check
description: Enforces consistent acronyms, expansions, and symbol definitions across manuscript.
---

# Purpose
Audits the manuscript for consistent acronym expansions on first use, unified method naming (`Adaptive-DynaSched`, `Round-Robin`, `Min-Min`), and coherent mathematical notation ($\mathcal{N}, \mathcal{T}, \mu_j, 	au_{i,j}$).

# When to use / not use
- **Use when**: Reviewing draft manuscripts for terminology rigor prior to publication.
- **Do not use**: For auditing simulation seeds or verifying CSV numbers.

# Inputs
- `paper/manuscript.md`: Draft manuscript text.

# Outputs
- `paper/reports/terminology_report.json`: Detailed terminology audit report.

# Step-by-step method
1. Parse manuscript text and extract all uppercase acronyms.
2. Verify that technical acronyms (SLA, MIPS, QoS) have expansions on first use.
3. Check for unauthorized method name variations (e.g., casing or hyphenation errors).
4. Verify mathematical symbols ($\mathcal{N}, \mathcal{T}, \mu_j$) conform to Section III definitions.
5. Emit structured report; fail with exit code 1 if strict violations occur.

# Rules
- Acronyms must be defined upon first occurrence.
- Method names must strictly match canonical identifiers.

# Self-check list
- [ ] No undefined technical acronyms.
- [ ] Canonical method naming verified.

# Failure modes
- Naming inconsistencies under strict mode return exit code 1.

# Definition of done
Audit report saved to `paper/reports/terminology_report.json` with exit code 0.

# Example CLI Call
```bash
python3 .agents/skills/terminology-check/scripts/terminology_check.py --manuscript paper/manuscript.md
```
