
# Chapter 08 - Organizing code

# Cleaned code for loading tiles

import csv
import os
from pygame.rect import Rect

CONFIG_PATH = os.path.split(__file__)[0]
TILE_POSITION_FILE = os.path.join(CONFIG_PATH, 'tiles.txt')
TILE_IMAGE_FILE = os.path.join(CONFIG_PATH, '../images/tiles.xpm')
SIZE = 32


def load_tile_positions(filename):
    """Returns a dictionary of positions {name: (x, y), ..} parsed from the file"""
    tile_positions = {}
    with open(filename) as f:
        for row in csv.reader(f, delimiter='\t'):
            name = row[0]
            if not name.startswith('REMARK'):
                x = int(row[1])
                y = int(row[2])
                rect = Rect(x*SIZE, y*SIZE, SIZE, SIZE)
                tile_positions[name] = rect
    return tile_positions


if __name__ == '__main__':
    tile_positions = load_tile_positions(TILE_POSITION_FILE)
    print(tile_positions)
