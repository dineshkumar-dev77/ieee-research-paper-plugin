---
name: table-builder
description: Generates IEEE-compliant tables (captions above with Roman numerals) from ledger data.
---

# Purpose
Generates publication-quality LaTeX, Markdown, and JSON tables strictly from `paper/results.csv` complying with IEEE style standards.

# When to use / not use
- **Use when**: Constructing comparative tables for manuscripts.
- **Do not use**: For generating plots or charts.

# Inputs
- `paper/results.csv`: Results ledger.
- `paper/venue.json`: Venue parameters.

# Outputs
- `paper/tables/table_1.tex`: LaTeX table markup.
- `paper/tables/table_1.md`: Markdown table.
- `paper/tables/table_1.json`: Structured table data.

# Step-by-step method
1. Extract metric statistics from `paper/results.csv`.
2. Format values as mean ± std.
3. Format IEEE caption above table with Roman numeral (e.g. `TABLE I`).
4. Generate LaTeX booktabs and Markdown tables in `paper/tables/`.

# Rules
- All numbers must originate strictly from `paper/results.csv`.
- Table caption must be positioned ABOVE the table with Roman numerals.
- Separate numbering from figures.

# Self-check list
- [ ] Table caption is above table with Roman numeral ("TABLE I").
- [ ] Values match ledger means and standard deviations.
- [ ] LaTeX and Markdown outputs generated.

# Failure modes
- Missing ledger data or invalid venue file exits with code 1.

# Definition of done
IEEE-compliant table files written in `paper/tables/` with exit code 0.

# Example CLI Call
```bash
python3 .agents/skills/table-builder/scripts/table_builder.py --ledger paper/results.csv --venue paper/venue.json --table-number 1
# Output: {"status": "success", "table_number": 1, "roman_numeral": "I"}
```
