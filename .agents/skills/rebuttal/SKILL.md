---
name: rebuttal
description: Generates point-by-point IEEE author rebuttal matrix citing ledger numbers.
---

# Purpose
Reads `paper/reports/peer_review.json` and `paper/results.csv` to generate an author rebuttal matrix and response letter citing exact empirical values, p-values, and manuscript updates.

# When to use / not use
- **Use when**: Formulating revision responses for peer review or preparing pre-emptive author rebuttals.
- **Do not use**: For modifying original experimental data in the ledger.

# Inputs
- `paper/reports/peer_review.json`: Peer review feedback.
- `paper/results.csv`: Experimental ledger.

# Outputs
- `paper/reports/rebuttal_matrix.json`: Structured response matrix.
- `paper/reports/rebuttal_letter.md`: Professional IEEE author response letter.

# Step-by-step method
1. Parse reviewer comments and actionable questions from `peer_review.json`.
2. Extract exact metrics, p-values, effect sizes, and baseline comparisons from `results.csv`.
3. Construct point-by-point responses referencing specific manuscript sections.
4. Export structured matrix and formatted rebuttal letter.

# Rules
- Every response to an experimental question must cite verified ledger figures.
- Never invent unbacked metrics.

# Self-check list
- [ ] Every reviewer comment addressed.
- [ ] Ledger figures cited in experimental responses.

# Failure modes
- Missing peer review JSON or ledger causes exit code 1.

# Definition of done
Rebuttal matrix and letter written with exit code 0.

# Example CLI Call
```bash
python3 .agents/skills/rebuttal/scripts/rebuttal_generator.py
```
