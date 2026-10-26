#!/usr/bin/env python3
"""IEEE Table Builder CLI.
Generates publication-quality IEEE tables strictly from paper/results.csv.
IEEE formatting: Captions above with Roman numerals ("TABLE I").
"""
import argparse
import csv
import json
import math
import os
import sys

ROMAN_NUMERALS = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X"}

def load_venue_layout(venue_path="paper/venue.json"):
    if os.path.exists(venue_path):
        with open(venue_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def extract_summary_stats_from_ledger(ledger_path="paper/results.csv"):
    if not os.path.exists(ledger_path):
        raise FileNotFoundError(f"Ledger file not found: {ledger_path}")

    # Collect raw values per (method, metric)
    data = {}
    with open(ledger_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if str(r.get("run_id", "")).startswith("summary_") or r.get("seed") == "summary":
                continue
            method = r.get("method")
            metric = r.get("metric")
            try:
                val = float(r.get("value", ""))
            except (ValueError, TypeError):
                continue
            data.setdefault(method, {}).setdefault(metric, []).append(val)

    stats = {}
    for m, metrics in data.items():
        stats[m] = {}
        for met, vals in metrics.items():
            mean_v = sum(vals) / len(vals)
            var_v = sum((x - mean_v) ** 2 for x in vals) / (len(vals) - 1) if len(vals) > 1 else 0.0
            std_v = math.sqrt(var_v)
            stats[m][met] = {
                "mean": round(mean_v, 2),
                "std": round(std_v, 2),
                "n": len(vals)
            }
    return stats

def generate_ieee_table(
    ledger_path="paper/results.csv",
    venue_path="paper/venue.json",
    output_dir="paper/tables",
    table_number=1,
    table_title="PERFORMANCE COMPARISON UNDER HETEROGENEOUS CLOUD WORKLOADS"
):
    venue = load_venue_layout(venue_path)
    stats = extract_summary_stats_from_ledger(ledger_path)

    os.makedirs(output_dir, exist_ok=True)
    roman_num = ROMAN_NUMERALS.get(table_number, str(table_number))

    # Order methods: Proposed first, then baselines
    ordered_methods = sorted(stats.keys(), key=lambda x: 0 if "adaptive" in x.lower() else 1)

    # Build Markdown Table
    md_lines = []
    md_lines.append(f"**TABLE {roman_num}**")
    md_lines.append(f"*{table_title}*")
    md_lines.append("")
    md_lines.append("| Method | Makespan (s) | Energy (kWh) | Latency (ms) | SLA Violations (%) |")
    md_lines.append("| :--- | :---: | :---: | :---: | :---: |")

    table_data = []

    for m in ordered_methods:
        m_stats = stats[m]
        ms = m_stats.get("makespan_sec", {"mean": 0, "std": 0})
        en = m_stats.get("energy_kwh", {"mean": 0, "std": 0})
        lat = m_stats.get("latency_ms", {"mean": 0, "std": 0})
        sla = m_stats.get("sla_violation_pct", {"mean": 0, "std": 0})

        row_str = f"| **{m}** | {ms['mean']:.2f} ± {ms['std']:.2f} | {en['mean']:.3f} ± {en['std']:.3f} | {lat['mean']:.1f} ± {lat['std']:.1f} | {sla['mean']:.2f}% ± {sla['std']:.2f}% |"
        md_lines.append(row_str)

        table_data.append({
            "method": m,
            "makespan_sec": f"{ms['mean']:.2f} ± {ms['std']:.2f}",
            "energy_kwh": f"{en['mean']:.3f} ± {en['std']:.3f}",
            "latency_ms": f"{lat['mean']:.1f} ± {lat['std']:.1f}",
            "sla_violation_pct": f"{sla['mean']:.2f}% ± {sla['std']:.2f}%"
        })

    md_content = "\n".join(md_lines) + "\n"
    md_file = os.path.join(output_dir, f"table_{table_number}.md")
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(md_content)

    # Build LaTeX Table
    tex_lines = [
        "\\begin{table}[t]",
        f"\\caption{{\\textsc{{{table_title}}}}}",
        f"\\label{{tab:results_{table_number}}}",
        "\\centering",
        "\\begin{tabular}{lcccc}",
        "\\hline",
        "\\textbf{Method} & \\textbf{Makespan (s)} & \\textbf{Energy (kWh)} & \\textbf{Latency (ms)} & \\textbf{SLA Viol. (\\%)} \\\\",
        "\\hline"
    ]
    for row in table_data:
        tex_lines.append(f"{row['method']} & {row['makespan_sec']} & {row['energy_kwh']} & {row['latency_ms']} & {row['sla_violation_pct']} \\\\")
    tex_lines.extend([
        "\\hline",
        "\\end{tabular}",
        "\\end{table}"
    ])
    tex_file = os.path.join(output_dir, f"table_{table_number}.tex")
    with open(tex_file, "w", encoding="utf-8") as f:
        f.write("\n".join(tex_lines) + "\n")

    # Save JSON data representation
    json_file = os.path.join(output_dir, f"table_{table_number}.json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump({
            "table_number": table_number,
            "roman_numeral": roman_num,
            "caption": f"TABLE {roman_num} {table_title}",
            "rows": table_data
        }, f, indent=2)

    return {
        "status": "success",
        "table_number": table_number,
        "roman_numeral": roman_num,
        "md_file": md_file,
        "tex_file": tex_file,
        "json_file": json_file
    }

def main():
    parser = argparse.ArgumentParser(description="Generate IEEE style tables from ledger data.")
    parser.add_argument("--ledger", default="paper/results.csv", help="Path to results.csv")
    parser.add_argument("--venue", default="paper/venue.json", help="Path to venue.json")
    parser.add_argument("--output-dir", default="paper/tables", help="Directory to save tables")
    parser.add_argument("--table-number", type=int, default=1, help="Table number (1, 2, ...)")
    parser.add_argument("--title", default="PERFORMANCE COMPARISON UNDER HETEROGENEOUS CLOUD WORKLOADS", help="Table title")

    args = parser.parse_args()

    try:
        res = generate_ieee_table(
            ledger_path=args.ledger,
            venue_path=args.venue,
            output_dir=args.output_dir,
            table_number=args.table_number,
            table_title=args.title
        )
        print(json.dumps(res, indent=2))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
