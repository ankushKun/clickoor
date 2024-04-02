import pygame
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import UIButton
from globals import state
from wifi import WifiScreen
from home import HomeScreen
from settings import SettingsScreen


class InfCam:
    def __init__(self):
        pygame.init()
        self.running = True
        self.screen_change = False
        self.screen = pygame.display.set_mode(state["res"])
        self.clock = pygame.time.Clock()
        self.manager = UIManager(state["res"])
        self.screens = {
            "Home": HomeScreen(self.manager, self.set_screen),
            "Settings": SettingsScreen(self.manager, self.set_screen),
            "Wifi": WifiScreen(self.manager, self.set_screen)
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
    # import arweave

    # wallet = arweave.Wallet("wallet.json")
    # print(wallet.address)

    # t = arweave.Transaction(wallet, data=open("img.png", "rb").read())
    # t.add_tag("App-Name", "Permacam")
    # t.add_tag("Content-Type", "Image")
    # t.sign()
    # print(t.signature)
    # print("price", t.get_price())
    # r = t.send()
    # with open("tx.json", "w") as f:
    #     f.write(r)

    cam = InfCam()
    cam.run()
