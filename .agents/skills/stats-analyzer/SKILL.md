---
name: stats-analyzer
description: Computes mean, std, 95% CI, p-values, Cohen's d, and appends summaries to ledger.
---

# Purpose
Performs rigorous inferential and descriptive statistical analysis on raw results in `paper/results.csv` and appends summary statistics back to the ledger.

# When to use / not use
- **Use when**: All seed runs are complete and statistical comparisons are needed.
- **Do not use**: Before raw simulation runs are recorded in `paper/results.csv`.

# Inputs
- `paper/results.csv`: Raw experimental results ledger.

# Outputs
- `paper/reports/stats_summary.json`: Detailed statistical results.
- `paper/reports/stats_summary.md`: Markdown summary report.
- `paper/results.csv`: Ledger updated with summary metrics.

# Step-by-step method
1. Read raw runs from `paper/results.csv`.
2. Compute mean, standard deviation, and 95% confidence intervals per method.
3. Perform Welch's t-test and compute Cohen's d against baselines.
4. Append summary statistics to `paper/results.csv`.
5. Export JSON and Markdown statistical reports.

# Rules
- Statistical significance must compute both p-value and effect size.
- Summary metrics appended to ledger must use seed `summary`.

# Self-check list
- [ ] 95% CI computed with appropriate critical t-values.
- [ ] Welch's t-test and Cohen's d calculated for each baseline.
- [ ] Summary rows appended to ledger.

# Failure modes
- Empty ledger or non-numeric values exits with code 1.

# Definition of done
Statistical reports written and summary metrics appended to ledger.

# Example CLI Call
```bash
python3 .agents/skills/stats-analyzer/scripts/stats_analyzer.py --ledger paper/results.csv --output paper/reports/stats_summary.json
# Output: {"status": "success", "summary_rows_added": 28}
```
