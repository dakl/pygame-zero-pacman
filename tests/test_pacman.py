from pacman.game import ACTIONS, PacmanGame
from pacman.settings import WIDTH


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

    # Assert
    assert len(state) == 3

    # np_world, ghost_coords, pacman_coords
    assert len(state[1]) == len(game.ghosts)
    assert state[2] == (game.pacman.x, game.pacman.y)


def test_world_is_xy():
    game = PacmanGame()
    np_world = game.get_state()[0]

    assert np_world[0, 3] == "."
    assert np_world[3, 0] == "="
