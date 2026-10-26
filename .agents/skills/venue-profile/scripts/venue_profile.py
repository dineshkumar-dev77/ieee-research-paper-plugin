#!/usr/bin/env python3
"""Venue Profile Management CLI.
Loads, validates, and queries venue-specific parameters from paper/venue.json.
"""
import argparse
import json
import os
import sys

DEFAULT_IEEE_CONFERENCE = {
    "venue_name": "IEEE Conference",
    "venue_id": "ieee_conference",
    "layout": {
        "columns": 2,
        "single_column_width_in": 3.5,
        "double_column_width_in": 7.16,
        "column_gutter_in": 0.16,
        "margin_top_in": 0.75,
        "margin_bottom_in": 1.0,
        "margin_side_in": 0.625
    },
    "typography": {
        "font_family": "Times New Roman",
        "title_size_pt": 24,
        "body_size_pt": 10,
        "abstract_size_pt": 9,
        "caption_size_pt": 8
    },
    "captions": {
        "table_caption_position": "above",
        "table_numbering": "Roman",
        "table_prefix": "TABLE",
        "figure_caption_position": "below",
        "figure_numbering": "Arabic",
        "figure_prefix": "Fig."
    },
    "graphics": {
        "min_dpi": 300,
        "line_art_dpi": 600,
        "preferred_format": "png",
        "vector_format": "pdf"
    }
}

DEFAULT_PROFILES = {
    "ieee_conference": DEFAULT_IEEE_CONFERENCE,
    "ieee_transactions": {
        **DEFAULT_IEEE_CONFERENCE,
        "venue_name": "IEEE Transactions",
        "venue_id": "ieee_transactions",
        "typography": {
            **DEFAULT_IEEE_CONFERENCE["typography"],
            "body_size_pt": 9.5
        }
    }
}

def load_venue(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Venue profile file not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_venue(file_path, data):
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def validate_venue_schema(data):
    required_sections = ["venue_id", "layout", "typography", "captions", "graphics"]
    for s in required_sections:
        if s not in data:
            return False, f"Missing required section: {s}"
    if data["layout"].get("single_column_width_in") is None:
        return False, "Missing layout.single_column_width_in"
    if data["captions"].get("table_numbering") != "Roman":
        return False, "IEEE requires Roman numerals for table numbering"
    if data["captions"].get("figure_numbering") != "Arabic":
        return False, "IEEE requires Arabic numerals for figure numbering"
    return True, "Valid"

def get_nested_param(data, key_path):
    parts = key_path.split(".")
    curr = data
    for p in parts:
        if not isinstance(curr, dict) or p not in curr:
            return None
        curr = curr[p]
    return curr

def main():
    parser = argparse.ArgumentParser(description="Manage venue profile parameters.")
    parser.add_argument("--init", action="store_true", help="Initialize venue profile")
    parser.add_argument("--venue", default="ieee_conference", choices=list(DEFAULT_PROFILES.keys()), help="Default profile")
    parser.add_argument("--venue-file", default="paper/venue.json", help="Path to venue.json")
    parser.add_argument("--get-param", help="Dot-notated parameter path (e.g. layout.single_column_width_in)")
    parser.add_argument("--validate", action="store_true", help="Validate existing venue profile")
    parser.add_argument("--output", help="Optional output JSON path")

    args = parser.parse_args()

    try:
        if args.init:
            profile = DEFAULT_PROFILES.get(args.venue, DEFAULT_IEEE_CONFERENCE)
            target = args.output if args.output else args.venue_file
            save_venue(target, profile)
            print(json.dumps({"status": "initialized", "venue_file": target, "profile": profile["venue_id"]}))
            sys.exit(0)

        data = load_venue(args.venue_file)

        if args.validate:
            valid, msg = validate_venue_schema(data)
            if not valid:
                print(json.dumps({"error": msg}), file=sys.stderr)
                sys.exit(1)
            print(json.dumps({"status": "valid", "venue_id": data.get("venue_id")}))
            sys.exit(0)

        if args.get_param:
            val = get_nested_param(data, args.get_param)
            if val is None:
                print(json.dumps({"error": f"Parameter not found: {args.get_param}"}), file=sys.stderr)
                sys.exit(1)
            print(json.dumps({"param": args.get_param, "value": val}))
            sys.exit(0)

        print(json.dumps(data, indent=2))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
