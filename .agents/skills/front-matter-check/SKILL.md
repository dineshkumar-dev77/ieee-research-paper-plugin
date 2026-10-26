---
name: front-matter-check
description: Enforces citation-free, equation-free Abstract and alphabetical Index Terms.
---

# Purpose
Audits Title, Abstract, and Index Terms in `paper/manuscript.md` ensuring IEEE compliance: no equations or citations in Abstract, and strict alphabetical sorting of Index Terms.

# When to use / not use
- **Use when**: Auditing paper front matter before submission or testing.
- **Do not use**: For verifying experimental sections.

# Inputs
- `paper/manuscript.md`: Paper manuscript.

# Outputs
- `paper/reports/front_matter_report.json`: Front matter compliance report.

# Step-by-step method
1. Extract Title, Abstract, and Index Terms.
2. Check that Abstract contains zero citations and zero equations.
3. Verify that Index Terms are sorted in strict alphabetical order.
4. Output report and exit with code 1 if any violation is found.

# Rules
- Abstract must be plain text with zero citations and zero equations.
- Index Terms must be strictly alphabetical.

# Self-check list
- [ ] Abstract contains no `[N]` citations or mathematical symbols.
- [ ] Index Terms are alphabetically ordered.

# Failure modes
- Citation or equation in Abstract, or unsorted Index Terms exits with code 1.

# Definition of done
Front matter audit passes with exit code 0.

# Example CLI Call
```bash
python3 .agents/skills/front-matter-check/scripts/front_matter_check.py --manuscript paper/manuscript.md
# Output: {"status": "PASS", "index_terms": ["Cloud computing", ...]}
```
