---
name: figure-builder
description: Generates publication-ready IEEE figures (captions below as Fig. N.) from ledger data.
---

# Purpose
Generates IEEE publication-quality figures (PNG >=300 DPI, vector PDF) strictly from ledger data, respecting IEEE column widths and caption conventions.

# When to use / not use
- **Use when**: Rendering visual plots for experimental evaluation.
- **Do not use**: For tabular representation of results.

# Inputs
- `paper/results.csv`: Results ledger.
- `paper/venue.json`: Venue layout configuration.

# Outputs
- `paper/figures/fig_1.png`: Raster figure (>=300 DPI).
- `paper/figures/fig_1.pdf`: Vector figure.
- `paper/figures/fig_1.json`: Figure metadata and caption.

# Step-by-step method
1. Query metric values from `paper/results.csv`.
2. Set figure dimensions to 3.5 in (single column) or 7.16 in (double column).
3. Render bar chart with error bars and value labels.
4. Format caption below as `Fig. N.` with Arabic numerals.
5. Export PNG (>=300 DPI) and PDF vector files.

# Rules
- Captions must be positioned BELOW the figure as `Fig. N.`.
- Width must match venue column width (3.5 in or 7.16 in).
- Minimum resolution >= 300 DPI.

# Self-check list
- [ ] Figure caption uses `Fig. N.` format with Arabic numeral.
- [ ] Dimensions and DPI comply with IEEE standards.
- [ ] Vector PDF and PNG files exist.

# Failure modes
- Missing metric in ledger exits with code 1.

# Definition of done
IEEE figure PNG and PDF generated in `paper/figures/` with exit code 0.

# Example CLI Call
```bash
python3 .agents/skills/figure-builder/scripts/figure_builder.py --ledger paper/results.csv --venue paper/venue.json --fig-number 1
# Output: {"status": "success", "fig_number": 1, "caption": "Fig. 1. ..."}
```
