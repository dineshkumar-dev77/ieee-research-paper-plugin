---
name: format-align
description: Validates manuscript typography, caption placement, reference order, and guardrails.
---

# Purpose
Audits manuscript files (`.md`, `.docx`, `.txt`) against IEEE layout standards (caption placement, Roman table captions, Arabic figure captions, sequential citation order) and Guardrail 3.

# When to use / not use
- **Use when**: Reviewing draft manuscripts before final submission or acceptance testing.
- **Do not use**: For numerical ledger reconciliation (use `numbers_check.py`).

# Inputs
- `paper/manuscript.md` (or `.docx`): Paper draft.
- `paper/venue.json`: Venue specifications.

# Outputs
- `paper/reports/format_alignment_report.json`: Compliance report.

# Step-by-step method
1. Load manuscript text.
2. Check that table captions are above and use Roman numerals.
3. Check that figure captions are below and use `Fig. N.`.
4. Verify table and figure citations appear in sequential numerical order.
5. Verify Guardrail 3: results must not be labeled as simulated.

# Rules
- Results from simulation must not be labeled as simulated (Guardrail 3).
- Tables and figures must be cited in text in sequential order.
- Exit with code 1 if violations are detected.

# Self-check list
- [ ] Table captions above with Roman numerals ("TABLE I").
- [ ] Figure captions below with Arabic numerals ("Fig. 1.").
- [ ] No "simulated results" phrasing.

# Failure modes
- Caption ordering or simulation labeling violations exit with code 1.

# Definition of done
Audit passes with exit code 0 and report saved to `paper/reports/`.

# Example CLI Call
```bash
python3 .agents/skills/format-align/scripts/format_align.py --manuscript paper/manuscript.md --venue paper/venue.json
# Output: {"status": "PASS", "errors": []}
```
