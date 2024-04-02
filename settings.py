import pygame
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import UIButton


class SettingsScreen:
    def __init__(self, manager: UIManager, set_screen):
        self.manager = manager
        self.set_screen = set_screen

    # Runs once
    def setup(self):
        self.back_btn = UIButton(pygame.Rect(
            (0, 0), (100, 50)), "Back", self.manager)
        self.wifi_settings = UIButton(pygame.Rect(
            (0, 50), (100, 50)), "Wifi", self.manager)

    # Runs inside the event loop
    def run(self, event: pygame.event.EventType):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            btn: UIButton = event.ui_element
            if btn == self.back_btn:
                self.set_screen("Home")
            elif btn == self.wifi_settings:
                self.set_screen("Wifi")

    # Runs outside the events loop
    def run_non_event(self):
        pass
