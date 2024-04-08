#!/usr/bin/bash

me=$(whoami)
cd /home/$me/infinitycam

# Install deps

# sudo apt install i3

# Create a virtual environment

echo "Setting up virtual environment"
python3 -m venv --system-site-packages venv

echo "Activating virtual environment"
source venv/bin/activate

echo "Installing dependencies"
pip3 install -r cam-py/requirements.txt --no-cache

echo "Setup Complete"
echo "Run start.sh to start the camera"