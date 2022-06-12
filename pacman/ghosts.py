import random
from typing import List

from pacman.actor import CustomActor
from pacman.settings import BLOCK_SIZE, GHOST_SPEED


def make_ghost_actors(world) -> List[CustomActor]:
    ghosts = []
    for y, row in enumerate(world):
        for x, block in enumerate(row):
            if block == "g" or block == "G":
                g = CustomActor(
                    x=x * BLOCK_SIZE,
                    y=y * BLOCK_SIZE,
                    width=BLOCK_SIZE,
                    height=BLOCK_SIZE,
                )
                g.dx = random.choice([-GHOST_SPEED, GHOST_SPEED])
                g.dy = random.choice([-GHOST_SPEED, GHOST_SPEED])
                g.block = block
                ghosts.append(g)
                # Now we have the ghost sprite we don't need this block
                world[y][x] = None

    return ghosts
