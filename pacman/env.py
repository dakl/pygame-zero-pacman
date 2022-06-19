from typing import Any, Tuple

import numpy as np
import numpy.typing as npt
from gym import Env, spaces

from pacman.game import PacmanGame
from pacman.settings import WORLD_SIZE


class PacmanV1(Env):
    def __init__(self):
        super().__init__()

        # Define a 3-D observation space
        self.observation_shape = (WORLD_SIZE, WORLD_SIZE, 5)
        self.observation_space = spaces.Box(
            low=np.zeros(self.observation_shape),
            high=np.ones(self.observation_shape),
            dtype=np.int8,
        )

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

    def _get_2d_state(self):
        state = self.game.get_state()
        world = np.full(state.shape[0:2], " ")
        world[state[:, :, 0] == 1] = "█"
        world[state[:, :, 1] == 1] = "·"
        world[state[:, :, 2] == 1] = "P"
        world[state[:, :, 3] == 1] = "G"
        world[state[:, :, 4] == 1] = "*"
        return world

    def render(self):
        print(self)
        print()

    def __str__(self) -> str:
        world = self._get_2d_state()
        s = ""
        for col in world.T:
            for row in col:
                s += row
            s += "\n"
        return s
