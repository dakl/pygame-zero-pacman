import os


WORLD_SIZE = 20
BLOCK_SIZE = 32
WIDTH = WORLD_SIZE * BLOCK_SIZE
HEIGHT = WORLD_SIZE * BLOCK_SIZE
SPEED = 2
GHOST_SPEED = 1
TITLE = "Pac-Man"
TEST_MODE = bool(os.getenv("PACMAN_TEST_MODE", True))
AGENT = os.getenv("PACMAN_AGENT")

char_to_image = {
    ".": "dot.png",
    "=": "wall.png",
    "*": "power.png",
    "g": "ghost1.png",
    "G": "ghost2.png",
}
