---
name: sim-runner
description: Runs smoke test, executes planned seeds, resumes interrupted runs, and populates ledger.
---

# Purpose
Executes planned evaluation seeds, saves individual run JSON files to `paper/runs/`, supports resuming interrupted executions, and records all metrics into `paper/results.csv`.

# When to use / not use
- **Use when**: Running benchmark simulations across seeds.
- **Do not use**: For statistical hypothesis testing or figure generation.

# Inputs
- `paper/paper.json`: Experiment plan.
- `paper/sim_engine.py`: Benchmark simulation engine.

# Outputs
- `paper/runs/run_*.json`: Individual seed run records.
- `paper/results.csv`: Ledger populated with all run metrics.

# Step-by-step method
1. Execute smoke test to ensure simulation stability.
2. Check `paper/runs/` and `paper/results.csv` to resume existing completed runs.
3. Compute code and config SHA256 hashes.
4. Execute remaining seeds and write run records.
5. Append rows to `paper/results.csv`.

# Rules
- Must run smoke test first.
- Resume capability: never rerun identical seed runs if output exists.
- Ledger entries must record `config_hash`, `code_hash`, and environment metadata.

# Self-check list
- [ ] Smoke test passes before full sweep.
- [ ] All planned seeds (e.g. 10 seeds) have run records in `paper/runs/`.
- [ ] Results ledger populated.

# Failure modes
- Smoke test failure stops execution and exits with code 1.

# Definition of done
All seeds executed, run records stored in `paper/runs/`, and results logged in ledger.

# Example CLI Call
```bash
python3 .agents/skills/sim-runner/scripts/sim_runner.py --smoke-test --run-all --config paper/paper.json
# Output: {"status": "success", "completed_runs": 30, "resumed_runs": 0}
```
