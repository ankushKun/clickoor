import pygame
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import UIButton, UIImage
import sys
from globals import state

try:
    from picamera2 import Picamera2
    from gpiozero import Button
    from libcamera import controls
except ImportError:
    print("Not a raspberry pi device, skipping imports")


class HomeScreen:
    def __init__(self, manager: UIManager, set_screen):
        self.manager: UIManager = manager
        self.set_screen = set_screen
        self.image_surface = pygame.Surface(state["res"])
        self.cam = None
        try:
            cam = Picamera2()
            cam.preview_configuration.main.size = state["res"]
            cam.preview_configuration.main.format = 'BGR888'
            cam.configure("preview")
            cam.set_controls({"AfMode": controls.AfModeEnum.Continuous})
            self.cam = cam
            self.capture_config = cam.create_still_configuration(
                {"size": state["image_res"]})
            self.cam.start()
            self.show_preview = True
        except NameError:
            print("Not a raspberry pi device, skipping camera setup")
            self.show_preview = False

    def capture_and_save(self):
        print("capturing image")
        if self.cam:
            self.cam.switch_mode_and_capture_file(
                self.capture_config, "img.png")
        else:
            print("Not a raspberry pi device, skipping capture")

    def setup(self):
        pygame.display.set_caption('Permacam')
        self.preview_image = UIImage(pygame.Rect(
            (0, 0), (state["res"][0], state["res"][1])), self.image_surface, self.manager)

        settings_rect = pygame.Rect((0, 0), (100, 50))
        settings_rect.topright = (state["res"][0], 0)
        self.open_settings_btn = UIButton(
            settings_rect, "Settings", self.manager)

        capture_rect = pygame.Rect((0, 0), (100, 50))
        capture_rect.bottomright = (state["res"][0], state["res"][1])
        self.capture_btn = UIButton(capture_rect, "Capture", self.manager)

        gallery_rect = pygame.Rect((0, 0), (100, 50))
        gallery_rect.bottomleft = (0, state["res"][1])
        self.back_btn = UIButton(gallery_rect, "Gallery", self.manager)

    def run(self, event: pygame.event.EventType):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            btn: UIButton = event.ui_element
            if btn == self.open_settings_btn:
                print("Switching to Wifi")
                self.set_screen("Settings")
            elif btn == self.capture_btn:
                self.capture_and_save()
            elif btn == self.back_btn:
                self.set_screen("Gallery")

    def run_non_event(self):
        self.image_surface.fill((30, 30, 30))
        if self.cam and self.show_preview:
            arr = self.cam.capture_array()
            img = pygame.image.frombuffer(arr.data, state["res"], 'RGB')
            self.image_surface.blit(img, (0, 0))
        self.preview_image.set_image(self.image_surface)
