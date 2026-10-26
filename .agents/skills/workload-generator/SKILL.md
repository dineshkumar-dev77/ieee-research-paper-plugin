---
name: workload-generator
description: Generates reproducible benchmark workload metadata and parameter sweeps in paper/workloads.json.
---

# Purpose
Generates reproducible cloud benchmark workload profiles, arrival rates, task instruction distributions, and parameter sweep definitions.

# When to use / not use
- **Use when**: Configuring workload traces and parameter sweep matrices.
- **Do not use**: For running individual simulation seeds.

# Inputs
- Workload parameters or default configuration.

# Outputs
- `paper/workloads.json`: Complete workload trace specification.

# Step-by-step method
1. Define task volume, node count, and Poisson arrival rate.
2. Establish task instruction bounds and SLA slack factors.
3. Configure parameter sweeps for arrival intensity.
4. Save to `paper/workloads.json`.

# Rules
- Workload parameters must match realistic cloud traces (e.g. Google cluster trace distributions).
- Random seeds must be explicitly recorded for determinism.

# Self-check list
- [ ] `paper/workloads.json` includes task distributions and SLA tiers.
- [ ] Arrival parameter sweeps defined.

# Failure modes
- Invalid parameters exit with code 1.

# Definition of done
`paper/workloads.json` written with exit code 0.

# Example CLI Call
```bash
python3 .agents/skills/workload-generator/scripts/workload_generator.py --tasks 1000 --nodes 16
# Output: {"status": "success", "workload_file": "paper/workloads.json"}
```
