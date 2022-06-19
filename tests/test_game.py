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
    assert state.shape == (WORLD_SIZE, WORLD_SIZE, 5)

    # Assert pacman exists in state
    assert state[game.pacman.x // BLOCK_SIZE, game.pacman.y // BLOCK_SIZE, 2] == 1

    # Assert ghosts exist in state
    for g in game.ghosts:
        assert state[g.x // BLOCK_SIZE, g.y // BLOCK_SIZE, 3] == 1


def test_world_is_xy():
    game = PacmanGame()
    state = game.get_state()

    assert state[0, 3, 0] == 0  # no wall (=) at x=0, y=3
    assert state[3, 0, 0] == 1  # wall (=) at x=3, y=0


def test_moves_right_in_state_after_20_steps():
    game = PacmanGame()
    old_x, old_y = game.pacman.x, game.pacman.y
    old_state = game.get_state()

    # Act
    for _ in range(int(BLOCK_SIZE/2)):
        game.step(ACTIONS["RIGHT"])
        game.update()
    state = game.get_state()

    # Assert
    assert old_x // BLOCK_SIZE == 1
    assert old_y // BLOCK_SIZE == 1
    assert old_state[old_x // BLOCK_SIZE, old_y // BLOCK_SIZE, 2] == 1
    assert old_state[game.pacman.x // BLOCK_SIZE, game.pacman.y // BLOCK_SIZE, 2] == 0

    assert game.pacman.x // BLOCK_SIZE == 2
    assert game.pacman.y // BLOCK_SIZE == 1
    assert state[old_x // BLOCK_SIZE, old_y // BLOCK_SIZE, 2] == 0
    assert state[game.pacman.x // BLOCK_SIZE, game.pacman.y // BLOCK_SIZE, 2] == 1
