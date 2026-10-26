---
name: flowchart-builder
description: Generates Mermaid architecture and renders 600 DPI IEEE system architecture diagram.
---

# Purpose
Generates a Mermaid architecture diagram (`paper/figures/fig_2_arch.mmd`) and renders publication-grade vector PDF and high-resolution line art PNG (>=600 DPI, 3.5 in width).

# When to use / not use
- **Use when**: Creating system architecture or scheduling pipeline diagrams.
- **Do not use**: For statistical bar charts (use `figure-builder`).

# Inputs
- System architecture components and parameters.

# Outputs
- `paper/figures/fig_2_arch.mmd`: Mermaid diagram source.
- `paper/figures/fig_2.png`: 600 DPI line art diagram.
- `paper/figures/fig_2.pdf`: Vector PDF diagram.
- `paper/figures/fig_2.json`: Caption and dimension metadata.

# Step-by-step method
1. Generate Mermaid architecture flow source.
2. Render crisp 600 DPI line art diagram using Matplotlib patches.
3. Set width to 3.5 in single-column width.
4. Export PNG, PDF, and metadata JSON with caption "Fig. 2. Proposed Adaptive-DynaSched system architecture and scheduling pipeline."

# Rules
- Line art resolution must be >= 600 DPI.
- Caption must use "Fig. N." format below the figure.

# Self-check list
- [ ] Mermaid file and 600 DPI PNG generated.
- [ ] Figure width is 3.5 in.
- [ ] Caption matches IEEE standard.

# Failure modes
- Rendering error exits with code 1.

# Definition of done
Diagram and metadata generated in `paper/figures/` with exit code 0.

# Example CLI Call
```bash
python3 .agents/skills/flowchart-builder/scripts/flowchart_builder.py --output-dir paper/figures/ --fig-number 2
# Output: {"status": "success", "fig_number": 2, "png_file": "paper/figures/fig_2.png"}
```
