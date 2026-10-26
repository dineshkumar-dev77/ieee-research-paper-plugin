---
name: originality-guard
description: Audits n-gram overlap against literature sources and prevents plagiarism per Guardrail 5.
---

# Purpose
Audits manuscript text against domain literature sources for 3-gram, 5-gram, and verbatim sentence overlap to guarantee originality and prepare for IEEE CrossCheck / iThenticate screening.

# When to use / not use
- **Use when**: Performing originality pre-flight screening before journal submission.
- **Do not use**: For auditing numerical figures or checking code execution.

# Inputs
- `paper/manuscript.md`: Draft manuscript.
- `paper/sources/`: Prior literature abstracts and reference texts.

# Outputs
- `paper/reports/originality_report.json`: Overlap metrics, similarity percentages, and screening reminder.

# Step-by-step method
1. Ingest reference texts from `paper/sources/` (auto-seeding `prior_abstracts.txt` if empty).
2. Tokenize manuscript text into clean sentences, 3-grams, and 5-grams.
3. Compute intersection and overlap ratios against source n-grams.
4. Flag high-overlap spans for author revision.
5. Emit similarity report and IEEE CrossCheck reminder.

# Rules
- Enforce Guardrail 5: zero unauthorized plagiarism or verbatim copy-paste.
- Exit code 1 if similarity exceeds the allowable threshold (default 20%).

# Self-check list
- [ ] 3-gram and 5-gram similarity under threshold.
- [ ] CrossCheck reminder included in output.

# Failure modes
- Overlap exceeding threshold triggers exit code 1.

# Definition of done
Report written to `paper/reports/originality_report.json` with exit code 0.

# Example CLI Call
```bash
python3 .agents/skills/originality-guard/scripts/originality_guard.py --manuscript paper/manuscript.md --sources paper/sources
```
