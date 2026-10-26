#!/usr/bin/env python3
"""Simulation Builder CLI.
Generates task-configurable benchmark evaluation code with unit tests.
"""
import argparse
import json
import os
import shutil
import sys

def main():
    parser = argparse.ArgumentParser(description="Build task-configurable benchmark simulation engine.")
    parser.add_argument("--generate", action="store_true", help="Generate simulation engine and test files")
    parser.add_argument("--config", default="paper/paper.json", help="Path to paper.json")
    parser.add_argument("--output", default="paper/sim_engine.py", help="Output path for simulation engine")
    parser.add_argument("--test-output", default="tests/test_sim_engine.py", help="Output path for tests")

    args = parser.parse_args()

    try:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        os.makedirs(os.path.dirname(os.path.abspath(args.test_output)), exist_ok=True)

        if not os.path.exists(args.output):
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(open("paper/sim_engine.py").read())
            os.chmod(args.output, 0o755)

        if not os.path.exists(args.test_output):
            with open(args.test_output, "w", encoding="utf-8") as f:
                f.write(open("tests/test_sim_engine.py").read())
            os.chmod(args.test_output, 0o755)

        print(json.dumps({
            "status": "generated",
            "sim_engine": args.output,
            "unit_test": args.test_output
        }, indent=2))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
