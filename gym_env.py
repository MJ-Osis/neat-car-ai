import gym
from gym import spaces
import numpy as np


class CustomEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, track, car):
        super(CustomEnv, self).__init__()

        self.action_space = spaces.Box(
            low=np.array([0, 0]), high=np.array([3, 3]), dtype=np.float16
        )

        self.observation_space = spaces.Discrete(5)

    def step(self, action):

        self.take_action(action)



    def reset(self, track):
        self.x = track.get_start_x()
        self.y = track.get_start_y()

        self.angle = track.get_start_angle()
        self.vel = 0

        self.frame_iteration = 0
        self.check_time = 0
        self.stag = 0
        self.score = 0

        self.gotten = 1

        return self.next_obs()

    def render(self, mode='human', close=False):
        # Render the environment to the screen
        ...

    def next_obs(self):
