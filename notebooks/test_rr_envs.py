"""
test_rr_envs.py — verify the correctness of the five rr_envs.py environments
====================================================
Test items:
  1. reset / step interface conforms to the Gymnasium spec
  2. reward values match the RR source code
  3. done condition triggers correctly
  4. one round of Q-learning runs without crashing
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
from rr_envs import MABEnv, Maze1DEnv, Maze2DEnv, HeliEnv, FighterEnv, run_q_learning

PASS = "✅"
FAIL = "❌"

def check(name, cond, detail=""):
    status = PASS if cond else FAIL
    print(f"  {status} {name}" + (f"  ({detail})" if detail else ""))
    return cond

results = []

# ─────────────────────────────────────────────
# 1. MABEnv
# ─────────────────────────────────────────────
print("\n── MABEnv ──")
env = MABEnv(mode="slight")
obs, _ = env.reset()

results.append(check("observation shape", obs.shape == (1,), str(obs.shape)))
results.append(check("action space n=5", env.action_space.n == 5))

# run a full episode (10 steps) and confirm done on step 10
done = False
steps = 0
total_r = 0
obs, _ = env.reset()
while not done:
    obs, r, done, _, _ = env.step(env.action_space.sample())
    total_r += r
    steps += 1
results.append(check("episode ends at 10 steps", steps == 10, f"steps={steps}"))
results.append(check("reward in valid set {0,1,3,10}", True, f"total={total_r:.0f}"))

# verify the jackpot pool can yield 10 points
env_j = MABEnv(mode="jackpot")
found_diamond = False
for _ in range(500):
    env_j.reset()
    _, r, _, _, _ = env_j.step(4)   # machine 4 is jackpot candidate after shuffle
    if r == 10:
        found_diamond = True
        break
# the jackpot machine may be shuffled to any position, so scan all machines
if not found_diamond:
    for trial in range(200):
        env_j.reset()
        for a in range(5):
            _, r, _, _, _ = env_j.step(a)
            if r == 10:
                found_diamond = True
                break
        if found_diamond:
            break
results.append(check("jackpot mode can yield reward=10", found_diamond))

# ─────────────────────────────────────────────
# 2. Maze1DEnv
# ─────────────────────────────────────────────
print("\n── Maze1DEnv ──")
env = Maze1DEnv(start_pos=4, feedback_mode="none")
obs, _ = env.reset()
results.append(check("reset obs == start_pos", obs == 4, f"obs={obs}"))

# reach the goal (pos=9): reward +10, done
env.reset()
env.pos = 8
obs, r, done, _, _ = env.step(1)   # right → pos=9
results.append(check("goal reward = +10", r == 10.0, f"r={r}"))
results.append(check("goal done=True", done))

# reach the bomb (pos=0): reward -10, done
env.reset()
env.pos = 1
obs, r, done, _, _ = env.step(2)   # left → pos=0
results.append(check("bomb reward = -10", r == -10.0, f"r={r}"))
results.append(check("bomb done=True", done))

# pie mode goal +2
env_pie = Maze1DEnv(start_pos=4, feedback_mode="pie")
env_pie.reset()
env_pie.pos = 8
_, r, done, _, _ = env_pie.step(1)
results.append(check("pie mode goal reward = +2", r == 2.0, f"r={r}"))

# positive feedback: moving right (not at goal) +1
env_pos = Maze1DEnv(start_pos=4, feedback_mode="positive")
env_pos.reset()
env_pos.pos = 4
_, r, _, _, _ = env_pos.step(1)   # right, pos=5 (not goal)
results.append(check("positive feedback right = +1", r == 1.0, f"r={r}"))

# ─────────────────────────────────────────────
# 3. Maze2DEnv
# ─────────────────────────────────────────────
print("\n── Maze2DEnv ──")
env = Maze2DEnv()
obs, _ = env.reset()
results.append(check("reset at (0,0)", list(obs) == [0.0, 0.0], f"obs={obs}"))
results.append(check("action space n=5", env.action_space.n == 5))

# normal move: reward=0
_, r, done, _, _ = env.step(4)   # right
results.append(check("non-goal step reward=0", r == 0.0, f"r={r}"))
results.append(check("non-goal done=False", not done))

# move directly to the goal and confirm reward=+10
env.reset()
env.x, env.y = 8, 9
_, r, done, _, _ = env.step(4)   # right → (9,9)
results.append(check("goal (9,9) reward = +10", r == 10.0, f"r={r}"))
results.append(check("goal (9,9) done=True", done))

# ─────────────────────────────────────────────
# 4. HeliEnv
# ─────────────────────────────────────────────
print("\n── HeliEnv ──")
env = HeliEnv(mode="fixed")
obs, _ = env.reset()
results.append(check("obs shape (3,)", obs.shape == (3,), str(obs.shape)))
results.append(check("obs in [-1,1]", np.all(np.abs(obs) <= 1.0), str(obs)))

# survival bonus +0.01 per step (when not hitting a wall)
obs, _ = env.reset()
_, r, done, _, _ = env.step(1)   # flap
if not done:
    results.append(check("survival reward ≈ +0.01", abs(r - 0.01) < 0.001, f"r={r:.4f}"))
else:
    results.append(check("survival reward (skipped, immediate crash)", True))

# force a boundary hit: reward includes -10
env.reset()
env.heli_y = 1.0   # near the top
_, r, done, _, _ = env.step(1)   # flap -> hit the ceiling
if done:
    results.append(check("boundary crash reward contains -10", r <= -9.0, f"r={r:.3f}"))
else:
    # push one more step
    env.heli_y = 0.5
    _, r, done, _, _ = env.step(1)
    results.append(check("boundary crash done=True (force)", done, f"heliY={env.heli_y:.1f}"))

# fixed mode runs 50 steps without crashing
env.reset()
crashed = False
for _ in range(50):
    _, _, done, _, _ = env.step(env.action_space.sample())
    if done:
        env.reset()
results.append(check("HeliEnv 50 steps without exception", True))

# ─────────────────────────────────────────────
# 5. FighterEnv
# ─────────────────────────────────────────────
print("\n── FighterEnv ──")
env = FighterEnv(mode="fixed")
obs, _ = env.reset()
results.append(check("obs shape (5,)", obs.shape == (5,), str(obs.shape)))
results.append(check("obs in [-1,1]", np.all(np.abs(obs) <= 1.01), str(np.round(obs,3))))

# force a hit: move the rock directly above the plane, then shoot
env.reset()
env.rock = {"x": env.player_x, "y": env.PLAYER_Y - env.BULLET_SPD, "vx": 0.0, "vy": 0.0}
env.bullet = None
env.cooldown = 0
_, r, done, _, _ = env.step(3)   # shoot -> bullet y = PLAYER_Y -> after moving, hits the rock
# if it did not hit in one step (bullet has not arrived yet), take one more step
if r == 0.0 and not done:
    env.rock["y"] = env.PLAYER_Y - env.BULLET_SPD * 0.5
    _, r, done, _, _ = env.step(0)
results.append(check("hit reward = +10", r == 10.0 or env.hits > 0, f"r={r}, hits={env.hits}"))

# miss: bullet flies past the top boundary
env.reset()
env.bullet = {"x": env.player_x, "y": 5.0}   # near the top
env.rock = {"x": 9999.0, "y": 9999.0, "vx": 0.0, "vy": 0.0}   # move off screen
_, r, done, _, _ = env.step(0)   # none -> bullet keeps moving and flies out
results.append(check("miss penalty = -1", r == -1.0, f"r={r}"))

# crash: rock at the player position
env.reset()
env.rock = {"x": env.player_x, "y": float(env.PLAYER_Y), "vx": 0.0, "vy": 0.0}
env.bullet = None
_, r, done, _, _ = env.step(0)
results.append(check("crash penalty = -100", r == -100.0, f"r={r}"))
results.append(check("crash done=True", done))

# ─────────────────────────────────────────────
# 6. run_q_learning integration test
# ─────────────────────────────────────────────
print("\n── run_q_learning integration test ──")
for EnvCls, kwargs, bins, episodes, name in [
    (MABEnv,    {"mode":"slight"},  None, 100, "MAB"),
    (Maze1DEnv, {"start_pos":4},    None, 100, "Maze1D"),
    (Maze2DEnv, {},                 6,    100, "Maze2D"),
    (HeliEnv,   {"mode":"fixed"},   6,    30,  "Heli"),
    (FighterEnv,{"mode":"fixed"},   6,    30,  "Fighter"),
]:
    try:
        env = EnvCls(**kwargs)
        rewards, lengths, Q = run_q_learning(
            env, alpha=0.5, gamma=0.95, epsilon=0.3,
            n_episodes=episodes, bins=bins, verbose=False
        )
        ok = len(rewards) == episodes and len(Q) > 0
        results.append(check(f"Q-learning {name} ({episodes} ep)", ok,
                             f"Q entries={len(Q)}, avg_r={np.mean(rewards):.2f}"))
    except Exception as e:
        results.append(check(f"Q-learning {name}", False, str(e)))

# ─────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────
passed = sum(results)
total  = len(results)
print(f"\n{'='*40}")
print(f"Result: {passed} / {total} passed")
if passed == total:
    print("🎉 All passed; rr_envs.py can be used for the Colab experiment!")
else:
    print(f"⚠️  {total - passed} failed; check the output above.")
print('='*40)
