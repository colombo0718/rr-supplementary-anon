"""
extract_data.py - extract all data needed for the figures from the CSVs in C.data_collection/ and write figures/data.js

Revised version (2026/6/26): per reviewer feedback, all scale analyses use the matched sample as the
                  primary scope, with non-parametric tests + effect sizes.

Usage:
    cd <repo root>
    python figures/extract_data.py
"""

import csv
import io
import json
import math
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "C.data_collection"
OUT_FILE = Path(__file__).parent / "data.js"

TEST_ID = "TEST01"
STRAIGHTLINERS = {"P10", "P14"}


def parse_score(s):
    return int(s.split("/")[0].strip())


def normalize_id(s):
    return s.lstrip("S").replace("-", "").replace(" ", "").upper()


def load_pre(fname):
    students = {}
    with io.open(DATA_DIR / fname, "r", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            sid = row["Student ID"].strip().upper()
            if sid == TEST_ID:
                continue
            students[sid] = parse_score(row["Score"])
    return students


def get_section_keys(row, prefix):
    keys = [k for k in row if k.startswith(prefix)]
    return sorted(keys, key=lambda k: int(k.split(".")[0].split("-")[1]))


def calc_sus(items):
    odd = [items[i] - 1 for i in [0, 2, 4, 6, 8]]
    even = [5 - items[i] for i in [1, 3, 5, 7, 9]]
    return sum(odd + even) * 2.5


def load_post(fname):
    students = {}
    with io.open(DATA_DIR / fname, "r", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            sid = row["Student ID"].strip().upper()
            if sid == TEST_ID:
                continue
            sec3_keys = get_section_keys(row, "3-")
            nasa_keys = get_section_keys(row, "4-")
            sus_keys = get_section_keys(row, "5-")
            students[sid] = {
                "score": parse_score(row["Score"]),
                "sec3": [int(row[k]) for k in sec3_keys],
                "nasa": [float(row[k]) for k in nasa_keys],
                "sus_raw": [int(row[k]) for k in sus_keys],
                "sus": calc_sus([int(row[k]) for k in sus_keys]),
            }
    return students


def match_pair_ids(pre, post):
    """Return the successfully matched (pre_id, post_id) tuples"""
    pairs = []
    for pid in pre:
        for poid in post:
            if normalize_id(pid) == normalize_id(poid):
                pairs.append((pid, poid))
                break
    return pairs


# === Load the four CSVs ===
pre_a = load_pre("RL_Lab_PreTest_GroupA.csv")
pre_b = load_pre("RL_Lab_PreTest_GroupB.csv")
post_a = load_post("RL_Lab_PostTest_GroupA.csv")
post_b = load_post("RL_Lab_PostTest_GroupB.csv")

# Matched student IDs
pairs_a = match_pair_ids(pre_a, post_a)  # [(pre_id, post_id), ...]
pairs_b = match_pair_ids(pre_b, post_b)

# Pre/post scores of matched students
A_pre_paired = [pre_a[pid] for pid, _ in pairs_a]
A_post_paired = [post_a[poid]["score"] for _, poid in pairs_a]
B_pre_paired = [pre_b[pid] for pid, _ in pairs_b]
B_post_paired = [post_b[poid]["score"] for _, poid in pairs_b]

# Post-test scale responses of matched students
A_post_paired_dicts = [post_a[poid] for _, poid in pairs_a]
B_post_paired_dicts = [post_b[poid] for _, poid in pairs_b]


def mean(lst):
    return sum(lst) / len(lst) if lst else 0


# === Assemble the data needed by each figure ===
data = {
    # Concept-test scores (Fig. 5-1 box plot / Fig. 5-2 gain chart)
    "concept_test": {
        # Whole class (kept for comparison)
        "A_pre_all": list(pre_a.values()),
        "A_post_all": [v["score"] for v in post_a.values()],
        "B_pre_all": list(pre_b.values()),
        "B_post_all": [v["score"] for v in post_b.values()],
        # Matched sample (primary analysis)
        "A_pre_paired": A_pre_paired,
        "A_post_paired": A_post_paired,
        "B_pre_paired": B_pre_paired,
        "B_post_paired": B_post_paired,
        # Gain
        "A_gain": [b - a for a, b in zip(A_pre_paired, A_post_paired)],
        "B_gain": [b - a for a, b in zip(B_pre_paired, B_post_paired)],
    },

    # Five-task completion rates (Fig. 5-3)
    "task_completion": {
        "tasks": ["T1 MAB", "T2 Maze1D", "T3 Maze2D", "T4 Heli", "T5 Fighter"],
        "A_completed": [11, 16, 8, 10, 11],
        "A_total": [26, 26, 18, 18, 18],
        "B_completed": [8, 8, 8, 6, 3],
        "B_total": [15, 15, 12, 12, 12],
        "A_rate": [11/26, 16/26, 8/18, 10/18, 11/18],
        "B_rate": [8/15, 8/15, 8/12, 6/12, 3/12],
    },

    # Section 3 platform feedback (Fig. 5-4) - matched sample is the primary analysis
    "section3": {
        "items": [
            "3-1 Interface ease of use",
            "3-2 Parameter confidence",
            "3-3 Visualization helpfulness",
            "3-4 Learning motivation",
            "3-5 Willingness to recommend",
        ],
        # All post-test participants (kept for comparison)
        "A_all": [mean([v["sec3"][i] for v in post_a.values()]) for i in range(5)],
        "B_all": [mean([v["sec3"][i] for v in post_b.values()]) for i in range(5)],
        # Matched sample
        "A_paired": [mean([v["sec3"][i] for v in A_post_paired_dicts]) for i in range(5)],
        "B_paired": [mean([v["sec3"][i] for v in B_post_paired_dicts]) for i in range(5)],
    },

    # System Usability Scale (Fig. 5-5 box plot)
    "sus": {
        # All post-test participants
        "A_all": [v["sus"] for v in post_a.values()],
        "A_clean": [
            v["sus"] for sid, v in post_a.items()
            if sid not in {s.upper() for s in STRAIGHTLINERS}
        ],
        "B_all": [v["sus"] for v in post_b.values()],
        # Matched sample (primary analysis)
        "A_paired": [v["sus"] for v in A_post_paired_dicts],
        "B_paired": [v["sus"] for v in B_post_paired_dicts],
    },

    # Mental workload scale (supplementary)
    "nasa_tlx": {
        "A_all": [mean(v["nasa"]) for v in post_a.values()],
        "B_all": [mean(v["nasa"]) for v in post_b.values()],
        "A_paired": [mean(v["nasa"]) for v in A_post_paired_dicts],
        "B_paired": [mean(v["nasa"]) for v in B_post_paired_dicts],
    },

    # Statistical test results (used in figure titles; revised per reviewer feedback)
    "stats": {
        # Matched sample (primary analysis)
        "concept_wilcoxon_A": {
            "n": len(A_pre_paired), "W": 3.0, "p": 0.113, "r": 0.647, "sig": "n.s.",
            "pre_M": mean(A_pre_paired), "post_M": mean(A_post_paired),
        },
        "concept_wilcoxon_B": {
            "n": len(B_pre_paired), "W": 5.0, "p": 0.012, "r": 0.756, "sig": "*",
            "pre_M": mean(B_pre_paired), "post_M": mean(B_post_paired),
        },
        "gain_MW_AvsB": {"U": 43.0, "p": 0.268, "r": 0.239, "sig": "n.s."},
        "pretest_MW_AvsB": {"U": 77.0, "p": 0.265, "r": 0.239, "sig": "n.s."},
        # Completion rates (chi-square / Fisher exact + Cramer's V)
        "completion_chi2": {
            "T1": {"p": 0.721, "V": 0.056, "sig": "n.s."},
            "T2": {"p": 0.854, "V": 0.029, "sig": "n.s."},
            "T3": {"p": 0.411, "V": 0.150, "sig": "n.s."},
            "T4": {"p": 1.000, "V": 0.000, "sig": "n.s."},
            "T5": {"p": 0.117, "V": 0.286, "sig": "n.s."},
        },
        # SUS (matched-sample Mann-Whitney U)
        "sus_MW_AvsB": {"U": 37.0, "p": 0.136, "r": 0.323, "sig": "n.s."},
        # Section 3 five items (matched-sample Mann-Whitney U)
        "sec3_MW": [
            {"U": 49.0, "p": 0.465, "r": 0.155, "sig": "n.s."},   # 3-1
            {"U": 71.0, "p": 0.471, "r": 0.155, "sig": "n.s."},   # 3-2
            {"U": 70.0, "p": 0.494, "r": 0.141, "sig": "n.s."},   # 3-3
            {"U": 71.0, "p": 0.475, "r": 0.155, "sig": "n.s."},   # 3-4
            {"U": 45.0, "p": 0.308, "r": 0.211, "sig": "n.s."},   # 3-5
        ],
    },

    # Descriptive metadata
    "meta": {
        "groups": {
            "A": "RR group (A), matched n=10",
            "B": "Colab group (B), matched n=12",
        },
        "note": "Figure analyses follow the 2026 revision per reviewer feedback: "
                "scales are analysed mainly on the matched sample using non-parametric tests (Wilcoxon / Mann-Whitney U) "
                "with effect size r reported; completion rates use chi-square tests + Cramer's V.",
    },
}


def write_js():
    js_content = "// figures/data.js - auto-generated by extract_data.py\n"
    js_content += "// Source: the four questionnaire CSVs in C.data_collection/; test account TEST01 excluded\n"
    js_content += "// revised per reviewer feedback: matched sample + non-parametric tests + effect size\n\n"
    js_content += "window.DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
    OUT_FILE.write_text(js_content, encoding="utf-8")
    print(f"[OK] Wrote {OUT_FILE}")
    print(f"   Whole class A pre={len(data['concept_test']['A_pre_all'])}, "
          f"post={len(data['concept_test']['A_post_all'])}")
    print(f"   Whole class B pre={len(data['concept_test']['B_pre_all'])}, "
          f"post={len(data['concept_test']['B_post_all'])}")
    print(f"   Matched: A n={len(data['concept_test']['A_pre_paired'])}, "
          f"B n={len(data['concept_test']['B_pre_paired'])}")
    print(f"   T5 completion rate: A={data['task_completion']['A_rate'][4]:.1%} "
          f"vs B={data['task_completion']['B_rate'][4]:.1%}")
    print(f"   Matched-sample Q4 motivation: A={data['section3']['A_paired'][3]:.2f} "
          f"vs B={data['section3']['B_paired'][3]:.2f}")
    print(f"   Matched-sample SUS: A M={mean(data['sus']['A_paired']):.2f}, "
          f"B M={mean(data['sus']['B_paired']):.2f}")


if __name__ == "__main__":
    write_js()
