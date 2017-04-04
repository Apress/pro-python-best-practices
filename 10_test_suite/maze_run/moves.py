from maze_run.load_tiles import load_tiles
from maze_run.generate_maze import create_maze
from maze_run.draw_maze import draw_grid, parse_grid
from pygame import image
import random
import sys


LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)


def get_player_pos(level, player_char='*'):
    """Returns a (x, y) tuple of player char on the level"""
    for y, row in enumerate(level):
        for x, char in enumerate(row):
            if char == player_char:
                return x, y


def move(level, direction):
    """Handles moves on the level"""
    oldx, oldy = get_player_pos(level)
    newx = oldx + direction[0]
    newy = oldy + direction[1]
    if level[newy][newx] == 'x':
        sys.exit(0)
    if level[newy][newx] == 'o':
        cratex = newx + direction[0]
        cratey = newy + direction[1]
        if level[cratey][cratex] in '. ':
            level[cratey][cratex] = 'o'
            level[newy][newx] = ' '
    if level[newy][newx] in '. ':
        level[oldy][oldx] = ' '
        level[newy][newx] = '*'


if __name__ == '__main__':
    tile_img, tiles = load_tiles()
    maze = create_maze(12, 7)
    maze = parse_grid(maze)
    maze[1][1] = '*'
    for i in range(100):
        direction = random.choice([LEFT, RIGHT, UP, DOWN])
        move(maze, direction)
    img = draw_grid(maze, tile_img, tiles)
    image.save(img, 'moved.png')
