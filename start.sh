#!/usr/bin/bash

cd /home/pi/infinitycam
source venv/bin/activate
DISPLAY=:0 python3 cam-py/main.py