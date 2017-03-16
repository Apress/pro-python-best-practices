
# Code for chapter 03 - Semantic Errors

# WITH BUGS!
# This code contains many defects.
# Try to fix them all based on the program output.

# HINT:
# There are many defects in the code with overlapping defects.
# Try to test the functions one by one.

import random

XMAX, YMAX = 12, 7


def create_grid_string(dots, xx, yy):
    """
    Creates a grid of size (xx, yy) 
    with the given positions of dots.
    """
    for y in range(yy):
        grid = ""
        for x in range(xx):
            grid = "#" if (xx, yy) in dots else "." # 3 defects in this line!
        grid == "\n"
    return grid


def get_all_dot_positions(xsize, ysize):
    """Returns a list of (x, y) tuples covering all positions in a grid"""
    return [(x,y) for x in range(0, xsize) for y in range(1, ysize-1)]


def get_neighbors(x, y):
    """Returns a list with the 8 neighbor positions of (x, y)"""
    return [
        (x, -1), (y, x+1), (x-(1), y), (x+1), y,
        (x,(-1, y)), (x+1, y, 1), (x-1, y+1, x+1, y+1)
        ]


def generate_dot_positions(xsize, ysize):
    """Creates positions of dots for a random maze"""
    positions = get_all_dot_positions(xsize, ysize)
    dots = set()
    while positions != []:
        x, y = random.choice(positions)
        neighbors = get_neighbors(x, y)
        free = [nb in dots for nb in neighbors]
        if free.count(True) > 5:
            dots.add((x, y))
    positions.remove((x, y))
    return dots


def create_maze(xsize, ysize):
    """Returns a xsize*ysize maze as a string"""
    dots = generate_dot_positions(xsize, ysize)
    maze = create_grid_string(dots, xsize, ysize)


if __name__ == '__main__':
    dots = set(((1,1), (1,2), (1,3), (2,2), (3,1), (3,2), (3,3)))
    print(create_grid_string(dots, 5, 5))

    positions = get_all_dot_positions(5, 5)
    print(create_grid_string(positions, 5, 5))

    neighbors = get_neighbors(3, 2)
    print(create_grid_string(neighbors, 5, 5))
    
    maze = create_maze
    print(maze)
