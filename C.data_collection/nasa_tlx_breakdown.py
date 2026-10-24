#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nasa_tlx_breakdown.py — NASA-TLX six-subscale t-test

Read the six NASA-TLX items (Section 4: 4-1 to 4-6) from the post-test CSVs and run independent-samples t-tests, RR vs Colab.

The six NASA-TLX subscales:
1. Mental Demand
2. Physical Demand
3. Temporal Demand
4. Performance (self-rated, reverse-scored)
5. Effort
6. Frustration
"""

import csv
import os
from scipy import stats
import numpy as np

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_ID = "TEST01"
STRAIGHTLINERS_A = {"P10", "P14"}

DIMS = ["Mental demand", "Physical demand", "Temporal demand", "Performance", "Effort", "Frustration"]


def load_nasa(filename, straightliners=None):
    """Return a list of (sid, [6 scores], is_straightline)"""
    rows = []
    with open(os.path.join(DATA_DIR, filename), encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            sid = row["Student ID"].strip().upper()
            if sid == TEST_ID:
                continue
            keys = sorted([k for k in row if k.startswith("4-")],
                          key=lambda k: int(k.split(".")[0].split("-")[1]))
            scores = [int(row[k]) for k in keys]
            sl = straightliners and (sid in {s.upper() for s in straightliners})
            rows.append((sid, scores, sl))
    return rows


def main():
    a = load_nasa("RL_Lab_PostTest_GroupA.csv", STRAIGHTLINERS_A)
    b = load_nasa("RL_Lab_PostTest_GroupB.csv")

    print(f"RR (A) n = {len(a)}, n after excluding straight-liners = {sum(1 for r in a if not r[2])}")
    print(f"Colab (B) n = {len(b)}\n")

    # Overall mean
    a_overall_all = [np.mean(r[1]) for r in a]
    a_overall_clean = [np.mean(r[1]) for r in a if not r[2]]
    b_overall = [np.mean(r[1]) for r in b]

    t_all, p_all = stats.ttest_ind(a_overall_all, b_overall, equal_var=False)
    t_clean, p_clean = stats.ttest_ind(a_overall_clean, b_overall, equal_var=False)

    print(f"Overall mean  RR(all, n={len(a_overall_all)})  M={np.mean(a_overall_all):.2f} SD={np.std(a_overall_all, ddof=1):.2f}")
    print(f"Overall mean  RR(excl. straight-liners, n={len(a_overall_clean)})  M={np.mean(a_overall_clean):.2f} SD={np.std(a_overall_clean, ddof=1):.2f}")
    print(f"Overall mean  Colab(n={len(b_overall)})  M={np.mean(b_overall):.2f} SD={np.std(b_overall, ddof=1):.2f}")
    print(f"  t(all vs Colab) = {t_all:+.3f}, p = {p_all:.3f}")
    print(f"  t(excl. straight-liners vs Colab) = {t_clean:+.3f}, p = {p_clean:.3f}\n")

    # Six subscales
    print("=" * 90)
    print(f"{'Subscale':<12}{'RR M(SD)':<18}{'RR excl. M(SD)':<18}{'Colab M(SD)':<18}{'t (all)':<12}{'p':<10}{'sig'}")
    print("=" * 90)

    rows_md = []
    for i, dim in enumerate(DIMS):
        a_all = [r[1][i] for r in a]
        a_clean = [r[1][i] for r in a if not r[2]]
        b_v = [r[1][i] for r in b]

        a_m, a_sd = np.mean(a_all), np.std(a_all, ddof=1)
        a_cm, a_csd = np.mean(a_clean), np.std(a_clean, ddof=1)
        b_m, b_sd = np.mean(b_v), np.std(b_v, ddof=1)

        t, p = stats.ttest_ind(a_all, b_v, equal_var=False)
        sig = '***' if p < .001 else '**' if p < .01 else '*' if p < .05 else 'n.s.'

        print(f"{dim:<10}  {a_m:.2f}({a_sd:.2f})    {a_cm:.2f}({a_csd:.2f})    {b_m:.2f}({b_sd:.2f})    {t:+.3f}     {p:.3f}    {sig}")

        rows_md.append((dim, a_m, a_sd, a_cm, a_csd, b_m, b_sd, t, p, sig))

    # Markdown table
    print("\n\n## Combined Markdown table (overall + six subscales)\n")
    print("| Dimension | RR all (n=18) M (SD) | RR excl. straight-liners (n=16) M (SD) | Colab (n=12) M (SD) | t (all vs Colab) | p | Significance |")
    print("|------|--------------------|---------------------------|---------------------|------|---|--------|")
    print(f"| **Overall mean** | {np.mean(a_overall_all):.2f} ({np.std(a_overall_all, ddof=1):.2f}) | {np.mean(a_overall_clean):.2f} ({np.std(a_overall_clean, ddof=1):.2f}) | {np.mean(b_overall):.2f} ({np.std(b_overall, ddof=1):.2f}) | {t_all:+.3f} | {p_all:.3f} | {'\\*'*(1 if p_all<.05 else 0) if p_all<.05 else 'n.s.'} |")
    for row in rows_md:
        dim, a_m, a_sd, a_cm, a_csd, b_m, b_sd, t, p, sig = row
        sig_md = '\\*\\*\\*' if p < .001 else '\\*\\*' if p < .01 else '\\*' if p < .05 else 'n.s.'
        print(f"| {dim} | {a_m:.2f} ({a_sd:.2f}) | {a_cm:.2f} ({a_csd:.2f}) | {b_m:.2f} ({b_sd:.2f}) | {t:+.3f} | {p:.3f} | {sig_md} |")


if __name__ == '__main__':
    main()
