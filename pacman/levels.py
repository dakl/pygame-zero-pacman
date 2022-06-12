from pacman.actor import CustomActor
from pacman.settings import BLOCK_SIZE


def load_level(number: int, pacman: CustomActor):
    world = []
    file = "level-%s.txt" % number
    pacman.food_left = 0

    with open(file) as f:
        for line in f:
            if line:
                row = []
                for block in line:
                    if block == "\n":
                        continue
                    row.append(block)
                    if block == ".":
                        pacman.food_left += 1
                    elif block == "P":
                        pacman.x = (len(row) - 1) * BLOCK_SIZE
                        pacman.y = len(world) * BLOCK_SIZE
                world.append(row)

    return world
