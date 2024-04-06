import pygame
from pygame import SurfaceType
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import UIButton, UIImage, UIProgressBar, UILabel
import sys
import os
import pygame_gui.elements.ui_label
from globals import state, get_config
from datetime import datetime
from calendar import timegm
from arweave.arweave_lib import Wallet, Transaction
from arweave.transaction_uploader import get_uploader
from lib.utils import run_cmd, get_wifi_signal_strength, has_internet_connection

try:
    from picamera2 import Picamera2
    from gpiozero import Button
    from libcamera import controls
except ImportError:
    print("Not a raspberry pi device, skipping imports")


class HomeScreen:
    def __init__(self, manager: UIManager, screen: SurfaceType, set_screen):
        self.manager: UIManager = manager
        self.screen: SurfaceType = screen
        self.set_screen = set_screen
        self.image_surface = pygame.Surface(state["res"])
        self.cam = None
        self.uploader = None
        try:
            cam = Picamera2()
            cam.preview_configuration.main.size = state["res"]
            cam.preview_configuration.main.format = 'BGR888'
            cam.configure("preview")
            try:
                cam.set_controls({"AfMode": controls.AfModeEnum.Continuous})
            except:
                print("No autofocus")
            self.cam = cam
            self.capture_config = cam.create_still_configuration(
                {"size": state["image_res"]})
            self.cam.start()
            self.show_preview = True
        except NameError:
            print("Not a raspberry pi device, skipping camera setup")
            self.show_preview = False

    def upload_to_arweave(self, fpath: str):
        if not os.path.exists("wallet.json"):
            print("Wallet not found, skipping upload")
            return
        wallet = Wallet('wallet.json')
        self.file_handler = open(fpath, "rb", buffering=0)
        tx = Transaction(
            wallet, file_handler=self.file_handler, file_path=fpath)
        tx.add_tag('Content-Type', 'image/png')
        tx.add_tag("Type", "image")
        tx.add_tag("App-Name", state["app_name"])
        tx.add_tag("App-Version", state["version"])
        tx.sign()
        b, p = wallet.balance, tx.get_price()
        print(f"Balance   : {b}")
        print(f"Cost      : {p}")
        print(f"Remaining : {b-p}")
        self.tx = tx
        self.uploader = get_uploader(self.tx, self.file_handler)
        # while not u.is_complete:
        #     u.upload_chunk()
        #     c = u.pct_complete
        #     d, t = u.uploaded_chunks, u.total_chunks
        #     print(f"{c}%, {d}/{t}")
        #     self.progress_bar.set_current_progress(c)
        #     self.manager.update(0.01)
        #     # self.manager.draw_ui(self.screen)
        #     pygame.display.update()
        # self.progress_bar.hide()
        # return tx.id

    def capture_and_save(self):
        print("capturing image")
        # ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        ts = datetime.now()
        ts = timegm(ts.utctimetuple())
        self.last_filename = f"captures/IMG_{ts}.png"
        if self.cam:
            self.cam.switch_mode_and_capture_file(
                self.capture_config, self.last_filename)
            # i = pygame.image.load(self.last_filename)
            # self.image_surface.blit(i, (0, 0))
            if get_config("upload_mode") == "Auto Upload" and has_internet_connection():
                self.upload_to_arweave(self.last_filename)
            else:
                print("No internet skipping upload")
        else:
            print("Not a raspberry pi device, skipping capture")

    def setup(self):
        self.manager.get_theme().load_theme("transparent_btn.json")
        pygame.display.set_caption(state["app_name"])
        self.preview_image = UIImage(pygame.Rect(
            (0, 0), (state["res"][0], state["res"][1])), self.image_surface, self.manager)

        settings_rect = pygame.Rect((0, 0), (60, 60))
        settings_rect.bottomleft = (0, state["res"][1])
        self.open_settings_btn = UIButton(
            settings_rect, "Settings", self.manager)
        self.open_settings_btn.normal_image = pygame.image.load(
            "assets/settings.png")
        UIImage(settings_rect, self.open_settings_btn.normal_image, self.manager)

        capture_rect = pygame.Rect((0, 0), (100, 100))
        capture_rect.bottomright = (state["res"][0], state["res"][1]//2 + 50)
        self.capture_btn = UIButton(capture_rect, "", self.manager)
        self.capture_btn.normal_image = pygame.image.load("assets/shutter.png")
        self.capture_btn.border_width = 0
        UIImage(capture_rect, self.capture_btn.normal_image, self.manager)

        gallery_rect = pygame.Rect((0, 0), (60, 60))
        gallery_rect.bottomright = (state["res"][0], state["res"][1])
        self.gallery_btn = UIButton(gallery_rect, "Gallery", self.manager)
        self.gallery_btn.normal_image = pygame.image.load("assets/gallery.png")
        UIImage(gallery_rect, self.gallery_btn.normal_image, self.manager)

        progress_rect = pygame.Rect((0, 0), (state["res"][0]//2, 50))
        progress_rect.center = (state["res"][0]//2, state["res"][1]//2)
        self.progress_bar = UIProgressBar(progress_rect, manager=self.manager)
        self.progress_bar.hide()

        wifi_rect = pygame.Rect((0, 0), (-1, -1))
        wifi_rect.topleft = (0, 0)
        self.wifi_label = UILabel(
            wifi_rect, "Wifi: " + run_cmd("iwgetid -r"), self.manager)
        self.wifi_label.text_horiz_alignment_padding = 6

    def run(self, event: pygame.event.EventType):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            btn: UIButton = event.ui_element
            if btn == self.open_settings_btn:
                print("Switching to Wifi")
                self.set_screen("Settings")
            elif btn == self.capture_btn:
                self.capture_and_save()
            elif btn == self.gallery_btn:
                self.set_screen("Gallery")

    def run_non_event(self):
        self.image_surface.fill((30, 30, 30))
        conn_name = run_cmd("iwgetid -r")
        sig = get_wifi_signal_strength()
        self.wifi_label.set_text(f"Wifi: {conn_name} | {sig}%")
        if self.uploader and not self.uploader.is_complete:
            i = pygame.image.load(self.last_filename)
            iw, ih = i.get_size()
            sf = min(state["res"][0] / iw, state["res"][1] / ih)
            i = pygame.transform.scale(i, (iw*sf, ih*sf))
            self.image_surface.blit(i, (0, 0))
            self.uploader.upload_chunk()
            self.progress_bar.show()
            self.progress_bar.set_current_progress(self.uploader.pct_complete)
            print(
                f"{self.uploader.pct_complete}% - {self.uploader.uploaded_chunks}/{self.uploader.total_chunks}")
            if self.uploader.uploaded_chunks == self.uploader.total_chunks:
                self.progress_bar.hide()
                self.uploader = None
                self.file_handler.close()
                print(f"Uploaded https://arweave.net/{self.tx.id}")
        elif self.cam and self.show_preview:
            arr = self.cam.capture_array()
            img = pygame.image.frombuffer(arr.data, state["res"], 'RGB')
            self.image_surface.blit(img, (0, 0))
        self.preview_image.set_image(self.image_surface)
