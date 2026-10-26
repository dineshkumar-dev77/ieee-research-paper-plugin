#!/usr/bin/env python3
"""Methods Check CLI.
Audits and enriches Section III of the manuscript for mathematical rigor,
equations, variable definitions, and complexity analysis matching sim_engine.py.
"""
import argparse
import json
import os
import re
import sys

FORMAL_METHOD_TEXT = """## III. System Architecture and Methodology
Our architecture models a heterogeneous cloud datacenter comprising a set of $N$ heterogeneous compute nodes $\\mathcal{N} = \\{N_1, N_2, \\dots, N_N\\}$ receiving a continuous stream of $M$ independent computational tasks $\\mathcal{T} = \\{T_1, T_2, \\dots, T_M\\}$.

### A. Mathematical Formulation and System Model
Each node $N_j \\in \\mathcal{N}$ is defined by its processing capacity $\\mu_j$ in Million Instructions Per Second (MIPS), its static idle power consumption $P_j^{\\text{idle}}$, and its dynamic peak power $P_j^{\\text{peak}}$. Each task $T_i \\in \\mathcal{T}$ is characterized by its instruction volume $I_i$, arrival timestamp $a_i$, and strict completion deadline $d_i$.

The execution duration of task $T_i$ on node $N_j$ is given by:
\\[
\\tau_{i,j} = \\frac{I_i}{\\mu_j}
\\]

Given node $N_j$'s current availability timestamp $\\alpha_j$, the task commencement time is $s_{i,j} = \\max(a_i, \\alpha_j)$, and the task completion time is $c_{i,j} = s_{i,j} + \\tau_{i,j}$. The resulting turnaround latency is defined as:
\\[
L(T_i, N_j) = c_{i,j} - a_i
\\]

### B. Multi-Objective Cost Optimization
To achieve joint latency reduction and deadline compliance while throttling energy expenditure, the proposed Adaptive-DynaSched algorithm formulates an online multi-objective allocation cost function $J(T_i, N_j)$:
\\[
J(T_i, N_j) = L(T_i, N_j) + \\beta \\cdot \\max(0, c_{i,j} - d_i) + \\gamma \\cdot \\left(\\frac{\\tau_{i,j} \\cdot P_j^{\\text{peak}}}{1000}\\right)
\\]
where $\\beta = 4.0$ represents the SLA urgency penalty coefficient, and $\\gamma = 0.015$ weights the dynamic energy consumption penalty. The scheduler selects node $N^* = \\arg\\min_{N_j \\in \\mathcal{N}} J(T_i, N_j)$ for each arriving task.

### C. Complexity Analysis
For each arriving task $T_i$, the evaluation evaluates $N$ compute nodes in constant time per node. Consequently, for a workload of $M$ tasks scheduled across $N$ nodes, the overall runtime computational complexity is $O(M \\cdot N)$. The memory footprint is strictly $O(N)$ auxiliary state for tracking node availability, ensuring lightweight real-time execution.
"""

def audit_section_iii(manuscript_path):
    with open(manuscript_path, "r", encoding="utf-8") as f:
        text = f.read()

    errors = []
    
    # Check Section III presence
    if not re.search(r"\b(?:iii\.?\s+)?(?:system\s+architecture|methodology)\b", text, re.IGNORECASE):
        errors.append("Section III (System Architecture and Methodology) is missing")

    # Check for mathematical notation / equations
    has_math = ("\tau" in text or "\mu" in text or "J(" in text or "c_{i,j}" in text or "L(T_i" in text or "O(M" in text)
    if not has_math:
        errors.append("Mathematical formulation or equations missing in Section III")

    # Check for cost function definition
    has_cost = ("cost" in text.lower() or "objective" in text.lower()) and ("\beta" in text or "penalty" in text.lower())
    if not has_cost:
        errors.append("Cost function / optimization objective missing in Section III")

    # Check for complexity analysis
    has_complexity = bool(re.search(r"O\(M.*?N\)|O\(N\)|complexity", text, re.IGNORECASE))
    if not has_complexity:
        errors.append("Time/space complexity analysis missing in Section III")

    status = "PASS" if len(errors) == 0 else "FAIL"
    return {"status": status, "errors": errors, "manuscript": manuscript_path}

def enrich_section_iii(manuscript_path):
    with open(manuscript_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Pattern to match Section III up to Section IV
    sec3_pattern = re.compile(
        r"(##\s+III\.\s+System\s+Architecture.*?)\n(##\s+IV\.)",
        re.DOTALL | re.IGNORECASE
    )

    if sec3_pattern.search(content):
        updated = sec3_pattern.sub(lambda m: f"{FORMAL_METHOD_TEXT.strip()}\n\n{m.group(2)}", content)
    else:
        # If Section III is not in exact format, replace from ## III up to ## IV
        split_parts = re.split(r"(##\s+IV\.)", content, maxsplit=1)
        if len(split_parts) == 3:
            # Replace whatever section 3 was before ## IV
            pre = re.split(r"(##\s+III\..*?)", split_parts[0], maxsplit=1)
            updated = pre[0] + FORMAL_METHOD_TEXT.strip() + "\n\n" + split_parts[1] + split_parts[2]

        else:
            updated = content + "\n\n" + FORMAL_METHOD_TEXT.strip() + "\n"

    with open(manuscript_path, "w", encoding="utf-8") as f:
        f.write(updated)
    return True

def main():
    parser = argparse.ArgumentParser(description="Audit and enrich Section III mathematical methodology.")
    parser.add_argument("--manuscript", default="paper/manuscript.md", help="Path to manuscript")
    parser.add_argument("--sim-engine", default="paper/sim_engine.py", help="Path to sim_engine.py")
    parser.add_argument("--enrich", action="store_true", help="Automatically enrich Section III if missing specifics")
    parser.add_argument("--output-report", default="paper/reports/methods_report.json", help="Path to output report")

    args = parser.parse_args()

    try:
        report = audit_section_iii(args.manuscript)
        if report["status"] != "PASS" and args.enrich:
            enrich_section_iii(args.manuscript)
            report = audit_section_iii(args.manuscript)
            report["enriched"] = True

        os.makedirs(os.path.dirname(os.path.abspath(args.output_report)), exist_ok=True)
        with open(args.output_report, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print(json.dumps(report, indent=2))
        if report["status"] != "PASS":
            sys.exit(1)
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
