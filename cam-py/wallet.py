import pygame
import pygame_gui
from pygame_gui.elements import UILabel, UIButton
from pygame_gui import UIManager
from globals import state
import arweave


class WalletScreen:
    def __init__(self, manager: UIManager, set_screen):
        self.manager = manager
        self.set_screen = set_screen
        self.wallet = arweave.Wallet('wallet.json')

    # Runs once
    def setup(self):
        self.back_btn = UIButton(pygame.Rect(
            (0, 0), (100, 50)), text="Back", manager=self.manager)
        self.addres_text = UILabel(pygame.Rect(
            (0, 50), (state["res"][0], 50)), text=self.wallet.address, manager=self.manager)

    def run(self, event: pygame.event.EventType):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            btn: UIButton = event.ui_element
            if btn == self.back_btn:
                self.set_screen("Settings")

    def run_non_event(self):
        pass
