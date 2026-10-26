---
name: sim-validity-check
description: Audits seed counts, seed independence, metric completeness, and ledger hash integrity.
---

# Purpose
Verifies that experimental run records in `paper/runs/` and `paper/results.csv` meet strict scientific reproducibility criteria (>=10 seeds, variance > 0, hash integrity).

# When to use / not use
- **Use when**: Validating raw simulation outputs before statistical analysis or manuscript updates.
- **Do not use**: For generating plots.

# Inputs
- `paper/runs/`: Directory of seed execution JSON records.
- `paper/results.csv`: Experimental ledger.

# Outputs
- `paper/reports/sim_validity_report.json`: Simulation validity report.

# Step-by-step method
1. Verify total run records and seed count (>=10 per method).
2. Compute sample variance across seeds to ensure stochastic independence.
3. Validate presence of `code_hash` and `config_hash`.
4. Output report.

# Rules
- Minimum seed count is 10.
- Stochastic metrics must exhibit non-zero variance across seeds.

# Self-check list
- [ ] At least 10 seeds executed per method.
- [ ] Variance > 0 across seeds for makespan and latency.
- [ ] Valid code and config hashes recorded.

# Failure modes
- Seed count < 10 or zero variance across seeds exits with code 1.

# Definition of done
Simulation validity verified with exit code 0.

# Example CLI Call
```bash
python3 .agents/skills/sim-validity-check/scripts/sim_validity_check.py --runs-dir paper/runs --ledger paper/results.csv
# Output: {"status": "PASS", "runs_analyzed": 30}
```
