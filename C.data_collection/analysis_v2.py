"""analysis_v2.py — revised analysis per reviewer feedback

The reviewer explicitly requested:
1. Restrict the sample to valid, matchable participants who attended both days: RR n=10, Colab n=12
2. Use non-parametric tests for n<30 (Wilcoxon, Mann-Whitney U)
3. Add an effect size (r) so readers can judge the practical magnitude of differences
4. If a result is not significant, report it as such; avoid words such as "wins"

The original analysis.py is kept unchanged for comparison.
"""
import csv
import os
import math
import numpy as np
from scipy import stats

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_ID = "TEST01"
STRAIGHTLINERS_A = {"P10", "P14"}


# ────── Data loading (same as analysis.py) ──────────────────────────────────────

def parse_score(s):
    return int(s.split("/")[0].strip())

def get_section_keys(row, prefix):
    keys = [k for k in row if k.startswith(prefix)]
    return sorted(keys, key=lambda k: int(k.split(".")[0].split("-")[1]))

def calc_sus(items):
    odd  = [items[i] - 1 for i in [0, 2, 4, 6, 8]]
    even = [5 - items[i] for i in [1, 3, 5, 7, 9]]
    return sum(odd + even) * 2.5

def load_pre(filename):
    students = {}
    with open(os.path.join(DATA_DIR, filename), encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            sid = row["Student ID"].strip().upper()
            if sid == TEST_ID:
                continue
            students[sid] = parse_score(row["Score"])
    return students

def load_post(filename, straightliners=None):
    students = {}
    with open(os.path.join(DATA_DIR, filename), encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            sid = row["Student ID"].strip().upper()
            if sid == TEST_ID:
                continue
            sec3_keys = get_section_keys(row, "3-")
            nasa_keys = get_section_keys(row, "4-")
            sus_keys  = get_section_keys(row, "5-")
            students[sid] = {
                "score": parse_score(row["Score"]),
                "sec3":  [int(row[k]) for k in sec3_keys],
                "nasa":  [int(row[k]) for k in nasa_keys],
                "sus":   [int(row[k]) for k in sus_keys],
                "sl":    straightliners and sid in {s.upper() for s in straightliners},
            }
    return students

def normalize_id(s):
    return s.lstrip("S").replace("-", "").replace(" ", "")

def matched_pairs_full(pre, post):
    """Return the successfully matched (sid, pre_score, post_score, post_dict)"""
    pairs = []
    for pid, pre_sc in pre.items():
        for poid, pdata in post.items():
            if normalize_id(pid) == normalize_id(poid):
                pairs.append((poid, pre_sc, pdata["score"], pdata))
                break
    return pairs


# ────── Statistical tools: non-parametric tests + effect size ──────────────────────────────

def sig_star(p):
    if p < 0.001: return "***"
    if p < 0.01:  return "**"
    if p < 0.05:  return "*"
    if p < 0.10:  return "†"
    return "n.s."

def wilcoxon_r(x, y):
    """Paired-sample Wilcoxon signed-rank + r = |Z| / sqrt(N)
    Returns (W, p, r, n_pairs, interp)
    """
    n = len(x)
    diffs = [b - a for a, b in zip(x, y)]
    nz = sum(1 for d in diffs if d != 0)
    if nz < 2:
        return None, None, None, n, "insufficient sample"
    try:
        res = stats.wilcoxon(x, y, method='approx')
        W = res.statistic
        p = res.pvalue
        z = res.zstatistic if hasattr(res, 'zstatistic') else None
        if z is None:
            # Fallback: back out z from W
            mean_w = nz * (nz + 1) / 4
            sd_w   = math.sqrt(nz * (nz + 1) * (2 * nz + 1) / 24)
            z = (W - mean_w) / sd_w if sd_w > 0 else 0
        r = abs(z) / math.sqrt(nz)  # Use nz rather than n (drops tied pairs)
        interp = "small" if r < 0.3 else "medium" if r < 0.5 else "large"
        return W, p, r, nz, interp
    except Exception as e:
        return None, None, None, n, str(e)

def mannwhitney_r(x, y):
    """Independent-sample Mann-Whitney U + r = |Z| / sqrt(N1+N2)
    Returns (U, p, r, n1, n2, interp)
    """
    n1, n2 = len(x), len(y)
    try:
        res = stats.mannwhitneyu(x, y, method='asymptotic', alternative='two-sided')
        U = res.statistic
        p = res.pvalue
        # Compute Z
        mean_u = n1 * n2 / 2
        sd_u   = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
        z = (U - mean_u) / sd_u if sd_u > 0 else 0
        r = abs(z) / math.sqrt(n1 + n2)
        interp = "small" if r < 0.3 else "medium" if r < 0.5 else "large"
        return U, p, r, n1, n2, interp
    except Exception as e:
        return None, None, None, n1, n2, str(e)


# ────── Load data ───────────────────────────────────────────────────

pre_a  = load_pre("RL_Lab_PreTest_GroupA.csv")
pre_b  = load_pre("RL_Lab_PreTest_GroupB.csv")
post_a = load_post("RL_Lab_PostTest_GroupA.csv", STRAIGHTLINERS_A)
post_b = load_post("RL_Lab_PostTest_GroupB.csv")

# Matched sample: attended both days and can be paired
pairs_a = matched_pairs_full(pre_a, post_a)   # n=10
pairs_b = matched_pairs_full(pre_b, post_b)   # n=12

print("═" * 75)
print(f"Data loading summary")
print("═" * 75)
print(f"  RR group (A): pre-test {len(pre_a)}, post-test {len(post_a)}, matched {len(pairs_a)}")
print(f"  Colab group (B): pre-test {len(pre_b)}, post-test {len(post_b)}, matched {len(pairs_b)}")
print()
print(f"  This analysis follows the reviewer's comments: matched sample only")
print(f"  -> RR group n={len(pairs_a)}, Colab group n={len(pairs_b)}")
print()

# Extract the matched-sample scores and post-test scale data
pre_a_v  = [p[1] for p in pairs_a]
post_a_v = [p[2] for p in pairs_a]
pre_b_v  = [p[1] for p in pairs_b]
post_b_v = [p[2] for p in pairs_b]

post_a_dicts = [p[3] for p in pairs_a]
post_b_dicts = [p[3] for p in pairs_b]

sus_a  = [calc_sus(v["sus"]) for v in post_a_dicts]
sus_b  = [calc_sus(v["sus"]) for v in post_b_dicts]
nasa_a_byq = [v["nasa"] for v in post_a_dicts]  # 6 subscales
nasa_b_byq = [v["nasa"] for v in post_b_dicts]
sec3_a_byq = [v["sec3"] for v in post_a_dicts]  # 5 items
sec3_b_byq = [v["sec3"] for v in post_b_dicts]

gains_a = [b - a for a, b in zip(pre_a_v, post_a_v)]
gains_b = [b - a for a, b in zip(pre_b_v, post_b_v)]


# ────── Result-printing helpers ────────────────────────────────────────────

def hr(title, width=75):
    print()
    print("═" * width)
    print(title)
    print("═" * width)

def print_within(label, x, y):
    """Within-group pre/post Wilcoxon"""
    W, p, r, n, interp = wilcoxon_r(x, y)
    if W is None:
        print(f"  {label}: {interp}")
        return
    star = sig_star(p)
    mean_x, mean_y = np.mean(x), np.mean(y)
    md_x, md_y = np.median(x), np.median(y)
    print(f"  {label}")
    print(f"    pre  M={mean_x:.2f} Mdn={md_x:.1f}  → post M={mean_y:.2f} Mdn={md_y:.1f}")
    print(f"    Wilcoxon W={W:.1f}, p={p:.4f} {star}, r={r:.3f} (effect size: {interp}), n={n} pairs")

def print_between(label, x, y, low_better=False):
    """Between-group Mann-Whitney U"""
    U, p, r, n1, n2, interp = mannwhitney_r(x, y)
    if U is None:
        print(f"  {label}: {interp}")
        return
    star = sig_star(p)
    print(f"  {label}")
    print(f"    A: M={np.mean(x):.2f} SD={np.std(x,ddof=1):.2f} Mdn={np.median(x):.2f} (n={n1})")
    print(f"    B: M={np.mean(y):.2f} SD={np.std(y,ddof=1):.2f} Mdn={np.median(y):.2f} (n={n2})")
    print(f"    Mann-Whitney U={U:.1f}, p={p:.4f} {star}, r={r:.3f} (effect size: {interp})")

def chi2_completion(succ_a, n_a, succ_b, n_b, label):
    """Completion rate: chi-square + Cramer's V"""
    fail_a, fail_b = n_a - succ_a, n_b - succ_b
    table = np.array([[succ_a, fail_a], [succ_b, fail_b]])
    try:
        chi2, p, dof, exp = stats.chi2_contingency(table)
        n_total = n_a + n_b
        # Cramer's V for 2x2
        v = math.sqrt(chi2 / n_total)
        # Use Fisher if any expected count is < 5
        use_fisher = (exp < 5).any()
        if use_fisher:
            _, p_fisher = stats.fisher_exact(table)
            p = p_fisher
    except Exception as e:
        print(f"  {label}: {e}")
        return
    star = sig_star(p)
    method = "Fisher's exact" if use_fisher else "Chi-square"
    print(f"  {label}")
    print(f"    A: {succ_a}/{n_a} = {succ_a/n_a*100:.1f}%   B: {succ_b}/{n_b} = {succ_b/n_b*100:.1f}%")
    print(f"    {method}: p={p:.4f} {star}, Cramer's V={v:.3f}")


# ────── Analysis begins ────────────────────────────────────────────────────

hr("1. Pre-test homogeneity check (are the two groups comparable at baseline?)")
print_between("Pre-test score A vs B", pre_a_v, pre_b_v)

hr("2. Within-group pre/post comparison (Wilcoxon signed-rank)")
print_within("RR group (A) pre -> post", pre_a_v, post_a_v)
print()
print_within("Colab group (B) pre -> post", pre_b_v, post_b_v)

hr("3. Between-group Gain Score comparison (Mann-Whitney U)")
print_between("Gain (post-pre) A vs B", gains_a, gains_b)

hr("4. System Usability Scale (SUS)")
print_between("SUS A vs B", sus_a, sus_b)

hr("5. Mental workload scale (NASA-TLX), overall and subscales")
nasa_labels = ["Mental demand", "Physical demand", "Temporal demand", "Effort", "Frustration", "Performance"]
nasa_a_overall = [np.mean(v) for v in nasa_a_byq]
nasa_b_overall = [np.mean(v) for v in nasa_b_byq]
print_between("Mental workload scale overall A vs B", nasa_a_overall, nasa_b_overall)
print()
for i, name in enumerate(nasa_labels):
    a_i = [v[i] for v in nasa_a_byq]
    b_i = [v[i] for v in nasa_b_byq]
    print_between(f"NASA-{i+1} {name} A vs B", a_i, b_i)
    print()

hr("6. Platform feedback scale (Section 3, five items)")
sec3_labels = ["Interface ease of use", "Parameter confidence", "Visualization helpfulness", "Post-class learning motivation", "Willingness to recommend"]
sec3_a_overall = [np.mean(v) for v in sec3_a_byq]
sec3_b_overall = [np.mean(v) for v in sec3_b_byq]
print_between("Sec3 overall A vs B", sec3_a_overall, sec3_b_overall)
print()
for i, name in enumerate(sec3_labels):
    a_i = [v[i] for v in sec3_a_byq]
    b_i = [v[i] for v in sec3_b_byq]
    print_between(f"Q{i+1} {name} A vs B", a_i, b_i)
    print()

hr("7. Task completion rate (chi-square + Cramer's V)")
# T4 Heli, T5 Fighter completion rates
# Note: the raw completion data cover the whole class (18 / 12), but the analysis should use the matched sample
# For now use the n=18 vs 12 originally recorded in the paper -> switch to the matched sample after review
print("  WARNING: completion rates originally used the whole class (n_A=18, n_B=12); check whether the completion records can be mapped to the matched sample, then re-run")
print()
# Example (matched-sample completion rates estimated from the original data; pending manual review)
# T4: A 56% × 18 ≈ 10, B 50% × 12 = 6
# T5: A 61% × 18 ≈ 11, B 25% × 12 = 3
print("  The following is an estimate assuming matched-sample completion rates equal the whole-class rates (needs review):")
chi2_completion(succ_a=int(round(0.556 * 10)), n_a=10, succ_b=int(round(0.500 * 12)), n_b=12, label="T4 Heli")
print()
chi2_completion(succ_a=int(round(0.611 * 10)), n_a=10, succ_b=int(round(0.250 * 12)), n_b=12, label="T5 Fighter")

hr("8. Reference: t-test results (the reviewer suggested non-parametric tests; kept here for comparison)")
t, p = stats.ttest_rel(pre_a_v, post_a_v)
print(f"  A paired t (n=10): t={t:+.3f}, p={p:.4f}  {sig_star(p)}")
t, p = stats.ttest_rel(pre_b_v, post_b_v)
print(f"  B paired t (n=12): t={t:+.3f}, p={p:.4f}  {sig_star(p)}")
t, p = stats.ttest_ind(gains_a, gains_b, equal_var=False)
print(f"  Gain Welch t: t={t:+.3f}, p={p:.4f}  {sig_star(p)}")

hr("9. Matched-sample Student ID list")
print("  RR group (A) matched IDs:")
for sid, pre, post, _ in pairs_a:
    print(f"    {sid}  pre={pre}, post={post}, gain={post-pre:+d}")
print()
print("  Colab group (B) matched IDs:")
for sid, pre, post, _ in pairs_b:
    print(f"    {sid}  pre={pre}, post={post}, gain={post-pre:+d}")
