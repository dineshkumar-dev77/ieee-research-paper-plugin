---
name: methods-check
description: Audits and enriches Section III mathematical notation, equations, and complexity.
---

# Purpose
Ensures Section III contains formal mathematical notation, cost optimization equations, variable definitions, and complexity analysis matching `paper/sim_engine.py`.

# When to use / not use
- **Use when**: Verifying or enriching the mathematical rigor of the methodology section.
- **Do not use**: For checking bibliographic references.

# Inputs
- `paper/manuscript.md`: Paper manuscript.
- `paper/sim_engine.py`: Simulation source code.

# Outputs
- `paper/manuscript.md`: Enriched manuscript (when run with `--enrich`).
- `paper/reports/methods_report.json`: Methodology compliance report.

# Step-by-step method
1. Audit Section III for mathematical formulations, cost objective J, and complexity O(M*N).
2. If missing specifics, automatically enrich Section III from `paper/sim_engine.py` (Guardrail 7).
3. Save audit report.

# Rules
- Mathematical symbols must match code implementation variables.
- Time and space complexity must be formally stated.

# Self-check list
- [ ] Section III defines task, node, latency, and SLA variables.
- [ ] Multi-objective cost equation is present.
- [ ] Computational complexity O(M*N) and memory O(N) documented.

# Failure modes
- Missing methodology details without `--enrich` exits with code 1.

# Definition of done
Section III verified with full mathematical rigor with exit code 0.

# Example CLI Call
```bash
python3 .agents/skills/methods-check/scripts/methods_check.py --manuscript paper/manuscript.md --enrich
# Output: {"status": "PASS", "enriched": true}
```
