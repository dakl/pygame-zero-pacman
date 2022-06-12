from random import random
from typing import Tuple

import numpy as np
from pacman.actor import CustomActor

from pacman.ghosts import make_ghost_actors
from pacman.levels import load_level
from pacman.settings import BLOCK_SIZE, HEIGHT, SPEED, WIDTH, WORLD_SIZE

TEST_MODE = True
# paw prints: 🐾

ACTIONS = {
    "LEFT": 0,
    "RIGHT": 1,
    "UP": 2,
    "DOWN": 3,
    "STAY": 4,
}


class PacmanGame:
    def __init__(self, screen) -> None:
        self.pacman = CustomActor(
            x=None,
            y=None,
            width=BLOCK_SIZE,
            height=BLOCK_SIZE,
        )
        self.pacman.dx = self.pacman.dy = 0
        self.pacman.level = 1

        self.world = load_level(1, self.pacman)

        self.ghosts = make_ghost_actors(self.world)
        self.ghost_start_pos = [(g.x, g.y) for g in self.ghosts]

    def step(self, action: int) -> None:
        """action 0 = left, 1 = right, 2 = up, 3 = down, 4 = stay"""
        if action == 0:
            self.pacman.dx = -SPEED
        if action == 1:
            self.pacman.dx = SPEED
        if action == 2:
            self.pacman.dy = -SPEED
        if action == 3:
            self.pacman.dy = SPEED

    def blocks_ahead_of(self, actor, dx, dy):
        """Return a list of tiles at this position + (dx,dy)"""

        # Here's where we want to move to, bit of rounding to
        # ensure we get the exact pixel position
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
        blocks = [self.world[iy][ix]]
        if rx:
            blocks.append(self.world[iy][ix + 1])
        if ry:
            blocks.append(self.world[iy + 1][ix])
        if rx and ry:
            blocks.append(self.world[iy + 1][ix + 1])

        return blocks

    def wrap_around(self, actor):
        if actor.x < 0:
            actor.x = WIDTH - BLOCK_SIZE
        if actor.x > WIDTH - BLOCK_SIZE:
            actor.x = 0
        if actor.y < 0:
            actor.y = HEIGHT - BLOCK_SIZE
        if actor.y > HEIGHT - BLOCK_SIZE:
            actor.y = 0

    def move_ahead(self, actor, is_pacman: bool = False):
        old_x, old_y = actor.x, actor.y
        # To go in direction (dx, dy) check for no walls
        if "=" not in self.blocks_ahead_of(actor, actor.dx, 0):
            actor.x += actor.dx
        if "=" not in self.blocks_ahead_of(actor, 0, actor.dy):
            actor.y += actor.dy

        # Keep actor on the screen
        self.wrap_around(actor)
        moved = (old_x != actor.x) or (old_y != actor.y)
        if moved and is_pacman:
            print("moved")
            if old_x < actor.x and old_y == actor.y:
                actor.angle = 0
            elif old_x > actor.x and old_y == actor.y:
                actor.angle = 180
            elif old_y > actor.y and old_x == actor.x:
                actor.angle = 90
            elif old_y < actor.y and old_x == actor.x:
                actor.angle = 270
        return old_x != actor.x or old_y != actor.y

    def eat_food(self) -> bool:
        ix = int(self.pacman.x / BLOCK_SIZE)
        iy = int(self.pacman.y / BLOCK_SIZE)
        did_eat_food = False
        if self.world[iy][ix] == ".":
            self.world[iy][ix] = None
            self.pacman.food_left -= 1
            print(f"Ate food. Food left: {self.pacman.food_left}")
            did_eat_food = True
        return did_eat_food

    def reset_sprites(self):
        self.pacman.x = self.pacman.y = BLOCK_SIZE
        self.pacman.angle = 0
        # Move ghosts back to their start pos
        for g, (x, y) in zip(self.ghosts, self.ghost_start_pos):
            g.x = x
            g.y = y

    def update(self, training: bool = False) -> Tuple[int, bool]:
        """Returns tuple (reward, done).
        Reward is
            1 if pacman ate food,
            0 if it did not,
            -100 if pacman died."""

        did_move = self.move_ahead(self.pacman, is_pacman=True)
        reward, done = 0, False

        if did_move:
            did_eat_food = self.eat_food()
            if did_eat_food:
                reward = 1

        if self.pacman.food_left == 0:
            self.next_level()

        for g in self.ghosts:
            if g.colliderect(self.pacman):
                reward, done = -100, True
                if training:
                    return reward, done
                else:
                    print("YOU LOSE!")
                    self.reset_sprites()

            did_move = self.move_ahead(g)
            if not did_move:
                if random() < 0.5:
                    g.dx = -g.dx
                if random() < 0.5:
                    g.dy = -g.dy
                self.move_ahead(g)

        return reward, done

    def next_level(self):
        self.pacman.level += 1
        self.world = load_level(self.pacman.level, pacman=self.pacman)
        self.ghosts = make_ghost_actors(self.world)
        self.ghost_start_pos = [(g.x, g.y) for g in self.ghosts]
        self.reset_sprites()

    def get_state(self):
        np_world = np.array(self.world)
        ghost_coords = [(g.x, g.y) for g in self.ghosts]
        pacman_coords = (self.pacman.x, self.pacman.y)
        return np_world, ghost_coords, pacman_coords
