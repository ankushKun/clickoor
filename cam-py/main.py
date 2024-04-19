import pygame
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import UIButton
from globals import state, get_config
from wifi import WifiScreen
from home import HomeScreen
from settings import SettingsScreen
from wallet import WalletScreen
from gallery import GalleryScreen
from lib.utils import run_cmd
from os import system


class InfCam:
    def __init__(self):
        disp_orientation = get_config("orientation")
        if disp_orientation == "Inverted":
            system("wlr-randr --output DSI-1 --transform 180")
            # system("xrandr -o inverted")
        else:
            system("wlr-randr --output DSI-1 --transform normal")
            # system("xrandr -o normal")
        pygame.init()
        self.running = True
        self.screen_change = False
        self.screen = pygame.display.set_mode(
            state["res"], pygame.FULLSCREEN, vsync=1)
        try:
            import gpiozero
            pygame.mouse.set_visible(False)
        except:
            pass
        self.clock = pygame.time.Clock()
        self.manager = UIManager(
            state["res"])
        self.screens = {
            "Home": HomeScreen(self.manager, self.screen, self.set_screen),
            "Settings": SettingsScreen(self.manager, self.screen, self.set_screen),
            "Wifi": WifiScreen(self.manager, self.screen, self.set_screen),
            "Wallet": WalletScreen(self.manager, self.screen, self.set_screen),
            "Gallery": GalleryScreen(self.manager, self.screen, self.set_screen)
        }
        self.active_screen = "Home"

    def set_screen(self, screen_name):
        print(f"Switching to {screen_name}")
        self.screen_change = True
        self.active_screen = screen_name

    def setup(self):
        pass

    def run(self):
        while self.running:
            self.manager.clear_and_reset()
            self.screen.fill((0, 0, 0))
            self.screens[self.active_screen].setup()
            self.screen_change = False
            while not self.screen_change:
                time_delta = self.clock.tick(60)/1000.0
                self.screens[self.active_screen].run_non_event()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                        print("Exiting")
                        self.running = False
                        self.screen_change = True
                    self.screens[self.active_screen].run(event)
                    self.manager.process_events(event)
                self.manager.update(time_delta)
                self.manager.draw_ui(self.screen)
                pygame.display.update()


if __name__ == "__main__":
    cam = InfCam()
    cam.run()
