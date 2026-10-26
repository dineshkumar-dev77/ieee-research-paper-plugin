---
name: experiment-planner
description: Plans research questions, baselines, sweeps, and seed runs in paper/paper.json.
---

# Purpose
Translates research objectives into an executable experiment matrix: research questions, primary metrics, proposed methods, baselines, workloads, parameter sweeps, and random seeds (default 10-30).

# When to use / not use
- **Use when**: Designing benchmark evaluations before executing simulations or writing evaluation text.
- **Do not use**: For executing simulation loops directly.

# Inputs
- Research problem description or existing `paper/paper.json`.

# Outputs
- `paper/paper.json`: Comprehensive experimental plan specification.

# Step-by-step method
1. Define research questions (RQs) paired with primary metrics.
2. Specify proposed algorithm and comparative baselines.
3. Configure workloads and random seeds (10 to 30 seeds).
4. Validate schema using `experiment_planner.py --validate`.

# Rules
- Must include at least one proposed method and at least two baselines.
- Minimum number of seeds is 10 (range 10-30).
- When input parameters are missing, use standard domain benchmarks.

# Self-check list
- [ ] `paper/paper.json` includes RQs, metrics, methods, workloads, and seeds.
- [ ] Seed count is between 10 and 30.
- [ ] Validation command exits with code 0.

# Failure modes
- Missing required sections or seed count < 1 exits with code 1.

# Definition of done
Validated `paper/paper.json` containing complete experimental configuration.

# Example CLI Call
```bash
python3 .agents/skills/experiment-planner/scripts/experiment_planner.py --init --seeds 10 --config paper/paper.json
# Output: {"status": "initialized", "config": "paper/paper.json", "seeds": 10}
```
