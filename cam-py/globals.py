import os
import json

config_path = "config.json"

state = {
    "app_name": "Clickoor",
    "commit": "",
    "res": (800, 480),
    "image_res": (1920, 1080)
}


def get_version():
    with open("current", "r") as f:
        return f.read().strip()


def get_config(key: str):
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            data = json.load(f)
            return data.get(key)
    return None


def set_config(key: str, value: str):
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            data = json.load(f)
    else:
        data = {}
    data[key] = value
    with open(config_path, "w") as f:
        json.dump(data, f)
