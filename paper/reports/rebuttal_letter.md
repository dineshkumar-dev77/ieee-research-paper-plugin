# IEEE Author Response & Rebuttal Letter
**Manuscript Title:** Dynamic Multi-Objective Task Scheduling in Heterogeneous Cloud Datacenters  
**Target Venue:** IEEE Transactions on Cloud Computing (TCC)  
**Authors' Response Date:** October 2026

Dear Editor and Reviewers,

We express our sincere gratitude to the Reviewers for their constructive critique and rigorous feedback. We have incorporated all recommendations into the revised manuscript, with point-by-point responses detailed below.

---
### Point 1 (Reviewer 1 - Methodology & Mathematical Rigor)
**Reviewer Comment:** *"How does the dispatch decision boundary adapt when node failure occurs mid-execution?"*

**Author Response:** We thank Reviewer 1 for this insightful observation. In Section III-C, we have clarified the dynamic decision boundary behavior under node degradation. Specifically, when a node experiences latency spikes, the dispatch heuristic shifts subsequent tasks to alternate processors within O(log |N|) time.

**Manuscript Revision:** Clarified dynamic fault mitigation in Section III-C.

---
### Point 2 (Reviewer 2 - Experimental Design, Baselines & Statistical Validity)
**Reviewer Comment:** *"Could the authors confirm whether makespan improvements persist across skewed workload traces?"*

**Author Response:** We appreciate Reviewer 2's feedback regarding workload distribution sensitivity. Across 10 randomized evaluation seeds recorded in paper/results.csv, Adaptive-DynaSched consistently outperforms Round-Robin by 22.41% in makespan (482.15s vs. 621.40s, p < 10^-6, Cohen's d = 2.45), even under skewed arrivals.

**Manuscript Revision:** Referenced 10-seed empirical ledger verification in Section IV-B.

---
### Point 3 (Reviewer 3 - IEEE Formatting, Graphics & Presentation)
**Reviewer Comment:** *"Are all vector graphics prepared to scale cleanly to 3.5-inch column constraints without line weight loss?"*

**Author Response:** We thank Reviewer 3 for highlighting graphical presentation clarity. All architectural and data flow diagrams have been rendered as 600 DPI vector PDFs and 300+ DPI PNGs conforming to IEEE 3.5-inch column guidelines.

**Manuscript Revision:** Enhanced vector graphic scaling and label typography in Section V.

---
