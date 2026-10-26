# IEEE Research Paper Autonomous Plugin (Phases 1, 2 & 3)

An enterprise-grade, fully autonomous research orchestration system for drafting, simulating, analyzing, formatting, reviewing, and packaging publication-ready IEEE Transactions papers.

The repository is built as a plug-and-play **Antigravity Customization Plugin** containing **29 specialized skills**, **5 parallel workflow waves**, and an immutable **results ledger** verifying every claim against experimental seeds.

---

## Quickstart: Plug-and-Play for Any IEEE Topic or AI Model

To retarget this entire autonomous pipeline to a brand new research topic (e.g., Federated Learning, 6G Edge Scheduling, or LLM Inference Serving):

1. **Update `paper/paper.json`**:
   Specify your paper title, authors, target venue (e.g., IEEE TCC, IEEE TPDS, IEEE TWC), problem formulation, and parameter sweeps:
   ```json
   {
     "title": "Your Novel Research Title",
     "target_venue": "IEEE Transactions on Cloud Computing",
     "primary_metric": "makespan",
     "baselines": ["Baseline-A", "Baseline-B"],
     "proposed_method": "YourMethod"
   }
   ```
2. **Execute Full Autonomous Pipeline**:
   ```bash
   python3 .agents/skills/submission-package/scripts/submission_package.py
   ```
3. **Inspect Submission Deliverables**:
   All artifacts are generated in `paper/submission_bundle/` and packaged as `paper/submission_bundle.zip` with cryptographic SHA-256 validation in `paper/submission_manifest.json`.

---

## 5-Wave Pipeline Architecture (29 Skills)

```
Wave 1: Ingestion & Specifications
  ├── paper-intake
  ├── venue-profile
  └── workload-generator

Wave 2: Simulation & Empirical Rigor
  ├── sim-builder
  ├── baseline-implementer
  ├── sim-runner
  ├── results-ledger
  ├── sim-validity-check
  └── stats-analyzer

Wave 3: Content Synthesis & IEEE Artifacts
  ├── methods-check
  ├── table-builder
  ├── figure-builder
  ├── flowchart-builder
  └── reference-formatter

Wave 4: Manuscript Assembly & Structural Audits
  ├── structure-review
  ├── front-matter-check
  ├── format-align
  ├── citation-check
  ├── graphics-compliance
  ├── claims-check
  └── numbers-check

Wave 5: Phase 3 Polish, Review & Packaging
  ├── author-voice (Evades AI detectors, enhances burstiness)
  ├── ai-disclosure (Enforces Guardrail 4 usage synchronization)
  ├── originality-guard (Audits n-gram overlap against literature)
  ├── permissions-register (Tracks intellectual property clearances)
  ├── terminology-check (Enforces acronym and symbol definitions)
  ├── reviewer-panel (Simulates 3-reviewer IEEE evaluation panel)
  ├── rebuttal (Generates point-by-point rebuttal citing ledger numbers)
  └── submission-package (Master pre-flight gate & ZIP packaging)
```

---

## Repository Structure

```
├── .agents/
│   ├── rules/
│   │   └── guardrails.md            # Exact rules governing empirical truth and ethics
│   ├── skills/                      # 29 independent skills with SKILL.md, scripts/, examples/
│   └── workflows/
│       ├── phase1_empirical_foundation.md
│       ├── phase2_manuscript_and_auditing.md
│       ├── phase3_polish_review_and_submission.md
│       └── full_autonomous_pipeline.md
├── paper/
│   ├── paper.json                   # Topic and configuration specifications
│   ├── venue.json                   # Venue layout parameters
│   ├── workloads.json               # Benchmark workload definitions
│   ├── results.csv                  # Single source of truth ledger
│   ├── manuscript.md                # Submission-ready IEEE manuscript
│   ├── manuscript.docx              # Auto-regenerated Word document
│   ├── figures/                     # 600 DPI vector PDFs and 300+ DPI PNGs
│   ├── tables/                      # LaTeX and Markdown tables
│   ├── reports/                     # Audit logs, peer review, and rebuttal
│   └── submission_bundle/           # Packaged deliverables
└── tests/                           # Complete test suite for all 29 skills
```

---

## Running Unit & Acceptance Tests

Execute all Phase 1, Phase 2, and Phase 3 unit tests:
```bash
python3 -m unittest discover tests
```

Execute Phase 3 acceptance workflow:
```bash
# 1. Author Voice Cadence Refinement
python3 .agents/skills/author-voice/scripts/author_voice.py

# 2. AI Disclosure Synchronization & Audit
python3 .agents/skills/ai-disclosure/scripts/ai_disclosure.py --sync
python3 .agents/skills/ai-disclosure/scripts/ai_disclosure.py --audit

# 3. Simulated 3-Reviewer IEEE Panel
python3 .agents/skills/reviewer-panel/scripts/reviewer_panel.py

# 4. Originality and CrossCheck Screening
python3 .agents/skills/originality-guard/scripts/originality_guard.py

# 5. Asset Permissions Register
python3 .agents/skills/permissions-register/scripts/permissions_register.py

# 6. Terminology & Acronym Consistency
python3 .agents/skills/terminology-check/scripts/terminology_check.py

# 7. Author Rebuttal Letter Generation
python3 .agents/skills/rebuttal/scripts/rebuttal_generator.py

# 8. Master Pre-Flight Gate & Submission Packaging
python3 .agents/skills/submission-package/scripts/submission_package.py
```
