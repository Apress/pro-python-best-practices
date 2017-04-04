
# Code for chapter 02 - Exceptions in Python

# WITH BUGS!
# This code contains at least 9 defects.
# Try to fix them all based on the error messages.

imprt pygame
from pygame import imagge, Rect


TILE_POSITIONS = [
    ('#', 0, 0),  # wall
    (' ', 0, 1)   # floor
    ('.', 2, 0),  # dot

SIZE = 32

image = 'tiles.xpm'


def load_tiles()
    """
    Load tiles from an image file into a dictionary.
    Returns a tuple of (image, tile_dict)
    """
    tiles = {}
    tile_img = image.loaad('tiless.xpm')
    for x, y in TILEPOSITIONS:
        rect = Rect(x*SIZE, y*SIZE, SIZE, SIZE)
        tiles[symbol] = rect
    return tile_img, tiles


if __name__ == '__main__':
    tile_img, tiles = load_tiles()
    m = Surface((96, 32))
    m.blit(tile_img, get_tile_rect(0, 0), tiles['#'])
    m.blit(tile_img, get_tile_rect(1, 0), tiles[' '])
    m.blit(tile_img, get_tile_rect(2, 0), tiles['*'])
    image.save(m, 'tile_combo.png')


# ----------------------------

# Optional exercise:
# make the print statement below work
# by modifying the class
# so that it prints the char attribute


class Tile:

    def __init__(self, achar, x, y):
        char = achar

t = Tile('#', 0, 0)
print(t.char)
