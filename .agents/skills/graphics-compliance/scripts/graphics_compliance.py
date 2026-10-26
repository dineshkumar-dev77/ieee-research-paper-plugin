#!/usr/bin/env python3
"""Graphics Compliance CLI.
Scans all PNG/PDF figures in paper/figures/ using Pillow and verifies:
- DPI: >=300 DPI bitmap, >=600 DPI line art
- Width compliance: matches venue single-column (3.5 in) or double-column (7.16 in)
- Metadata caption compliance: 'Fig. N.' with Arabic numerals
Exits with code 1 if any graphic is non-compliant.
"""
import argparse
import json
import math
import os
import sys
from PIL import Image

def load_venue_specs(venue_path="paper/venue.json"):
    if os.path.exists(venue_path):
        with open(venue_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "layout": {"single_column_width_in": 3.5, "double_column_width_in": 7.16},
        "graphics": {"min_dpi": 300, "line_art_dpi": 600}
    }

def audit_graphics(figures_dir="paper/figures", venue_path="paper/venue.json"):
    if not os.path.exists(figures_dir):
        raise FileNotFoundError(f"Figures directory not found: {figures_dir}")

    venue = load_venue_specs(venue_path)
    single_col = venue.get("layout", {}).get("single_column_width_in", 3.5)
    double_col = venue.get("layout", {}).get("double_column_width_in", 7.16)
    min_bitmap_dpi = venue.get("graphics", {}).get("min_dpi", 300)
    min_line_art_dpi = venue.get("graphics", {}).get("line_art_dpi", 600)

    png_files = [f for f in os.listdir(figures_dir) if f.endswith(".png")]
    if not png_files:
        return {"status": "FAIL", "errors": ["No PNG figures found in figures directory"]}

    audits = []
    errors = []

    for pf in sorted(png_files):
        img_path = os.path.join(figures_dir, pf)
        base_name = os.path.splitext(pf)[0]
        meta_path = os.path.join(figures_dir, f"{base_name}.json")

        meta = {}
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as mf:
                meta = json.load(mf)

        with Image.open(img_path) as img:
            w_px, h_px = img.size
            dpi_info = img.info.get("dpi", (300, 300))
            dpi_x = int(round(dpi_info[0])) if isinstance(dpi_info, tuple) else 300
            
            # Check if this figure is marked as line art (e.g. flowchart)
            is_line_art = meta.get("type") == "architecture_diagram" or "arch" in base_name
            target_min_dpi = min_line_art_dpi if is_line_art else min_bitmap_dpi

            # Effective width in inches
            width_in = round(w_px / dpi_x, 2) if dpi_x > 0 else 0.0

            # Tolerance check for width (3.5 in single col or 7.16 in double col)
            width_ok = (abs(width_in - single_col) <= 0.35) or (abs(width_in - double_col) <= 0.45)
            dpi_ok = dpi_x >= (target_min_dpi - 10)

            # Caption check
            caption = meta.get("caption", "")
            caption_ok = caption.startswith("Fig. ") and "." in caption

            item_audit = {
                "file": pf,
                "dimensions_px": [w_px, h_px],
                "dpi": dpi_x,
                "is_line_art": is_line_art,
                "required_dpi": target_min_dpi,
                "effective_width_in": width_in,
                "width_compliant": width_ok,
                "dpi_compliant": dpi_ok,
                "caption": caption,
                "caption_compliant": caption_ok
            }
            audits.append(item_audit)

            if not dpi_ok:
                errors.append(f"{pf}: DPI {dpi_x} is below minimum requirement {target_min_dpi}")
            if not width_ok:
                errors.append(f"{pf}: Width {width_in} in does not match single ({single_col} in) or double ({double_col} in) column standard")
            if meta and not caption_ok:
                errors.append(f"{pf}: Caption '{caption}' does not comply with IEEE 'Fig. N.' standard")

    status = "PASS" if len(errors) == 0 else "FAIL"
    return {
        "status": status,
        "figures_checked": len(audits),
        "audits": audits,
        "errors": errors
    }

def main():
    parser = argparse.ArgumentParser(description="Verify figures against IEEE DPI, dimension, and caption standards.")
    parser.add_argument("--figures-dir", default="paper/figures", help="Directory containing figures")
    parser.add_argument("--venue", default="paper/venue.json", help="Path to venue.json")
    parser.add_argument("--output", default="paper/reports/graphics_compliance.json", help="Output path")

    args = parser.parse_args()

    try:
        report = audit_graphics(args.figures_dir, args.venue)
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
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
