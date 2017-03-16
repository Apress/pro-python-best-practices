
import pygame
import logging
import sys
from chapter09_event_loop_with_mediator import EXIT
from chapter10_data_structures import Position
from chapter11_classes import Game, TileGrid
from part1 import create_maze

#logging.basicConfig(filename='random_levels.log', level=logging.INFO)

log = logging.getLogger('moves')
log.addHandler(logging.FileHandler('moves.log', mode='w'))
log.setLevel(logging.INFO)

eventlog = logging.getLogger('events')
eventlog.addHandler(logging.StreamHandler(sys.stderr))
#fmt='%(asctime)s %(message)s'
#eventlog.addFormatter(logging.Formatter(fmt), datefmt='%m/%d/%Y %I:%M:%S %p')
eventlog.setLevel(logging.WARNING)



def event_loop(callbacks, delay=10):
    """Processes events and updates callbacks."""
    repeat_key = None
    running = True
    while running:
        pygame.event.pump()
        event = pygame.event.poll()
        action = callbacks.get(event.type)
        if action:
            action(event)
            eventlog.warning('event executed: ' + str(event))
        elif event.type == EXIT:
            running = False
            eventlog.critical('exit event received: ' + str(event))
        else:
            eventlog.info('unhandled event: ' + str(event))
        pygame.time.delay(delay)


class LoggedGame(Game):

    def create_random_maze(self, size):
        maze_data = create_maze(size.x, size.y)
        maze = TileGrid(maze_data)
        maze[Position(size.x-2, size.y-2)] = 'x'
        log.info("random level created\n" + str(maze))
        return maze

    def replay(self, replay_filename):
        import time
        log.handlers.pop()

        logdata = open('mymoves.log').read()
        parts = logdata.split("----------------")
        maze = TileGrid(parts[0].split('random level created')[-1].strip())

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


if __name__ == '__main__':
    game = LoggedGame()
    game.run(event_loop)
    game.replay('mymoves.log')  
