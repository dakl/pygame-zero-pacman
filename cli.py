from curses import wrapper
import curses
from pacman.agents.heuristic import RandomAgent

from pacman.env import PacmanV1


def main(stdscr):
    env = PacmanV1()
    agent = RandomAgent()

    done = False
    # Initializing the program
    curses.setupterm()
    curses.curs_set(False)

    def display_game(world, reward):
        width, height = world.shape
        stdscr.clear()
        for x in range(0, width):
            for y in range(0, height):
                stdscr.addstr(y + 1, x, str(world[x, y]))

        stdscr.addstr(0, 0, f"total reward {reward}")
        stdscr.refresh()

    total_reward = 0
    steps_taken = 0
    while not done:
        action = agent.act()
        _, reward, done, [] = env.step(action)
        total_reward += reward
        steps_taken += 1
        world = env._get_2d_state()
        display_game(world, total_reward)

    return f"You lost after {steps_taken} steps and got {total_reward} reward."


print(wrapper(main))
