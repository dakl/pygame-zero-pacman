from random import random
from typing import Tuple
from urllib import request

import numpy as np
import pygame
from pgzero.actor import Actor
from pgzero.screen import Screen

from ghosts import make_ghost_actors
from levels import load_level
from settings import BLOCK_SIZE, HEIGHT, SPEED, WIDTH, WORLD_SIZE, char_to_image

screen = Screen(surface=pygame.Surface((WIDTH, HEIGHT)))
# screen =
pygame.display.set_mode((800, 600))  # change to the real resolution
TEST_MODE = True

# Our sprites
pacman = Actor("pacman_o.png")
pacman.dx = pacman.dy = 0
pacman.level = 1

world = load_level(1, pacman=pacman)

ghosts = make_ghost_actors(world)
ghost_start_pos = [(g.x, g.y) for g in ghosts]

# paw prints: 🐾


def step(action: int):
    """action 0 = left, 1 = right, 2 = up, 3 = down, 4 = stay"""
    if action == 0:
        pacman.dx = -SPEED
    if action == 1:
        pacman.dx = SPEED
    if action == 2:
        pacman.dy = -SPEED
    if action == 3:
        pacman.dy = SPEED


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


ACTIONS = {
    "LEFT": 0,
    "RIGHT": 1,
    "UP": 2,
    "DOWN": 3,
    "STAY": 4,
}


def on_key_down(key):
    if key == keys.LEFT:
        step(ACTIONS["LEFT"])
    if key == keys.RIGHT:
        step(ACTIONS["RIGHT"])
    if key == keys.UP:
        step(ACTIONS["UP"])
    if key == keys.DOWN:
        step(ACTIONS["DOWN"])


def on_key_up(key):
    if key in (keys.LEFT, keys.RIGHT):
        pacman.dx = 0
    if key in (keys.UP, keys.DOWN):
        pacman.dy = 0
    if TEST_MODE:
        # Put special key commands here
        if key == keys.N:
            next_level()


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


def eat_food() -> bool:
    ix, iy = int(pacman.x / BLOCK_SIZE), int(pacman.y / BLOCK_SIZE)
    did_eat_food = False
    if world[iy][ix] == ".":
        world[iy][ix] = None
        pacman.food_left -= 1
        print(f"Ate food. Food left: {pacman.food_left}")
        did_eat_food = True
    return did_eat_food


def reset_sprites(pacman, ghosts, ghost_start_pos):
    pacman.x = pacman.y = 1.5 * BLOCK_SIZE
    pacman.angle = 0
    # Move ghosts back to their start pos
    for g, (x, y) in zip(ghosts, ghost_start_pos):
        g.x = x
        g.y = y


def update(training: bool = False) -> Tuple[int, bool]:
    """Returns tuple (reward, done).
    Reward is 1 if pacman ate food, 0 if it did not, -100 if pacman died."""

    did_move = move_ahead(pacman, is_pacman=True)
    reward, done = 0, False

    if did_move:
        did_eat_food = eat_food()
        if did_eat_food:
            reward = 1

    if pacman.food_left == 0:
        next_level()

    for g in ghosts:
        if g.colliderect(pacman):
            reward, done = -100, True
            if training:
                return reward, done
            else:
                print("YOU LOSE!")
                reset_sprites(pacman, ghosts, ghost_start_pos)

        did_move = move_ahead(g)
        if not did_move:
            if random() < 0.5:
                g.dx = -g.dx
            if random() < 0.5:
                g.dy = -g.dy
            move_ahead(g)

    return reward, done


def next_level():
    global world, ghosts, ghost_start_pos

    pacman.level += 1
    world = load_level(pacman.level, pacman=pacman)
    ghosts = make_ghost_actors(world)
    ghost_start_pos = [(g.x, g.y) for g in ghosts]

    reset_sprites(pacman, ghosts, ghost_start_pos)


def get_state():
    np_world = np.array(world)
    ghost_coords = [(g.x, g.y) for g in ghosts]
    pacman_coords = (pacman.x, pacman.y)
    return np_world, ghost_coords, pacman_coords


if __name__ == "__main__":
    import pgzrun

    pgzrun.go()
