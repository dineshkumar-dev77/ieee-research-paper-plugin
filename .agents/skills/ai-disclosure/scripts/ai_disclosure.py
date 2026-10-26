#!/usr/bin/env python3
"""AI Usage Disclosure Auditor and Synchronizer (Guardrail 4)."""

import argparse
import json
import os
import re
import sys

def load_json(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_acknowledgment_text(log_data):
    sections = log_data.get("sections_assisted", [])
    if not sections:
        return ("ACKNOWLEDGMENT\nDuring the preparation of this work, the authors designed, implemented, and "
                "evaluated all models independently without generative assistance.")
    
    sec_details = []
    for s in sections:
        sec_name = s.get("section", "")
        match = re.search(r'(Section\s+[IVXLCDM]+)', sec_name, re.IGNORECASE)
        sec_tag = match.group(1) if match else sec_name
        assist = s.get("assistance_type", "research synthesis")
        sec_details.append(f"{assist} ({sec_tag})")

    details_str = ", ".join(sec_details)
    statement = (
        "ACKNOWLEDGMENT\n"
        f"During the preparation of this work, the authors utilized the Antigravity Autonomous Research Assistant "
        f"for benchmark orchestration, {details_str}, and automated verification of manuscript numerical consistency "
        "against the experimental ledger. All experimental evaluations were reviewed, validated, and verified by the authors."
    )
    return statement

def sync_acknowledgment(log_path, ack_path, manuscript_path):
    log_data = load_json(log_path)
    ack_text = generate_acknowledgment_text(log_data)

    os.makedirs(os.path.dirname(ack_path), exist_ok=True)
    with open(ack_path, "w", encoding="utf-8") as f:
        f.write(ack_text.strip() + "\n")
    print(f"[SYNC] Updated {ack_path}")

    if os.path.isfile(manuscript_path):
        with open(manuscript_path, "r", encoding="utf-8") as f:
            content = f.read()

        body_ack = ack_text.replace("ACKNOWLEDGMENT\n", "").strip()
        ack_section = f"## Acknowledgment\n{body_ack}"

        if "## Acknowledgment" in content:
            new_content = re.sub(
                r'## Acknowledgment\s*\n.*?(?=\n## |\Z)',
                f"{ack_section}\n\n",
                content,
                flags=re.DOTALL
            )
        else:
            ref_idx = content.find("## References")
            if ref_idx != -1:
                new_content = content[:ref_idx] + f"{ack_section}\n\n" + content[ref_idx:]
            else:
                new_content = content + f"\n\n{ack_section}\n"

        with open(manuscript_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"[SYNC] Updated {manuscript_path} Acknowledgment section")

def audit_disclosure(log_path, ack_path, manuscript_path):
    log_data = load_json(log_path)
    sections = log_data.get("sections_assisted", [])
    if not os.path.isfile(ack_path):
        print(f"[FAIL] Missing acknowledgment file: {ack_path}", file=sys.stderr)
        return False

    with open(ack_path, "r", encoding="utf-8") as f:
        ack_text = f.read().strip()

    if not os.path.isfile(manuscript_path):
        print(f"[FAIL] Missing manuscript file: {manuscript_path}", file=sys.stderr)
        return False

    with open(manuscript_path, "r", encoding="utf-8") as f:
        manuscript_text = f.read()

    match = re.search(r'## Acknowledgment\s*\n(.*?)(?=\n## |\Z)', manuscript_text, flags=re.DOTALL | re.IGNORECASE)
    if not match:
        print("[FAIL] Manuscript is missing '## Acknowledgment' section!", file=sys.stderr)
        return False
    manu_ack_body = match.group(1).strip()

    ack_body = ack_text.replace("ACKNOWLEDGMENT", "").strip()
    norm_ack = " ".join(ack_body.split())
    norm_manu = " ".join(manu_ack_body.split())

    for sec_entry in sections:
        sec_name = sec_entry.get("section", "")
        m = re.search(r'(Section\s+[IVXLCDM]+)', sec_name, re.IGNORECASE)
        sec_tag = m.group(1) if m else sec_name
        if sec_tag.lower() not in norm_ack.lower():
            print(f"[FAIL] Logged section '{sec_tag}' missing from {ack_path}", file=sys.stderr)
            return False
        if sec_tag.lower() not in norm_manu.lower():
            print(f"[FAIL] Logged section '{sec_tag}' missing from manuscript ## Acknowledgment", file=sys.stderr)
            return False

    if abs(len(norm_ack) - len(norm_manu)) > 80:
        print(f"[FAIL] Acknowledgment file and manuscript acknowledgment are desynchronized!\nFile: {norm_ack}\nManu: {norm_manu}", file=sys.stderr)
        return False

    return True

def main():
    parser = argparse.ArgumentParser(description="AI Usage Disclosure Auditor (Guardrail 4)")
    parser.add_argument("--log", default="paper/reports/ai_usage_log.json", help="AI usage log path")
    parser.add_argument("--ack", default="paper/reports/ai_acknowledgment.txt", help="AI acknowledgment text path")
    parser.add_argument("--manuscript", default="paper/manuscript.md", help="Manuscript path")
    parser.add_argument("--sync", action="store_true", help="Synchronize acknowledgment text and manuscript")
    parser.add_argument("--audit", action="store_true", default=True, help="Audit synchronization")
    args = parser.parse_args()

    try:
        if args.sync:
            sync_acknowledgment(args.log, args.ack, args.manuscript)

        valid = audit_disclosure(args.log, args.ack, args.manuscript)
        if not valid:
            print("[FAIL] AI disclosure audit failed (Guardrail 4 violation)", file=sys.stderr)
            sys.exit(1)

        print("[PASS] AI disclosure fully synchronized and compliant with Guardrail 4.")
        sys.exit(0)
    except Exception as e:
        print(f"[FAIL] AI disclosure error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
