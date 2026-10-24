#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
timing_analysis.py - task completion time analysis

Parse each student's completion time for every task from task_completion_record_group_A.md / group_B.md,
subtract the task start time to get the completion duration (minutes), and run an independent-samples
t-test between the RR and Colab groups.

Usage: python timing_analysis.py
"""

import re
from pathlib import Path
from scipy import stats
import statistics

DATA_DIR = Path(__file__).parent
TASKS = ["T1", "T2", "T3", "T4", "T5"]


def parse_time(s):
    """'15:03'  / '**15:03**'  / '15:00?' -> integer minutes; None otherwise."""
    s = s.strip().strip('*').strip()
    if not s or s == '✗' or s == 'Makeup':
        return None
    # Strip common suffixes such as "?" and "(Makeup)" annotations
    s = s.split('?')[0].split('(')[0].strip()
    m = re.match(r'^(\d{1,2}):(\d{2})$', s)
    if not m:
        return None
    return int(m.group(1)) * 60 + int(m.group(2))


def parse_md_table(filepath):
    """Read the record-sheet md and return (start_times, student_times)
    start_times: dict {task: minute_int}
    student_times: list of dict per student {T1:..., T2:...}
    """
    text = filepath.read_text(encoding='utf-8')
    lines = text.splitlines()

    # Detect the T1 column index dynamically (column offsets may differ between the two sheets)
    start_times = {}
    student_rows = []
    in_table = False
    t1_col_idx = None
    sid_col_idx = None

    for line in lines:
        if line.startswith('|') and 'T1' in line and 'T2' in line:
            in_table = True
            cells = [c.strip() for c in line.strip('|').split('|')]
            for i, c in enumerate(cells):
                if c.startswith('T1'):
                    t1_col_idx = i
                if 'Student ID' in c:
                    sid_col_idx = i
            continue
        if line.startswith('|---'):
            continue
        if in_table and line.startswith('|'):
            cells = [c.strip() for c in line.strip('|').split('|')]
            if not cells or t1_col_idx is None:
                continue
            first = cells[0].strip('* ').strip()
            if 'Task start time' in first:
                for i, task in enumerate(TASKS):
                    idx = t1_col_idx + i
                    t = parse_time(cells[idx]) if idx < len(cells) else None
                    if t is not None:
                        start_times[task] = t
            else:
                if len(cells) <= t1_col_idx:
                    continue
                sid = cells[sid_col_idx].strip() if (sid_col_idx is not None and sid_col_idx < len(cells)) else ''
                if not sid:
                    continue
                row = {'sid': sid}
                for i, task in enumerate(TASKS):
                    idx = t1_col_idx + i
                    t = parse_time(cells[idx]) if idx < len(cells) else None
                    row[task] = t
                student_rows.append(row)
        elif in_table and not line.startswith('|'):
            break

    return start_times, student_rows


def compute_durations(start_times, students):
    """Completion duration (minutes) for each student and task; skipped when data are missing."""
    durations = {task: [] for task in TASKS}
    for s in students:
        for task in TASKS:
            t = s[task]
            if t is None or task not in start_times:
                continue
            dur = t - start_times[task]
            # Only reject non-positive durations (time earlier than the start time is an obvious entry error)
            if dur > 0:
                durations[task].append(dur)
    return durations


def main():
    a_file = DATA_DIR / "task_completion_record_group_A.md"
    b_file = DATA_DIR / "task_completion_record_group_B.md"

    a_start, a_students = parse_md_table(a_file)
    b_start, b_students = parse_md_table(b_file)

    print(f"Group A task start times (min): {a_start}")
    print(f"Group A students: {len(a_students)}")
    print(f"Group B task start times (min): {b_start}")
    print(f"Group B students: {len(b_students)}\n")

    a_dur = compute_durations(a_start, a_students)
    b_dur = compute_durations(b_start, b_students)

    print("=" * 80)
    print(f"{'Task':<8}{'A n':<8}{'A M(SD)':<18}{'B n':<8}{'B M(SD)':<18}{'t':<10}{'p':<10}{'sig'}")
    print("=" * 80)
    for task in TASKS:
        a_vals = a_dur[task]
        b_vals = b_dur[task]
        a_n, b_n = len(a_vals), len(b_vals)
        if a_n < 2 or b_n < 2:
            print(f"{task:<8}{a_n:<8}{'Insufficient n':<18}{b_n:<8}{'Insufficient n':<18}{'-':<10}{'-':<10}n.s.")
            continue
        a_m, a_sd = statistics.mean(a_vals), statistics.stdev(a_vals)
        b_m, b_sd = statistics.mean(b_vals), statistics.stdev(b_vals)
        t, p = stats.ttest_ind(a_vals, b_vals, equal_var=False)
        sig = '***' if p < .001 else '**' if p < .01 else '*' if p < .05 else 'n.s.'
        a_str = f"{a_m:.1f}({a_sd:.1f})"
        b_str = f"{b_m:.1f}({b_sd:.1f})"
        print(f"{task:<8}{a_n:<8}{a_str:<18}{b_n:<8}{b_str:<18}{t:<10.3f}{p:<10.3f}{sig}")

    # Also print a markdown table
    print("\n\n## Markdown table (ready to paste into the paper)\n")
    print("| Task | RR n | RR M (SD) | Colab n | Colab M (SD) | t | p | Significance |")
    print("|------|------|-----------|---------|--------------|---|---|--------|")
    for task in TASKS:
        a_vals = a_dur[task]
        b_vals = b_dur[task]
        a_n, b_n = len(a_vals), len(b_vals)
        if a_n < 2 or b_n < 2:
            print(f"| {task} | {a_n} | Insufficient n | {b_n} | Insufficient n | - | - | - |")
            continue
        a_m, a_sd = statistics.mean(a_vals), statistics.stdev(a_vals)
        b_m, b_sd = statistics.mean(b_vals), statistics.stdev(b_vals)
        t, p = stats.ttest_ind(a_vals, b_vals, equal_var=False)
        sig = '\\*\\*\\*' if p < .001 else '\\*\\*' if p < .01 else '\\*' if p < .05 else 'n.s.'
        print(f"| {task} | {a_n} | {a_m:.1f} ({a_sd:.1f}) | {b_n} | {b_m:.1f} ({b_sd:.1f}) | {t:+.3f} | {p:.3f} | {sig} |")


if __name__ == '__main__':
    main()
