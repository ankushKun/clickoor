import pygame
import pygame_gui
from pygame_gui.elements import UIButton
from pygame_gui import UIManager
from globals import state

# Example class template


class GalleryScreen:
    def __init__(self, manager: UIManager, set_screen):
        self.manager = manager
        self.set_screen = set_screen

    # Runs once
    def setup(self):
        # Add your gui elements here
        back_rect = pygame.Rect((0, 0), (100, 50))
        self.back_btn = UIButton(back_rect, text="Back", manager=self.manager)

    # Runs inside the event loop
    def run(self, event: pygame.event.EventType):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.back_btn:
                self.set_screen("Home")

    # Runs outside the events loop
    def run_non_event(self):
        pass
