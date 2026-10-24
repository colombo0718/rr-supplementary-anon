# Experimental Group Platform Task Plan (RR Platform)

**Design principle:** Students only need to adjust the slider values marked `🔧` in the Rein Room interface and press start to observe the results.  
No mathematical derivation is required; the focus is on observing how the platform's visualizations react when parameters change.

Platform URL: **[platform URL withheld for anonymous review]**

Divided into two sessions:
- **Day 1** (4/21): MAB → Maze1D (demonstration) → Maze2D + Q-table heatmap
- **Day 2** (4/28): Heli → Fighter (optional) → interactive chart discussion

---

## Day 1

---

### Activity 1 — Multi-Armed Bandit: Exploration vs. Exploitation (30 min) | Objective 2: RQ1

**Platform steps:**
1. Go to [platform URL withheld for anonymous review]
2. Select the task: **Multi-Armed Bandit (MAB)**
3. Switch to the 📊 dashboard page and find the ε (epsilon) slider

**Concept explanation (projected on screen):**

```
Imagine a row of slot machines.
Each machine has a hidden probability of giving you a reward.

With HIGH ε → the agent tries random machines often  (more exploration)
With LOW  ε → the agent mostly picks the best machine it knows  (more exploitation)
```

---

**Round 1**

| 🔧 Parameter | Value |
|---|---|
| ε (epsilon) | **0.9** |

→ Press **Start**, observe for about 1 minute, then press Pause.

**Observation questions:**
- What does the reward curve look like? Is it noisy or smooth?
- Is the agent converging toward the best machine?

---

**Round 2**

| 🔧 Parameter | Value |
|---|---|
| ε (epsilon) | **0.1** |

→ Press **Reset**, then **Start**, and observe for about another minute.

**Observation questions:**
- Compare to Round 1: which reward curve is smoother? Which is higher?
- If the agent only exploits (ε ≈ 0), what risk does it face?

---

**Class discussion (corresponds to the T1 assessment):**
> "Which ε gave a better average reward in the end?  
> Why might an agent that *never* explores get stuck with a bad strategy?"

> ✅ **T1 completion criterion:** The student can verbally describe the difference between the ε=0.9 and ε=0.1 curves

---

### Instructor Demonstration — Maze1D: The Effect of γ (40 min) | Demonstration, not assessed

> ⚠️ This segment is an instructor demonstration. Students only watch and do not need to operate it themselves; it is not included in the post-test questions.

**Platform steps:**
1. Select the task: **Maze 1D**
2. The instructor demonstrates adjusting γ (0.5 vs. 0.99) so students can observe the difference between a short-sighted and a far-sighted agent strategy

**Key demonstration points:**
- With γ = 0.5, the agent only looks at near-term rewards and may stop midway
- With γ = 0.99, the agent is more willing to "take a longer detour" to obtain the larger goal reward

---

### Activity 2 — Maze2D: Q-table Heatmap (50 min) | Objective 4: RQ2

**Platform steps:**
1. Select the task: **Maze 2D**
2. Start with the default parameters and observe the agent's early behavior
3. Press Pause, switch to the 🔬 analysis page, and observe the Q-table heatmap

---

**Part A: Observing the learning process**

| 🔧 Parameter | Suggested Value |
|---|---|
| α (alpha)   | **0.5** |
| γ (gamma)   | **0.95** |
| ε (epsilon) | **0.2** |

→ Press **Start**, wait for about **500-1000 steps**, then Pause.

**Observation questions:**
- In the early episodes, how does the agent move? (random? systematic?)
- After 1000 steps, does the agent find a shorter path than at the start?

---

**Part B: Interpreting the Q-table heatmap**

Switch to the 🔬 analysis page.

**Observation questions:**
1. Which area of the maze has the **strongest, most consistent colors**?  
   → What does strong color mean about the agent's confidence?

2. Can you **trace a path from Start to Goal** just by following the arrow colors?  
   → Try it — does it lead to the goal?

3. Are there any cells with **weak or mixed colors**?  
   → Why might those cells be uncertain?

---

**Part C: Free adjustment (optional)**

| 🔧 Try changing | Suggested test values |
|---|---|
| ε (epsilon) | 0.05 (less explore) vs. 0.5 (more explore) |
| α (alpha)   | 0.1 (slow update) vs. 0.9 (fast update) |

→ Observe whether the convergence speed of the heatmap changes.

---

**Class discussion (corresponds to the T2 assessment):**
> "Look at the cells near the goal versus far from the goal.  
> Which area has clearer arrows? Why does the learning 'spread' from the goal outward?"

> ✅ **T2 completion criterion:** The student can point out the path from Start to Goal on the Q-table heatmap

---

## Day 2

---

### Activity 3 — Heli: Training Curve Convergence (50 min) | Objective 3: RQ2

**Platform steps:**
1. Select the task: **Heli** (a helicopter flying through gaps)
2. Switch to the 📊 dashboard page
3. Start with the default parameters and first observe the early behavior

**Concept explanation:**

```
Heli is different from MAB — the agent must learn to fly through gaps.
Each episode, the helicopter starts fresh.
Your job: watch the reward curve and observe when improvement begins.
```

---

**Round 1: Observing basic learning (observe at least 50 episodes)**

| 🔧 Parameter | Value |
|---|---|
| α (alpha)   | **0.5** |
| γ (gamma)   | **0.95** |
| ε (epsilon) | **0.3** |

→ Press **Start** and keep observing for at least **50 episodes**.

**Observation questions:**
1. In the early episodes, what happens? Does the helicopter crash immediately?
2. Around which episode do you first notice the agent starting to improve?
3. Describe the shape of the reward curve in **one sentence**.

---

**Round 2: Comparing high vs. low ε (optional)**

Reset first, then:

| 🔧 Change | Value |
|---|---|
| ε (epsilon) | **0.05** (almost no exploration) |

→ Restart, observe 50 episodes, and compare with Round 1.

**Observation questions:**
- Did the agent improve faster or slower with low ε?
- Did the reward curve ever suddenly drop? What might cause a sudden drop?

---

**Class discussion (corresponds to the T3 assessment):**
> "Look at the reward curve after 50+ episodes. Is it trending upward, flat, or noisy?  
> What does an upward trend tell you about the agent's learning?"

> ✅ **T3 completion criterion:** The student observes at least 50 episodes and can describe the trend of the reward curve (e.g., flat then rising, continuously oscillating)

---

### Activity 4 — Fighter: Extended Free Exploration (30 min) | Optional, not assessed

> ⚠️ This segment is an extended experience and is **not included in the post-test assessment**; students may explore freely. Simply record whether they tried it (T4).

**Platform steps:**
1. Select the task: **Fighter**
2. Try any combination of parameters and observe the agent learning

| 🔧 Parameter | Try anything! |
|---|---|
| ε (epsilon) | high → more random, low → more focused |
| α (alpha)   | affects how fast the Q-table updates |

**Open-ended exploration questions (no written answers needed; oral discussion is enough):**
- Does the agent ever learn to fight effectively?
- Is this easier or harder than Heli? Why?

> ✅ **T4 record:** Any attempt at Fighter is recorded as completed (not included in the completion-rate analysis)

---

### Activity 5 — Interactive Chart Discussion (30 min) | Objectives 3, 4: RQ2

> The instructor projects the following scenario charts and the whole class discusses them orally (no written answers are collected in this segment; both groups use the same questions).

---

**Discussion question 1: A reward curve that is flat and then rises**

```
Reward ↑
        |               /‾‾‾‾‾‾
        |              /
        |_____________/
        +─────────────────────── Episode
            0        100       200
```

> "What's happening in the first 100 episodes?  
> Why does the reward start rising around episode 100?  
> Does this mean the agent suddenly 'got smart'?"

---

**Discussion question 2: Two learning curves, A vs. B**

```
Reward ↑
        |   /\/\/\/\/\  ← Curve A: rises fast, very noisy
        |  /\/\/\/\/\/
        | /‾‾‾‾‾‾‾‾‾‾‾  ← Curve B: rises slowly, smooth
        +──────────────────────── Episode
```

> "Which curve likely has a **higher learning rate α**?  
> Which is more stable? Which would you trust more for deployment?  
> Is there a trade-off between learning speed and stability?"

---

**Discussion question 3: Maze2D Q-table heatmap**

(Project a Maze2D heatmap in which colors are dark near the goal and light far away.)

> "Which cell does the agent feel most confident about?  
> Why are cells near the goal darker?  
> If you see a cell with no color at all, what does that tell you?"

---

## Appendix: Quick Parameter Reference

| Parameter | Full name | What it affects | Suggested classroom demo values |
|------|------|---------|--------------|
| α (alpha) | Learning rate | Speed of Q-value updates | 0.1 / 0.5 / 0.9 |
| γ (gamma) | Discount factor | Weight of long-term vs. near-term rewards | 0.5 / 0.95 / 0.99 |
| ε (epsilon) | Exploration rate | Ratio of exploration to exploitation | 0.05 / 0.2 / 0.5 / 0.9 |

> The intuition for α and γ is explained during the Maze1D demonstration and is not included in the pre-/post-test questions.  
> ε is the core tested concept (Objective 2: exploration vs. exploitation).  
> CartPole has been removed from the course (the learning barrier of continuous state is too high; it easily causes frustration and interferes with the study results).
