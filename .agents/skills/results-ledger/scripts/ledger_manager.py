#!/usr/bin/env python3
"""Results Ledger Management CLI.
Maintains paper/results.csv as the single source of truth for all experimental numbers.
"""
import argparse
import csv
import json
import os
import sys

REQUIRED_COLUMNS = [
    "run_id",
    "metric",
    "value",
    "method",
    "workload",
    "seed",
    "config_hash",
    "code_hash",
    "env",
    "timestamp",
    "source_file"
]

def init_ledger(path="paper/results.csv"):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(REQUIRED_COLUMNS)
    return True

def validate_ledger(path="paper/results.csv"):
    if not os.path.exists(path):
        return False, f"File does not exist: {path}"
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if not header:
            return False, "File is empty"
        if header != REQUIRED_COLUMNS:
            return False, f"Header mismatch. Expected {REQUIRED_COLUMNS}, got {header}"
    return True, "Valid"

def append_rows(path, rows):
    init_ledger(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for r in rows:
            row_data = [r.get(col, "") for col in REQUIRED_COLUMNS]
            writer.writerow(row_data)

def query_ledger(path="paper/results.csv", method=None, metric=None, workload=None):
    if not os.path.exists(path):
        return []
    results = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if method and row.get("method") != method:
                continue
            if metric and row.get("metric") != metric:
                continue
            if workload and row.get("workload") != workload:
                continue
            results.append(row)
    return results

def get_all_numeric_values(path="paper/results.csv"):
    if not os.path.exists(path):
        return []
    values = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                v = float(row.get("value", ""))
                values.append(v)
            except (ValueError, TypeError):
                continue
    return values

def main():
    parser = argparse.ArgumentParser(description="Manage results ledger CSV.")
    parser.add_argument("--init", action="store_true", help="Initialize results.csv")
    parser.add_argument("--ledger", default="paper/results.csv", help="Path to results.csv")
    parser.add_argument("--validate", action="store_true", help="Validate ledger schema")
    parser.add_argument("--append-json", help="JSON string or file containing row or list of rows")
    parser.add_argument("--query", action="store_true", help="Query ledger rows")
    parser.add_argument("--method", help="Filter by method")
    parser.add_argument("--metric", help="Filter by metric")
    parser.add_argument("--workload", help="Filter by workload")

    args = parser.parse_args()

    try:
        if args.init:
            init_ledger(args.ledger)
            print(json.dumps({"status": "initialized", "ledger": args.ledger, "columns": REQUIRED_COLUMNS}))
            sys.exit(0)

        if args.validate:
            valid, msg = validate_ledger(args.ledger)
            if not valid:
                print(json.dumps({"error": msg}), file=sys.stderr)
                sys.exit(1)
            print(json.dumps({"status": "valid", "ledger": args.ledger}))
            sys.exit(0)

        if args.append_json:
            if os.path.exists(args.append_json):
                with open(args.append_json, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                data = json.loads(args.append_json)
            rows = data if isinstance(data, list) else [data]
            append_rows(args.ledger, rows)
            print(json.dumps({"status": "appended", "count": len(rows)}))
            sys.exit(0)

        if args.query:
            rows = query_ledger(args.ledger, args.method, args.metric, args.workload)
            print(json.dumps({"count": len(rows), "rows": rows}, indent=2))
            sys.exit(0)

        valid, msg = validate_ledger(args.ledger)
        if not valid:
            print(json.dumps({"error": msg}), file=sys.stderr)
            sys.exit(1)
        print(json.dumps({"status": "ok", "ledger": args.ledger}))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
