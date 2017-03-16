
import random
import pygame
from pygame import image, Rect, Surface
from pygame.locals import KEYDOWN
from util import user_events
from util import create_display
from collections import namedtuple
from chapter08_load_tile_positions import load_tile_positions
from chapter08_load_tile_positions import TILE_POSITION_FILE, TILE_IMAGE_FILE, SIZE
from chapter09_event_loop_with_mediator import event_loop, exit_game
from chapter10_data_structures import TileSet, Position
from chapter10_data_structures import get_tile_rect, wait_for_key
from chapter10_data_structures import UP, DOWN, LEFT, RIGHT
from part1 import create_maze


DRAW = next(user_events)
MOVE_GHOST = next(user_events)
DRAW_REPEAT_TIME = 100
MOVE_GHOST_TIME = 500


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

    def draw_grid(self, tileset):
        """Returns an image of a tile-based grid"""
        img = Surface((self.xsize * SIZE, self.ysize * SIZE))
        for pos, char in self:
            rect = get_tile_rect(pos)
            img.blit(tileset.image, rect, tileset.positions[char])
        return img



class Sprite:

    def __init__(self, maze, tile, startpos):
        self.maze = maze
        self.tile = tile
        self.pos = startpos

    def move(self, direction):
        """Handles moves on a level"""
        old = self.pos
        new = Position(old.x + direction.x, old.y + direction.y)
        if self.maze[new] in [" ", ".", "x"]:
            self.pos = new

    def draw(self, img, tileset):
        """Returns an image of a tile-based grid"""
        rect = get_tile_rect(self.pos)
        img.blit(tileset.image, rect, tileset.positions[self.tile])


class Player(Sprite):

    directions = {
        276: LEFT, 275: RIGHT,
        273: UP, 274: DOWN
    }

    def move(self, direction):
        super(Player, self).move(direction)
        tile = self.maze[self.pos]
        if tile == '.':
            self.maze[self.pos] = ' ' # eats dot
        elif tile == 'x':
            exit_game()
        
    def handle_key(self, event):
        """Handles key events in the game"""
        direction = self.directions.get(event.key)
        if direction:
            self.move(direction)


class Ghost(Sprite):

    def random_move(self, event):
        direction = random.choice([LEFT, RIGHT, UP, DOWN])
        self.move(direction)


class Game:

    def __init__(self):
        self.display = create_display((800, 600))
        self.tileset = self.create_tileset()
        self.maze = self.create_random_maze(Position(12, 7))
        self.maze[Position(10, 5)] = 'x'
        self.player = Player(self.maze, '*', Position(1,1))
        self.ghost = Ghost(self.maze, 'g', Position(10, 1))

    def create_tileset(self):
        tile_image = image.load(TILE_IMAGE_FILE)
        tile_positions = load_tile_positions(TILE_POSITION_FILE)
        return TileSet(tile_image, tile_positions)

    def create_random_maze(self, size):
        maze_data = create_maze(size.x, size.y)
        maze = TileGrid(maze_data)
        maze[Position(size.x-2, size.y-2)] = 'x'
        return maze

    @property
    def sprites(self):
        return [self.player, self.ghost]

    def draw(self, event):
        img = self.maze.draw_grid(self.tileset)
        for sprite in self.sprites:
            sprite.draw(img, self.tileset)
        self.display.blit(img, Rect((0, 0, 384, 224)), Rect((0, 0, 384, 224)))
        pygame.display.update()

    def run(self, event_loop):
        callbacks = {
            KEYDOWN: self.player.handle_key,
            DRAW: self.draw,
            MOVE_GHOST: self.ghost.random_move
        }
        pygame.time.set_timer(DRAW, DRAW_REPEAT_TIME)
        pygame.time.set_timer(MOVE_GHOST, MOVE_GHOST_TIME)
        event_loop(callbacks)


if __name__ == '__main__':
    game = Game()
    game.run(event_loop)
