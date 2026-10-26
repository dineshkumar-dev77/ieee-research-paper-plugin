---
name: venue-profile
description: Configures and validates venue-specific formatting parameters in paper/venue.json.
---

# Purpose
Maintains venue-specific parameters (column widths, margins, typography, caption styles) in `paper/venue.json` so formatting logic is never hard-coded in skills.

# When to use / not use
- **Use when**: Initializing formatting constraints for an IEEE venue (conference or transactions) or querying layout dimensions for figures and tables.
- **Do not use**: For writing manuscript prose or executing simulation runs.

# Inputs
- `paper/venue.json`: Venue configuration profile.

# Outputs
- `paper/venue.json`: Validated or initialized venue parameters.

# Step-by-step method
1. Select target profile (`ieee_conference` or `ieee_transactions`).
2. Run `venue_profile.py --init --venue <profile> --output paper/venue.json`.
3. Validate schema using `--validate`.
4. Expose parameters via `--get-param <dot.path>` for table and figure generators.

# Rules
- Parameter values must never be hard-coded inside generator scripts.
- IEEE table captions must be above tables with Roman numerals.
- IEEE figure captions must be below figures with Arabic numerals.
- When an input is missing, use the default IEEE conference profile.

# Self-check list
- [ ] `paper/venue.json` exists and validates against schema.
- [ ] Single column width is 3.5 in and double column width is 7.16 in.
- [ ] Captions follow IEEE table (Roman above) and figure (Arabic below) rules.

# Failure modes
- Corrupted JSON or missing required layout sections exits with code 1.
- Querying non-existent parameter exits with code 1.

# Definition of done
`paper/venue.json` is validated with exit code 0 and ready for downstream skills.

# Example CLI Call
```bash
python3 .agents/skills/venue-profile/scripts/venue_profile.py --init --venue ieee_conference --output paper/venue.json
# Output: {"status": "initialized", "venue_file": "paper/venue.json", "profile": "ieee_conference"}
```
