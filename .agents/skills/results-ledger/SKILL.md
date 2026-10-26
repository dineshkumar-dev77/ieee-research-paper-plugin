---
name: results-ledger
description: Enforces paper/results.csv as the single source of truth for all experimental numbers.
---

# Purpose
Acts as the single source of truth for all numbers reported in the paper. Verifies with `numbers_check.py` that no unbacked experimental claim enters the manuscript.

# When to use / not use
- **Use when**: Appending execution metrics, querying values, or auditing manuscript claims against `paper/results.csv`.
- **Do not use**: For generating synthetic figures without ledger backing.

# Inputs
- `paper/results.csv`: Results ledger with required schema.
- `paper/manuscript.md` (or `.docx`): Paper manuscript to audit.

# Outputs
- `paper/results.csv`: Initialized or updated ledger.
- `paper/reports/numbers_audit.json`: Audit log of matched and unmatched numbers.

# Step-by-step method
1. Initialize `paper/results.csv` with standard 11-column header.
2. Record all raw run records and statistical aggregates into the ledger.
3. Run `numbers_check.py` against the manuscript.
4. If unverified numbers are detected, fail with exit code 1.

# Rules
- Ledger columns: `run_id,metric,value,method,workload,seed,config_hash,code_hash,env,timestamp,source_file`.
- Every experimental number in the manuscript must match a ledger record.
- If code cannot be executed, generate simulation code, execute it, and record values.

# Self-check list
- [ ] Ledger contains exact required header columns.
- [ ] `numbers_check.py` returns exit code 0 on verified manuscript.
- [ ] Any tampered number triggers exit code 1.

# Failure modes
- Missing ledger columns or empty ledger triggers validation failure.
- Experimental claim not found in ledger exits with code 1.

# Definition of done
All experimental numbers in the manuscript are verified against the ledger with exit code 0.

# Example CLI Call
```bash
python3 .agents/skills/results-ledger/scripts/numbers_check.py --manuscript paper/manuscript.md --ledger paper/results.csv
# Output: [PASS] All experimental numbers verified against ledger.
```
