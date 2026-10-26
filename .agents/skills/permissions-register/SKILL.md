---
name: permissions-register
description: Tracks third-party assets, datasets, and figures in paper/reports/permissions_register.json.
---

# Purpose
Compiles and audits intellectual property, provenance, copyright, and licensing records for all figures, tables, and benchmark datasets incorporated into the manuscript.

# When to use / not use
- **Use when**: Preparing final submission assets and verifying IEEE copyright compliance.
- **Do not use**: For auditing prose stylistic voice or calculating statistics.

# Inputs
- `paper/figures/*.json`: Figure metadata files.
- `paper/tables/*.json`: Table metadata files.
- `paper/workloads.json`: Workload specifications.

# Outputs
- `paper/reports/permissions_register.json`: Clearance registry covering all paper assets.

# Step-by-step method
1. Discover all figure descriptors in `paper/figures/`.
2. Discover all table descriptors in `paper/tables/`.
3. Read workload and benchmark specifications in `paper/workloads.json`.
4. Validate copyright ownership (author original vs. third-party open access).
5. Compile comprehensive clearances into `paper/reports/permissions_register.json`.

# Rules
- Every asset must have an explicit provenance and license status.
- Third-party copyrighted material without license clearance causes audit failure.

# Self-check list
- [ ] All figures and tables indexed.
- [ ] Clearance status set to "CLEARED" for all entries.

# Failure modes
- Unregistered assets or missing workload configs return exit code 1.

# Definition of done
Complete permissions register generated with exit code 0.

# Example CLI Call
```bash
python3 .agents/skills/permissions-register/scripts/permissions_register.py
```
