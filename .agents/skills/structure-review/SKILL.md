---
name: structure-review
description: Audits manuscript structure against required IEEE sections.
---

# Purpose
Verifies that the paper manuscript contains all mandatory IEEE sections (Abstract, Index Terms, I. Introduction through V. Conclusion, and References).

# When to use / not use
- **Use when**: Reviewing draft completeness before submission or acceptance testing.
- **Do not use**: For detailed mathematical notation checking (use `methods-check`).

# Inputs
- `paper/manuscript.md` (or `.docx`): Paper draft.

# Outputs
- `paper/reports/structure_report.json`: Section audit report.

# Step-by-step method
1. Load manuscript text.
2. Scan for required section headings.
3. Verify presence of Abstract, Index Terms, Sections I-V, and References.
4. Export report and exit with code 1 if any required section is absent.

# Rules
- All required IEEE sections must be present.
- Section titles must follow IEEE Roman numeral ordering.

# Self-check list
- [ ] All 8 required IEEE sections identified.
- [ ] Report saved to `paper/reports/structure_report.json`.

# Failure modes
- Missing any required section exits with code 1.

# Definition of done
Manuscript confirmed to possess all required IEEE sections with exit code 0.

# Example CLI Call
```bash
python3 .agents/skills/structure-review/scripts/structure_review.py --manuscript paper/manuscript.md
# Output: {"status": "PASS", "found_count": 8, "missing_sections": []}
```
