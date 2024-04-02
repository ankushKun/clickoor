import pygame
import pygame_gui
from pygame_gui import UIManager


class SomeScreen:
    def __init__(self, manager: UIManager, set_screen):
        self.manager = manager
        self.set_screen = set_screen

    # Runs once
    def setup(self):
        pass

    # Runs inside the event loop
    def run(self, event: pygame.event.EventType):
        pass

    # Runs outside the events loop
    def run_non_event(self):
        pass
