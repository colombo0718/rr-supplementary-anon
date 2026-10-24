# Teaching Plan Overview

**Experiment period:** 2026/04/21-04/29 | **Each session:** 14:10-17:00 (about 170 minutes)
**Language of instruction:** English (international students)
**Pre-test:** Administered before Session 1 begins (about 20 minutes)
**Post-test:** Administered at the end of Session 2 (about 30 minutes, including NASA-TLX + SUS)

---

## Shared Teaching Objectives for Both Groups

> Hyperparameters such as α / γ are only demonstrated in class and are **not included in the pre-/post-tests**.
> RQ3 (motivation / usability) is collected through the post-test questionnaire and does not need a corresponding teaching objective.

| # | Objective | Description | Related RQ |
|---|------|------|---------|
| 1 | SAR loop + episode | Can explain what state / action / reward / episode each represent | RQ1 Concept understanding |
| 2 | Exploration vs. exploitation (ε) | Understands the role of ε; can predict how the curves differ when ε is high vs. low | RQ1 Concept understanding |
| 3 | Reading training curves | Can judge from the reward curve and steps curve whether learning is improving | RQ2 Chart reading |
| 4 | Basic Q-table reading | Can tell from a heatmap or values which action is preferred in a state (higher Q value = better) | RQ2 Chart reading |

---

## Assessment Task List (Identical for Both Groups)

> The TA records completion in class; completion rates are used in the RQ2 task-performance analysis.
> The four formal tasks (T1-T4) each correspond to one teaching objective; Fighter is an optional extension.

| Task | Game | Assessment focus | Corresponding teaching objective |
|------|------|---------|------------|
| T1 | MAB | Adjust ε and describe the curve difference between ε=0.9 and 0.1 | Objective 2: exploration vs. exploitation |
| T2 | Maze1D | (1) Identify what state / action / reward / episode each represent (2) Point to the value of one cell in the Q-table and explain how it was updated from the previous step (Bellman update) | Objective 1: SAR loop + episode; Objective 4: Q-table reading (update mechanism) |
| T3 | Maze2D | Trace the Start→Goal path on the Q-table heatmap | Objective 4: Q-table reading (spatial path) |
| T4 | Heli | Run at least 50 episodes, describe the trend of the reward curve, and judge whether the agent is improving | Objective 3: reading training curves |
| T5 (optional) | Fighter | Free exploration; record whether the student tried it (not counted in the completion rate) | — |

> CartPole has been removed from the course (the learning barrier of continuous state is too high; it easily causes frustration and interferes with the study results).
> Maze1D serves two functions: a demonstration of the γ effect (led by the instructor) and a check of SAR loop understanding (students answer; T2 assessment).

---

## Experimental Group (RR Platform, Undergraduates)

**Dates:** 4/21 (Session 1), 4/28 (Session 2)

| Time slot | Duration | Activity | Corresponding teaching objective |
|------|------|------|------------|
| **Session 1 (4/21)** | | | |
| 14:10-14:30 | 20 min | Pre-test questionnaire (Google Form) | — |
| 14:30-14:50 | 20 min | RL concept lecture PPT (SAR loop, episode) | Objective 1: RQ1 |
| 14:50-15:20 | 30 min | RR interface tour + **MAB task**: adjust ε and observe exploration behavior | Objective 2: RQ1 (T1) |
| 15:20-15:30 | 10 min | Break | — |
| 15:30-15:45 | 15 min | V2 video: Q-table & Update Rule | — |
| 15:45-16:30 | 45 min | **Maze1D task**: instructor demonstrates the γ effect; students identify SAR + Q-table | Objective 1: RQ1 (T2) |
| 16:30-17:00 | 30 min | **Maze2D first look** (A3 video + let the agent run; not assessed) | — |
| **Session 2 (4/28)** | | | |
| 14:10-14:20 | 10 min | Review of last week's key points | — |
| 14:20-14:35 | 15 min | V3 video: Reading the Q-table Heatmap | — |
| 14:35-15:05 | 30 min | **Maze2D deep dive**: Q-table heatmap, point out the Start→Goal path | Objective 4: RQ2 (T3) |
| 15:05-15:20 | 15 min | V4 video: Reading Training Curves + A4 Heli Demo | — |
| 15:20-15:30 | 10 min | Break | — |
| 15:30-16:00 | 30 min | **Heli task**: observe the training curve converge (at least 50 ep) | Objective 3: RQ2 (T4) |
| 16:00-16:10 | 10 min | V5 video: Continuous State & Discretization | — |
| 16:10-16:40 | 30 min | **Fighter challenge** (extended free exploration, not assessed) | — |
| 16:40-17:00 | 20 min | Post-test questionnaire (Google Form, including NASA-TLX + SUS) | — |

---

## Control Group (Gymnasium + Colab, Master's Students)

**Dates:** 4/22 (Session 1), 4/29 (Session 2)
**Materials:** `RL_Day1_RR.ipynb` (MAB → Maze1D → Maze2D), `RL_Day2_RR.ipynb` (Heli → Fighter)
**Environment:** `rr_envs.py` (custom Gymnasium environments whose rewards exactly match the RR source code)

| Time slot | Duration | Activity | Corresponding teaching objective |
|------|------|------|------------|
| **Session 1 (4/22)** | | | |
| 14:10-14:30 | 20 min | Pre-test questionnaire (Google Form, same as the experimental group) | — |
| 14:30-14:50 | 20 min | RL concept lecture PPT (**identical slides to the experimental group**) | Objective 1: RQ1 |
| 14:50-15:20 | 30 min | Colab introduction + **MAB code**: adjust ε and observe the reward curve | Objective 2: RQ1 (T1) |
| 15:20-15:30 | 10 min | Break | — |
| 15:30-15:45 | 15 min | V2 video: Q-table & Update Rule | — |
| 15:45-16:30 | 45 min | **Maze1D code**: adjust γ and observe behavior differences; students identify SAR + Q-table | Objective 1: RQ1 (T2) |
| 16:30-17:00 | 30 min | **Maze2D first look** (B3 video + let the agent run; not assessed) | — |
| **Session 2 (4/29)** | | | |
| 14:10-14:20 | 10 min | Review of last week's key points | — |
| 14:20-14:35 | 15 min | V3 video: Reading the Q-table Heatmap | — |
| 14:35-15:05 | 30 min | **Maze2D deep dive**: Q-table heatmap, point out the Start→Goal path | Objective 4: RQ2 (T3) |
| 15:05-15:20 | 15 min | V4 video: Reading Training Curves + B4 Heli Demo | — |
| 15:20-15:30 | 10 min | Break | — |
| 15:30-16:00 | 30 min | **Heli code**: observe the training curve converge (at least 50 ep) | Objective 3: RQ2 (T4) |
| 16:00-16:10 | 10 min | V5 video: Continuous State & Discretization | — |
| 16:10-16:40 | 30 min | **Fighter challenge** (extended free exploration, not assessed) | — |
| 16:40-17:00 | 20 min | Post-test questionnaire (Google Form, including NASA-TLX + SUS) | — |

---

## Design Differences Between the Two Groups

| Aspect | Experimental group (RR) | Control group (Colab) | Research significance |
|------|------------|----------------|---------|
| Game environment | Built into the RR platform (JavaScript) | rr_envs.py (Python, rewards aligned with RR) | The only variable is the platform interface; the game logic is the same |
| Interface | Graphical sliders; adjust parameters with a click | Edit the 🔧 values in the code and re-run the cell | Core embodiment of the difference in entry barrier |
| Q-table visualization | Interactive heatmap (updates in real time) | Static matplotlib heatmap | Difference in visualization quality |
| Training curve | Real-time dynamic line chart | Output by matplotlib after execution | Real-time feedback vs. post-run feedback |
| Learning background | Undergraduates | Master's students | ⚠️ Study limitation; must be stated in the paper |

> **Invariants (to ensure study validity):**  
> The same games (MAB / Maze1D / Maze2D / Heli), the same reward function, the same algorithm (Q-learning), the same concept PPT, the same chart discussion questions, and the same pre-/post-test items.
