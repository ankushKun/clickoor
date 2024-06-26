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

# replace pi with $me in camera.desktop file
sed -i "s/pi/$me/" configuration/camera.desktop

sudo cp configuration/camera.desktop /etc/xdg/autostart
sudo cp configuration/camera.desktop /usr/share/applications
sudo cp configuration/disp-invert.desktop /usr/share/applications
sudo cp configuration/disp-normal.desktop /usr/share/applications

# sudo cp configuration/40-libinput.conf /etc/X11/xorg.conf.d/40-libinput.conf

# add bin/ to path
chmod +x bin/startcam
sudo cp bin/startcam /usr/local/bin

# add startcamera autoexec to bashrc if its not already there
if ! grep -q "startcam" ~/.bashrc; then
    echo "Adding startcam to ~/.bashrc"
    echo "startcam" >> ~/.bashrc
fi

sudo cp configuration/splash.png /usr/share/plymouth/themes/pix/splash.png
sudo plymouth-set-default-theme --rebuild-initrd pix

echo "Setup Complete"
echo "Run Menu > Other > Clickoor Camera, or Run startcam from cli mode"

sudo raspi-config nonint do_boot_behaviour B2

sudo reboot now
