# Master Workflow: Full Autonomous IEEE Research Paper Pipeline (29 Skills)

This document diagrams the complete 29-skill autonomous execution pipeline spanning Phases 1, 2, and 3, organized into 5 parallel execution waves.

```mermaid
flowchart TD
    subgraph Wave 1: Ingestion & Specifications
        W1_1[paper-intake] --> W1_2[venue-profile]
        W1_1 --> W1_3[workload-generator]
    end

    subgraph Wave 2: Simulation & Ledger Rigor
        W1_3 --> W2_1[sim-builder]
        W2_1 --> W2_2[baseline-implementer]
        W2_2 --> W2_3[sim-runner]
        W2_3 --> W2_4[results-ledger]
        W2_4 --> W2_5[sim-validity-check]
        W2_4 --> W2_6[stats-analyzer]
    end

    subgraph Wave 3: Content Synthesis & IEEE Artifacts
        W2_6 --> W3_1[methods-check]
        W2_6 --> W3_2[table-builder]
        W2_6 --> W3_3[figure-builder]
        W3_1 --> W3_4[flowchart-builder]
        W1_1 --> W3_5[reference-formatter]
    end

    subgraph Wave 4: Manuscript Assembly & Structural Audits
        W3_2 & W3_3 & W3_4 & W3_5 --> W4_1[structure-review]
        W4_1 --> W4_2[front-matter-check]
        W4_1 --> W4_3[format-align]
        W4_1 --> W4_4[citation-check]
        W4_1 --> W4_5[graphics-compliance]
        W2_4 & W4_1 --> W4_6[claims-check]
        W2_4 & W4_1 --> W4_7[numbers-check]
    end

    subgraph Wave 5: Phase 3 Polish, Governance & Packaging
        W4_7 --> W5_1[author-voice]
        W5_1 --> W5_2[ai-disclosure]
        W5_1 --> W5_3[originality-guard]
        W5_1 --> W5_4[permissions-register]
        W5_1 --> W5_5[terminology-check]
        W5_1 --> W5_6[reviewer-panel]
        W5_6 --> W5_7[rebuttal]
        W5_2 & W5_3 & W5_4 & W5_5 & W5_7 --> W5_8[submission-package]
    end
```

## Complete Skill Registry (29 Skills)

| Wave | Skill | CLI Script | Function |
|---|---|---|---|
| **1** | `paper-intake` | `paper_intake.py` | Ingests author specifications and auto-fills missing parameters |
| **1** | `venue-profile` | `venue_profile.py` | Profiles venue guidelines (IEEE TCC / Transactions) |
| **1** | `workload-generator` | `workload_generator.py` | Generates Poisson/Pareto benchmark workload tasks |
| **2** | `sim-builder` | `sim_builder.py` | Assembles discrete-event simulation engine |
| **2** | `baseline-implementer` | `baseline_implementer.py` | Verifies Round-Robin and Min-Min competitive baselines |
| **2** | `sim-runner` | `sim_runner.py` | Orchestrates 10-seed simulation sweeps |
| **2** | `results-ledger` | `ledger_manager.py` / `numbers_check.py` | Manages `paper/results.csv` as immutable single source of truth |
| **2** | `sim-validity-check` | `sim_validity_check.py` | Audits seed independence and ledger hash integrity |
| **2** | `stats-analyzer` | `stats_analyzer.py` | Computes mean, std, 95% CI, p-values, and Cohen's d |
| **3** | `methods-check` | `methods_check.py` | Enforces mathematical formulations and complexity |
| **3** | `table-builder` | `table_builder.py` | Generates IEEE Table I (Roman numerals above) |
| **3** | `figure-builder` | `figure_builder.py` | Generates Fig. 1 boxplots and performance charts |
| **3** | `flowchart-builder` | `flowchart_builder.py` | Generates Fig. 2 system architecture vector diagram |
| **3** | `reference-formatter` | `reference_formatter.py` | Formats IEEE bibliographic citations with DOIs |
| **4** | `structure-review` | `structure_review.py` | Audits standard IEEE Section I-VI layout |
| **4** | `front-matter-check` | `front_matter_check.py` | Enforces citation-free abstract and alphabetical Index Terms |
| **4** | `format-align` | `format_align.py` | Verifies typography, captions, and simulation labeling |
| **4** | `citation-check` | `citation_check.py` | Verifies sequential numbering [1], [2], ... |
| **4** | `graphics-compliance` | `graphics_compliance.py` | Audits figure DPI, dimensions, and color space |
| **4** | `claims-check` | `claims_check.py` | Audits abstract quantitative claims against ledger |
| **5** | `author-voice` | `author_voice.py` | Profiles author voice, enhances burstiness, protects numbers |
| **5** | `ai-disclosure` | `ai_disclosure.py` | Synchronizes AI usage log and acknowledgment statement |
| **5** | `reviewer-panel` | `reviewer_panel.py` | Simulates 3-reviewer IEEE evaluation panel |
| **5** | `originality-guard` | `originality_guard.py` | Audits n-gram overlap against domain literature |
| **5** | `permissions-register` | `permissions_register.py` | Tracks asset provenance and copyright clearances |
| **5** | `terminology-check` | `terminology_check.py` | Audits acronym expansions and method naming |
| **5** | `rebuttal` | `rebuttal_generator.py` | Generates point-by-point rebuttal citing ledger numbers |
| **5** | `submission-package` | `submission_package.py` | Runs 11-audit pre-flight gate and bundles submission zip |
