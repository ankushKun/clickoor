import subprocess
import pygame
from pygame import SurfaceType
import pygame_gui
from pygame_gui.elements import UILabel, UIButton
from pygame_gui import UIManager
import arweave
from flask import Flask, render_template, request
import multiprocessing
from python_graphql_client import GraphqlClient
from lib.utils import run_cmd
import os
from globals import state

if os.path.exists('wallet.json'):
    wallet = arweave.Wallet('wallet.json')
else:
    wallet = None


app = Flask(__name__)


try:
    hn = run_cmd('hostname -I').split(" ")[0]
except Exception as e:
    hn = run_cmd('hostname')


def valid_filename(filename):
    return filename.endswith('.json') and len(filename.split('.')) == 2


@app.route('/')
def home():
    return render_template('index.html', data={"address": wallet.address if wallet else 'NO WALLET', "balance": wallet.balance if wallet else 'NO WALLET'})


@app.route('/gallery')
def gallery():
    my_addr = wallet.address if wallet else 'NO WALLET'
    client = GraphqlClient(endpoint="https://arweave.net/graphql")

    query = """
query {
    transactions(owners:["8iD-Gy_sKx98oth27JhjjP2V_xUSIGqs_8-skb63YHg"]) {
        edges {
            node {
                id
            }
        }
    }
}
    """
    data = client.execute(query=query)
    print(data)

    return render_template('gallery.html', data=data)


@app.route('/upload', methods=['POST'])
def upload():
    jwk_file = request.files['jwk']
    filename = jwk_file.filename
    if not valid_filename(filename):
        return "Invalid File, should be a valid wallet.json file"
    # Need to add more checks to verify if the wallet json is valid
    jwk_file.save("wallet.json")
    global wallet
    # Init throws an error if wallet is invalid, catch this exception to use the old wallet or replace with new one
    wallet = arweave.Wallet('wallet.json')
    return "JWK Uploaded"


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
        self.manager.get_theme().load_theme("normal.json")
        if os.path.exists('wallet.json'):
            self.wallet = arweave.Wallet('wallet.json')
        else:
            self.wallet = None

        self.back_btn = UIButton(pygame.Rect(
            (0, 0), (100, 50)), text="Back", manager=self.manager)
        self.addres_text = UILabel(pygame.Rect(
            (0, 50), (state["res"][0], 50)), text=self.wallet.address if self.wallet else 'NO WALLET', manager=self.manager)
        self.balance_text = UILabel(pygame.Rect(
            (0, 100), (state["res"][0], 50)), text=f"Balance: {self.wallet.balance if self.wallet else 'NO WALLET'} AR", manager=self.manager)
        self.portal_url_pre = UILabel(pygame.Rect(
            (0, 150), (state["res"][0], 50)), text=f"http://infinitycam.local:8080", manager=self.manager)
        UILabel(pygame.Rect(
            (0, 170), (state["res"][0], 50)), text="or", manager=self.manager)
        self.portal_url_dyn = UILabel(pygame.Rect(
            (0, 190), (state["res"][0], 50)), text=f"http://{hn}:8080", manager=self.manager)

        # self.flask_process = multiprocessing.Process(target=run_server)
        # self.flask_process.start()
        # subprocess.run("cd cam-py && gunicorn -w 1 wallet:app -b 0.0.0.0:8080")
        self.flask_process = subprocess.Popen(
            "cd cam-py && gunicorn -w 1 wallet:app -b 0.0.0.0:8080", shell=True)

    def run(self, event: pygame.event.EventType):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            btn: UIButton = event.ui_element
            if btn == self.back_btn:
                self.flask_process.terminate()
                self.flask_process.kill()
                self.set_screen("Settings")

    def run_non_event(self):
        pass
