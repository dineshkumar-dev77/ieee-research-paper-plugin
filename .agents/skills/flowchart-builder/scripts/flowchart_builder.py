#!/usr/bin/env python3
"""Flowchart Builder CLI.
Generates Mermaid architecture specification and renders IEEE publication-grade
system architecture diagram (600 DPI line art, 3.5 in width, vector PDF).
"""
import argparse
import json
import os
import sys

MERMAID_TEMPLATE = """graph TD
    A[Task Arrival Queue<br/>Poisson Process &lambda;] --> B[Task Profiler & Slack Estimator]
    B --> C[Adaptive-DynaSched Core Engine]
    C -->|Evaluate Cost J| D{Multi-Objective Utility}
    D -->|Latency + SLA + Energy| E[Optimal Node Selector]
    E --> F1[Node N1: General Compute<br/>1500 MIPS]
    E --> F2[Node N2: Compute-Optimized<br/>2500 MIPS]
    E --> F3[Node N3: High-Performance<br/>4000 MIPS]
    F1 --> G[SLA & Energy Feedback Monitor]
    F2 --> G
    F3 --> G
    G -.->|Dynamic Availability| C
"""

def render_architecture_diagram(output_dir="paper/figures", fig_number=2, width_in=3.5, dpi=600):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    os.makedirs(output_dir, exist_ok=True)

    # 1. Save Mermaid file
    mmd_path = os.path.join(output_dir, f"fig_{fig_number}_arch.mmd")
    with open(mmd_path, "w", encoding="utf-8") as f:
        f.write(MERMAID_TEMPLATE.strip() + "\n")

    # 2. Render crisp 600 DPI line art diagram using Matplotlib
    fig_height = 4.2
    fig, ax = plt.subplots(figsize=(width_in, fig_height), dpi=dpi)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    def draw_box(x, y, w, h, text, bg="#f0f4f8", border="#1f77b4", title_font=8, sub_font=6.5):
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.8,rounding_size=2",
            facecolor=bg,
            edgecolor=border,
            linewidth=1.2
        )
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=title_font, wrap=True, fontweight="bold", color="#111827")

    def draw_arrow(x1, y1, x2, y2, label=""):
        ax.annotate(
            label,
            xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(facecolor="#374151", edgecolor="#374151", arrowstyle="->", lw=1.2),
            ha="center", va="center", fontsize=6, color="#4b5563"
        )

    # Diagram components
    draw_box(10, 85, 80, 10, "Task Arrival Queue\n(Poisson Stream & Inter-Arrival Delay)", bg="#e0f2fe", border="#0284c7")
    draw_arrow(50, 85, 50, 75)

    draw_box(15, 65, 70, 10, "Task Profiler & Slack Estimator\n(Instruction Volume I_i, Deadline d_i)", bg="#f1f5f9", border="#475569")
    draw_arrow(50, 65, 50, 55)

    draw_box(10, 43, 80, 12, "Adaptive-DynaSched Optimization Engine\nmin J(T_i, N_j) = L(T_i, N_j) + \u03b2\u00b7U(T_i, N_j) + \u03b3\u00b7E(T_i, N_j)", bg="#fef3c7", border="#d97706", title_font=7.5)
    
    draw_arrow(30, 43, 20, 30)
    draw_arrow(50, 43, 50, 30)
    draw_arrow(70, 43, 80, 30)

    # Nodes
    draw_box(5, 18, 26, 12, "Node Cluster A\nGeneral Compute\n(1500 MIPS)", bg="#f3f4f6", border="#6b7280", title_font=6.5)
    draw_box(37, 18, 26, 12, "Node Cluster B\nCompute-Opt.\n(2500 MIPS)", bg="#f3f4f6", border="#6b7280", title_font=6.5)
    draw_box(69, 18, 26, 12, "Node Cluster C\nHigh-Perf.\n(4000 MIPS)", bg="#f3f4f6", border="#6b7280", title_font=6.5)

    draw_arrow(18, 18, 50, 8)
    draw_arrow(50, 18, 50, 8)
    draw_arrow(82, 18, 50, 8)

    draw_box(10, 2, 80, 6, "SLA & Energy Feedback Ledger (results.csv)", bg="#dcfce7", border="#16a34a", title_font=6.5)

    plt.tight_layout()

    png_path = os.path.join(output_dir, f"fig_{fig_number}.png")
    pdf_path = os.path.join(output_dir, f"fig_{fig_number}.pdf")
    meta_path = os.path.join(output_dir, f"fig_{fig_number}.json")

    fig.savefig(png_path, dpi=dpi, bbox_inches="tight")
    fig.savefig(pdf_path, bbox_inches="tight")
    plt.close(fig)

    caption = f"Fig. {fig_number}. Proposed Adaptive-DynaSched system architecture and scheduling pipeline."
    meta = {
        "figure_number": fig_number,
        "caption": caption,
        "type": "architecture_diagram",
        "width_in": width_in,
        "dpi": dpi,
        "png_path": png_path,
        "pdf_path": pdf_path,
        "mmd_path": mmd_path
    }

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    return {
        "status": "success",
        "fig_number": fig_number,
        "caption": caption,
        "png_file": png_path,
        "pdf_file": pdf_path,
        "mmd_file": mmd_path,
        "meta_file": meta_path
    }

def main():
    parser = argparse.ArgumentParser(description="Build IEEE architecture diagram.")
    parser.add_argument("--output-dir", default="paper/figures", help="Figures output directory")
    parser.add_argument("--fig-number", type=int, default=2, help="Figure number (default: 2)")
    parser.add_argument("--dpi", type=int, default=600, help="Line art DPI (>=600)")
    parser.add_argument("--width", type=float, default=3.5, help="Width in inches")

    args = parser.parse_args()

    try:
        res = render_architecture_diagram(
            output_dir=args.output_dir,
            fig_number=args.fig_number,
            width_in=args.width,
            dpi=args.dpi
        )
        print(json.dumps(res, indent=2))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
