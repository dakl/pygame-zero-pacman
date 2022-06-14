from pacman.game import ACTIONS, PacmanGame
from pacman.settings import BLOCK_SIZE, WORLD_SIZE


def test_pacman_can_move_right_on_level_1():
    game = PacmanGame()
    old_x, old_y = game.pacman.x, game.pacman.y

    # Act
    game.step(ACTIONS["RIGHT"])
    game.update()

    # Assert
    assert game.pacman.x > old_x and game.pacman.y == old_y


def test_pacman_does_not_move_if_no_step_is_taken():
    game = PacmanGame()
    old_x, old_y = game.pacman.x, game.pacman.y

    # Act
    game.update()

    # Assert
    assert game.pacman.x == old_x and game.pacman.y == old_y


def test_pacman_does_not_move_if_update_is_not_run():
    game = PacmanGame()
    old_x, old_y = game.pacman.x, game.pacman.y

    # Act
    game.step(ACTIONS["RIGHT"])

    # Assert
    assert game.pacman.x == old_x and game.pacman.y == old_y


def test_get_state():
    game = PacmanGame()

    # Act
    state = game.get_state()

    # Assert state shape is (WORLD_SIZE, WORLD_SIZE)
    assert state.shape == (WORLD_SIZE, WORLD_SIZE)

    # Assert pacman exists in state
    assert state[game.pacman.x//BLOCK_SIZE, game.pacman.y//BLOCK_SIZE] == "P"

    # Assert ghosts exist in state
    for g in game.ghosts:
        assert state[g.x//BLOCK_SIZE, g.y//BLOCK_SIZE] == "G"


def test_world_is_xy():
    game = PacmanGame()
    np_world = game.get_state()

    assert np_world[0, 3] != "="
    assert np_world[3, 0] == "="
