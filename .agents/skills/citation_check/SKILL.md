---
name: citation_check
description: Verifies sequential in-text citations ([1], [2], ...) and matching reference entries.
---

# Purpose
Audits the manuscript to ensure all in-text citations appear in sequential numerical order ([1], [2], ...) and that every in-text citation has a corresponding entry in References.

# When to use / not use
- **Use when**: Reviewing citation integrity and ordering in the manuscript.
- **Do not use**: For checking number values in evaluation (use `numbers_check.py`).

# Inputs
- `paper/manuscript.md`: Paper manuscript.

# Outputs
- `paper/reports/citation_report.json`: Citation integrity report.

# Step-by-step method
1. Parse in-text citation tokens from the body.
2. Verify citations appear in strictly increasing sequential order of first mention.
3. Parse entries in the References section.
4. Flag any orphan or uncited reference.

# Rules
- In-text citations must be sequential ([1], [2], [3], ...).
- No orphan in-text citations and no uncited bibliography entries.

# Self-check list
- [ ] Citations appear in numerical sequence.
- [ ] Set of in-text citations exactly equals set of references.

# Failure modes
- Out-of-order citation or orphan reference triggers exit code 1.

# Definition of done
Citation report confirms compliance with status PASS and exit code 0.

# Example CLI Call
```bash
python3 .agents/skills/citation_check/scripts/citation_check.py --manuscript paper/manuscript.md
# Output: {"status": "PASS", "citations_found_count": 10}
```
