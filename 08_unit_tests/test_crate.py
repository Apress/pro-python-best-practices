
from draw_maze import parse_grid
from moves import move
from moves import LEFT, RIGHT, UP, DOWN
import pytest

LEVEL = """#######
#.....#
#..o..#
#.o*o.#
#..o..#
#.....#
#######"""


def move_crate(direction, plr_pos, crate_pos):
    """Helper function for testing crate moves"""
    maze = parse_grid(LEVEL)
    move(maze, direction)
    assert maze[plr_pos[0]][plr_pos[1]] == '*'
    assert maze[crate_pos[0]][crate_pos[1]] == 'o'


def test_move_crate_left():
    move_crate(LEFT, (3, 2), (3, 1))


def test_move_crate_right():
    move_crate(RIGHT, (3, 4), (3, 5))


def test_move_crate_up():
    move_crate(UP, (2, 3), (1, 3))


def test_move_crate_down():
    move_crate(DOWN, (4, 3), (5, 3))


def test_assert_examples():
    maze = parse_grid(LEVEL)
    assert len(maze) <= 7                           # comparison operator
    assert 1 < len(maze) < 10                       # range check
    assert maze[0][0] == '#' and maze[1][1] == '.'  # logical operators
    assert maze[0].count('#') == 7                  # using methods


def test_push_crate_to_wall():
    maze = parse_grid("*o#")
    move(maze, RIGHT)
    assert maze[0] == ['*', 'o', '#']


def test_push_crate_to_crate():
    maze = parse_grid("*oo")
    move(maze, RIGHT)
    assert maze == [['*', 'o', 'o']]


def test_move_to_none():
    """direction=None generates an Exception"""
    maze = parse_grid(LEVEL)
    with pytest.raises(TypeError):
        move(maze, None)
