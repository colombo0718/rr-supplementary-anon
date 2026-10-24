# Control Group Lesson Plan (Gymnasium + Colab)

**Audience:** Master's students (international students) | **Language of instruction:** English
**Dates:** Session 1: 4/22 (Wed), Session 2: 4/29 (Wed) | **Time:** 14:10-17:00
**Tool:** Google Colab (the instructor creates the notebooks in advance; students just open the link and work)
**Materials:** `RL_Day1_RR.ipynb` (MAB → Maze1D → Maze2D), `RL_Day2_RR.ipynb` (Heli → Fighter)
**Environment:** `rr_envs.py` (custom Gymnasium environments whose rewards exactly match the RR source code)

---

## Session 1 (4/22)

### 14:10-14:30 | Pre-test questionnaire (20 min)

**Instructor script:**
> "Before we start, please open the Google Form link on the screen and complete the questionnaire. This is NOT a graded test — it helps us understand your background. Please answer honestly, even if you have no prior experience with reinforcement learning. It takes about 15–20 minutes."

**Student task:**
- Open the Google Form (the same questionnaire as the experimental group)
- Complete the background information and the RL concept questions

**Notes:** Make sure every student fills in a Student ID so that the pre- and post-tests can be matched.

---

### 14:30-14:50 | RL concept lecture PPT (20 min)

**Instructor script:** (**identical slides to the experimental group**)

> "Now let's talk about what reinforcement learning actually is. You might have heard of AlphaGo, or games where AI learns to play by itself — that's reinforcement learning."

**Key points (corresponds to Objective 1: SAR loop):**

1. **Analogy:** The process of training a pet
   > "Imagine you're training a dog. The dog is the *agent*. The room is the *environment*. What the dog sees right now — that's the *state*. What the dog does — that's the *action*. When the dog does something right and gets a treat — that's the *reward*."

2. **SAR loop diagram:**
   > "Every step follows this loop: observe state → choose action → receive reward → move to next state. This repeats until the episode ends."

3. **Episode concept:**
   > "An *episode* is one complete run — from start to finish. The agent resets and starts fresh each episode, but carries the knowledge it has learned."

**Student task:** Listen and raise hands to ask questions. Leave one PPT slide blank so students can say out loud what State / Action / Reward each are.

---

### 14:50-15:20 | Colab interface introduction + MAB code (30 min)

**Instructor script:**
> "Now open your browser and go to this Colab link: [RL_Day1_RR.ipynb link]. You don't need to install anything — just open it and run the cells one by one."

**Interface highlights (about 5 min):**
> "In Colab, each block is called a *cell*. Press the play button on the left to run it. The output appears below. We'll go through the cells together. You only need to change the values marked with 🔧."

**MAB code (corresponds to Objective 2: exploration vs. exploitation):**

> "Our first task is a bandit problem — a row of slot machines with different hidden reward probabilities. The agent uses an ε-greedy strategy: with probability ε it tries a random machine, with probability 1-ε it picks the best one it knows so far."

Step 1: Run the default code (ε = 0.1) and observe the reward curve output by matplotlib.
> "Run this cell. The x-axis is the number of rounds, the y-axis is the average reward. What does the curve look like?"

Step 2: Change 🔧 ε to **0.9**, re-run, and compare the two curves.
> "Now change ε to 0.9 and run again. With more exploration, does the agent learn faster or slower at the beginning?"

> "Key question: if ε = 0, the agent never explores. What problem does that cause?"

**Student task (corresponds to the T1 assessment):**
- Run ε = 0.1 and ε = 0.9 once each
- Prepare to answer: which setting gives a more stable curve over the first 50 rounds? Why?

> ✅ **T1 completion criterion:** Finish both runs and be able to verbally describe the difference between the ε=0.9 and ε=0.1 curves

---

### 15:20-15:30 | Break (10 min)

---

### 15:30-15:45 | V2 video: How Agents Learn — Q-table & Update Rule (15 min)

**Instructor script:**
> "Before we try Maze1D, watch this short video — it explains how the agent stores and updates what it learns."

---

### 15:45-16:30 | Maze1D code: the effect of γ + SAR check (45 min) | Objective 1: RQ1 (T2)

**Instructor script:**
> "Now let's look at a 1D maze. The agent is on a line and needs to reach the goal. We'll first see how gamma affects behavior, then confirm your understanding of state, action, reward, and episode."

**Part A: Adjust γ and observe behavior differences (about 15 min)**

- γ = 0.5: the agent only looks at near-term rewards and may be "short-sighted," stopping midway
- γ = 0.99: the agent is more willing to take a detour to chase the high reward at the final goal

> "Gamma controls how much the agent cares about future rewards. We won't test gamma directly — this is just to build your intuition."

**Student task:** Follow the instructor and change 🔧 gamma once for each value, run the code, and observe the change in behavior.

**Part B: SAR loop check (about 20 min) | T2 assessment**

After students run Maze1D, the TA asks each student in turn:
> "In this Maze1D code — **what is the state? What are the actions? When does the agent receive a reward? Where does one episode start and end?**"

Expected answers:
- **State**: the agent's position on the 1D line (an integer index)
- **Actions**: move left / move right
- **Reward**: a positive reward for reaching the goal; a negative reward for timing out
- **Episode**: one episode is a run from the start position until the agent reaches the goal or times out and is reset

> ✅ **T2 completion criterion:** Can correctly state what state / action / reward / episode each represent in the Maze1D code

---

### 16:30-17:00 | Maze2D first look (30 min) | Not assessed

**Instructor script:**
> "Now open the Maze2D section. Just run the training cell and watch the agent. We'll do a deeper analysis next class after watching a video about Q-table heatmaps."

**Student task:**
- Run the Maze2D training cell and observe the agent's exploration
- Feel free to adjust the 🔧 parameters and observe changes in behavior
- **No assessment task needs to be completed**; the aim is simply to get familiar with the environment

> ℹ️ T3 (identifying the path on the Q-table heatmap) takes place in Session 2 after the V3 video.

---

## Session 2 (4/29)

### 14:10-14:20 | Review (10 min)

**Instructor script:**
> "Quick recap. Last week we covered the RL loop and Q-learning. Let me ask a few questions."

> "What does the Q-table store? What does a high Q-value for a state-action pair mean?"

Expected answer: stores expected future reward, high = this action is good from this state (confirms Objectives 1 and 4)

> "What does ε control?"

Expected answer: how often the agent explores randomly (confirms Objective 2)

---

### 14:20-14:35 | V3 video: Reading the Q-table Heatmap (15 min)

**Instructor script:**
> "Before we dive into Maze2D analysis, watch this video — it explains how to read the Q-table heatmap and trace a path."

---

### 14:35-15:05 | Maze2D deep dive (30 min) | Objective 4: RQ2 (T3)

**Instructor script:**
> "Now go back to the Maze2D section. This time run the heatmap visualization cell."

**Code explanation highlights:**
> "Q-learning builds a Q-table. Each row is a state, each column is an action. The heatmap shows, for each maze cell, what action the agent currently prefers — arrow direction and color intensity show confidence."

Step 1: Run the training cell (with the default 🔧 parameters).

Step 2: Run the Q-table heatmap cell and observe the output.

**Student task (T3 assessment):**
- Run the Q-table heatmap cell
- Answer orally: Can you trace a path from Start to Goal using the heatmap?

> ✅ **T3 completion criterion:** Point out the Start→Goal path on the heatmap

---

### 15:05-15:20 | V4 video: Reading Training Curves + B4 Heli Demo (15 min)

**Instructor script:**
> "Good work. Now watch these two short videos — one on how to read training curves, one showing what we'll do with Heli."

---

### 15:20-15:30 | Break (10 min)

---

### 15:30-16:00 | Heli code: observe training curve convergence (30 min) | Objective 3: RQ2 (T4)

**Instructor script:**
> "Today we try Heli. The agent is a helicopter that must fly through gaps. Each episode the helicopter starts fresh. We'll watch the reward curve to see when the agent starts improving."

> "This is the same Heli environment as in Rein Room — we built a Python version with the exact same reward function, so the learning behavior should be very similar."

**Step 1: Run the code and observe early behavior (about 10 min)**
> "In the first few episodes, the helicopter crashes quickly — that's normal. Watch the reward per episode."

**Step 2: Wait for training and observe the curve (about 20 min)**

Corresponds to Objective 3: reading training curves
> "As training continues, what happens to the reward? A higher reward means the helicopter survived longer and flew through more gaps."

> "Look at the reward curve. When does it start trending upward? Is the improvement gradual or sudden?"

> "Does the curve ever drop suddenly after improving? What might cause that?"

**Step 3: Adjust 🔧 ε for comparison (about 15 min, optional)**

| 🔧 Change | Value |
|---|---|
| ε (epsilon) | **0.05** (almost no exploration) |

→ Re-run and compare the curves.

**Student task (T4 assessment):**
- Run Heli Q-learning and observe at least 50 episodes
- Answer (orally):
  1. Describe the reward curve shape in one sentence.
  2. At roughly what episode did you notice improvement?
  3. What does a sudden drop in reward tell you?

> ✅ **T4 completion criterion:** Observe at least 50 episodes and be able to describe the trend of the reward curve

---

### 16:00-16:10 | V5 video: Continuous State & Discretization (10 min)

**Instructor script:**
> "Before Fighter, watch this short video on continuous states — it explains why Heli and Fighter need a different approach than Maze1D/2D."

---

### 16:10-16:40 | Fighter code: extended free exploration (30 min) | Optional, not assessed (T5)

> ⚠️ This segment is an extended experience and is **not included in the post-test assessment**; students may explore freely.

**Instructor script:**
> "Now open the Fighter section of Day 2 notebook. Try different parameter combinations and observe how the agent learns. There's no specific task — just explore."

**Student task:** Freely adjust the 🔧 parameters and observe the agent's behavior.

> ✅ **T5 record:** Any attempt at Fighter is recorded as completed (not included in the completion-rate analysis)

---

### 16:40-17:00 | Post-test questionnaire (20 min)

**Instructor script:**
> "Last step — please open the post-test Google Form. Same RL concept questions as the pre-test, plus platform questions, a cognitive load survey, and a usability survey."

**Student task:** Complete the Google Form post-test (including Sections 1-2 concept questions, Section 3B platform feedback, Section 4 NASA-TLX, Section 5B SUS).

---

## Additional Notes

**The single-variable principle:**
- The control group uses the Python environments in `rr_envs.py`, whose reward functions exactly match the RR platform source code
- The only difference is the interface: the control group edits the 🔧 values in the code and re-runs the cell, while the experimental group uses the RR platform's graphical sliders
- The game logic, reward design, RL algorithm (Q-learning), teaching objectives, chart discussion questions, and pre-/post-tests are all identical
