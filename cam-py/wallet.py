import subprocess
import pygame
from pygame import SurfaceType
import pygame_gui
from pygame_gui.elements import UILabel, UIButton, UIDropDownMenu, UIImage
from pygame_gui import UIManager
import arweave
from flask import Flask, render_template, request, send_file
import multiprocessing
from python_graphql_client import GraphqlClient
from lib.utils import run_cmd
import os
from globals import state, set_config, get_config
from threading import Thread

# wallet = []

# if os.path.exists('wallet.json'):
#     if wallet == []:
#         wallet.append(arweave.Wallet('wallet.json'))
#     else:
#         wallet[0] = arweave.Wallet('wallet.json')
# else:
#     if wallet == []:
#         wallet.append(None)
#     else:
#         wallet[0] = None


app = Flask(__name__)

try:
    hn = run_cmd('hostname -I').split(" ")[0]
except Exception as e:
    hn = run_cmd('hostname')


def valid_filename(filename):
    return filename.endswith('.json') and len(filename.split('.')) == 2


@app.route('/', methods=['GET'])
def home():
    # if len(wallet) > 0:
    #     w = wallet[0]
    # else:
    #     w = None
    # print(w)
    w = arweave.Wallet('../wallet.json') if os.path.exists(
        '../wallet.json') else None
    return render_template('index.html', data={"address": w.address if w else 'NO WALLET', "balance": w.balance if w else 'NO WALLET'})


# @app.route('/gallery')
# def gallery():
#     w = wallet[0]
#     my_addr = wallet.address if wallet else 'NO WALLET'
#     client = GraphqlClient(endpoint="https://arweave.net/graphql")

#     query = """
# query {
#     transactions(owners:["8iD-Gy_sKx98oth27JhjjP2V_xUSIGqs_8-skb63YHg"]) {
#         edges {
#             node {
#                 id
#             }
#         }
#     }
# }
#     """
#     data = client.execute(query=query)
#     print(data)

#     return render_template('gallery.html', data="")


@app.route('/upload', methods=['POST'])
def upload():
    jwk_file = request.files['jwk']
    filename = jwk_file.filename
    if not valid_filename(filename):
        return "Invalid File, should be a valid wallet.json file"
    # Need to add more checks to verify if the wallet json is valid
    jwk_file.save("../wallet.json")
    global wallet
    # Init throws an error if wallet is invalid, catch this exception to use the old wallet or replace with new one
    wallet = arweave.Wallet('../wallet.json')
    return "JWK Uploaded"


@app.route('/download', methods=['GET'])
def download():
    # download wallet.json file
    return send_file('../wallet.json', as_attachment=True)

# def run_server():
#     global pid
#     os.system("cd cam-py && gunicorn -w 1 wallet:app -b 0.0.0.0:8080")
    # app.run(host='0.0.0.0', port=8080)  # was getting no perms on port 80


class WalletScreen:
    def __init__(self, manager: UIManager, screen: SurfaceType, set_screen):
        self.manager = manager
        self.screen = screen
        self.set_screen = set_screen

    # Runs once
    def setup(self):
        global wallet
        os.system("fuser -k 8080/tcp")
        self.manager.get_theme().load_theme("pygame-themes/transparent_btn.json")
        self.wallet = None
        wallet = None

        back_btn_rect = pygame.Rect((10, 10), (50, 50))
        self.back_btn = UIButton(back_btn_rect, "Back", self.manager)
        self.back_btn.normal_image = pygame.image.load("assets/back.png")
        UIImage(self.back_btn.rect, self.back_btn.normal_image, self.manager)

        self.addres_text = UILabel(pygame.Rect(
            (0, 50), (state["res"][0], 50)), text=self.wallet.address if self.wallet else 'NO WALLET', manager=self.manager)
        self.balance_text = UILabel(pygame.Rect(
            (0, 100), (state["res"][0], 50)), text=f"Balance: {self.wallet.balance if self.wallet else 'NO WALLET'} AR", manager=self.manager)
        self.portal_url_pre = UILabel(pygame.Rect(
            (0, 150), (state["res"][0], 50)), text=f"http://clickoor.local:8080", manager=self.manager)
        UILabel(pygame.Rect(
            (0, 170), (state["res"][0], 50)), text="or", manager=self.manager)
        self.portal_url_dyn = UILabel(pygame.Rect(
            (0, 190), (state["res"][0], 50)), text=f"http://{hn}:8080", manager=self.manager)

        self.gallery_url = UILabel(pygame.Rect(
            (0, 230), (state["res"][0], 50)), text="Gallery: https://clickoor.arweave.dev", manager=self.manager)

        if os.path.exists('wallet.json'):
            self.addres_text.set_text("Loading wallet...")

            def load_wallet():
                self.wallet = arweave.Wallet('wallet.json')
                wallet = self.wallet
                self.addres_text.set_text(self.wallet.address)
                self.balance_text.set_text(
                    f"Balance: {self.wallet.balance} AR")
            Thread(target=load_wallet).start()

        # self.flask_process = multiprocessing.Process(target=run_server)
        # self.flask_process.start()
        # subprocess.run("cd cam-py && gunicorn -w 1 wallet:app -b 0.0.0.0:8080")
        self.flask_process = subprocess.Popen(
            "cd cam-py && gunicorn -w 1 wallet:app -b 0.0.0.0:8080", shell=True)

        selector_label_rect = pygame.Rect(
            (0, 270), (state["res"][0], 50))
        self.selector_label = UILabel(
            selector_label_rect, text="Upload Mode", manager=self.manager)

        upload_selector_rect = pygame.Rect(
            (0, 310), (state["res"][0]//2, 50))
        upload_selector_rect.centerx = state["res"][0]//2
        # self.upload_dropdown = UIDropDownMenu(relative_rect=upload_selector_rect, manager=self.manager, default_selection=get_config(
        #     "upload_mode") or "Manual Upload", item_list=["Auto Upload", "Manual Upload"], allow_double_clicks=False)
        self.upload_selector = UIDropDownMenu(
            ["Auto Upload", "Manual Upload"], get_config("upload_mode"), upload_selector_rect, self.manager)

    def run(self, event: pygame.event.EventType):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            btn: UIButton = event.ui_element
            if btn == self.back_btn:
                self.flask_process.terminate()
                self.flask_process.kill()
                os.system("fuser -k 8080/tcp")
                self.set_screen("Settings")
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            # selection_list: UISelectionList = event.ui_element
            # set_config("upload_mode", selection_list.get_single_selection())
            # print(selection_list.get_single_selection())
            if event.ui_element == self.upload_selector:
                set_config("upload_mode", event.text)
                print(event.text)

    def run_non_event(self):
        self.screen.fill((0, 0, 0))
