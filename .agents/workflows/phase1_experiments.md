# Phase 1 Experiments Workflow

This workflow orchestrates the end-to-end Phase 1 execution for empirical validation and IEEE paper artifacts.

## Phase 1 Execution Steps

1. **Venue Initialization (`venue-profile`)**:
   - Command: `python3 .agents/skills/venue-profile/scripts/venue_profile.py --init --venue ieee_conference --output paper/venue.json`
   - Verifies target column widths (3.5 in single column, 7.16 in two-column), typography, and IEEE caption rules.

2. **Ledger Setup (`results-ledger`)**:
   - Command: `python3 .agents/skills/results-ledger/scripts/ledger_manager.py --init --output paper/results.csv`
   - Establishes the single source of truth for all experimental numbers.

3. **Experiment Planning (`experiment-planner`)**:
   - Command: `python3 .agents/skills/experiment-planner/scripts/experiment_planner.py --plan --config paper/paper.json`
   - Formulates research questions, metrics, methods (proposed + baselines), parameter sweeps, workloads, and seed counts (default 10-30).

4. **Simulation Code Generation (`sim-builder`)**:
   - Command: `python3 .agents/skills/sim-builder/scripts/sim_builder.py --generate --config paper/paper.json --output paper/sim_engine.py`
   - Builds modular, reproducible benchmark execution code with self-tests.

5. **Simulation Execution (`sim-runner`)**:
   - Command: `python3 .agents/skills/sim-runner/scripts/sim_runner.py --smoke-test --run-all --config paper/paper.json --runs-dir paper/runs/ --ledger paper/results.csv`
   - Executes smoke test first; executes planned seeds; supports resume on interruption; saves run records into `paper/runs/` and logs to `paper/results.csv`.

6. **Statistical Analysis (`stats-analyzer`)**:
   - Command: `python3 .agents/skills/stats-analyzer/scripts/stats_analyzer.py --ledger paper/results.csv --output paper/reports/stats_summary.json`
   - Computes mean, std, 95% CI, p-values (Welch t-test), and effect size (Cohen's d). Appends summary metrics back to `paper/results.csv`.

7. **Table Construction (`table-builder`)**:
   - Command: `python3 .agents/skills/table-builder/scripts/table_builder.py --ledger paper/results.csv --venue paper/venue.json --output-dir paper/tables/`
   - Produces IEEE Table I formatted with Roman numerals above table ("TABLE I").

8. **Figure Construction (`figure-builder`)**:
   - Command: `python3 .agents/skills/figure-builder/scripts/figure_builder.py --ledger paper/results.csv --venue paper/venue.json --output-dir paper/figures/`
   - Produces publication-grade IEEE figures with Arabic captions below ("Fig. 1.") at >=300 DPI.

9. **Format Alignment & Number Verification (`format-align` & `numbers_check.py`)**:
   - Command: `python3 .agents/skills/format-align/scripts/format_align.py --manuscript paper/manuscript.md --venue paper/venue.json`
   - Command: `python3 .agents/skills/results-ledger/scripts/numbers_check.py --manuscript paper/manuscript.md --ledger paper/results.csv`
   - Verifies formatting compliance and strictly audits that every experimental figure/statistic in the text matches the ledger.
