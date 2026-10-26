---
name: graphics-compliance
description: Audits figure DPI, dimensions, aspect ratio, and captions using Pillow against IEEE rules.
---

# Purpose
Scans all generated figures in `paper/figures/` using Pillow to verify compliance with IEEE graphics standards (>=300 DPI bitmap, >=600 DPI line art, 3.5 in or 7.16 in width).

# When to use / not use
- **Use when**: Verifying figure compliance prior to submission or acceptance testing.
- **Do not use**: For generating figures.

# Inputs
- `paper/figures/`: Directory of figure files.
- `paper/venue.json`: Venue parameters.

# Outputs
- `paper/reports/graphics_compliance.json`: Compliance report.

# Step-by-step method
1. Iterate over all PNG figures in `paper/figures/`.
2. Inspect image size, DPI, and calculate effective width in inches.
3. Verify width matches 3.5 in (single) or 7.16 in (double) column standards.
4. Verify DPI >= 300 (or >= 600 for line art).
5. Verify metadata caption format.

# Rules
- Raster graphics must be >= 300 DPI; line art must be >= 600 DPI.
- Dimensions must conform to IEEE venue column widths.

# Self-check list
- [ ] All figures pass DPI thresholds.
- [ ] Widths conform to column width standards.

# Failure modes
- Any figure under DPI threshold or non-compliant width exits with code 1.

# Definition of done
Compliance report indicates status PASS with exit code 0.

# Example CLI Call
```bash
python3 .agents/skills/graphics-compliance/scripts/graphics_compliance.py --figures-dir paper/figures
# Output: {"status": "PASS", "figures_checked": 2}
```
