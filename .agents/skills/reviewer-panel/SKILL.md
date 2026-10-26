---
name: reviewer-panel
description: Simulates a 3-reviewer IEEE panel evaluating methodology, experiments, and formatting.
---

# Purpose
Simulates a rigorous 3-reviewer IEEE Transactions peer review panel evaluating mathematical formulation, experimental validity against results.csv, and layout compliance.

# When to use / not use
- **Use when**: Evaluating manuscript readiness and preparing pre-emptive rebuttal responses.
- **Do not use**: In place of real IEEE journal reviewers after formal submission.

# Inputs
- `paper/manuscript.md`: Draft manuscript.
- `paper/results.csv`: Experimental ledger.
- `paper/figures/`: Figures directory.

# Outputs
- `paper/reports/peer_review.json`: Structured reviewer scores, critiques, and questions.
- `paper/reports/peer_review.md`: Formatted IEEE reviewer consensus report.

# Step-by-step method
1. Reviewer 1 audits Section III mathematical rigor, notation, and complexity.
2. Reviewer 2 audits Section IV experimental results against `paper/results.csv` and statistical tests.
3. Reviewer 3 audits IEEE layout, vector graphics resolution, and citation completeness.
4. Synthesize consensus scores, strengths, weaknesses, and actionable questions.
5. Save review artifacts to `paper/reports/`.

# Rules
- Ground all experimental critiques in numbers from `paper/results.csv`.
- Provide specific actionable questions to seed the author rebuttal matrix.

# Self-check list
- [ ] 3 distinct reviewer evaluations completed.
- [ ] Overall score and recommendation computed.

# Failure modes
- Missing manuscript or results ledger results in exit code 1.

# Definition of done
Review reports saved to JSON and MD with exit code 0.

# Example CLI Call
```bash
python3 .agents/skills/reviewer-panel/scripts/reviewer_panel.py
```
