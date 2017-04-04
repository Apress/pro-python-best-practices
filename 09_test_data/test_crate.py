
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

@pytest.mark.parametrize('direction, pos, tile', [
    (LEFT,  (3, 2), '*'),
    (LEFT,  (3, 1), 'o'),
    (RIGHT, (3, 4), '*'),
    (RIGHT, (3, 5), 'o'),
    (UP,    (2, 3), '*'),
    (UP,    (1, 3), 'o'),
    (DOWN,  (4, 3), '*'),
    (DOWN,  (5, 3), 'o'),
    (DOWN,  (3, 3), ' '),
])
def test_move_crate(direction, pos, tile):
    """Move a crate and check a given tile"""
    maze = parse_grid(LEVEL)
    move(maze, direction)
    assert maze[pos[0]][pos[1]] == tile


def test_push_crate_to_wall():
    maze = parse_grid("*o#")
    move(maze, RIGHT)
    assert maze[0] == ['*', 'o', '#']


def test_push_crate_to_crate():
    maze = parse_grid("*oo")
    move(maze, RIGHT)
    assert maze == [['*', 'o', 'o']]


def test_push_crate_to_exit():
    maze = parse_grid("*ox")
    with pytest.raises(NotImplementedError):
        move(maze, RIGHT)


@pytest.fixture
def bf_crate():
    """A single crate that can be pushed back and forth"""
    maze = parse_grid(""".*o..\n.....""")
    return maze


def test_move_left_right(bf_crate):
    for d in [DOWN, RIGHT, RIGHT, UP, LEFT, DOWN, LEFT, LEFT, UP, RIGHT]:
        move(bf_crate, d)
    assert bf_crate[0][2] == 'o'

def test_move_right_left(bf_crate):
    for d in [RIGHT, DOWN, RIGHT, RIGHT, UP, LEFT]:
        move(bf_crate, d)
    assert bf_crate[0][2] == 'o'

def test_move_lrrl(bf_crate):
    for d in [DOWN, RIGHT, RIGHT, UP, LEFT, DOWN, LEFT, LEFT, UP,
              RIGHT, RIGHT, DOWN, RIGHT, RIGHT, UP, LEFT]:
        move(bf_crate, d)
    assert bf_crate[0][2] == 'o'


SMALL_MAZE = """
#####
#...#
#*o.#
#...#
#####"""

PATHS = [
    (UP, RIGHT, RIGHT, DOWN),
    (UP, RIGHT, DOWN, RIGHT),
    (DOWN, RIGHT, UP, RIGHT),
    pytest.mark.xfail((RIGHT, RIGHT))
]

@pytest.mark.parametrize('path', PATHS)
def test_paths(path):
    """Different paths to the same spot"""
    maze = parse_grid(SMALL_MAZE)
    for direction in path:
        move(maze, direction)
    assert maze[2][3] == '*'
