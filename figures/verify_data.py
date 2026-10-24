"""
verify_data.py - verify that data.js is consistent with the raw CSV data

Usage:
    cd <repo root>
    python figures/verify_data.py
"""

import csv
import io
from pathlib import Path
from statistics import mean, stdev
import math

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "C.data_collection"

TEST_ID = "TEST01"
STRAIGHTLINERS = {"P10", "P14"}


def parse_score(s):
    return int(s.split("/")[0].strip())


def normalize_id(s):
    return s.lstrip("S").replace("-", "").replace(" ", "").upper()


print("=" * 70)
print("Paper data verification report")
print("=" * 70)

# 1. Check sample sizes
print("\n[Sample size check]")
with io.open(DATA_DIR / "RL_Lab_PreTest_GroupA.csv", "r", encoding="utf-8-sig") as f:
    pre_a = list(csv.DictReader(f))
    pre_a_valid = [r for r in pre_a if r["Student ID"].strip().upper() != TEST_ID]
    print(f"[ok] Experimental group pre-test: {len(pre_a_valid)} (raw {len(pre_a)}, excluding 1 test account)")

with io.open(DATA_DIR / "RL_Lab_PostTest_GroupA.csv", "r", encoding="utf-8-sig") as f:
    post_a = list(csv.DictReader(f))
    post_a_valid = [r for r in post_a if r["Student ID"].strip().upper() != TEST_ID]
    print(f"[ok] Experimental group post-test: {len(post_a_valid)}")

with io.open(DATA_DIR / "RL_Lab_PreTest_GroupB.csv", "r", encoding="utf-8-sig") as f:
    pre_b = list(csv.DictReader(f))
    pre_b_valid = [r for r in pre_b if r["Student ID"].strip().upper() != TEST_ID]
    print(f"[ok] Control group pre-test: {len(pre_b_valid)}")

with io.open(DATA_DIR / "RL_Lab_PostTest_GroupB.csv", "r", encoding="utf-8-sig") as f:
    post_b = list(csv.DictReader(f))
    post_b_valid = [r for r in post_b if r["Student ID"].strip().upper() != TEST_ID]
    print(f"[ok] Control group post-test: {len(post_b_valid)}")

# 2. Check concept-test score statistics
print("\n[Concept-test score check]")
pre_a_scores = [parse_score(r["Score"]) for r in pre_a_valid]
post_a_scores = [parse_score(r["Score"]) for r in post_a_valid]
pre_b_scores = [parse_score(r["Score"]) for r in pre_b_valid]
post_b_scores = [parse_score(r["Score"]) for r in post_b_valid]

print(f"Experimental pre-test: M={mean(pre_a_scores):.2f}, SD={stdev(pre_a_scores):.2f}, n={len(pre_a_scores)}")
print(f"Experimental post-test: M={mean(post_a_scores):.2f}, n={len(post_a_scores)}")
print(f"Control pre-test: M={mean(pre_b_scores):.2f}, SD={stdev(pre_b_scores):.2f}, n={len(pre_b_scores)}")
print(f"Control post-test: M={mean(post_b_scores):.2f}, n={len(post_b_scores)}")

# 3. Read task completion records
print("\n[Task completion check]")
with io.open(DATA_DIR / "task_completion_record_group_A.md", "r", encoding="utf-8") as f:
    content_a = f.read()
    print(f"[ok] Experimental group task sheet read ({len(content_a)} chars)")

with io.open(DATA_DIR / "task_completion_record_group_B.md", "r", encoding="utf-8") as f:
    content_b = f.read()
    print(f"[ok] Control group task sheet read ({len(content_b)} chars)")

# 4. Check Section 3 platform-feedback computation
print("\n[Section 3 platform feedback check]")


def get_section_keys(row, prefix):
    keys = [k for k in row if k.startswith(prefix)]
    return sorted(keys, key=lambda k: int(k.split(".")[0].split("-")[1]))


sec3_a = []
for row in post_a_valid:
    sec3_keys = get_section_keys(row, "3-")
    sec3_a.append([int(row[k]) for k in sec3_keys])

sec3_b = []
for row in post_b_valid:
    sec3_keys = get_section_keys(row, "3-")
    sec3_b.append([int(row[k]) for k in sec3_keys])

if sec3_a:
    sec3_a_means = [mean([s[i] for s in sec3_a]) for i in range(5)]
    print(f"Experimental 3-1 Interface ease of use: {sec3_a_means[0]:.4f}")
    print(f"Experimental 3-2 Parameter confidence: {sec3_a_means[1]:.4f}")
    print(f"Experimental 3-3 Visualization helpfulness: {sec3_a_means[2]:.4f}")
    print(f"Experimental 3-4 Learning motivation: {sec3_a_means[3]:.4f}  <- checklist expects 4.17")
    print(f"Experimental 3-5 Willingness to recommend: {sec3_a_means[4]:.4f}")

if sec3_b:
    sec3_b_means = [mean([s[i] for s in sec3_b]) for i in range(5)]
    print(f"\nControl 3-1 Interface ease of use: {sec3_b_means[0]:.4f}")
    print(f"Control 3-2 Parameter confidence: {sec3_b_means[1]:.4f}")
    print(f"Control 3-3 Visualization helpfulness: {sec3_b_means[2]:.4f}")
    print(f"Control 3-4 Learning motivation: {sec3_b_means[3]:.4f}  <- checklist expects 3.33")
    print(f"Control 3-5 Willingness to recommend: {sec3_b_means[4]:.4f}")

# 5. Check SUS computation
print("\n[SUS usability check]")


def calc_sus(items):
    odd = [items[i] - 1 for i in [0, 2, 4, 6, 8]]
    even = [5 - items[i] for i in [1, 3, 5, 7, 9]]
    return sum(odd + even) * 2.5


sus_a = []
sus_b = []

for row in post_a_valid:
    sus_keys = get_section_keys(row, "5-")
    if sus_keys:
        sus_raw = [int(row[k]) for k in sus_keys]
        sus_a.append(calc_sus(sus_raw))

for row in post_b_valid:
    sus_keys = get_section_keys(row, "5-")
    if sus_keys:
        sus_raw = [int(row[k]) for k in sus_keys]
        sus_b.append(calc_sus(sus_raw))

print(f"Experimental SUS: M={mean(sus_a):.2f}, SD={stdev(sus_a):.2f}, n={len(sus_a)}")
print(f"Control SUS: M={mean(sus_b):.2f}, SD={stdev(sus_b):.2f}, n={len(sus_b)}")

# After excluding straight-line responders
sus_a_clean = [v for i, v in enumerate(sus_a)
               if list(post_a_valid)[i]["Student ID"].strip().upper() not in {s.upper() for s in STRAIGHTLINERS}]
print(f"Experimental SUS (excl. straight-liners): M={mean(sus_a_clean):.2f}, SD={stdev(sus_a_clean):.2f}, n={len(sus_a_clean)}")

print("\n" + "=" * 70)
print("[DONE] Verification complete. Check that the values above agree with figures/data.js and the paper.")
print("=" * 70)
