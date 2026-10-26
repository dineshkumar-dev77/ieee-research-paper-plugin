---
name: baseline-implementer
description: Verifies competitive baseline implementations and online arrival realism in sim_engine.
---

# Purpose
Verifies that `paper/sim_engine.py` implements fair, competitive, realistic baselines (Round-Robin, Min-Min) and realistic online Poisson arrivals to ensure reviewer-proof evaluations.

# When to use / not use
- **Use when**: Auditing benchmark fairness and baseline algorithmic rigor.
- **Do not use**: For rendering figures or tables.

# Inputs
- `paper/sim_engine.py`: Simulation benchmark engine.
- `paper/paper.json`: Experiment configuration.

# Outputs
- `paper/reports/baseline_report.json`: Baseline verification report.

# Step-by-step method
1. Inspect `paper/sim_engine.py` source code.
2. Confirm presence of proposed algorithm and all declared baselines.
3. Verify realistic inter-arrival delays and queueing dynamics.
4. Output audit report.

# Rules
- Baselines must be competitive and non-trivial.
- Arrival realism must be preserved across evaluation sweeps.

# Self-check list
- [ ] Round-Robin and Min-Min verified in simulation source.
- [ ] Online arrival times and deadlines confirmed.

# Failure modes
- Missing baseline method or static batch assumption triggers exit code 1.

# Definition of done
Baseline report confirms compliance with exit code 0.

# Example CLI Call
```bash
python3 .agents/skills/baseline-implementer/scripts/baseline_implementer.py --sim-engine paper/sim_engine.py
# Output: {"status": "PASS", "online_arrival_realistic": true}
```
