import pygame
from pygame import SurfaceType
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import UIButton, UILabel, UIDropDownMenu
from globals import state
import globals
import os
import sys
from globals import set_config, get_config


class SettingsScreen:
    def __init__(self, manager: UIManager, screen: SurfaceType, set_screen):
        self.manager = manager
        self.screen = screen
        self.set_screen = set_screen

    # Runs once
    def setup(self):
        self.manager.get_theme().load_theme("pygame-themes/normal.json")
        back_rect = pygame.Rect((0, 0), (100, 50))
        back_rect.center = (state["res"][0]//2, state["res"][1]//2 - 50)
        self.back_btn = UIButton(back_rect, "Back", self.manager)

        wifi_rect = pygame.Rect((0, 0), (100, 50))
        wifi_rect.center = (state["res"][0]//2, state["res"][1]//2)
        self.wifi_settings = UIButton(wifi_rect, "Wifi", self.manager)

        wallet_rect = pygame.Rect((0, 0), (100, 50))
        wallet_rect.center = (state["res"][0]//2, state["res"][1]//2 + 50)
        self.wallet_settings = UIButton(wallet_rect, "Wallet", self.manager)

        # exit_rect = pygame.Rect((0, 0), (100, 50))
        # exit_rect.center = (state["res"][0]//2, state["res"][1]//2 + 100)
        # self.exit_btn = UIButton(exit_rect, "Exit", self.manager)

        shutdown_rect = pygame.Rect((0, 0), (100, 50))
        shutdown_rect.center = (state["res"][0]//2, state["res"][1]//2 + 100)
        self.shutdown_btn = UIButton(shutdown_rect, "Shutdown", self.manager)

        version_rect = pygame.Rect((0, 0), (100, 50))
        version_rect.topleft = (0, 0)
        self.version_label = UILabel(
            version_rect, globals.get_version(), self.manager)

        display_orientation_rect = pygame.Rect((0, 0), (100, 50))
        display_orientation_rect.center = (
            state["res"][0]//2, state["res"][1]//2 + 150)
        self.display_orientation = UIDropDownMenu(
            ["Normal", "Inverted"], get_config("orientation"), display_orientation_rect, self.manager)

    # Runs inside the event loop

    def run(self, event: pygame.event.EventType):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            btn: UIButton = event.ui_element
            if btn == self.back_btn:
                self.set_screen("Home")
            elif btn == self.wifi_settings:
                self.set_screen("Wifi")
            elif btn == self.wallet_settings:
                self.set_screen("Wallet")
            # elif btn == self.exit_btn:
            #     pygame.quit()
            #     sys.exit()
            elif btn == self.shutdown_btn:
                os.system("sudo shutdown now")
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == self.display_orientation:
                    if event.text == "Normal":
                        try:
                            set_config("orientation", "Normal")
                            os.system("wlr-randr --output DSI-1 --transform 0")
                            os.system("xrandr -o normal")
                        except:
                            pass
                    elif event.text == "Inverted":
                        try:
                            set_config("orientation", "Inverted")
                            os.system(
                                "wlr-randr --output DSI-1 --transform 180")
                            os.system("xrandr -o inverted")
                        except:
                            pass

    # Runs outside the events loop
    def run_non_event(self):
        self.screen.fill((0, 0, 0))
