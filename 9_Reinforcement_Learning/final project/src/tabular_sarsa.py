from collections import defaultdict
from typing import Tuple

import numpy as np

from .env_wrappers import reset_env, step_env


def obs_to_state(obs) -> bytes:
    """Convert an observation to a hashable state key."""
    arr = np.asarray(obs, dtype=np.float32).flatten()
    return arr.tobytes()


def epsilon_greedy(q_table, state, n_actions: int, epsilon: float) -> int:
    if np.random.rand() < epsilon:
        return int(np.random.randint(n_actions))
    return int(np.argmax(q_table[state]))


def train_sarsa(
    env,
    episodes: int = 500,
    alpha: float = 0.1,
    gamma: float = 0.95,
    epsilon: float = 1.0,
    epsilon_min: float = 0.05,
    epsilon_decay: float = 0.995,
    max_steps: int = 200,
    role: str = "defender",
):
    """Tabular SARSA training (on-policy)."""
    n_actions = env.action_space.n
    q_table = defaultdict(lambda: np.zeros(n_actions, dtype=np.float32))
    rewards = []
    epsilons = []

    for _ in range(episodes):
        epsilons.append(epsilon)
        obs, _ = reset_env(env, role=role)
        state = obs_to_state(obs)
        action = epsilon_greedy(q_table, state, n_actions, epsilon)

        total_reward = 0.0
        for _ in range(max_steps):
            next_obs, reward, done, _ = step_env(env, action, role=role)
            total_reward += reward
            next_state = obs_to_state(next_obs)
            next_action = epsilon_greedy(q_table, next_state, n_actions, epsilon)

            td_target = reward + (0.0 if done else gamma * q_table[next_state][next_action])
            td_error = td_target - q_table[state][action]
            q_table[state][action] += alpha * td_error

            state, action = next_state, next_action
            if done:
                break

        rewards.append(total_reward)
        epsilon = max(epsilon_min, epsilon * epsilon_decay)

    return q_table, rewards, epsilons


def evaluate_sarsa(
    env,
    q_table,
    episodes: int = 20,
    max_steps: int = 200,
    role: str = "defender",
) -> Tuple[float, list]:
    n_actions = env.action_space.n
    rewards = []

    for _ in range(episodes):
        obs, _ = reset_env(env, role=role)
        state = obs_to_state(obs)
        total_reward = 0.0

        for _ in range(max_steps):
            action = int(np.argmax(q_table[state])) if state in q_table else int(np.random.randint(n_actions))
            next_obs, reward, done, _ = step_env(env, action, role=role)
            total_reward += reward
            state = obs_to_state(next_obs)
            if done:
                break

        rewards.append(total_reward)

    return float(np.mean(rewards)), rewards
