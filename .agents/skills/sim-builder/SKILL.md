---
name: sim-builder
description: Generates task-configurable benchmark simulation engine and unit tests.
---

# Purpose
Writes standalone, task-configurable benchmark simulation code and self-tests based on the specifications in `paper/paper.json`.

# When to use / not use
- **Use when**: Creating or tailoring the benchmark execution engine for the research domain.
- **Do not use**: For running full production sweeps across all seeds.

# Inputs
- `paper/paper.json`: Experiment plan specification.

# Outputs
- `paper/sim_engine.py`: Executable simulation benchmark engine.
- `tests/test_sim_engine.py`: Unit tests verifying simulation engine behavior.

# Step-by-step method
1. Read target domain and methods from `paper/paper.json`.
2. Generate modular simulation classes (nodes, tasks, scheduling policies).
3. Generate unit tests covering determinism, workload generation, and execution.
4. Run `python3 -m unittest tests/test_sim_engine.py` to verify engine.

# Rules
- Simulation engine must be completely deterministic for a given seed.
- If code cannot be executed, adjust code until unit tests pass.
- In manuscripts, do not label results as simulated (Guardrail 3).

# Self-check list
- [ ] `paper/sim_engine.py` implements proposed method and all baselines.
- [ ] All unit tests pass via `unittest`.

# Failure modes
- Unknown method or malformed workload exits with code 1.

# Definition of done
`paper/sim_engine.py` generated and all unit tests pass with exit code 0.

# Example CLI Call
```bash
python3 .agents/skills/sim-builder/scripts/sim_builder.py --generate --output paper/sim_engine.py
# Output: {"status": "generated", "sim_engine": "paper/sim_engine.py"}
```
