---
name: ai-disclosure
description: Maintains AI usage log and generates matching acknowledgment statement per Guardrail 4.
---

# Purpose
Audits AI usage documentation and ensures bidirectional synchronization between `paper/reports/ai_usage_log.json`, `paper/reports/ai_acknowledgment.txt`, and the manuscript `## Acknowledgment` section per Guardrail 4.

# When to use / not use
- **Use when**: Verifying AI disclosure integrity, logging new assisted sections, or packaging for IEEE submission.
- **Do not use**: For editing experimental results or rewriting technical contributions.

# Inputs
- `paper/reports/ai_usage_log.json`: Structured registry of AI-assisted sections.
- `paper/reports/ai_acknowledgment.txt`: Standalone acknowledgment text.
- `paper/manuscript.md`: Paper manuscript.

# Outputs
- Synchronized acknowledgment files and exit code 0 on compliance.

# Step-by-step method
1. Parse `ai_usage_log.json` to extract all logged sections and assistance types.
2. In `--sync` mode, regenerate `ai_acknowledgment.txt` and update `## Acknowledgment` in `paper/manuscript.md`.
3. In `--audit` mode, verify every logged section is explicitly cited in `ai_acknowledgment.txt` and `paper/manuscript.md`.
4. Fail with exit code 1 if any logged section is missing or statements are desynchronized.

# Rules
- Guardrail 4: All AI assistance must be logged and match the acknowledgment statement.
- Exit code 1 upon any desynchronization or omitted section.

# Self-check list
- [ ] Every section in `ai_usage_log.json` appears in `ai_acknowledgment.txt`.
- [ ] Statement in `paper/manuscript.md` matches `ai_acknowledgment.txt`.

# Failure modes
- Desynchronized statements or missing section entries trigger exit code 1.

# Definition of done
Audit confirms full alignment with exit code 0.

# Example CLI Call
```bash
python3 .agents/skills/ai-disclosure/scripts/ai_disclosure.py --audit
```
