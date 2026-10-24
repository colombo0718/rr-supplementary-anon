# Control Group Colab Notebook Content Plan

**Design principle:** All code is written in advance; students only need to change the parameter values marked `🔧` and run it.
Students are not required to understand every line of code; the focus is on observing the visualization results after parameters change.

Split into two notebooks (file names correspond to the rr_envs.py environments):
- `RL_Day1_RR.ipynb`: MAB → Maze1D → Maze2D (used in Session 1)
- `RL_Day2_RR.ipynb`: Heli → Fighter (used in Session 2)

**Environment source:** `rr_envs.py` (custom Gymnasium environments whose reward functions are aligned with the RR source code)

---

## RL_Day1_RR.ipynb

---

### Cell 1 — Installation and imports (Setup)

```python
# Run this cell first — downloads the custom environment and installs packages
import subprocess, sys

# Download rr_envs.py from GitHub (public repo)
subprocess.run(["wget", "-q", "-O", "rr_envs.py",
    "https://raw.githubusercontent.com/<YOUR_REPO>/main/rr_envs.py"])

subprocess.run([sys.executable, "-m", "pip", "install",
    "gymnasium", "matplotlib", "seaborn", "numpy", "--quiet"])

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from rr_envs import MABEnv, Maze1DEnv, Maze2DEnv

print("✅ Setup complete!")
```

---

### Cell 2 — Markdown: Today's goal

```markdown
## Today's Goal

We'll explore three reinforcement learning environments — the same games used in Rein Room:
1. **Multi-Armed Bandit (MAB)** — to understand *exploration vs. exploitation*
2. **Maze 1D** — to see how γ (gamma) affects long-term planning *(teacher demo)*
3. **Maze 2D** — to understand *Q-learning* and *Q-table visualization*

You don't need to understand every line of code.
Focus on **what changes when you adjust the 🔧 parameters**.
```

---

### Cell 3 — Markdown: Part 1 — MAB

```markdown
## Part 1: Multi-Armed Bandit (MAB)

Imagine a row of slot machines. Each machine has a *hidden* probability of giving you a reward.
Your agent uses **ε-greedy strategy**:
- With probability **ε** → try a random machine *(explore)*
- With probability **1 - ε** → pick the machine that looked best so far *(exploit)*

### 🔧 Your task:
Run the cell below with **ε = 0.1**, then change it to **ε = 0.9** and run again.
What's different about the two reward curves?
```

---

### Cell 4 — MAB code (students only change epsilon)

```python
# ============================================================
# 🔧 CHANGE THIS VALUE and re-run to see the difference
epsilon = 0.1   # try: 0.1 / 0.5 / 0.9
# ============================================================

env = MABEnv(n_bandits=5, seed=42)
n_rounds = 500

Q = np.zeros(env.n_bandits)
N = np.zeros(env.n_bandits)
rewards = []

for t in range(n_rounds):
    if np.random.random() < epsilon:
        action = np.random.randint(env.n_bandits)   # explore
    else:
        action = np.argmax(Q)                        # exploit

    reward, _ = env.step(action)
    N[action] += 1
    Q[action] += (reward - Q[action]) / N[action]
    rewards.append(reward)

# --- Plot ---
window = 30
smoothed = np.convolve(rewards, np.ones(window)/window, mode='valid')

plt.figure(figsize=(10, 4))
plt.plot(smoothed, label=f'ε = {epsilon}', linewidth=2)
plt.axhline(y=max(env.true_probs), color='gray', linestyle='--',
            label='Best possible reward')
plt.xlabel('Round')
plt.ylabel('Average Reward (smoothed)')
plt.title(f'MAB ε-greedy  |  ε = {epsilon}')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print(f"Agent's best guess: Machine #{np.argmax(Q)}")
print(f"Actual best machine: Machine #{np.argmax(env.true_probs)}")
```

---

### Cell 5 — Markdown: Part 2 — Maze1D (instructor demo)

```markdown
## Part 2: Maze 1D — Effect of γ (Gamma)  *(Teacher Demo)*

The agent is on a 1D line and must reach the goal.

**γ (gamma)** controls how much the agent cares about future rewards:
- **γ = 0.5** → agent is "short-sighted" — only cares about immediate reward
- **γ = 0.99** → agent is "patient" — willing to take a longer path for bigger future reward

### 🔧 Teacher will demonstrate:
Change **gamma** between 0.5 and 0.99 and observe the difference in learned behavior.

> *Note: γ will not be tested in the assessment — this is for intuition building only.*
```

---

### Cell 6 — Maze1D demo code (used by the instructor; students run along)

```python
# ============================================================
# 🔧 CHANGE gamma and re-run to see the difference
alpha   = 0.5
gamma   = 0.99   # try: 0.5 / 0.99
epsilon = 0.2
n_episodes = 500
# ============================================================

env = Maze1DEnv()
Q = np.zeros([env.observation_space.n, env.action_space.n])
episode_rewards = []

for ep in range(n_episodes):
    state, _ = env.reset()
    total_reward, done = 0, False
    while not done:
        if np.random.random() < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(Q[state])
        next_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        Q[state, action] += alpha * (reward + gamma * np.max(Q[next_state]) - Q[state, action])
        state = next_state
        total_reward += reward
    episode_rewards.append(total_reward)

# --- Plot ---
window = 50
smoothed = np.convolve(episode_rewards, np.ones(window)/window, mode='valid')
plt.figure(figsize=(10, 4))
plt.plot(smoothed, linewidth=2)
plt.title(f'Maze1D  |  γ = {gamma}  (higher reward = reached goal faster)')
plt.xlabel('Episode')
plt.ylabel('Total Reward')
plt.grid(True, alpha=0.3)
plt.show()
```

---

### Cell 7 — Markdown: Part 3 — Maze2D

```markdown
## Part 3: Maze 2D — Q-Table Visualization

Now we move to a 2D maze — same grid as Rein Room Maze2D.
The agent starts at **S** (top-left) and must reach **G** (bottom-right).

The agent learns using **Q-learning**: it builds a Q-table that stores
how good each action (Up/Down/Left/Right) is from each cell.

### 🔧 Your task:
1. Run the training cell with default parameters.
2. Run the Q-table visualization cell.
3. Can you trace a path from **S** to **G** just by following the arrows?
```

---

### Cell 8 — Maze2D Q-learning (students change only three parameters)

```python
# ============================================================
# 🔧 CHANGE THESE VALUES and re-run
alpha   = 0.5    # learning rate   — try: 0.1 / 0.5 / 0.8
gamma   = 0.95   # discount factor — try: 0.5 / 0.95 / 0.99
epsilon = 0.2    # exploration     — try: 0.05 / 0.2 / 0.5
n_episodes = 2000
# ============================================================

env = Maze2DEnv()
Q = np.zeros([env.observation_space.n, env.action_space.n])
episode_rewards = []
episode_lengths = []

for ep in range(n_episodes):
    state, _ = env.reset()
    total_reward, steps, done = 0, 0, False
    while not done:
        if np.random.random() < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(Q[state])
        next_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        Q[state, action] += alpha * (reward + gamma * np.max(Q[next_state]) - Q[state, action])
        state = next_state
        total_reward += reward
        steps += 1
    episode_rewards.append(total_reward)
    episode_lengths.append(steps)

# --- Plot ---
window = 100
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4))

smoothed_r = np.convolve(episode_rewards, np.ones(window)/window, mode='valid')
ax1.plot(smoothed_r, color='steelblue', linewidth=2)
ax1.set_title(f'Maze2D Reward  |  α={alpha}  γ={gamma}  ε={epsilon}')
ax1.set_xlabel('Episode')
ax1.set_ylabel('Total Reward')
ax1.grid(True, alpha=0.3)

smoothed_l = np.convolve(episode_lengths, np.ones(window)/window, mode='valid')
ax2.plot(smoothed_l, color='coral', linewidth=2)
ax2.set_title('Steps per Episode (fewer = better path)')
ax2.set_xlabel('Episode')
ax2.set_ylabel('Steps')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
print(f"Success rate (last 500 episodes): {np.mean(episode_rewards[-500:]):.1%}")
```

---

### Cell 9 — Markdown: Q-table visualization

```markdown
## Q-Table Visualization

The Q-table stores a value for every (state, action) pair.
- **High value** → the agent thinks this action is good from this state
- **Arrow** → the action the agent currently prefers in each cell
- **Color intensity** → how confident the agent is

### 🔧 Your task:
Look at the heatmap. Can you trace a path from **S** to **G** just by following the arrows?
```

---

### Cell 10 — Maze2D Q-table heatmap

```python
grid_size = env.grid_size   # e.g. 5 for 5×5
action_symbols = ['↑', '↓', '←', '→']
best_actions = np.argmax(Q, axis=1).reshape(grid_size, grid_size)
max_Q_vals   = np.max(Q, axis=1).reshape(grid_size, grid_size)
best_arrows  = np.vectorize(lambda x: action_symbols[x])(best_actions)

fig, ax = plt.subplots(figsize=(7, 6))
mask = (max_Q_vals == 0)
sns.heatmap(max_Q_vals, annot=best_arrows, fmt='', cmap='YlOrRd',
            linewidths=1, ax=ax, mask=mask,
            cbar_kws={'label': 'Max Q-value (confidence)'})

# Mark Start and Goal
start_r, start_c = 0, 0
goal_r,  goal_c  = grid_size - 1, grid_size - 1
ax.text(start_c + 0.5, start_r + 0.5, 'S', ha='center', va='center',
        fontsize=14, fontweight='bold', color='navy')
ax.text(goal_c  + 0.5, goal_r  + 0.5, 'G', ha='center', va='center',
        fontsize=14, fontweight='bold', color='darkgreen')

ax.set_title('Maze2D Q-Table: Best Action per Cell\n(arrow = preferred direction, color = confidence)')
ax.set_xlabel('Column')
ax.set_ylabel('Row')
plt.tight_layout()
plt.show()
```

---

## RL_Day2_RR.ipynb

---

### Cell 1 — Installation and imports

```python
import subprocess, sys

subprocess.run(["wget", "-q", "-O", "rr_envs.py",
    "https://raw.githubusercontent.com/<YOUR_REPO>/main/rr_envs.py"])

subprocess.run([sys.executable, "-m", "pip", "install",
    "gymnasium", "matplotlib", "numpy", "--quiet"])

import numpy as np
import matplotlib.pyplot as plt
from rr_envs import HeliEnv, FighterEnv

print("✅ Setup complete!")
```

---

### Cell 2 — Markdown: Today's goal

```markdown
## Today's Goal

Two more environments — the same games as in Rein Room:
1. **Heli** — watch the reward curve and identify when the agent starts improving *(main task)*
2. **Fighter** — free exploration *(optional)*

Same as yesterday: you only need to change the 🔧 values.
```

---

### Cell 3 — Markdown: Part 1 — Heli

```markdown
## Part 1: Heli — Training Curve Analysis

The helicopter must fly through gaps. Each episode starts fresh.
The agent uses Q-learning to learn which actions keep it flying longer.

### 🔧 Your task:
1. Run the cell below with default parameters.
2. Watch the reward curve for at least **50 episodes**.
3. Describe the curve shape in one sentence.
   - Is it going up? Flat? Noisy?
   - When does improvement start?
```

---

### Cell 4 — Heli Q-learning (students change only three parameters)

```python
# ============================================================
# 🔧 CHANGE THESE VALUES and re-run
alpha     = 0.5    # learning rate   — try: 0.2 / 0.5 / 0.8
gamma     = 0.95   # discount factor — try: 0.9 / 0.95 / 0.99
epsilon   = 0.3    # exploration     — try: 0.1 / 0.3 / 0.5
n_episodes = 200
# ============================================================

env = HeliEnv()
Q = {}
get_q  = lambda s, a: Q.get((s, a), 0.0)
best_a = lambda s: max(range(env.action_space.n), key=lambda a: get_q(s, a))

episode_rewards = []
episode_lengths = []

for ep in range(n_episodes):
    state, _ = env.reset()
    total_reward, steps, done = 0, 0, False
    while not done:
        action = env.action_space.sample() if np.random.random() < epsilon else best_a(state)
        next_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        old_q      = get_q(state, action)
        next_max_q = max(get_q(next_state, a) for a in range(env.action_space.n))
        Q[(state, action)] = old_q + alpha * (reward + gamma * next_max_q - old_q)
        state = next_state
        total_reward += reward
        steps += 1
    episode_rewards.append(total_reward)
    episode_lengths.append(steps)

# --- Plot ---
window = 10
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4))

smoothed_r = np.convolve(episode_rewards, np.ones(window)/window, mode='valid')
ax1.plot(smoothed_r, linewidth=2)
ax1.set_title(f'Heli Reward  |  α={alpha}  γ={gamma}  ε={epsilon}')
ax1.set_xlabel('Episode')
ax1.set_ylabel('Total Reward')
ax1.grid(True, alpha=0.3)

smoothed_l = np.convolve(episode_lengths, np.ones(window)/window, mode='valid')
ax2.plot(smoothed_l, color='orange', linewidth=2)
ax2.set_title('Steps per Episode (more = flew longer)')
ax2.set_xlabel('Episode')
ax2.set_ylabel('Steps')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
print(f"Average reward (last 20 episodes): {np.mean(episode_rewards[-20:]):.2f}")
```

---

### Cell 5 — Markdown: Part 2 — Fighter (optional)

```markdown
## Part 2: Fighter — Free Exploration  *(Optional)*

This is a fighting game environment. Try any parameter combinations you like.
There's no specific task — just explore and observe.

### 🔧 Try anything:
- High ε: the agent acts randomly → what happens?
- Low ε: the agent exploits what it knows → does it improve?
```

---

### Cell 6 — Fighter (free exploration)

```python
# ============================================================
# 🔧 Try any values!
alpha   = 0.5
gamma   = 0.95
epsilon = 0.3
n_episodes = 100
# ============================================================

env = FighterEnv()
Q = {}
get_q  = lambda s, a: Q.get((s, a), 0.0)
best_a = lambda s: max(range(env.action_space.n), key=lambda a: get_q(s, a))

episode_rewards = []
for ep in range(n_episodes):
    state, _ = env.reset()
    total_reward, done = 0, False
    while not done:
        action = env.action_space.sample() if np.random.random() < epsilon else best_a(state)
        next_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        old_q      = get_q(state, action)
        next_max_q = max(get_q(next_state, a) for a in range(env.action_space.n))
        Q[(state, action)] = old_q + alpha * (reward + gamma * next_max_q - old_q)
        state = next_state
        total_reward += reward
    episode_rewards.append(total_reward)

window = 10
smoothed = np.convolve(episode_rewards, np.ones(window)/window, mode='valid')
plt.figure(figsize=(10, 4))
plt.plot(smoothed, linewidth=2, color='mediumpurple')
plt.title(f'Fighter  |  α={alpha}  γ={gamma}  ε={epsilon}')
plt.xlabel('Episode')
plt.ylabel('Total Reward')
plt.grid(True, alpha=0.3)
plt.show()
```

---

## Notes

- The reward functions of all `rr_envs.py` environments are aligned with the RR platform source code, ensuring that the learning behavior of the two groups is comparable.
- **FrozenLake and CartPole do not appear in these two notebooks** — the custom rr_envs.py environments are used throughout.
- Replace `<YOUR_REPO>` with the actual repo path after pushing to GitHub.
- After pushing the two notebooks, obtain stable Colab open links (`colab.research.google.com/github/...`).
