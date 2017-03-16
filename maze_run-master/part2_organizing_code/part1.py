
from util import debug_print
from pygame import image, Rect, Surface
from pygame.locals import KEYDOWN
import pygame
import sys
import random

# ------------ CONSTANTS ----------------
TILE_POSITIONS = [
    ('#', 0, 0), # wall
    (' ', 0, 1), # floor
    ('x', 1, 1), # exit
    ('.', 2, 0), # dot
    ('*', 3, 0), # player
    ]


SIZE = 32

LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)

DIRECTIONS = {
    276: LEFT, 275: RIGHT,
    273: UP, 274: DOWN
}

# ------------- LOADING TILES -----------

def get_tile_rect(x, y):
    """Converts tile indices to a pygame.Rect"""
    return Rect(x*SIZE, y*SIZE, SIZE, SIZE)


def load_tiles():
    """Returns a tuple of (image, tile_dict)"""
    tile_image = image.load('../images/tiles.xpm')
    tiles = {}
    for symbol, x, y in TILE_POSITIONS:
        tiles[symbol] = get_tile_rect(x, y)
    return tile_image, tiles


# ------------- GENERATING MAZES ------------

def create_grid_string(dots, xsize, ysize):
    grid = ""
    for y in range(ysize):
        for x in range(xsize):
            grid += "." if (x, y) in dots else "#"
        grid += "\n"
    return grid


def get_all_dot_positions(xsize, ysize):
    return [(x, y) for x in range(1, xsize-1) for y in range(1, ysize-1)]


def get_neighbors(x, y):
    # design flaw: defects are hard to spot in this function
    return [
        (x, y-1), (x, y+1), (x-1, y), (x+1, y),
        (x-1, y-1), (x+1, y-1), (x-1, y+1), (x+1, y+1)
        ]


def generate_dot_positions(xsize, ysize):
    positions = get_all_dot_positions(xsize, ysize)
    dots = set()
    while positions != []:
        x, y = random.choice(positions)
        neighbors = get_neighbors(x, y)
        free = [nb in dots for nb in neighbors]
        if free.count(True) < 5:
            dots.add((x, y))
        positions.remove((x, y))
    return dots


def create_maze(xsize, ysize):
    """Returns a xsize*ysize maze as a string"""
    dots = generate_dot_positions(xsize, ysize)
    maze = create_grid_string(dots, xsize, ysize)
    return maze

# ------------- EVENT LOOP --------------

def event_loop(handle_key, delay=10):
    """Processes events and updates callbacks."""
    while True:
        pygame.event.pump()
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            handle_key(event.key)
        pygame.time.delay(delay)

# ------------- DRAWING GRIDS --------------

def parse_grid(data):
    """Parses the string representation into a nested list"""
    return [list(row) for row in data.strip().split("\n")]


def draw_grid(data, tile_img, tiles):
    """Returns an image of a tile-based grid"""
    debug_print("drawing level", data)
    xsize = len(data[0]) * SIZE
    ysize = len(data) * SIZE
    img = Surface((xsize, ysize))
    for y, row in enumerate(data):
        for x, char in enumerate(row):
            rect = get_tile_rect(x, y)
            img.blit(tile_img, rect, tiles[char])
    return img

# ------------- GAME MECHANICS --------------

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
    if level[newy][newx] != '#':
        level[oldy][oldx] = ' '
        level[newy][newx] = '*'

# ------------- MAIN GAME --------------

def game(key):
    """Handles key events in the game"""
    direction = DIRECTIONS.get(key)
    if direction:
        move(maze, direction)
    img = draw_grid(maze, tile_img, tiles)
    display.blit(img, Rect((0, 0, 384, 224)), Rect((0, 0, 384, 224)))
    pygame.display.update()
    # design flaw: uses global variables 'display', tile_img', 'tiles'


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_mode((800, 600))
    display = pygame.display.get_surface()
    maze = parse_grid(create_maze(12, 7))
    maze[1][1] = '*'
    maze[5][10] = 'x'
    tile_img, tiles = load_tiles()
    img = draw_grid(maze, tile_img, tiles)
    display.blit(img, Rect((0, 0, 384, 224)), Rect((0, 0, 384, 224)))
    pygame.display.update()
    event_loop(game)
