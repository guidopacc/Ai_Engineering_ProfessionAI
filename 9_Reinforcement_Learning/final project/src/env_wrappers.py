from typing import Tuple

import numpy as np


def _is_sequence(x) -> bool:
    return isinstance(x, (tuple, list))


def extract_obs(obs, obs_space):
    """Return the observation that matches the env observation space."""
    if _is_sequence(obs):
        # If the observation space is a Tuple, return as-is
        if hasattr(obs_space, "spaces"):
            return obs
        for item in obs:
            try:
                if obs_space.contains(item):
                    return item
            except Exception:
                pass
        return obs[0]
    return obs


def flatten_obs(obs) -> np.ndarray:
    return np.asarray(obs, dtype=np.float32).flatten()


def extract_reward(reward, role: str = "defender") -> float:
    if _is_sequence(reward) and len(reward) == 2:
        return float(reward[1] if role == "defender" else reward[0])
    return float(reward)


def reset_env(env, seed: int | None = None, role: str = "defender") -> Tuple[np.ndarray, dict]:
    if seed is None:
        out = env.reset()
    else:
        out = env.reset(seed=seed)
    if _is_sequence(out) and len(out) == 2:
        obs, info = out
    else:
        obs, info = out, {}
    obs = extract_obs(obs, env.observation_space)
    return obs, info


def step_env(env, action, role: str = "defender") -> Tuple[np.ndarray, float, bool, dict]:
    out = env.step(action)
    if len(out) == 5:
        obs, reward, terminated, truncated, info = out
        done = bool(terminated or truncated)
    else:
        obs, reward, done, info = out
    obs = extract_obs(obs, env.observation_space)
    reward = extract_reward(reward, role=role)
    return obs, reward, bool(done), info


def make_env(env_id: str, seed: int | None = None):
    try:
        import gymnasium as gym
    except Exception:
        import gym  # type: ignore

    env = gym.make(env_id)
    if seed is not None:
        reset_env(env, seed=seed)
    return env
