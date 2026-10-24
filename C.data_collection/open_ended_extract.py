#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
open_ended_extract.py — extract open-ended responses from the post-test CSVs and print them as markdown

To ease manual coding: one line per response (student ID + 6-1 + 6-2 + 6-3)
"""

import csv
import os

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_ID = "TEST01"

FILES = {
    "RR (A)": "RL_Lab_PostTest_GroupA.csv",
    "Colab (B)": "RL_Lab_PostTest_GroupB.csv",
}


def load_open(filename):
    """Return a list of (sid, q1, q2, q3)"""
    rows = []
    with open(os.path.join(DATA_DIR, filename), encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        # Locate the open-ended columns
        keys = reader.fieldnames
        q1_key = next((k for k in keys if k.startswith("6-1")), None)
        q2_key = next((k for k in keys if k.startswith("6-2")), None)
        q3_key = next((k for k in keys if k.startswith("6-3")), None)
        for row in reader:
            sid = row["Student ID"].strip().upper()
            if sid == TEST_ID:
                continue
            q1 = (row.get(q1_key) or "").strip()
            q2 = (row.get(q2_key) or "").strip()
            q3 = (row.get(q3_key) or "").strip()
            rows.append((sid, q1, q2, q3))
    return rows


def main():
    for group, fn in FILES.items():
        rows = load_open(fn)
        print(f"\n## {group} (n={len(rows)})\n")
        print(f"### 6-1 What was the most helpful part of today's class?\n")
        for sid, q1, _, _ in rows:
            print(f"- **{sid}**: {q1 if q1 else '(empty)'}")
        print(f"\n### 6-2 What was the most confusing or difficult part?\n")
        for sid, _, q2, _ in rows:
            print(f"- **{sid}**: {q2 if q2 else '(empty)'}")
        print(f"\n### 6-3 Any other comments or suggestions?\n")
        for sid, _, _, q3 in rows:
            print(f"- **{sid}**: {q3 if q3 else '(empty)'}")


if __name__ == "__main__":
    main()
