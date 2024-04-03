import pygame
import pygame_gui
from pygame_gui.elements import UIButton
from pygame_gui import UIManager
from globals import state
import os


class GalleryScreen:
    def __init__(self, manager: UIManager, set_screen):
        self.manager = manager
        self.set_screen = set_screen

    # Runs once
    def setup(self):
        back_rect = pygame.Rect((0, 0), (100, 50))
        self.back_btn = UIButton(back_rect, text="Back", manager=self.manager)

        image_list = os.listdir('captures')
        image_list = list(filter(lambda x: x.endswith(".jpg")
                          or x.endswith(".png"), image_list))
        print(image_list)

    # Runs inside the event loop

    def run(self, event: pygame.event.EventType):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.back_btn:
                self.set_screen("Home")

    # Runs outside the events loop
    def run_non_event(self):
        pass
