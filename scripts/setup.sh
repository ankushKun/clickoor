#!/usr/bin/bash

me=$(whoami)
cd /home/$me/clickoor


# Install deps

#echo "Installing dependencies"

#sudo apt update
#sudo apt install git -y

# Installing i3wm
#sudo apt install i3 -y
#sudo apt remove i3lock -y # we dont want a lockscreen

# set i3wm as default window manager
#sudo update-alternatives --set x-session-manager /usr/bin/i3
#sudo update-alternatives --set x-window-manager /usr/bin/i3

#mkdir ~/.config/i3
#cp configuration/config ~/.config/i3/config

#cd /etc/xdg/lxsession/LXDE-pi

# in desktop.conf set window_manager=i3
#sudo sed -i 's/window_manager=openbox-lxde-pi/window_manager=i3/' desktop.conf

# comment all lines in autostart
#sudo sed -i 's/^/#/' autostart

################################################

cd /home/$me/clickoor

#sudo apt-get install gcc python3-dev -y
#sudo apt install -y python3-libcamera python3-kms++ libcap-dev

# Create a virtual environment

echo "Setting up virtual environment"
python3 -m venv --system-site-packages venv

echo "Activating virtual environment"
source venv/bin/activate

echo "Installing dependencies"
pip3 install -r cam-py/requirements.txt --no-cache

sudo cp configuration/camera.desktop /etc/xdg/autostart
sudo cp configuration/camera.desktop /usr/share/applications

echo "Setup Complete"
echo "Run Menu > Other > Clickoor Camera"