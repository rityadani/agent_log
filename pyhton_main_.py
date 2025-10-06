
# gridworld_qlearning.py
# Simple 4x4 GridWorld with terminal at (3,3). Q-learning demo.
import random, csv, math, time
from collections import defaultdict

GRID_SIZE = 4
ACTIONS = [(0,1),(0,-1),(1,0),(-1,0)]  # right,left,down,up
ACTION_NAMES = ["R","L","D","U"]
EPISODES = 500
MAX_STEPS = 50
ALPHA = 0.7
GAMMA = 0.98
EPS_START = 1.0
EPS_END = 0.05
EPS_DECAY = 0.995

def is_terminal(s):
    return s == (GRID_SIZE-1, GRID_SIZE-1)

def step(state, action):
    x,y = state
    dx,dy = action
    nx = min(max(x+dx,0), GRID_SIZE-1)
    ny = min(max(y+dy,0), GRID_SIZE-1)
    new_state = (nx,ny)
    # reward: -1 per step, +10 at goal
    if is_terminal(new_state):
        return new_state, 10.0, True
    return new_state, -1.0, False

def choose_action(Q, state, eps):
    if random.random() < eps:
        return random.randrange(len(ACTIONS))
    qs = [Q[(state,a)] for a in range(len(ACTIONS))]
    maxq = max(qs)
    # tie-breaker random
    candidates = [i for i,q in enumerate(qs) if q==maxq]
    return random.choice(candidates)

def train():
    Q = defaultdict(float)
    eps = EPS_START
    stats = []
    for ep in range(1, EPISODES+1):
        state = (0,0)
        total_reward = 0
        for step_i in range(MAX_STEPS):
            a_idx = choose_action(Q, state, eps)
            action = ACTIONS[a_idx]
            new_state, reward, done = step(state, action)
            total_reward += reward
            # Q-learning update
            old = Q[(state,a_idx)]
            future_qs = [Q[(new_state,aa)] for aa in range(len(ACTIONS))]
            Q[(state,a_idx)] = old + ALPHA * (reward + GAMMA*max(future_qs) - old)
            state = new_state
            if done:
                break
        eps = max(EPS_END, eps * EPS_DECAY)
        stats.append((ep, total_reward, step_i+1, eps))
        if ep % 50 == 0:
            print(f"Episode {ep:4d}  reward={total_reward:6.1f}  steps={step_i+1}  eps={eps:.3f}")
    return Q, stats

def extract_policy(Q):
    policy = {}
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            s = (x,y)
            if is_terminal(s):
                policy[s] = "G"
            else:
                qs = [Q[(s,a)] for a in range(len(ACTIONS))]
                policy[s] = ACTION_NAMES[qs.index(max(qs))]
    return policy

def save_stats_csv(stats, path="grid_stats.csv"):
    with open(path,"w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["episode","total_reward","steps","eps"])
        w.writerows(stats)
    print("Saved stats to", path)

if __name__ == "__main__":
    random.seed(0)
    Q, stats = train()
    policy = extract_policy(Q)
    print("\nLearned policy (grid coordinates):")
    for i in range(GRID_SIZE):
        row = []
        for j in range(GRID_SIZE):
            row.append(policy[(i,j)])
        print(" ".join(row))
    save_stats_csv(stats)
