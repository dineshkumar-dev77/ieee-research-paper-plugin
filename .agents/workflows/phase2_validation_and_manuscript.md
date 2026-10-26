# Phase 2 Workflow: Validation, Graphics, and Manuscript Synthesis

This workflow orchestrates the end-to-end Phase 2 execution pipeline across 12 specialized skills for rigorous experimental verification, automated structural auditing, IEEE compliance, and manuscript refinement.

## Execution Graph & Dependencies

```
[Author Input / Topic Draft]
           │
           ▼
   (paper-intake) ────► (baseline-implementer) ────► (workload-generator)
           │                                                │
           ▼                                                ▼
  (sim-validity-check) ◄──────────────────────── (paper/results.csv & runs/)
           │
           ├──────────────────────────────┬──────────────────────────────┐
           ▼                              ▼                              ▼
   (structure-review)              (methods-check)                (claims-check)
           │                              │                              │
           └──────────────────────────────┼──────────────────────────────┘
                                          ▼
                               (flowchart-builder)
                                          │
                                          ▼
                             (graphics-compliance)
                                          │
           ┌──────────────────────────────┴──────────────────────────────┐
           ▼                                                             ▼
  (reference-formatter)                                         (front-matter-check)
           │                                                             │
           ▼                                                             ▼
   (citation_check) ──────────────────────────────────────────► [Verified Manuscript]
```

## Detailed Execution Steps

### Stage 1: Ingestion and Baseline Rigor
1. **Paper Intake (`paper-intake`)**:
   - `python3 .agents/skills/paper-intake/scripts/paper_intake.py --config paper/paper.json --domain cloud_task_scheduling`
   - Ingests user requirements; auto-fills missing system parameters with historical cloud benchmarks per Guardrail 7.
2. **Baseline Realism Verification (`baseline-implementer`)**:
   - `python3 .agents/skills/baseline-implementer/scripts/baseline_implementer.py --sim-engine paper/sim_engine.py --config paper/paper.json`
   - Ensures online arrival realism and competitive baseline implementations (Min-Min, Round-Robin).
3. **Workload Specification (`workload-generator`)**:
   - `python3 .agents/skills/workload-generator/scripts/workload_generator.py --tasks 1000 --nodes 16 --output paper/workloads.json`
   - Generates trace parameters and synthetic arrival models.

### Stage 2: Simulation Validity & Ledger Integrity
4. **Simulation Validity Audit (`sim-validity-check`)**:
   - `python3 .agents/skills/sim-validity-check/scripts/sim_validity_check.py --runs-dir paper/runs/ --ledger paper/results.csv --min-seeds 10`
   - Verifies seed count (>=10), seed variance > 0, hash integrity, and metric completeness.

### Stage 3: Narrative & Scientific Auditing (Can run in parallel)
5. **Structure Review (`structure-review`)**:
   - `python3 .agents/skills/structure-review/scripts/structure_review.py --manuscript paper/manuscript.md`
   - Enforces presence of all mandatory IEEE sections.
6. **Methods Rigor & Mathematical Enrichment (`methods-check`)**:
   - `python3 .agents/skills/methods-check/scripts/methods_check.py --manuscript paper/manuscript.md --sim-engine paper/sim_engine.py`
   - Verifies notation consistency, cost equations, and complexity analysis ($O(M \cdot N)$).
7. **Empirical Claims Reconciliation (`claims-check`)**:
   - `python3 .agents/skills/claims-check/scripts/claims_check.py --manuscript paper/manuscript.md --ledger paper/results.csv --stats paper/reports/stats_summary.json`
   - Traces every qualitative and quantitative claim back to ledger evidence.

### Stage 4: Visuals & IEEE Graphics Compliance
8. **System Architecture Flowchart (`flowchart-builder`)**:
   - `python3 .agents/skills/flowchart-builder/scripts/flowchart_builder.py --output-dir paper/figures/ --fig-number 2`
   - Generates `fig_2_arch.mmd` and renders vector PDF and high-res PNG (>=600 DPI line art).
9. **Graphics Compliance Audit (`graphics-compliance`)**:
   - `python3 .agents/skills/graphics-compliance/scripts/graphics_compliance.py --figures-dir paper/figures/ --venue paper/venue.json`
   - Validates dimensions (3.5 in / 7.16 in), DPI thresholds (>=300 bitmap, >=600 line art), and metadata.

### Stage 5: Scholarly Integrity & Formatting
10. **Reference Formatting (`reference-formatter`)**:
    - `python3 .agents/skills/reference-formatter/scripts/reference_formatter.py --manuscript paper/manuscript.md --output paper/references.json`
    - Injects standardized IEEE citations and DOIs per Guardrail 2.
11. **Citation Sequence Verification (`citation_check`)**:
    - `python3 .agents/skills/citation_check/scripts/citation_check.py --manuscript paper/manuscript.md`
    - Ensures monotonic sequential citations ([1], [2], ...) with no orphan entries.
12. **Front-Matter Compliance (`front-matter-check`)**:
    - `python3 .agents/skills/front-matter-check/scripts/front_matter_check.py --manuscript paper/manuscript.md`
    - Ensures Abstract has zero citations/equations and Index Terms are strictly alphabetical.
