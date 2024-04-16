#!/usr/bin/bash

me=$(whoami)
cd /home/$me/clickoor

bash scripts/update.sh

source venv/bin/activate
DISPLAY=:0 xrandr -o inverted
DISPLAY=:0 python3 cam-py/main.py
