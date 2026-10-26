---
name: paper-intake
description: Ingests author requirements and auto-fills missing system parameters per Guardrail 7.
---

# Purpose
Reads an author's topic, paper draft, or configuration and auto-fills any missing experimental parameters using simulated and domain benchmark defaults.

# When to use / not use
- **Use when**: Initializing a new paper project or onboarding an author draft with incomplete parameters.
- **Do not use**: For executing benchmark simulations directly.

# Inputs
- `paper/paper.json`: Project experiment plan.

# Outputs
- `paper/paper.json`: Completed experiment specification.

# Step-by-step method
1. Parse author configuration or existing `paper/paper.json`.
2. Inspect required parameters (task count, node profiles, arrival rates, seeds).
3. If parameters are missing, auto-fill with reproducible cloud scheduling defaults per Guardrail 7.
4. Save validated `paper/paper.json`.

# Rules
- When an input is missing, use simulated values or standard domain defaults (Guardrail 7).
- Preserve all author-specified overrides.

# Self-check list
- [ ] `paper/paper.json` contains complete system parameters and seed definitions.
- [ ] Task count, node count, and power profiles are populated.

# Failure modes
- Invalid JSON input exits with code 1.

# Definition of done
`paper/paper.json` contains fully specified parameters with exit code 0.

# Example CLI Call
```bash
python3 .agents/skills/paper-intake/scripts/paper_intake.py --config paper/paper.json
# Output: {"status": "success", "domain": "cloud_task_scheduling", "seeds_count": 10}
```
