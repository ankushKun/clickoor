# InfinityCam


## Hardware Components

- Raspberry Pi 3b+ (or 4)
- Raspberry Pi Camera Module V3 (or any compatible camera module)
- 3.5" Touchscreen Display compatible with Raspberry Pi (or any compatible display)

Other common components such as a power supply, microSD card, keyboard, mouse etc.

## Software Components

- Raspbian OS (or any linux based OS), I am running a headless version of Raspi OS Lite, with xorg and i3 setup to auto run a python kivy app on running startx and stop i3 on pressing mod+x


## Setup

The following steps assume you are in a headless raspi os lite environment. \ 
With the user and wifi already setup before flashing with raspi imager.

### Update and Upgrade

```bash
sudo apt update
sudo apt upgrade
```

### picam v3

No setup needed for 3b+. \ 
Connect the camera module to the camera port using the ribbon cable. \ 

pi 4: TBA

### Touchscreen Display

TBA

### Wifi (from raspi-config)
    
```bash
sudo raspi-config
```

- Select Network Options
- Select Wi-fi
- Enter your SSID and password

### Python GUI

```bash
cd gui
python3 -m venv venv
source venv/bin/activate
venv/bin/python3 -m pip install -r requirements.txt
venv/bin/python3 -m python3 main.py # will start the GUI in fullscreen if an xorg display is available
```

### i3

Add this to the end of your i3 config file (usually located at ~/.config/i3/config)

```bash
bindsym $mod+x exec "i3-msg exit" # to stop the gui and exit i3
exec_always --no-startup-id python3 ~/camera.py # autostarts the gui when i3 starts
```

To autostart i3 on boot, add a  cronjob (not recommended for dev setups)

```bash
@reboot startx
```