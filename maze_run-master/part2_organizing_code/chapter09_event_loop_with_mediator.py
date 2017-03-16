
# Chapter 09 - Decomposing functionality

import pygame
from util import user_events
from itertools import count

EXIT = next(user_events)


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


def exit_game():
    exit = pygame.event.Event(EXIT)
    pygame.event.post(exit)


if __name__ == '__main__':
    
    def countdown(event):
        """exits when the counter reaches 0"""
        number = next(ticker)
        print(number)
        if number == 0:
            exit_game()
    
    COUNTDOWN = next(user_events)
    callbacks = {COUNTDOWN: countdown}

    ticker = count(10, -1)
    pygame.init()
    pygame.display.set_mode((10, 10))
    pygame.time.set_timer(COUNTDOWN, 100)
    event_loop(callbacks)
