import pgzrun
import pygame
from pgzero.screen import Screen
from pgzero.actor import Actor

from pacman.game import ACTIONS, PacmanGame
from pacman.settings import HEIGHT, WIDTH, char_to_image, BLOCK_SIZE

TEST_MODE = True

pygame.display.set_mode((WIDTH, HEIGHT))
screen = Screen(surface=pygame.Surface((WIDTH, HEIGHT)))
game = PacmanGame(screen)

pacman = Actor("pacman_o.png", anchor=('left', 'top'))
ghosts = [
    Actor(
        image=char_to_image[game_g.block],
        anchor=("left", "top"),
    )
    for game_g in game.ghosts
]


def draw():
    screen.clear()
    for y, row in enumerate(game.world):
        for x, block in enumerate(row):
            image = char_to_image.get(block, None)
            if image:
                screen.blit(
                    char_to_image[block],
                    (x * BLOCK_SIZE, y * BLOCK_SIZE),
                )

    pacman.x = game.pacman.x
    pacman.y = game.pacman.y
    pacman.draw()

    for g, game_g in zip(ghosts, game.ghosts):
        g.x = game_g.x
        g.y = game_g.y
        g.draw()


def update():
    game.update()


def on_key_down(key):
    if key == keys.LEFT:
        game.step(ACTIONS["LEFT"])
    if key == keys.RIGHT:
        game.step(ACTIONS["RIGHT"])
    if key == keys.UP:
        game.step(ACTIONS["UP"])
    if key == keys.DOWN:
        game.step(ACTIONS["DOWN"])


def on_key_up(key):
    if key in (keys.LEFT, keys.RIGHT):
        game.pacman.dx = 0
    if key in (keys.UP, keys.DOWN):
        game.pacman.dy = 0
    if TEST_MODE:
        # Put special key commands here
        if key == keys.N:
            game.next_level()


pgzrun.go()
