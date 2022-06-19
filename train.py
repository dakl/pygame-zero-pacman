from fire import Fire

from pacman.agents.heuristic import RandomAgent
from pacman.env import PacmanV1


def main():
    env = PacmanV1()
    obs = env.reset()
    done = False
    while not done:
        state, _, done, _ = env.step(env.action_space.sample())

    print(env)
if __name__ == "__main__":
    Fire(main)
