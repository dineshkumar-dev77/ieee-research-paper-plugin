---
name: submission-package
description: Verifies pre-flight checks and bundles submission artifacts into a ZIP package.
---

# Purpose
Executes the master pre-flight audit gate across all 11 verification skills, regenerates `paper/manuscript.docx` from `paper/manuscript.md`, and bundles all submission-ready artifacts into a sealed submission bundle and manifest.

# When to use / not use
- **Use when**: Performing the final automated submission gate and packaging deliverables for IEEE Transactions.
- **Do not use**: As a substitute for running the simulation engine or building tables.

# Inputs
- Manuscript files (`paper/manuscript.md`).
- Tables (`paper/tables/table_1.tex`).
- Figures (`paper/figures/*.pdf`, `paper/figures/*.png`).
- Disclosures & Rebuttal (`paper/reports/ai_acknowledgment.txt`, `paper/reports/rebuttal_letter.md`).

# Outputs
- `paper/manuscript.docx`: Regenerated DOCX manuscript.
- `paper/submission_bundle/`: Directory containing all verified submission files.
- `paper/submission_bundle.zip`: Compressed archive for IEEE portal upload.
- `paper/submission_manifest.json`: Cryptographic SHA-256 manifest and audit log.

# Step-by-step method
1. Execute the 11-stage pre-flight audit gate as independent subprocesses.
2. Halt immediately with exit code 1 if any pre-flight audit returns non-zero.
3. Convert `paper/manuscript.md` into `paper/manuscript.docx`.
4. Copy all submission deliverables into `paper/submission_bundle/`.
5. Compress into `paper/submission_bundle.zip`.
6. Compute SHA-256 checksums and write `paper/submission_manifest.json`.

# Rules
- Any failing pre-flight audit terminates the packaging with exit code 1.
- All artifact checksums must be recorded in the manifest.

# Self-check list
- [ ] All 11 audits passed.
- [ ] Manuscript DOCX generated.
- [ ] SHA-256 hashes computed.

# Failure modes
- Any audit failure halts packaging and exits with code 1.

# Definition of done
`submission_manifest.json` and `submission_bundle.zip` created with exit code 0.

# Example CLI Call
```bash
python3 .agents/skills/submission-package/scripts/submission_package.py
```
