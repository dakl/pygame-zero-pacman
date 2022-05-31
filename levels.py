from settings import BLOCK_SIZE


def load_level(number, pacman):
    world = []
    file = "level-%s.txt" % number
    pacman.food_left = 0

    with open(file) as f:
        for line in f:
            row = []
            for block in line:
                row.append(block)
                if block == ".":
                    pacman.food_left += 1
                elif block == "P":
                    pacman.x = 1.5 * (len(row) - 1) * BLOCK_SIZE
                    pacman.y = 1.5 * len(world) * BLOCK_SIZE
            world.append(row)
    print(f"pacman.food_left = {pacman.food_left}")

    return world
