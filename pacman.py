import random

import pgzrun
from pgzero.actor import Actor

WORLD_SIZE = 20
BLOCK_SIZE = 32
WIDTH = WORLD_SIZE * BLOCK_SIZE
HEIGHT = WORLD_SIZE * BLOCK_SIZE
SPEED = 2
GHOST_SPEED = 1
TITLE = "Pac-Man"

# Our sprites
pacman = Actor("pacman_o.png", anchor=("left", "top"))
pacman.x = pacman.y = 1 * BLOCK_SIZE
pacman.dx, pacman.dy = 0, 0
ghosts = []

world = []
char_to_image = {
    ".": "dot.png",
    "=": "wall.png",
    "*": "power.png",
    "g": "ghost1.png",
    "G": "ghost2.png",
}


def make_ghost_actors():
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


def load_level(number):
    file = "level-%s.txt" % number
    with open(file) as f:
        for line in f:
            row = []
            for block in line:
                row.append(block)
            world.append(row)


# paw prints: 🐾


def draw():
    for y, row in enumerate(world):
        for x, block in enumerate(row):
            image = char_to_image.get(block, None)
            if image:
                screen.blit(
                    char_to_image[block],
                    (x * BLOCK_SIZE, y * BLOCK_SIZE),
                )
    pacman.draw()

    for g in ghosts:
        g.draw()


def on_key_down(key):
    if key == keys.LEFT:
        pacman.dx = -1
    if key == keys.RIGHT:
        pacman.dx = 1
    if key == keys.UP:
        pacman.dy = -1
    if key == keys.DOWN:
        pacman.dy = 1


def on_key_up(key):
    if key in (keys.LEFT, keys.RIGHT):
        pacman.dx = 0
    if key in (keys.UP, keys.DOWN):
        pacman.dy = 0


def blocks_ahead_of(actor, dx, dy):
    """Return a list of tiles at this position + (dx,dy)"""

    # Here's where we want to move to
    x = actor.x + dx
    y = actor.y + dy

    # Find integer block pos, using floor (so 4.7 becomes 4)
    ix, iy = int(x // BLOCK_SIZE), int(y // BLOCK_SIZE)
    # Remainder let's us check adjacent blocks
    rx, ry = x % BLOCK_SIZE, y % BLOCK_SIZE
    if ix == WORLD_SIZE - 1:
        rx = 0
    if iy == WORLD_SIZE - 1:
        ry = 0

    blocks = [world[iy][ix]]
    if rx:
        blocks.append(world[iy][ix + 1])
    if ry:
        blocks.append(world[iy + 1][ix])
    if rx and ry:
        blocks.append(world[iy + 1][ix + 1])

    return blocks


def wrap_around(actor):
    if actor.x < 0:
        actor.x = WIDTH - BLOCK_SIZE
    if actor.x > WIDTH - BLOCK_SIZE:
        actor.x = 0
    if actor.y < 0:
        actor.y = HEIGHT - BLOCK_SIZE
    if actor.y > HEIGHT - BLOCK_SIZE:
        actor.y = 0


def move_ahead(actor):
    old_x, old_y = actor.x, actor.y
    # To go in direction (dx, dy) check for no walls
    if "=" not in blocks_ahead_of(actor, actor.dx, 0):
        actor.x += actor.dx
    if "=" not in blocks_ahead_of(actor, 0, actor.dy):
        actor.y += actor.dy
    # Keep actor on the screen
    wrap_around(actor)
    return old_x != actor.x or old_y != actor.y


def update():
    move_ahead(pacman)
    # for g in ghosts:
    #     did_move = move_ahead(g)
    #     if not did_move:
    #         if random.random() < 0.5:
    #             g.dx = -g.dx
    #         if random.random() < 0.5:
    #             g.dy = -g.dy
    #         move_ahead(g)


load_level(1)
make_ghost_actors()

pgzrun.go()
