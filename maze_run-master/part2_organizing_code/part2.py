
from util import debug_print
from pygame import image, Rect, Surface
from pygame.locals import KEYDOWN, KEYUP, USEREVENT
import pygame
import sys
import random
import json
import os
from collections import namedtuple
from functools import partial
import argparse
import logging

#logging.basicConfig(filename='random_levels.log', level=logging.INFO)

log = logging.getLogger('moves')
log.addHandler(logging.FileHandler('moves.log', mode='w'))
log.setLevel(logging.INFO)

eventlog = logging.getLogger('events')
eventlog.addHandler(logging.StreamHandler(sys.stderr))
#fmt='%(asctime)s %(message)s'
#eventlog.addFormatter(logging.Formatter(fmt), datefmt='%m/%d/%Y %I:%M:%S %p')
eventlog.setLevel(logging.WARNING)


Position = namedtuple("Position", ["x", "y"])

# ------------ CONSTANTS ----------------

CONFIG_PATH = os.path.split(__file__)[0]

TILE_POSITION_FILE = CONFIG_PATH + 'tiles.json'
TILE_IMAGE_FILE = CONFIG_PATH + '../images/tiles.xpm'

SIZE = 32
SPEED = 4


LEFT = Position(-1, 0)
RIGHT = Position(1, 0)
UP = Position(0, -1)
DOWN = Position(0, 1)

DIRECTIONS = {
    276: LEFT, 275: RIGHT,
    273: UP, 274: DOWN
}

KEY_REPEAT_TIME = 250
DRAW_REPEAT_TIME = 100
UPDATE_REPEAT_TIME = 20
MOVE_GHOST_TIME = 500

KEY_REPEATED, DRAW, UPDATE, MOVE_GHOST, EXIT = range(USEREVENT + 1, USEREVENT + 6)
# ------------- LOADING TILES -----------

def get_tile_rect(pos):
    """Converts tile indices to a pygame.Rect"""
    return Rect(pos.x*SIZE, pos.y*SIZE, SIZE, SIZE)

def load_tiles(json_fn):
    """Loads tile positions from a JSON file name"""
    tiles = {}
    jd = json.loads(open(json_fn).read())
    for tile in jd.values():
        abbrev = tile["abbrev"]
        pos = Position(tile["x"], tile["y"])
        rect = get_tile_rect(pos)
        tiles[abbrev] = rect
    return tiles


# ------------- GENERATING MAZES ------------

class MazeGenerator:
    """Generates two-dimensional mazes consisting of walls and dots."""
    
    @staticmethod
    def create_grid_string(dots, xsize, ysize):
        grid = ""
        for y in range(ysize):
            for x in range(xsize):
                grid += "." if Position(x, y) in dots else "#"
            grid += "\n"
        return grid

    @staticmethod
    def get_all_dot_positions(xsize, ysize):
        return [Position(x, y) for x in range(1, xsize-1) for y in range(1, ysize-1)]

    @staticmethod
    def get_neighbors(pos):
        return [
            Position(pos.x  , pos.y-1), Position(pos.x  , pos.y+1), 
            Position(pos.x-1, pos.y  ), Position(pos.x+1, pos.y  ),
            Position(pos.x-1, pos.y-1), Position(pos.x+1, pos.y-1), 
            Position(pos.x-1, pos.y+1), Position(pos.x+1, pos.y+1)
            ]

    @staticmethod
    def generate_dot_positions(xsize, ysize):
        positions = MazeGenerator.get_all_dot_positions(xsize, ysize)
        dots = set()
        while positions != []:
            pos = random.choice(positions)
            neighbors = MazeGenerator.get_neighbors(pos)
            free = [nb in dots for nb in neighbors]
            if free.count(True) < 5:
                dots.add(pos)
            positions.remove(pos)
        return dots

    @staticmethod
    def create_maze(size):
        """Returns a size.x * size.y maze as a string"""
        dots = MazeGenerator.generate_dot_positions(size.x, size.y)
        maze = MazeGenerator.create_grid_string(dots, size.x, size.y)
        return maze

# ------------- DRAWING GRIDS --------------

class TileGrid:

    def __init__(self, data):
        self._grid = self.parse_grid(data)

    def __repr__(self):
        return "\n".join(["".join(row) for row in self._grid])

    def parse_grid(self, data):
        """Parses the string representation into a nested list"""
        return [list(row) for row in data.strip().split("\n")]

    @property
    def rows(self):
        return self._grid
    
    @property
    def xsize(self):
        return len(self.rows[0])

    @property
    def ysize(self):
        return len(self.rows)

    def __getitem__(self, pos):
        return self._grid[pos.y][pos.x]

    def __setitem__(self, pos, value):
        self._grid[pos.y][pos.x] = value

    def __iter__(self):
        """Iterate over all grid tiles"""
        for y, row in enumerate(self.rows):
            for x, char in enumerate(row):
                pos = Position(x, y)
                yield pos, char
        
    def find_tile(self, query='*'):
        """Returns a Position tuple for the given char on the level"""
        for pos, char in self:
            if char == query:
                return pos

    def draw_grid(self, tile_img, tiles):
        """Returns an image of a tile-based grid"""
        #debug_print("drawing level", data)
        img = Surface((self.xsize * SIZE, self.ysize * SIZE))
        for pos, char in self:
            rect = get_tile_rect(pos)
            img.blit(tile_img, rect, tiles[char])
        return img

# ------------- SPRITES --------------

class Sprite:

    def __init__(self, maze, tile, startpos):
        self.maze = maze
        self.tile = tile
        self.pos = startpos
        self.anim_direction = None
        self.anim_offset = Position(0, 0)

    def move(self, direction):
        """Handles moves on a level"""
        if not self.is_moving():
            old = self.pos
            new = Position(old.x + direction.x, old.y + direction.y)
            if self.maze[new] in [" ", ".", "x"]:
                self.pos = new
                self.anim_direction = direction
                self.anim_offset = Position(-direction.x * SIZE, -direction.y * SIZE)

    def is_moving(self):
        return self.anim_direction

    def arrives_on_new_tile(self):
        pass

    def draw(self, img, tile_img, tiles):
        """Returns an image of a tile-based grid"""
        rect = get_tile_rect(self.pos)
        rect = Rect([rect.x + self.anim_offset.x, rect.y + self.anim_offset.y, rect.w, rect.h])
        img.blit(tile_img, rect, tiles[self.tile])

    def animate(self):
        if self.anim_direction:
            ofs_x = self.anim_offset.x + self.anim_direction.x * SPEED
            ofs_y = self.anim_offset.y + self.anim_direction.y * SPEED
            self.anim_offset = Position(ofs_x, ofs_y)
            if ofs_x == 0 and ofs_y == 0:
                self.arrives_on_new_tile()
                self.anim_direction = None


class Ghost(Sprite):

    def random_move(self, event):
        direction = random.choice([LEFT, RIGHT, UP, DOWN])
        self.move(direction)


class Player(Sprite):
            
    def arrives_on_new_tile(self):
        tile = self.maze[self.pos]
        if tile == '.':
            self.maze[self.pos] = ' ' # eats dot
        elif tile == 'x':
            exit_game()

    def handle_key(self, key):
        """Handles key events in the game"""
        direction = DIRECTIONS.get(key)
        if direction:
            self.move(direction)


# ------------- EVENT LOOP --------------

def event_loop(callbacks, delay=10, repeat=KEY_REPEAT_TIME):
    """Processes events and updates callbacks."""
    repeat_key = None
    running = True
    while running:
        pygame.event.pump()
        event = pygame.event.poll()
        action = callbacks.get(event.type)
        if action:
            action(event)
        elif event.type == EXIT:
            running = False
            eventlog.critical('exit event received: ' + str(event))
        else:
            eventlog.info('unhandled event: ' + str(event))
        pygame.time.delay(delay)

# ------------- GAME MECHANICS --------------

def exit_game():
    eve = pygame.event.Event(EXIT)
    pygame.event.post(eve)
    

# ------------- MAIN GAME --------------


class MazeRun:

    def create_display(self):
        pygame.init()
        pygame.display.set_mode((800, 600))
        self.display = pygame.display.get_surface()

    def create_tiles(self):
        self.tile_img = image.load(TILE_IMAGE_FILE)
        self.tiles = load_tiles(TILE_POSITION_FILE)

    def load_level(self, fn):
        data = open(fn).read()
        self.maze = TileGrid(data)
            
    def create_random_maze(self, size):
        maze_data = MazeGenerator.create_maze(size)
        self.maze = TileGrid(maze_data)
        self.maze[Position(size.x-2, size.y-2)] = 'x'
        log.info("random level created\n" + str(self.maze))

    def create_sprites(self, size):
        self.player = Player(self.maze, '*', Position(1, 1))
        self.ghost = Ghost(self.maze, 'g', Position(size.x-2, 1))

    def draw(self, event):
        img = self.maze.draw_grid(self.tile_img, self.tiles)
        self.player.draw(img, self.tile_img, self.tiles)
        self.ghost.draw(img, self.tile_img, self.tiles)
        rect = Rect((0, 0, self.maze.xsize*SIZE, self.maze.ysize*SIZE))
        self.display.blit(img, rect, rect)
        pygame.display.update()

    def handle_key(self, event):
        """Handles key events in the game"""
        direction = DIRECTIONS.get(event.key)
        if direction:
            self.player.move(direction)
            self.check_collision()

    def check_collision(self):
        if self.player.pos == self.ghost.pos:
            exit_game()

    def update(self, event):
        """Manages recurring checks in the game"""
        self.check_collision()
        self.player.animate()
        self.ghost.animate()

    def replay(self, replay_filename):
        import time
        log.handlers.pop()

        logdata = open('mymoves.log').read()
        parts = logdata.split("----------------")
        maze = TileGrid(parts[0].split('random level created')[-1].strip())

        display = create_display()
        sprites = create_sprites(Position(maze.xsize, maze.ysize))

        tile_img = image.load(TILE_IMAGE_FILE)
        tiles = load_tiles(TILE_POSITION_FILE)

        moves = parts[1].strip().split('\n')
        for m in moves:
            tokens = m.split()
            actor = tokens[0]
            direction = tokens[-1].split('/')
            direction = Position(int(direction[0]), int(direction[1]))
            move(maze, direction, actor)
            draw()
            pygame.display.update()
            time.sleep(0.5)
            
    def start_game(self):
        callbacks = {
            KEYDOWN: self.handle_key,
            DRAW: self.draw,
            UPDATE: self.update,
            MOVE_GHOST: self.ghost.random_move
        }
        pygame.time.set_timer(DRAW, DRAW_REPEAT_TIME)
        pygame.time.set_timer(UPDATE, UPDATE_REPEAT_TIME)
        pygame.time.set_timer(MOVE_GHOST, MOVE_GHOST_TIME)
        event_loop(callbacks)


# TODO: fix and check all command-line arguments

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start the MazeRun game.')
    parser.add_argument('--x', type=int, default=12,
                   help='x size of random maze')
    parser.add_argument('--y', type=int, default=7,
                   help='y size of random maze')
    parser.add_argument('--ghost', 
                   #dest="MOVE_GHOST_TIME", action="store_const",
                   type=int, default=500,
                   help='ghost speed (milliseconds per move)')
    parser.add_argument('-f', '--fast', 
                   dest="MOVE_GHOST_TIME", action="store_const",
                   const=250,
                   help='ghost speed (milliseconds per move)')

    g = parser.add_mutually_exclusive_group()
    g.add_argument('-l', '--load', type=str, default=None,
                   help='load maze from text file')
    g.add_argument('-r', '--replay', nargs='?', type=argparse.FileType('r'),
                   default=None,
                   help='log file to replay from')

    parser.add_argument('-e', '--eventlog', nargs='?', type=argparse.FileType('w'),
                   default=sys.stdout,
                   help="log file to store events")
    parser.add_argument('-v', '--verbose', action="store_true",
                   # type=int,
                   #choices=[0, 1, 2],
                   help='set debugging level')
    parser.add_argument('-playlist', type=str, metavar='.mp3', nargs='+',
                   help='mp3 filename(s) to be played')

    args = parser.parse_args()
    print(args)
    size = Position(args.x, args.y)

    mr = MazeRun()
    mr.create_display()
    mr.create_tiles()
    mr.create_random_maze(size)
    mr.create_sprites(size)
    mr.start_game()
    #mr.load_level(LEVEL_FILE)
