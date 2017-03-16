
"""

"""

import pygame
from pygame import image, Rect
from pygame.locals import KEYDOWN
from collections import namedtuple
from part1 import draw_grid
from chapter08_load_tile_positions import load_tile_positions
from chapter08_load_tile_positions import TILE_POSITION_FILE, TILE_IMAGE_FILE, SIZE
from chapter09_event_loop_with_mediator import event_loop, exit_game
from util import create_display


Position = namedtuple('Position', ['x', 'y'])
TileSet = namedtuple('TileSet', ['image', 'positions'])

LEFT = Position(-1, 0)
RIGHT = Position(1, 0)
UP = Position(0, -1)
DOWN = Position(0, 1)

def get_tile_rect(position):
    """Converts tile indices to a pygame.Rect"""
    return Rect(position.x*SIZE, position.y*SIZE, SIZE, SIZE)


maze = [ # convert to nested list.
    "#####",
    "#...#",
    "#..x#",
    "#####"
    ]


player = {
    'maze': maze,
    'position': Position(1, 1),
    'tile': "*",
    'move_keys': {276: LEFT, 275: RIGHT,  273: UP, 274: DOWN}
    }


ghost = {
    'maze': maze,
    'position': Position(3, 1),
    'tile': "g",
    }


def draw_sprite(sprite, img, tiles):
        """Draws sprite on a grid"""
        rect = get_tile_rect(sprite['position'])
        symbol = sprite['tile']
        img.blit(tiles.image, rect, tiles.positions[symbol])


def draw(maze, sprites, display, tiles):
    img = draw_grid(maze, tiles.image, tiles.positions)
    for s in sprites:
        draw_sprite(s, img, tiles)
    display.blit(img, Rect((0, 0, 384, 224)), Rect((0, 0, 384, 224)))
    pygame.display.update()


def wait_for_key(event):
    exit_game()


if __name__ == '__main__':
    display = create_display((800, 600))
    tile_image = image.load(TILE_IMAGE_FILE)
    tile_positions = load_tile_positions(TILE_POSITION_FILE)
    tiles = TileSet(tile_image, tile_positions)
    sprites = [player, ghost]
    draw(maze, sprites, display, tiles)
    event_loop({KEYDOWN: wait_for_key})

