
from maze_run.draw_maze import parse_grid
from maze_run.moves import move
from maze_run.moves import LEFT, RIGHT, UP, DOWN
from fixtures import level
import pytest

CRATE_MOVES = [
    (LEFT,  (3, 2), (3, 1)),
    (RIGHT, (3, 4), (3, 5)),
    (UP,    (2, 3), (1, 3)),
    (DOWN,  (4, 3), (5, 3)),
]


class TestCrateMoves:

    @pytest.mark.parametrize('direction, plr_pos, crate_pos', CRATE_MOVES)
    def test_move_crate(self, level, direction, plr_pos, crate_pos):
        """After move player and crate moved by one square"""
        print(direction, plr_pos, crate_pos)
        move(level, direction)
        assert level[plr_pos[0]][plr_pos[1]] == '*'
        assert level[crate_pos[0]][crate_pos[1]] == 'o'

    def test_push_crate_to_wall(self):
        maze = parse_grid("*o#")
        move(maze, RIGHT)
        assert maze[0] == ['*', 'o', '#']

    def test_push_crate_to_crate(self):
        maze = parse_grid("*oo")
        move(maze, RIGHT)
        assert maze == [['*', 'o', 'o']]

    def test_move_crate_to_corner(self, level):
        """Moves top crate to upper left corner"""
        for d in [UP, RIGHT, UP, LEFT, LEFT, LEFT]:
            move(level, d)
        assert level[1][1] == 'o'

    def test_move_crate_back_forth(self, level):
        """Sanity check: move the top crate twice"""
        for d in [LEFT, UP, RIGHT, UP, RIGHT, RIGHT, DOWN, LEFT, LEFT, LEFT]:
            move(level, d)
        assert level[2] == list('#o*   #')


PATHS = [
    ((UP, LEFT), 2, 2),
    ((LEFT, UP), 2, 2),
    ((RIGHT, UP, LEFT, LEFT), 2, 2),
    pytest.mark.xfail(((DOWN, DOWN), 0, 0)),
    ((LEFT,), 2, 3),
    ((LEFT, RIGHT), 3, 3),
    ((RIGHT, RIGHT), 4, 3),
]


class TestPlayerMoves:

    def test_move_to_none(self, level):
        """direction=None generates an Exception"""
        with pytest.raises(TypeError):
            move(level, None)

    @pytest.mark.parametrize('path, expected_x, expected_y', PATHS)
    def test_move_player(self, level, path, expected_x, expected_y):
        """Player position changes correctly"""
        for direction in path:
            move(level, direction)
        assert level[expected_y][expected_x] == '*'
