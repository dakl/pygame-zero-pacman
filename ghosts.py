import random
from typing import List

from pgzero.actor import Actor

from settings import BLOCK_SIZE, GHOST_SPEED, char_to_image


def make_ghost_actors(world) -> List[Actor]:
    ghosts = []
    for y, row in enumerate(world):
        for x, block in enumerate(row):
            if block == "g" or block == "G":
                g = Actor(
                    char_to_image[block],
                    (x * BLOCK_SIZE, y * BLOCK_SIZE),
                    anchor=("left", "top"),
                )
                g.dx = random.choice([-GHOST_SPEED, GHOST_SPEED])
                g.dy = random.choice([-GHOST_SPEED, GHOST_SPEED])
                ghosts.append(g)
                # Now we have the ghost sprite we don't need this block
                world[y][x] = None

    return ghosts
