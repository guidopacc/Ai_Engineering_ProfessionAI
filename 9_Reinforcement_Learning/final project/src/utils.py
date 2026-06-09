import random
from typing import Callable, Tuple

import numpy as np

from .env_wrappers import reset_env, step_env


def set_seed(seed: int) -> None:
    """Set random seeds for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch

        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    except Exception:
        pass


def moving_average(values, window: int = 50) -> np.ndarray:
    if len(values) == 0:
        return np.array([])
    if len(values) < window:
        return np.array(values, dtype=np.float32)
    weights = np.ones(window, dtype=np.float32) / window
    return np.convolve(np.array(values, dtype=np.float32), weights, mode="valid")


def plot_rewards(rewards, window: int = 50, title: str = "Reward per Episode") -> None:
    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 4))
    plt.plot(rewards, label="Reward", alpha=0.6)
    if len(rewards) >= window:
        ma = moving_average(rewards, window)
        plt.plot(range(window - 1, window - 1 + len(ma)), ma, label=f"MA({window})")
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def run_random_policy(env, episodes: int = 20, max_steps: int = 200, role: str = "defender"):
    """Run a random policy for baseline comparison."""
    rewards = []
    lengths = []
    for _ in range(episodes):
        obs, _ = reset_env(env, role=role)
        total = 0.0
        for t in range(max_steps):
            action = env.action_space.sample()
            obs, reward, done, _ = step_env(env, action, role=role)
            total += reward
            if done:
                break
        rewards.append(total)
        lengths.append(t + 1)
    return float(np.mean(rewards)), float(np.mean(lengths)), rewards, lengths


def evaluate_policy(
    env,
    policy_fn: Callable[[np.ndarray], int],
    episodes: int = 20,
    max_steps: int = 200,
    role: str = "defender",
) -> Tuple[float, list]:
    """Evaluate a deterministic policy function."""
    rewards = []
    for _ in range(episodes):
        obs, _ = reset_env(env, role=role)
        total = 0.0
        for _ in range(max_steps):
            action = policy_fn(obs)
            obs, reward, done, _ = step_env(env, action, role=role)
            total += reward
            if done:
                break
        rewards.append(total)
    return float(np.mean(rewards)), rewards
