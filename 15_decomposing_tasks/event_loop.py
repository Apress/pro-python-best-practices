
# Chapter 09 - Decomposing functionality

import pygame
from pygame.locals import USEREVENT, KEYDOWN


EXIT = USEREVENT
UPDATE_DISPLAY = USEREVENT + 1
MOVE_GHOST = USEREVENT + 2


def move_player(event):
    """moves when keys are pressed"""
    print('player moves')

def move_ghost(event):
    """Ghost moves randomly"""
    print('ghost moves')

def update_graphics(event):
    """Re-draws the game window"""
    print('graphics updated')
    pass



callbacks = {
    KEYDOWN: move_player,
    MOVE_GHOST: move_ghost,
    UPDATE_DISPLAY: update_graphics,
}

def post_event(event):
    """Example for a user-generated event"""
    exit = pygame.event.Event(EXIT)
    pygame.event.post(exit)

def event_loop(callbacks, delay=10):
    """Processes events and updates callbacks."""
    running = True
    while running:
        pygame.event.pump()
        event = pygame.event.poll()
        action = callbacks.get(event.type)
        if action:
            action(event)
        pygame.time.delay(delay)
        if event.type == EXIT:
            running = False


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_mode((10, 10))
    pygame.time.set_timer(UPDATE_DISPLAY, 1000)
    pygame.time.set_timer(MOVE_GHOST, 300)
    pygame.time.set_timer(EXIT, 5000)
    event_loop(callbacks)
