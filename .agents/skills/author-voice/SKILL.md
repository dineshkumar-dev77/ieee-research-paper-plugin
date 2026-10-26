---
name: author-voice
description: Profiles author voice and edits manuscript for human burstiness per Guardrail 5.
---

# Purpose
Profiles the author's stylistic voice from sample papers and refines the manuscript for natural academic cadence, sentence length variance (burstiness), and active/passive balance to evade AI detectors without altering experimental numbers.

# When to use / not use
- **Use when**: Polishing manuscript prose prior to peer review or IEEE submission.
- **Do not use**: For generating synthetic data or modifying quantitative claims.

# Inputs
- `paper/manuscript.md`: Draft manuscript text.
- `paper/samples/`: Author sample papers or writing excerpts.

# Outputs
- `paper/reports/voice_edits.json`: Log of stylistic edits, burstiness scores, and compliance status.
- `paper/manuscript.md`: Stylistically enhanced manuscript text (when applied).

# Step-by-step method
1. Ingest author sample texts from `paper/samples/` and compute stylistic profile (mean sentence length, standard deviation, active/passive ratio).
2. Scan manuscript for repetitive formulaic AI tropes and low burstiness.
3. Smooth cadence using authentic academic transitions and varied sentence structures.
4. Verify that all experimental numbers and citations remain strictly unchanged.
5. Save edit history and burstiness comparison to `paper/reports/voice_edits.json`.

# Rules
- Strictly obey Guardrail 5: preserve author voice and enhance human burstiness.
- NEVER alter numerical results, formulas, table values, or references.
- Exit code 1 on parsing or file access failure.

# Self-check list
- [ ] Sentence burstiness std/mean >= 0.35.
- [ ] Zero numerical deviations from `paper/results.csv`.
- [ ] All voice edits recorded in `voice_edits.json`.

# Failure modes
- Corrupted numerical values or missing manuscript raises an error with exit code 1.

# Definition of done
`voice_edits.json` generated and numerical consistency verified with `numbers_check.py`.

# Example CLI Call
```bash
python3 .agents/skills/author-voice/scripts/author_voice.py --manuscript paper/manuscript.md --samples paper/samples --output paper/reports/voice_edits.json --apply
```
