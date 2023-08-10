import gymnasium as gym
import numpy as np
import hive

from gymnasium import spaces
from stable_baselines3.common.env_checker import check_env

class HiveEnv(gym.Env):
    """Hive game Environment that implements StableBaselines3's gym interface."""
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    hivegym = HiveEnv()
    check_env(hivegym)