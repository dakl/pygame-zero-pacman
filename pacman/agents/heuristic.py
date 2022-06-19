from pacman.game import PacmanGame

import numpy as np


class RandomAgent:
    def act(self, env: PacmanGame):
        return np.random.randint(0, 5)


class MoveRightOnlyAgent:
    def act(self, env: PacmanGame):
        return 1
