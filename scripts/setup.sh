#!/usr/bin/bash

me=$(whoami)
cd /home/$me/infinitycam

# Install deps

echo "Installing dependencies"

sudo apt update

# Installing i3wm
sudo apt install i3
sudo apt remove i3lock # we dont want a lockscreen

# set i3wm as default window manager
sudo update-alternatives --set x-session-manager /usr/bin/i3
sudo update-alternatives --set x-window-manager /usr/bin/i3

cp config/i3/config ~/.config/i3/config

cd /etc/xdg/lxsession/LXDE-pi

# in desktop.conf set window_manager=i3
sed -i 's/window_manager=openbox-lxde/window_manager=i3/' desktop.conf

# comment all lines in autostart
sed -i 's/^/#/' autostart

################################################

cd /home/$me/infinitycam

# Create a virtual environment

echo "Setting up virtual environment"
python3 -m venv --system-site-packages venv

echo "Activating virtual environment"
source venv/bin/activate

echo "Installing dependencies"
pip3 install -r cam-py/requirements.txt --no-cache

echo "Setup Complete"
echo "Run scripts/start.sh to start the camera"