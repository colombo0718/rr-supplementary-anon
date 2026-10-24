# Questionnaire Content Plan

**Language of administration:** English
**Mode of administration:** Google Form (one for the pre-test, one for the post-test)
**Post-test design:** A single form; Section 3 is split into two parts (the experimental group fills in 3A, the control group fills in 3B)

---

## Pre-Test

> Duration: about 20 minutes | One form shared by both groups

### Section 0: Background Information

| # | Question | Type |
|---|------|------|
| 0-1 | Student ID | Short answer (required; used to match pre- and post-tests) |
| 0-2 | Group (Group A — RR Platform / Group B — Colab) | Single choice |
| 0-3 | Year of study (1st / 2nd / 3rd / 4th / Graduate) | Single choice |
| 0-4 | Programming experience (None / Basic / Intermediate / Advanced) | Single choice |
| 0-5 | Prior knowledge of reinforcement learning (Never heard of it / Heard but don't understand / Some understanding / Familiar with it) | Single choice |

### Section 1: RL Concept Understanding (RQ1)

| # | Question | Options | Answer |
|---|------|------|------|
| 1-1 | In reinforcement learning, what does "state" refer to? | A. The action taken by the agent / B. The current observation of the environment / C. The reward received / D. The learning rate | B |
| 1-2 | What happens at the start of a new "episode"? | A. The agent receives a large reward / B. The Q-table is cleared / C. The environment resets to the initial condition / D. The agent stops exploring | C |
| 1-3 | In an ε-greedy strategy, what does a HIGH ε value mean? | A. The agent always picks the best known action / B. The agent explores more randomly / C. The agent learns faster / D. The agent ignores all rewards | B |
| 1-4 | Which of the following best describes what Q(s, a) represents? | A. The probability of choosing action a from state s / B. The immediate reward for taking action a / C. The expected future reward when taking action a from state s / D. The number of times action a was taken | C |
| 1-5 | If an agent always picks the action with the highest Q-value and never tries anything new, what problem might occur? | A. The agent learns too slowly / B. The agent might miss a better action it has never tried / C. The Q-table grows too large / D. The reward curve becomes too smooth | B |

### Section 2: Chart Reading (RQ2)

> Note: At administration time, the corresponding image must be inserted next to each question (uploaded manually in Google Form)

| # | Scenario description | Options | Answer |
|---|------------|------|------|
| 2-1 | A reward curve stays flat for the first 100 episodes, then steadily increases. What does this most likely indicate? | A. The agent stopped exploring after episode 100 / B. The agent began learning effectively around episode 100 / C. The reward function changed at episode 100 / D. The agent reached the maximum possible reward | B |
| 2-2 | Two reward curves: Curve A rises quickly but is noisy and unstable. Curve B rises slowly but is smooth and steady. Which is most likely correct? | A. Curve A has a lower learning rate than Curve B / B. Curve A has a higher learning rate than Curve B / C. Curve B has a higher exploration rate than Curve A / D. Both curves used the same parameters | B |
| 2-3 | In a Q-table heatmap for a maze, cells near the goal show strong consistent colors. Cells far from the goal show weak or mixed colors. What does this mean? | A. The goal area has a higher reward in all directions / B. The agent has visited cells near the goal more and is more confident there / C. The agent avoids cells far from the goal / D. The maze is more complex near the goal | B |

---

## Post-Test

> Duration: about 40 minutes | A single form; Section 3 is filled in by group
> ⚠️ The post-test needs 40 minutes (30 minutes for concept and platform items + 10 minutes for NASA-TLX + SUS); this time has been reserved in the lesson plan.

### Section 0: Background Information

| # | Question | Type |
|---|------|------|
| 0-1 | Student ID | Short answer (required) |
| 0-2 | Group (Group A — RR Platform / Group B — Colab) | Single choice |

### Section 1: RL Concept Understanding (RQ1) | Shared by both groups

> The same 5 items as Section 1 of the pre-test (to measure improvement)

### Section 2: Chart Reading (RQ2) | Shared by both groups

> The same 3 items as Section 2 of the pre-test (to measure improvement)

### Section 3A: Platform Feedback — Experimental Group (RR Platform)

> ⚠️ Only Group A (RR Platform) fills in this part; Group B skips it
> Scale: 1 (Strongly Disagree) → 5 (Strongly Agree)

| # | Question | Type |
|---|------|------|
| 3A-1 | The Rein Room interface was easy to use. | Likert 1–5 |
| 3A-2 | I felt confident adjusting the parameters (α, γ, ε) using the sliders. | Likert 1–5 |
| 3A-3 | The visualizations (heatmap, reward curves) helped me understand what the agent was learning. | Likert 1–5 |
| 3A-4 | I am interested in learning more about reinforcement learning after this class. | Likert 1–5 |
| 3A-5 | I would recommend Rein Room to someone who wants to learn about RL. | Likert 1–5 |

### Section 3B: Platform Feedback — Control Group (Colab)

> ⚠️ Only Group B (Colab) fills in this part; Group A skips it
> Scale: 1 (Strongly Disagree) → 5 (Strongly Agree)

| # | Question | Type |
|---|------|------|
| 3B-1 | The Colab interface was easy to use. | Likert 1–5 |
| 3B-2 | I felt confident modifying the parameters (alpha, gamma, epsilon) in the code. | Likert 1–5 |
| 3B-3 | The charts generated by the code helped me understand what the agent was learning. | Likert 1–5 |
| 3B-4 | I am interested in learning more about reinforcement learning after this class. | Likert 1–5 |
| 3B-5 | I would recommend Colab + the course notebooks to someone who wants to learn about RL. | Likert 1–5 |

### Section 4: NASA-TLX Cognitive Load Scale (Task Load Index) | Shared by both groups

> The instructor explicitly requested its inclusion on 4/2. Six dimensions, each scored 0–100 (a 21-tick slider in steps of 5), or simplified to a 1–10 Likert scale.
> **Recommended: Linear Scale 1–10** (supported by Google Form; a higher number means a higher load, except for Performance)

| # | Dimension | Question text | Direction |
|---|------|---------|------|
| 4-1 | Mental Demand | How much mental and perceptual activity was required? (thinking, deciding, calculating, remembering, looking, searching, etc.) | High = high load |
| 4-2 | Physical Demand | How much physical activity was required? (pushing, pulling, turning, controlling, activating, etc.) | High = high load |
| 4-3 | Temporal Demand | How much time pressure did you feel due to the rate or pace at which the tasks or task elements occurred? | High = high load |
| 4-4 | Performance | How successful do you think you were in accomplishing the goals set by the instructor? | **Low = poor performance** (reversed: 1=Perfect, 10=Failure) |
| 4-5 | Effort | How hard did you have to work to accomplish your level of performance? | High = high load |
| 4-6 | Frustration | How insecure, discouraged, irritated, stressed, and annoyed were you? | High = high load |

> **Scoring note:** The Performance item is reverse-scored and must be flipped (11 - score) when computing the overall NASA-TLX score.

**Section Title (shown in the Google Form):**
> "Please rate each dimension based on your experience with the learning activities in this course. Use 1 (Very Low) to 10 (Very High)."

---

### Section 5: SUS System Usability Scale | Fill in the version matching the group

> The instructor explicitly requested its inclusion on 4/2. 10 items, Likert 1–5 (Strongly Disagree → Strongly Agree).
> The experimental and control groups are routed by Section in the Google Form (5A / 5B), with the item wording adjusted slightly to match each platform.

#### Section 5A — Experimental Group (RR Platform)

> ⚠️ Only Group A (RR Platform) fills this in

| # | Question | Positive/Negative |
|---|------|-------|
| 5A-1 | I think that I would like to use Rein Room frequently. | Positive |
| 5A-2 | I found Rein Room unnecessarily complex. | Negative |
| 5A-3 | I thought Rein Room was easy to use. | Positive |
| 5A-4 | I think that I would need the support of a technical person to be able to use Rein Room. | Negative |
| 5A-5 | I found the various functions in Rein Room were well integrated. | Positive |
| 5A-6 | I thought there was too much inconsistency in Rein Room. | Negative |
| 5A-7 | I would imagine that most people would learn to use Rein Room very quickly. | Positive |
| 5A-8 | I found Rein Room very cumbersome to use. | Negative |
| 5A-9 | I felt very confident using Rein Room. | Positive |
| 5A-10 | I needed to learn a lot of things before I could get going with Rein Room. | Negative |

#### Section 5B — Control Group (Google Colab)

> ⚠️ Only Group B (Colab) fills this in

| # | Question | Positive/Negative |
|---|------|-------|
| 5B-1 | I think that I would like to use Google Colab with these notebooks frequently. | Positive |
| 5B-2 | I found the Colab + notebook setup unnecessarily complex. | Negative |
| 5B-3 | I thought the Colab + notebook setup was easy to use. | Positive |
| 5B-4 | I think that I would need the support of a technical person to be able to use the Colab notebooks. | Negative |
| 5B-5 | I found the various parts of the Colab notebooks were well integrated. | Positive |
| 5B-6 | I thought there was too much inconsistency in how the Colab notebooks worked. | Negative |
| 5B-7 | I would imagine that most people would learn to use these Colab notebooks very quickly. | Positive |
| 5B-8 | I found the Colab + notebook setup very cumbersome to use. | Negative |
| 5B-9 | I felt very confident using Google Colab for this course. | Positive |
| 5B-10 | I needed to learn a lot of things before I could get going with the Colab notebooks. | Negative |

> **SUS scoring (for post-class analysis):**
> - Positive items: score - 1
> - Negative items: 5 - score
> - Sum of the 10 items × 2.5 = SUS score (0–100; 68 is the average)

---

### Section 6: Overall Course Feedback | Shared by both groups

| # | Question | Type |
|---|------|------|
| 6-1 | What was the most helpful part of today's class? | Short answer |
| 6-2 | What was the most confusing or difficult part? | Short answer |
| 6-3 | Any other comments or suggestions? | Short answer (optional) |

---

## Notes

- **Chart-reading items (Section 2):** Before administration, insert the corresponding image manually in the Google Form (one image for each of the 3 items).
- **Post-test 3A/3B:** In the Google Form, label them with the Section Titles "★ Group A Only (Rein Room)" and "★ Group B Only (Colab)" to remind students to fill in the correct part.
- **Post-test 5A/5B:** Same as above; routed by Section Title.
- **NASA-TLX Section 4** is shared by both groups and is not split.
- Sections 1 and 2 are identical in the pre-test and post-test, to allow paired comparison of improvement.
- **Use Group A / Group B for the group options**, without writing out the full platform names, to avoid implying superiority (the principle of neutral group labels).
