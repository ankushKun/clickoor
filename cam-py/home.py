import pygame
from pygame import SurfaceType
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import UIButton, UIImage, UIProgressBar, UILabel
import sys
import os
import pygame_gui.elements.ui_label
from globals import state, get_config
import globals
from datetime import datetime
from calendar import timegm
from arweave.arweave_lib import Wallet, Transaction
from arweave.transaction_uploader import get_uploader
from lib.utils import run_cmd, get_wifi_signal_strength, has_internet_connection
from threading import Thread

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
        self.status = ""
        self.exposure_times = {
            "1/10": 100000,
            "1/30": 33333,
            "1/60": 16666,
            "1/100": 10000,
            "1/200": 5000,
            "1/250": 4000,
        }
        self.selected_exposure_idx = 0
        self.selected_exposure: str = list(self.exposure_times.keys())[
            self.selected_exposure_idx]
        try:
            self.shutter = Button(5, hold_time=1)
            self.shutter.when_pressed = self.capture_and_save
            cam = Picamera2()
            cam.preview_configuration.main.size = state["res"]
            cam.preview_configuration.main.format = 'BGR888'
            # cam.configure("preview")
            try:
                cam.set_controls({"AfMode": controls.AfModeEnum.Continuous})
            except:
                print("No autofocus")
            self.cam = cam
            self.capture_config = cam.create_still_configuration(
                {"size": state["image_res"]}, buffer_count=1)
            self.cam.configure(self.capture_config)
            self.selected_exposure: str = list(self.exposure_times.keys())[
                self.selected_exposure_idx]
            self.cam.set_controls({"ExposureTime": 10000})
            # {"ExposureTime": self.exposure_times[self.selected_exposure]})
            self.cam.start()
            self.show_preview = True
        except NameError:
            print("Not a raspberry pi device, skipping camera setup")
            self.show_preview = False

    def upload_to_arweave(self, fpath: str):
        if not self.wallet:
            print("Wallet not found, skipping upload")
            return

        self.file_handler = open(fpath, "rb", buffering=0)
        tx = Transaction(
            self.wallet, file_handler=self.file_handler, file_path=fpath)
        tx.add_tag('Content-Type', 'image/png')
        tx.add_tag("Type", "image")
        tx.add_tag("App-Name", globals.state["app_name"])
        tx.add_tag("App-Version", globals.get_version())
        tx.sign()
        # b, p = self.wallet.balance, tx.get_price()
        # print(f"Balance   : {b}")
        # print(f"Cost      : {p}")
        # print(f"Remaining : {b-p}")
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
            # I feel this is slow, TODO: capture_array and save as image (could be faster)
            # self.cam.switch_mode_and_capture_file(
            #     self.capture_config, self.last_filename)
            self.cam.capture_file(self.last_filename)
            # i = pygame.image.load(self.last_filename)
            # self.image_surface.blit(i, (0, 0))
            m = get_config("upload_mode")
            if m in "Auto Upload":
                if has_internet_connection():
                    self.status = "Uploading..."
                    self.upload_to_arweave(self.last_filename)
                else:
                    print("No internet connection, skipping upload")
                    self.status = "No internet connection, skipping upload"
            else:
                print("Manual mode")
                self.status = "Skipping upload, Manual mode"
        else:
            print("Not a raspberry pi device, skipping capture")

    def setup(self):
        self.manager.get_theme().load_theme("pygame-themes/transparent_btn.json")
        pygame.display.set_caption(state["app_name"])
        if os.path.exists("wallet.json"):
            self.status = "Wallet found"

            def load_wallet():
                self.wallet = Wallet('wallet.json')
                self.status = "Wallet loaded"
            Thread(target=load_wallet).start()
        else:
            self.status = "No wallet"
            self.wallet = None
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

        status_rect = pygame.Rect((0, 0), (state["res"][0], 100))
        status_rect.bottomleft = (0, state["res"][1])
        self.status_label = UILabel(
            status_rect, self.status, self.manager)
        self.status_label.set_text_scale(1.1)

        shutter_speed_plus_rect = pygame.Rect((0, 0), (50, 50))
        shutter_speed_plus_rect.topleft = (0, 50)
        self.shutter_speed_plus_btn = UIButton(
            shutter_speed_plus_rect, "+", self.manager)

        shutter_speed_minus_rect = pygame.Rect((0, 0), (50, 50))
        shutter_speed_minus_rect.topleft = (50, 50)
        self.shutter_speed_minus_btn = UIButton(
            shutter_speed_minus_rect, "-", self.manager)

        self.shutter_speed_label = UILabel(
            pygame.Rect((0, 0), (200, 50)), f"Shutter Speed: {self.selected_exposure}", self.manager)
        self.shutter_speed_label.set_text_scale(1.1)
        self.shutter_speed_label.rect.topleft = (0, 100)

        # run the image preview code in a seperate thread

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
            elif btn == self.shutter_speed_plus_btn:
                if self.selected_exposure_idx < len(self.exposure_times)-1:
                    self.selected_exposure_idx += 1
                    self.selected_exposure = list(
                        self.exposure_times.keys())[self.selected_exposure_idx]
                    self.cam.set_controls(
                        {"ExposureTime": self.exposure_times[self.selected_exposure]})
                    self.shutter_speed_label.set_text(
                        f"Shutter Speed: {self.selected_exposure}")
            elif btn == self.shutter_speed_minus_btn:
                if self.selected_exposure_idx > 0:
                    self.selected_exposure_idx -= 1
                    self.selected_exposure = list(
                        self.exposure_times.keys())[self.selected_exposure_idx]
                    self.cam.set_controls(
                        {"ExposureTime": self.exposure_times[self.selected_exposure]})
                    self.shutter_speed_label.set_text(
                        f"Shutter Speed: {self.selected_exposure}")

    def run_non_event(self):
        self.image_surface.fill((30, 30, 30))
        try:
            conn_name = run_cmd("iwgetid -r")
            sig = get_wifi_signal_strength()
            self.wifi_label.set_text(f"Wifi: {conn_name} | {sig}%")
        except Exception as e:
            print(e)
            self.wifi_label.set_text("Wifi: Not Connected")
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
                os.remove(self.last_filename)
                self.status = "Uploaded"
        elif self.cam and self.show_preview:
            # this is state["image_res"] (1920,1080)
            arr = self.cam.capture_array()
            img = pygame.image.frombuffer(arr.data, state["image_res"], 'RGB')
            img = pygame.transform.scale(img, state["res"])
            # img = pygame.image.frombuffer(arr.data, state["res"], 'RGB')
            self.image_surface.blit(img, (0, 0))
        self.preview_image.set_image(self.image_surface)
        self.status_label.set_text(self.status)
