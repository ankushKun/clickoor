import pygame
from pygame import SurfaceType
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import UITextEntryLine, UIButton, UILabel
from globals import state
from lib.utils import connect_to_wifi, run_cmd, get_wifi_signal_strength

altkey = {
    '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(',  '0': ')', '-': '_', '=': '+',
    'q': 'Q', 'w': 'W', 'e': 'E', 'r': 'R', 't': 'T', 'y': 'Y', 'u': 'U', 'i': 'I', 'o': 'O', 'p': 'P', '[': '{', ']': '}', '\\': '|',
    'a': 'A', 's': 'S', 'd': 'D', 'f': 'F', 'g': 'G', 'h': 'H', 'j': 'J', 'k': 'K', 'l': 'L', ';': ':', '\'': '"',
    'z': 'Z', 'x': 'X', 'c': 'C', 'v': 'V', 'b': 'B', 'n': 'N', 'm': 'M', ',': '<', '.': '>', '/': '?',

    '!': '1', '@': '2', '#': '3', '$': '4', '%': '5', '^': '6', '&': '7', '*': '8', '(': '9', ')': '0', '_': '-', '+': '=',
    'Q': 'q', 'W': 'w', 'E': 'e', 'R': 'r', 'T': 't', 'Y': 'y', 'U': 'u', 'I': 'i', 'O': 'o', 'P': 'p', '{': '[', '}': ']', '|': '\\',
    'A': 'a', 'S': 's', 'D': 'd', 'F': 'f', 'G': 'g', 'H': 'h', 'J': 'j', 'K': 'k', 'L': 'l', ':': ';', '"': '\'',
    'Z': 'z', 'X': 'x', 'C': 'c', 'V': 'v', 'B': 'b', 'N': 'n', 'M': 'm', '<': ',', '>': '.', '?': '/',

    'Caps': 'Caps',
    'Enter': 'Enter',
    'Backspace': 'Backspace',
    'Space': 'Space'
}

characters = [
    [['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7'], [
        '8'], ['9'], ['0'], ['-'], ['='], ['Backspace']],
    [['q'], ['w'], ['e'], ['r'], ['t'], ['y'], ['u'],
        ['i'], ['o'], ['p'], ['['], [']'], ['\\']],
    [['a'], ['s'], ['d'], ['f'], ['g'], ['h'], ['j'],
        ['k'], ['l'], [';'], ['\''], ['Enter']],
    [['Caps'], ['z'], ['x'], ['c'], ['v'], [
        'b'], ['n'], ['m'], [','], ['.'], ['/'], ['Space']]
]


class WifiScreen:
    def __init__(self, manager: UIManager, screen: SurfaceType, set_screen):
        self.manager: UIManager = manager
        self.screen: SurfaceType = screen
        self.keylist = []
        self.caps = False
        self.focused_input = "SSID"
        self.set_screen = set_screen
        self.wifi_name = run_cmd("iwgetid -r")

    def draw_keys(self):
        for i, row in enumerate(characters):
            for j, char in enumerate(row):
                key_rect = pygame.Rect((0, 0), (50, 50))
                key_rect.center = (j*50 + 50, i*50 + 275)
                key = UIButton(relative_rect=key_rect,
                               text=char[0], manager=self.manager)
                self.keylist.append(key)

    def setup(self):
        self.manager.get_theme().load_theme("pygame-themes/transparent_btn.json")
        pygame.display.set_caption('Wifi Config')
        input_offset = -150

        self.draw_keys()

        conn_rect = pygame.Rect((0, 0), (400, -1))
        conn_rect.topright = (state["res"][0], 0)
        self.conn_label = UILabel(
            conn_rect, f"Wifi: {self.wifi_name}", self.manager)
        self.conn_label

        ssid_input_rect = pygame.Rect((0, 0), (200, 50))
        ssid_input_rect.center = (
            state["res"][0]//2, state["res"][1]//2 + input_offset)
        self.ssid_input = UITextEntryLine(
            relative_rect=ssid_input_rect, manager=self.manager, placeholder_text="SSID")

        pass_input_rect = pygame.Rect((0, 0), (200, 50))
        pass_input_rect.center = (
            state["res"][0]//2, state["res"][1]//2 + (input_offset + 50))
        self.pass_input = UITextEntryLine(
            relative_rect=pass_input_rect, manager=self.manager, placeholder_text="Password")

        btn_rect = pygame.Rect((0, 0), (200, 50))
        btn_rect.center = (state["res"][0]//2, state["res"][1] //
                           2 + (input_offset + 100))
        self.conn_btn = UIButton(relative_rect=btn_rect,
                                 text='Connect', manager=self.manager)

        self.back_btn = UIButton(pygame.Rect(
            (0, 0), (100, 50)), "Back", self.manager)

    def run(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            btn: UIButton = event.ui_element
            if btn.text == 'Caps':
                self.caps = not self.caps
                for key in self.keylist:
                    altk = altkey.get(key.text)
                    key.set_text(altk)
            elif btn.text == 'Enter':
                print('Entering')
            elif btn.text == 'Backspace':
                print('Backspacing')
                if self.focused_input == "SSID":
                    self.ssid_input.set_text(self.ssid_input.get_text()[:-1])
                elif self.focused_input == "PASS":
                    self.pass_input.set_text(self.pass_input.get_text()[:-1])
            elif btn.text == 'Space':
                if self.focused_input == "SSID":
                    self.ssid_input.set_text(self.ssid_input.get_text() + ' ')
                elif self.focused_input == "PASS":
                    self.pass_input.set_text(self.pass_input.get_text() + ' ')
            elif btn == self.conn_btn:
                print('Connecting')
                # disconnect
                # run_cmd("nmcli dev wifi rescan")
                connect_to_wifi(self.ssid_input.get_text().strip(),
                                self.pass_input.get_text().strip())
                ssid = run_cmd("iwgetid -r")
                if ssid.strip() == self.ssid_input.get_text().strip():
                    print("Connected")
                else:
                    print("Failed to connect")
            elif btn == self.back_btn:
                self.set_screen("Settings")
            else:
                if self.focused_input == "SSID":
                    self.ssid_input.set_text(
                        self.ssid_input.get_text() + btn.text)
                elif self.focused_input == "PASS":
                    self.pass_input.set_text(
                        self.pass_input.get_text() + btn.text)
                print(btn.text)

    def run_non_event(self):
        self.screen.fill((0, 0, 0))
        if self.ssid_input.is_focused:
            self.focused_input = "SSID"
        elif self.pass_input.is_focused:
            self.focused_input = "PASS"
        try:
            self.conn_label.set_text(
                f"Wifi: {run_cmd('iwgetid -r')} | {get_wifi_signal_strength()}%")
        except Exception as e:
            print(e)
            self.conn_label.set_text("Wifi: Not Connected")
