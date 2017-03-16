
from pygame.locals import KEYDOWN, KEYUP, QUIT
from pygame.event import Event
import pygame


class EventGenerator:
    """Event loop for dispatching key events."""
    def __init__(self, handle_key, delay=10, key_repeat=80):
        self.handle_key = handle_key
        self.lastkey = 0
        self.delay = delay
        self.key_repeat = key_repeat
        self.key_repeat_delay = key_repeat
        self.running = True

    def key_pressed(self, event):
        """Called each time a key is pressed. Makes key repeats."""
        if self.lastkey == event.key:
            if self.key_repeat_delay > 0:
                self.key_repeat_delay -= 1
            if self.key_repeat_delay == 0:
                self.key_repeat_delay = self.key_repeat
                self.handle_key(self.lastkey)
        else:
            self.key_repeat_delay = self.key_repeat
            self.handle_key(event.key)
            self.lastkey = event.key

    def key_released(self, event):
        self.lastkey = 0

    def event_loop(self):
        """Processes events and updates callbacks."""
        while self.running:
            pygame.event.pump()
            event = pygame.event.poll()
            if event.type == KEYDOWN:
                self.key_pressed(event)
            elif event.type == KEYUP:
                self.key_released(event)
            pygame.time.delay(self.delay)

def print_key(key):
    print(key)

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_mode((640, 400))
    eg = EventGenerator(print_key)
    eg.event_loop()

