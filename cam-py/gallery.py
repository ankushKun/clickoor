import pygame
from pygame import SurfaceType
import pygame_gui
from pygame_gui.elements import UIButton, UIImage, UILabel
from pygame_gui import UIManager
from globals import state
import os
import requests
from io import BytesIO


class GalleryScreen:
    def __init__(self, manager: UIManager, screen: SurfaceType, set_screen):
        self.manager = manager
        self.screen = screen
        self.set_screen = set_screen
        self.im_num = 0
        self.local_images = []

    # Runs once
    def setup(self):
        self.manager.get_theme().load_theme("pygame-themes/normal.json")
        self.im_num = 0
        img_list = os.listdir('captures')
        self.local_images = list(
            filter(lambda x: x.endswith(".jpg") or x.endswith(".png"), img_list))
        self.local_images.sort(key=lambda x: os.path.getmtime(
            f"captures/{x}"), reverse=True)

        print(self.local_images)
        if len(self.local_images) > 0:
            self.img = pygame.image.load(
                f"captures/{self.local_images[self.im_num]}")
            sf = min(state["res"][0] / self.img.get_width(),
                     state["res"][1] / self.img.get_height())
            self.img = pygame.transform.scale(
                self.img, (int(self.img.get_width()*sf), int(self.img.get_height()*sf)))
        else:
            self.img = pygame.image.frombytes(
                b'\x00\x00\x00\x00', (1, 1), 'RGBA'
            )

        self.image_p = UIImage(pygame.Rect(
            (0, 0), (state["res"][0], state["res"][1])), self.img, manager=self.manager)

        self.back_btn = UIButton(pygame.Rect(
            (0, 0), (100, 50)), text="Back", manager=self.manager)
        self.next_btn = UIButton(pygame.Rect(
            (state["res"][0] - 100, 0), (100, 50)), text="Next", manager=self.manager)
        self.prev_btn = UIButton(pygame.Rect(
            (state["res"][0] - 200, 0), (100, 50)), text="Prev", manager=self.manager)
        self.delete_btn = UIButton(pygame.Rect(
            (state["res"][0] - 300, 0), (100, 50)), text="Delete", manager=self.manager)
        self.upload_btn = UIButton(pygame.Rect(
            (state["res"][0] - 400, 0), (100, 50)), text="Upload", manager=self.manager)
        self.img_counter = UILabel(pygame.Rect(
            (0, state["res"][1] - 50), (state["res"][0], 50)), text=f"Image {self.im_num+1} / {len(self.local_images)}", manager=self.manager)

    # Runs inside the event loop

    def run(self, event: pygame.event.EventType):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.back_btn:
                self.set_screen("Home")
                return
            elif event.ui_element == self.next_btn:
                if len(self.local_images) > 0 and self.im_num < len(self.local_images)-1:
                    self.im_num += 1
            elif event.ui_element == self.prev_btn:
                if len(self.local_images) > 0 and self.im_num > 0:
                    self.im_num -= 1
            if len(self.local_images) > 0:
                self.img = pygame.image.load(
                    f"captures/{self.local_images[self.im_num]}")
                sf = min(state["res"][0] / self.img.get_width(),
                         state["res"][1] / self.img.get_height())
                self.img = pygame.transform.scale(
                    self.img, (int(self.img.get_width()*sf), int(self.img.get_height()*sf)))
                self.image_p.set_image(self.img)
            if event.ui_element == self.delete_btn:
                if len(self.local_images) > 0:
                    os.remove(f"captures/{self.local_images[self.im_num]}")
                    self.local_images.pop(self.im_num)
                    if len(self.local_images) == 0:
                        self.img = pygame.image.frombytes(
                            b'\x00\x00\x00\x00', (1, 1), 'RGBA'
                        )
                        self.image_p.set_image(self.img)
                    else:
                        self.im_num = min(
                            self.im_num, len(self.local_images)-1)
                        self.img = pygame.image.load(
                            f"captures/{self.local_images[self.im_num]}")
                        sf = min(state["res"][0] / self.img.get_width(),
                                 state["res"][1] / self.img.get_height())
                        self.img = pygame.transform.scale(
                            self.img, (int(self.img.get_width()*sf), int(self.img.get_height()*sf)))
                        self.image_p.set_image(self.img)
            if event.ui_element == self.upload_btn:
                print("Uploading")

    # Runs outside the events loop
    def run_non_event(self):
        self.screen.fill((0, 0, 0))
        self.img_counter.set_text(
            f"Image {self.im_num+1} / {len(self.local_images)}")
