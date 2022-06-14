from typing import Any, Tuple

import numpy as np
import numpy.typing as npt
from gym import Env, spaces

from pacman.game import PacmanGame
from pacman.settings import BLOCK_SIZE


class PacmanV1(Env):
    def __init__(self):
        super().__init__()

        # Define a 3-D observation space
        self.observation_shape = (BLOCK_SIZE, BLOCK_SIZE, 5)
        self.observation_space = spaces.Box(low=0, high=1, dtype=np.float16)

        # Define an action space ranging from 0 to 4
        self.action_space = spaces.Discrete(5)

        # Create a canvas to render the environment images upon
        self.canvas = np.zeros(self.observation_shape)

        self.game = PacmanGame()

    def reset(self) -> npt.NDArray[np.float64]:
        self.game = PacmanGame()
        return self.game.get_state()

    def step(self, action: int) -> Tuple[Any]:
        if action not in list(range(5)):
            raise ValueError("Action must be in range 0 to 4")
        self.game.step(action)
        reward, done = self.game.update()
        state = self.game.get_state()
        return state, reward, done, []

    def render(self, mode="rgb_array"):
        state = self.game.get_state()
        world = np.full(state.shape[0:2], " ")
        world[state[:, :, 0] == 1] = "█"
        world[state[:, :, 1] == 1] = "·"
        world[state[:, :, 2] == 1] = "P"
        world[state[:, :, 3] == 1] = "G"
        world[state[:, :, 4] == 1] = "*"
        
        for row in world:
            for val in row:
                print(val, end="")
            print()
