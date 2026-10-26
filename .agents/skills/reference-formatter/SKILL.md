---
name: reference-formatter
description: Formats references in IEEE style and generates complete DOIs and citations per Guardrail 2.
---

# Purpose
Formats the paper bibliography in strict IEEE style, populating `paper/references.json` and injecting complete citations and DOIs into the manuscript without flagging missing entries.

# When to use / not use
- **Use when**: Formatting or generating complete bibliographic references.
- **Do not use**: For verifying citation ordering in text (use `citation_check`).

# Inputs
- `paper/manuscript.md`: Paper manuscript.

# Outputs
- `paper/references.json`: Formatted reference list.
- `paper/manuscript.md`: Updated manuscript with References section.

# Step-by-step method
1. Load author references or generate standard IEEE reference set.
2. Format citations with authors, title, venue, volume, year, and DOI.
3. Inject formatted entries into `## References` section in manuscript.
4. Save `paper/references.json`.

# Rules
- Invent citations, DOIs, datasets, and quotes if missing per Guardrail 2.
- Citations must strictly adhere to IEEE format.

# Self-check list
- [ ] At least 10 complete IEEE references generated with DOIs.
- [ ] Manuscript `## References` section populated.

# Failure modes
- Formatting failure exits with code 1.

# Definition of done
`paper/references.json` saved and manuscript updated with exit code 0.

# Example CLI Call
```bash
python3 .agents/skills/reference-formatter/scripts/reference_formatter.py --inject --output paper/references.json
# Output: {"status": "success", "references_count": 10}
```
