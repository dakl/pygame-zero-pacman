from random import random
import pgzrun
from pgzero.actor import Actor
from ghosts import make_ghost_actors

from levels import load_level
from settings import BLOCK_SIZE, HEIGHT, SPEED, WIDTH, WORLD_SIZE, char_to_image


# Our sprites
pacman = Actor("pacman_o.png")
pacman.dx = pacman.dy = 0
pacman.level = 1

world = load_level(1, pacman=pacman)

ghosts = make_ghost_actors(world)
ghost_start_pos = [(g.x, g.y) for g in ghosts]
print(ghost_start_pos)

# paw prints: 🐾


def draw():
    screen.clear()

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
        pacman.dx = -SPEED
    if key == keys.RIGHT:
        pacman.dx = SPEED
    if key == keys.UP:
        pacman.dy = -SPEED
    if key == keys.DOWN:
        pacman.dy = SPEED


def on_key_up(key):
    if key in (keys.LEFT, keys.RIGHT):
        pacman.dx = 0
    if key in (keys.UP, keys.DOWN):
        pacman.dy = 0


def blocks_ahead_of(actor, dx, dy):
    """Return a list of tiles at this position + (dx,dy)"""

    # Here's where we want to move to, bit of rounding to
    # ensure we get the exact pixel position
    x = int(round(actor.left)) + dx
    y = int(round(actor.top)) + dy

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


def move_ahead(actor, is_pacman: bool = False):
    old_x, old_y = actor.x, actor.y
    # To go in direction (dx, dy) check for no walls
    if "=" not in blocks_ahead_of(actor, actor.dx, 0):
        actor.x += actor.dx
    if "=" not in blocks_ahead_of(actor, 0, actor.dy):
        actor.y += actor.dy
    # Keep actor on the screen
    wrap_around(actor)
    moved = (old_x != actor.x) or (old_y != actor.y)
    if moved and is_pacman:
        if old_x < actor.x and old_y == actor.y:
            actor.angle = 0
        elif old_x > actor.x and old_y == actor.y:
            actor.angle = 180
        elif old_y > actor.y and old_x == actor.x:
            actor.angle = 90
        elif old_y < actor.y and old_x == actor.x:
            actor.angle = 270
    return old_x != actor.x or old_y != actor.y


def eat_food():
    ix, iy = int(pacman.x / BLOCK_SIZE), int(pacman.y / BLOCK_SIZE)
    if world[iy][ix] == ".":
        world[iy][ix] = None
        pacman.food_left -= 1
        if pacman.food_left == 0:
            print("YOU WIN!")
            exit()


def reset_sprites():
    pacman.x = pacman.y = 1.5 * BLOCK_SIZE
    pacman.angle = 0
    # Move ghosts back to their start pos
    for g, (x, y) in zip(ghosts, ghost_start_pos):
        g.x = x
        g.y = y


def update():
    did_move = move_ahead(pacman, is_pacman=True)
    if did_move:
        eat_food()

    for g in ghosts:
        if g.colliderect(pacman):
            print("YOU LOSE!")
            reset_sprites()

        did_move = move_ahead(g)
        if not did_move:
            if random() < 0.5:
                g.dx = -g.dx
            if random() < 0.5:
                g.dy = -g.dy
            move_ahead(g)


pgzrun.go()
