import pygame
from pygame import SurfaceType
import pygame_gui
from pygame_gui.elements import UIButton, UIImage, UILabel, UIProgressBar
from pygame_gui import UIManager
import globals
from globals import state
from lib.utils import has_internet_connection
import os
import requests
from io import BytesIO
from arweave.arweave_lib import Wallet, Transaction
from arweave.transaction_uploader import get_uploader
from threading import Thread


class GalleryScreen:
    def __init__(self, manager: UIManager, screen: SurfaceType, set_screen):
        self.manager = manager
        self.screen = screen
        self.set_screen = set_screen
        self.im_num = 0
        self.local_images = []
        self.upload_filename = None
        self.file_handler = None
        self.uploader = None
        self.wallet = None
        self.status = ""

    # Runs once
    def setup(self):
        if os.path.exists('wallet.json'):
            def load_wallet():
                self.wallet = Wallet('wallet.json')
                self.status = "Wallet loaded"
            Thread(target=load_wallet).start()

        # self.manager.get_theme().load_theme("pygame-themes/transparent_btn.json")
        self.im_num = 0
        img_list = os.listdir('captures')
        self.local_images = list(
            filter(lambda x: x.endswith(".jpg") or x.endswith(".png"), img_list))
        self.local_images.sort(key=lambda x: os.path.getmtime(
            f"captures/{x}"), reverse=True)

        print(self.local_images)
        if len(self.local_images) > 0:
            p = os.path.join(".", "captures",
                             f"{self.local_images[self.im_num]}")
            print(p)
            self.img = pygame.image.load(p)
            # os.pa(f"captures/{self.local_images[self.im_num]}"))
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
            (10, 10), (50, 50)), text="Back", manager=self.manager)
        self.back_btn.normal_image = pygame.image.load("assets/back.png")
        UIImage(self.back_btn.rect, self.back_btn.normal_image,
                manager=self.manager)

        next_btn_rect = pygame.Rect((0, 0), (50, 50))
        next_btn_rect.bottomright = (state["res"][0]-10, state["res"][1]-10)
        self.next_btn = UIButton(
            next_btn_rect, text="Next", manager=self.manager)
        self.next_btn.normal_image = pygame.transform.rotate(
            pygame.image.load("assets/previous.png"), 180)
        UIImage(self.next_btn.rect, self.next_btn.normal_image,
                manager=self.manager)

        prev_btn_rect = pygame.Rect((0, 0), (50, 50))
        prev_btn_rect.bottomright = (
            state["res"][0] - 65, state["res"][1] - 10)
        self.prev_btn = UIButton(
            prev_btn_rect, text="Prev", manager=self.manager)
        self.prev_btn.normal_image = pygame.image.load("assets/previous.png")
        UIImage(self.prev_btn.rect, self.prev_btn.normal_image,
                manager=self.manager)

        delete_btn_rect = pygame.Rect((0, 0), (50, 50))
        delete_btn_rect.bottomleft = (10, state["res"][1]-10)
        self.delete_btn = UIButton(
            delete_btn_rect, text="Delete", manager=self.manager)
        self.delete_btn.normal_image = pygame.image.load("assets/trash.png")
        UIImage(self.delete_btn.rect,
                self.delete_btn.normal_image, manager=self.manager)

        upload_btn_rect = pygame.Rect((0, 0), (50, 50))
        upload_btn_rect.topright = (state["res"][0]-10, 10)
        self.upload_btn = UIButton(
            upload_btn_rect, text="Upload", manager=self.manager)
        self.upload_btn.normal_image = pygame.image.load("assets/upload.png")
        UIImage(self.upload_btn.rect,
                self.upload_btn.normal_image, manager=self.manager)

        self.img_counter = UILabel(pygame.Rect(
            (0, state["res"][1] - 50), (state["res"][0], 50)), text=f"Image {self.im_num+1} / {len(self.local_images)}", manager=self.manager)

        progress_rect = pygame.Rect((0, 0), (state["res"][0]//2, 50))
        progress_rect.center = (state["res"][0]//2, state["res"][1]//2)
        self.progress_bar = UIProgressBar(progress_rect, manager=self.manager)
        self.progress_bar.hide()

        status_rect = pygame.Rect((0, 0), (state["res"][0], 100))
        status_rect.bottomleft = (0, state["res"][1])
        self.status_label = UILabel(status_rect, self.status, self.manager)
        self.status_label.set_text_scale(1.1)

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
                try:
                    self.img = pygame.image.load(
                        f"captures/{self.local_images[self.im_num]}")
                    sf = min(state["res"][0] / self.img.get_width(),
                             state["res"][1] / self.img.get_height())
                    self.img = pygame.transform.scale(
                        self.img, (int(self.img.get_width()*sf), int(self.img.get_height()*sf)))
                except:
                    self.status = "Error loading image"
                    self.img = pygame.image.frombytes(
                        b'\x00\x00\x00\x00', (1, 1), 'RGBA'
                    )
                self.image_p.set_image(self.img)
            if event.ui_element == self.delete_btn:
                try:
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
                except:
                    self.status = "Error deleting image"
            if event.ui_element == self.upload_btn:
                if has_internet_connection() and len(self.local_images) > 0:
                    self.upload_filename = "captures/" + \
                        self.local_images[self.im_num]
                    self.status = "Uploading..."
                    self.upload_to_arweave(self.upload_filename)
                else:
                    self.status = "Skipping upload, No internet connection"

    def upload_to_arweave(self, fpath: str):
        if not self.wallet:
            print("Wallet not found, skipping upload")
            self.status = "Wallet not found, skipping upload"
            return

        print("Uploading")
        self.status = "Uploading..."

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

    def run_non_event(self):
        self.screen.fill((0, 0, 0))
        self.img_counter.set_text(
            f"Image {self.im_num+1} / {len(self.local_images)}")
        if self.uploader and not self.uploader.is_complete:
            i = pygame.image.load(self.upload_filename)
            iw, ih = i.get_size()
            sf = min(state["res"][0] / iw, state["res"][1] / ih)
            i = pygame.transform.scale(i, (iw*sf, ih*sf))
            # self.image_surface.blit(i, (0, 0))
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
                os.remove(self.upload_filename)
                self.status = f"Uploaded"
                self.upload_filename = None
                img_list = os.listdir('captures')
                self.local_images = list(
                    filter(lambda x: x.endswith(".jpg") or x.endswith(".png"), img_list))
                self.local_images.sort(key=lambda x: os.path.getmtime(
                    f"captures/{x}"), reverse=True)
                if len(self.local_images) > 0:
                    self.im_num -= 1
                else:
                    self.img = pygame.image.frombytes(
                        b'\x00\x00\x00\x00', (1, 1), 'RGBA'
                    )
                    self.image_p.set_image(self.img)
        self.status_label.set_text(self.status)
