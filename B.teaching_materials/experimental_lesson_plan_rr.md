# Experimental Group Lesson Plan (RR Platform)

**Audience:** University students (international students) | **Language of instruction:** English
**Dates:** Session 1: 4/21 (Tue), Session 2: 4/28 (Tue) | **Time:** 14:10-17:00
**Platform:** Rein Room — [platform URL withheld for anonymous review]

---

## Session 1 (4/21)

### 14:10-14:30 | Pre-test questionnaire (20 min)

**Instructor script:**
> "Before we start today's class, please open the Google Form link on the screen and complete the questionnaire. This is NOT a graded test — it's just to understand your background. Please answer honestly, including if you've never heard of reinforcement learning before. It should take about 15–20 minutes."

**Student task:**
- Open the Google Form (link projected by the instructor or shared link)
- Complete the background information and the RL concept questions

**Notes:** Make sure every student enters a student ID or class code so that the pre- and post-tests can be matched.

---

### 14:30-14:50 | RL concept lecture PPT (20 min)

**Instructor script:**
> "Now let's talk about what reinforcement learning actually is. You might have heard of AlphaGo, or games where AI learns to play by itself — that's reinforcement learning. Let me show you the core idea."

**Key points (corresponds to Objective 1: SAR loop):**

1. **Analogy:** The process of training a pet
   > "Imagine you're training a dog. The dog is the *agent*. The room is the *environment*. What the dog sees right now — that's the *state*. What the dog does (sit, run, bark) — that's the *action*. When the dog does something right and gets a treat — that's the *reward*."

2. **SAR loop diagram:**
   > "Every single step follows this loop: the agent observes the state → chooses an action → receives a reward → moves to the next state. This loop repeats until the episode ends."

3. **Episode concept:**
   > "An *episode* is one complete run — like one game of chess from start to finish. After the episode ends, we reset and start a new one. The agent learns a little more each episode."

**Student task:** Listen and raise hands to ask questions. Leave one PPT slide blank: ask students to say out loud what State / Action / Reward each are.

---

### 14:50-15:20 | RR interface tour + MAB task (30 min)

**Instructor script (interface tour):**
> "Now open your browser and go to the Rein Room URL shown on the screen [platform URL withheld]. This is the platform we'll be using today. Let me walk you through the interface."

**Interface highlights:**
- Left side, game area: the agent acts here
- Right side, control panel:
  - 🎮 Game page: choose a task
  - 📊 Dashboard page: adjust parameters (α, γ, ε) and view training charts
  - 🔬 Analysis page: Q-table heatmap

**MAB task (corresponds to Objective 2: exploration vs. exploitation):**

> "Let's start with the simplest task — Multi-Armed Bandit. Think of it as a row of slot machines. Each machine has a different hidden probability of giving you a reward. Your agent has to figure out which machine is best — but it can only learn by trying."

Step 1: Load the MAB task, set ε to **0.9**, press start, and let students observe for about 1 minute.
> "With ε = 0.9, the agent tries random machines 90% of the time. What do you notice about the reward curve?"

Step 2: Clear, change ε to **0.1**, restart, and compare.
> "Now with ε = 0.1, the agent mostly sticks to what it thinks is the best machine. Is this better or worse? Why might always choosing the 'best' option be a problem?"

**Student task:**
- Try both settings themselves (ε = 0.9 and ε = 0.1)
- Observe the difference in the reward curves and prepare to answer orally: "Which setting makes the average reward more stable?"

---

### 15:20-15:30 | Break (10 min)

---

### 15:30-15:45 | V2 video: How Agents Learn — Q-table & Update Rule (15 min)

**Instructor script:**
> "Before we try Maze1D, watch this short video — it explains how the agent actually stores and updates what it learns."

---

### 15:45-16:30 | Maze1D task (45 min) | Objective 1: SAR loop + Q-table (T2)

**Instructor script:**
> "Now let's try a maze. In Maze1D, the agent is on a line and needs to reach the goal. This environment is simple enough that we can clearly see what state, action, reward, and episode each mean — let's verify your understanding here."

**Part A: Instructor demonstrates the γ effect (about 15 min)**

> "First, I'll show you how the discount factor γ affects behavior. γ controls whether the agent cares about immediate or future rewards."

- γ = 0.1:
  > "With a low γ, the agent is short-sighted — it only cares about the reward right now. Watch what happens."

- γ = 0.9:
  > "With a high γ, the agent is patient — willing to take a longer path for a bigger reward later."

> Note: γ will not be tested directly — this is for building intuition only.

**Part B: SAR loop check (about 15 min) | T2 assessment**

After students run Maze1D, the TA asks each student in turn:

> "In this Maze1D game — **what is the state? What are the actions? When does the agent receive a reward? Where does one episode start and end?**"

Expected answers:
- **State**: the agent's position on the 1D line
- **Actions**: move left / move right
- **Reward**: a positive reward for reaching the goal; a negative reward for falling into a trap or timing out
- **Episode**: starts from the start position and ends when the agent reaches the goal or times out; after a reset the next episode begins

**Student task:** Try two γ values and observe the difference in paths; then be able to answer the four questions above orally.

> ✅ **T2 completion criterion:** Can correctly state what state / action / reward / episode each represent in Maze1D

---

### 16:30-17:00 | Maze2D first look (30 min) | Not assessed

**Instructor script:**
> "Now let's get a first look at 2D maze. Just start the agent and watch it explore — we'll do a deeper analysis next class after watching a video about Q-table heatmaps."

**Student task:**
- Open Maze2D, press Start, and observe how the agent moves on the grid
- Feel free to adjust parameters and observe changes in behavior
- **No assessment task needs to be completed**; the aim is simply to get familiar with the environment

> ℹ️ T3 (identifying the path on the Q-table heatmap) takes place in Session 2 after the V3 video.

---

## Session 2 (4/28)

### 14:10-14:20 | Review (10 min)

**Instructor script:**
> "Let's do a quick recap. Last week we covered the core loop of reinforcement learning. Can anyone tell me — what are the three key elements in every RL step?"

Expected student answer: State, Action, Reward (confirms Objective 1)

> "And what does ε control in the MAB task?"

Expected answer: exploration vs. exploitation (confirms Objective 2)

---

### 14:20-14:35 | V3 video: Reading the Q-table Heatmap (15 min)

**Instructor script:**
> "Before we dive into Maze2D analysis, watch this video — it explains how to read the Q-table heatmap and trace a path."

---

### 14:35-15:05 | Maze2D deep dive (30 min) | Objective 4: Basic Q-table reading (T3)

**Instructor script:**
> "Now open Maze2D again. This time we're going to the Analysis tab to read the Q-table heatmap."

**Step 1: Switch to the analysis page and explain the heatmap (about 10 min)**
> "Click on the 🔬 Analysis tab. Each cell shows the direction the agent currently thinks is best. Strong color = confident; weak color = hasn't explored much."

**Step 2: Students trace the path (about 20 min)**
> "Can you trace a path from Start to Goal just by following the arrow colors?"

**Student task:**
- Start Maze2D training and wait for about 500-1000 steps
- Switch to the analysis page and orally point out the path from Start to Goal

> ✅ **T3 completion criterion:** Can point out the Start→Goal path on the Q-table heatmap

---

### 15:05-15:20 | V4 video: Reading Training Curves + A4 Heli Demo (15 min)

**Instructor script:**
> "Good work on Maze2D. Now watch these two short videos — one on how to read training curves, one showing what we'll do with Heli."

---

### 15:20-15:30 | Break (10 min)

---

### 15:30-16:00 | Heli task (30 min) | Objective 3: Reading training curves (T4)

**Instructor script:**
> "Today's main task is Heli — a helicopter that needs to fly through gaps. Each episode, the helicopter starts fresh. Your job is to watch the reward curve and figure out when the agent starts improving."

**Step 1: Start and observe early behavior (about 5 min)**
> "In the first few episodes, the helicopter crashes quickly — that's expected. Watch the reward chart on the right. What does a very low reward mean?"

**Step 2: Observe at least 50 episodes and watch the curve trend (about 25 min)**

Corresponds to Objective 3: reading training curves
> "As training continues, does the reward go up? Stay flat? What does an upward trend tell you about the agent's learning?"

> "Look at the shape of the curve. Is it noisy? Smooth? Does it ever suddenly drop after improving — what might cause that?"

**Step 3: Compare high vs. low ε (optional, about 15 min)**

Reset first, change ε from 0.3 to 0.05, and observe another 50 episodes:
> "With almost no exploration, does the agent improve faster or slower? Why might that be a problem?"

**Student task (T4 assessment):**
- Observe at least 50 episodes
- Answer (orally):
  1. Describe the shape of the reward curve in one sentence.
  2. Around which episode did you first notice improvement?
  3. What does a sudden drop in reward tell you?

> ✅ **T4 completion criterion:** Observe at least 50 episodes and be able to describe the trend of the reward curve (e.g., low then rising, continuously oscillating)

---

### 16:00-16:10 | V5 video: Continuous State & Discretization (10 min)

**Instructor script:**
> "Before Fighter, watch this short video on continuous states — it explains why Heli and Fighter need a different approach."

---

### 16:10-16:40 | Fighter challenge (30 min) | Extended free exploration, not assessed (T5 optional)

**Instructor script:**
> "This one is free exploration — no assessment. Fighter is a fighting game environment. Try any parameter combinations you want and see how the agent learns. Have fun with it."

**Student task:** Freely adjust ε and α and observe the agent's learning behavior. The instructor walks around and answers questions.

> ✅ **T5 record:** Any attempt at Fighter is recorded as completed (not included in the completion-rate analysis)

---

### 16:40-17:00 | Post-test questionnaire (20 min)

**Instructor script:**
> "Last step — please open the post-test Google Form on the screen. It covers the same RL concept questions from the pre-test, plus questions about the platform, a cognitive load survey, and a usability survey."

**Student task:** Complete the Google Form post-test (Sections 1+2 concept questions, Section 3A RR platform feedback, Section 4 NASA-TLX, Section 5A SUS).
