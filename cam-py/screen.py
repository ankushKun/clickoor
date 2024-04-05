import pygame
from pygame import SurfaceType
import pygame_gui
from pygame_gui import UIManager


# Example class template
class SomeScreen:
    def __init__(self, manager: UIManager, screen: SurfaceType, set_screen):
        self.manager = manager
        self.screen = screen
        self.set_screen = set_screen

    # Runs once
    def setup(self):
        # Add your gui elements here
        pass

    # Runs inside the event loop
    def run(self, event: pygame.event.EventType):
        # check for button clicks and stuff here
        pass

    # Runs outside the events loop
    def run_non_event(self):
        self.screen.fill((0, 0, 0))
        pass
