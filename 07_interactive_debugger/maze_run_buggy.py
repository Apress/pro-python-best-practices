
# Code for chapter 07 - Interactive Debugger

# there is defect when integrating this module with the others

from load_tiles import load_tiles
from generate_maze import create_maze
from event_loop import event_loop
from draw_maze import draw_grid, parse_grid
from moves import move, LEFT, RIGHT, UP, DOWN
from pygame import Rect
import pygame


DIRECTIONS = {
    276: LEFT, 275: RIGHT,
    273: UP, 274: DOWN
}


def draw():
    """Displays the maze on the screen"""
    img = draw_grid(maze, tile_img, tiles)
    display.blit(img, Rect((0, 0, 384, 224)), Rect((0, 0, 384, 224)))
    pygame.display.update()


def handle_key(key):
    """Handles key events in the game"""
    move(maze, DIRECTIONS.get(key))
    draw()


if __name__ == '__main__':
    # initialize display
    pygame.init()
    pygame.display.set_mode((800, 600))
    display = pygame.display.get_surface()
    tile_img, tiles = load_tiles()

    # prepare the maze
    maze = parse_grid(create_maze(12, 7))
    maze[1][1] = '*'
    maze[5][10] = 'x'

    # start the game
    draw()
    event_loop(handle_key)
