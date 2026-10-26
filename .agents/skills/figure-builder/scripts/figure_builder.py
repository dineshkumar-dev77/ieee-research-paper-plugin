#!/usr/bin/env python3
"""IEEE Figure Builder CLI.
Generates publication-quality IEEE figures strictly from paper/results.csv.
IEEE formatting: Captions below as 'Fig. N.' with Arabic numerals, 3.5 in / 7.16 in width, >=300 dpi.
"""
import argparse
import csv
import json
import math
import os
import sys

def load_venue_params(venue_path="paper/venue.json"):
    if os.path.exists(venue_path):
        with open(venue_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "layout": {"single_column_width_in": 3.5, "double_column_width_in": 7.16},
        "graphics": {"min_dpi": 300, "line_art_dpi": 600}
    }

def load_metric_data(ledger_path="paper/results.csv", target_metric="makespan_sec"):
    if not os.path.exists(ledger_path):
        raise FileNotFoundError(f"Ledger file not found: {ledger_path}")

    method_values = {}
    with open(ledger_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if str(r.get("run_id", "")).startswith("summary_") or r.get("seed") == "summary":
                continue
            if r.get("metric") == target_metric:
                m = r.get("method")
                try:
                    val = float(r.get("value", ""))
                    method_values.setdefault(m, []).append(val)
                except ValueError:
                    continue
    return method_values

def generate_ieee_figure(
    ledger_path="paper/results.csv",
    venue_path="paper/venue.json",
    output_dir="paper/figures",
    fig_number=1,
    metric="makespan_sec",
    metric_label="Makespan (seconds)",
    two_column=False,
    caption_text="Makespan comparison across 10 evaluation seeds."
):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    venue = load_venue_params(venue_path)
    dpi = venue.get("graphics", {}).get("min_dpi", 300)
    col_width = venue.get("layout", {}).get("double_column_width_in" if two_column else "single_column_width_in", 3.5)

    data = load_metric_data(ledger_path, target_metric=metric)
    if not data:
        raise ValueError(f"No raw data found in ledger for metric: {metric}")

    os.makedirs(output_dir, exist_ok=True)

    # Sort methods so proposed method is highlighted
    methods = sorted(data.keys(), key=lambda x: 0 if "adaptive" in x.lower() else 1)
    means = []
    stds = []
    for m in methods:
        vals = data[m]
        mean_v = sum(vals) / len(vals)
        var_v = sum((x - mean_v) ** 2 for x in vals) / (len(vals) - 1) if len(vals) > 1 else 0.0
        means.append(mean_v)
        stds.append(math.sqrt(var_v))

    fig_width = col_width
    fig_height = 2.6 if not two_column else 3.2

    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=dpi)

    colors = ["#1f77b4" if "adaptive" in m.lower() else "#7f7f7f" for m in methods]
    x_positions = range(len(methods))

    bars = ax.bar(
        x_positions,
        means,
        yerr=stds,
        capsize=4,
        color=colors,
        edgecolor="black",
        linewidth=0.8,
        width=0.55
    )

    ax.set_xticks(x_positions)
    ax.set_xticklabels([m.replace("-", "\n") for m in methods], fontsize=8)
    ax.set_ylabel(metric_label, fontsize=8)
    ax.tick_params(axis="both", which="major", labelsize=7.5)
    ax.grid(axis="y", linestyle="--", alpha=0.5, linewidth=0.6)
    ax.set_axisbelow(True)

    # Annotate value on top of bars
    for bar, m_val in zip(bars, means):
        yval = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            yval + max(stds) * 0.35,
            f"{m_val:.1f}",
            ha="center",
            va="bottom",
            fontsize=7.5,
            fontweight="bold"
        )

    plt.tight_layout()

    png_path = os.path.join(output_dir, f"fig_{fig_number}.png")
    pdf_path = os.path.join(output_dir, f"fig_{fig_number}.pdf")
    meta_path = os.path.join(output_dir, f"fig_{fig_number}.json")

    fig.savefig(png_path, dpi=dpi, bbox_inches="tight")
    fig.savefig(pdf_path, bbox_inches="tight")
    plt.close(fig)

    formatted_caption = f"Fig. {fig_number}. {caption_text}"

    meta = {
        "figure_number": fig_number,
        "caption": formatted_caption,
        "width_in": fig_width,
        "dpi": dpi,
        "png_path": png_path,
        "pdf_path": pdf_path,
        "metric": metric,
        "methods": methods,
        "means": means,
        "stds": stds
    }

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    return {
        "status": "success",
        "fig_number": fig_number,
        "caption": formatted_caption,
        "png_file": png_path,
        "pdf_file": pdf_path,
        "json_meta": meta_path
    }

def main():
    parser = argparse.ArgumentParser(description="Generate IEEE style figures from results.csv.")
    parser.add_argument("--ledger", default="paper/results.csv", help="Path to results.csv")
    parser.add_argument("--venue", default="paper/venue.json", help="Path to venue.json")
    parser.add_argument("--output-dir", default="paper/figures", help="Directory to save figures")
    parser.add_argument("--fig-number", type=int, default=1, help="Figure number (1, 2, ...)")
    parser.add_argument("--metric", default="makespan_sec", help="Metric to plot")
    parser.add_argument("--ylabel", default="Makespan (seconds)", help="Y-axis label")
    parser.add_argument("--caption", default="Makespan comparison across 10 evaluation seeds.", help="Caption text")
    parser.add_argument("--two-column", action="store_true", help="Two column width (7.16 in)")

    args = parser.parse_args()

    try:
        res = generate_ieee_figure(
            ledger_path=args.ledger,
            venue_path=args.venue,
            output_dir=args.output_dir,
            fig_number=args.fig_number,
            metric=args.metric,
            metric_label=args.ylabel,
            two_column=args.two_column,
            caption_text=args.caption
        )
        print(json.dumps(res, indent=2))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
