# Workflow: Phase 3 - Polish, Review & Packaging

This workflow specifies the sequential and parallel execution stages for Phase 3 of the IEEE Research Paper Plugin, completing the autonomous pipeline from draft polish to submission bundle.

## Stage 1: Stylistic Cadence Profiling (`author-voice`)
- Ingest author writing samples from `paper/samples/` (auto-seeding `author_sample.txt` if needed).
- Measure sentence length burstiness (std/mean), passive/active ratio, and transition distribution.
- Polish `paper/manuscript.md` by replacing formulaic tropes with authentic transitions while strictly preserving all numerical values in `paper/results.csv`.
- CLI:
  ```bash
  python3 .agents/skills/author-voice/scripts/author_voice.py --manuscript paper/manuscript.md --samples paper/samples --output paper/reports/voice_edits.json --apply
  ```

## Stage 2: AI Usage Disclosure Synchronization (`ai-disclosure`)
- Audit `paper/reports/ai_usage_log.json` to ensure all assisted sections are tracked.
- Synchronize acknowledgment statement into `paper/reports/ai_acknowledgment.txt` and the `## Acknowledgment` section of `paper/manuscript.md`.
- Enforce Guardrail 4: exit with code 1 if any assisted section is omitted.
- CLI:
  ```bash
  python3 .agents/skills/ai-disclosure/scripts/ai_disclosure.py --sync
  python3 .agents/skills/ai-disclosure/scripts/ai_disclosure.py --audit
  ```

## Stage 3: Simulated 3-Reviewer IEEE Peer Review Panel (`reviewer-panel`)
- Simulate Reviewer 1 (Methodology & Math Rigor), Reviewer 2 (Experiments & Ledger Numbers), and Reviewer 3 (IEEE Formatting & Graphics).
- Generate structured scores and actionable questions.
- CLI:
  ```bash
  python3 .agents/skills/reviewer-panel/scripts/reviewer_panel.py --manuscript paper/manuscript.md --ledger paper/results.csv --figures paper/figures
  ```

## Stage 4: Prior Art Originality & CrossCheck Screening (`originality-guard`)
- Check 3-gram and 5-gram overlap between manuscript and `paper/sources/prior_abstracts.txt`.
- Verify composite similarity is <= 20% and provide official IEEE CrossCheck notice.
- CLI:
  ```bash
  python3 .agents/skills/originality-guard/scripts/originality_guard.py --manuscript paper/manuscript.md --sources paper/sources
  ```

## Stage 5: Asset Provenance & Permissions Audit (`permissions-register`)
- Index all figures, tables, and workload configurations.
- Verify intellectual property clearance status for all deliverables.
- CLI:
  ```bash
  python3 .agents/skills/permissions-register/scripts/permissions_register.py
  ```

## Stage 6: Acronym and Terminology Audit (`terminology-check`)
- Verify acronym expansions (SLA, MIPS, QoS) on first use.
- Confirm unified canonical method names (`Adaptive-DynaSched`, `Round-Robin`, `Min-Min`).
- CLI:
  ```bash
  python3 .agents/skills/terminology-check/scripts/terminology_check.py --manuscript paper/manuscript.md
  ```

## Stage 7: Empirical Rebuttal Generation (`rebuttal`)
- Extract peer review feedback and ground responses in numerical metrics from `paper/results.csv`.
- Generate point-by-point author rebuttal letter and structured response matrix.
- CLI:
  ```bash
  python3 .agents/skills/rebuttal/scripts/rebuttal_generator.py
  ```

## Stage 8: Master Pre-Flight Gate & Submission Packaging (`submission-package`)
- Execute 11-audit pre-flight gate.
- Regenerate `paper/manuscript.docx` from `paper/manuscript.md`.
- Package deliverables into `paper/submission_bundle/` and `paper/submission_bundle.zip` with SHA-256 manifest.
- CLI:
  ```bash
  python3 .agents/skills/submission-package/scripts/submission_package.py
  ```
