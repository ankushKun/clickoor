# InfinityCam

# TODO:

- [ ] Sample image save for when running on a non-raspi device (only for testing)
- [ ] Save each image as new timestamped file instead of overwriting
- [ ] Gallery images view, incl. local and onchain images
- [ ] Wallet options for change seed, upload jwk file (through a webserver?)
- [ ] Options for creation of jwk for first time users
- [ ] Upload selected images from gallery to Arweave
- [ ] Wifi connection from Wifi Screen
- [ ] Image compression under 500kb
- [ ] Turbo sdk integration (through changing api or ardrive-cli)
- [ ] Pull latest code whenever there is an update

## Components

<details>
<summary>Hardware</summary>

- Raspberry Pi 4b
- Raspberry Pi Camera Module V3 (or any compatible camera module)
- 3.5" Touchscreen Display compatible with Raspberry Pi (or any compatible display)

Other common components such as a power supply, microSD card, keyboard, mouse, hdmi display etc.
</details>

<details>
<summary>Software</summary>

- Raspbian OS (or any linux based OS). (I'm running 32bit one as I was getting some issues with 64 bit, maybe it's just me)
- Python3
- i3 (window manager)

</details>

## Setup

The following steps assume you are in a headless raspi os lite environment, with a logged in user and working internet.

<details>
<summary>Wifi (using raspi-config if not already setup)</summary>
    
```bash
sudo raspi-config
```

- Select Network Options
- Select Wi-fi
- Enter your SSID and password

</details>

<details>
<summary>Update and Upgrade always</summary>

```bash
sudo apt update
sudo apt upgrade
```

</details>

<details>
<summary>picam v3</summary>

Connect the camera module to the camera port using the ribbon cable.

No specific setup is needed

There might be an error about `libEGL, DRI2: failed to authenticate`, fear not, the cam should be working, this error is related to the camera preview window that fails to run when you use a `rpicam-*` command.

</details>

<details>
<summary>Touchscreen Display</summary>

```bash
git clone https://github.com/goodtft/LCD-show
cd LCD-show
sudo ./LCD35-show
```

Display should start working after an automatic reboot

Install the touchscreen calibrator

```bash
cd LCD-show
sudo apt install ./xinput-calibrator_0.7.5-1_armhf.deb
xinput_calibrator
```

</details>

<details>
<summary>i3</summary>

install i3wm

```bash
sudo apt install i3
sudo apt remove i3lock # we dont want lockscreen
```

Configure to use i3 instead of lxde

```bash
cd /etc/xdg/lxsession/LXDE-pi
```

1. edit `desktop.conf` and set `window_manager=i3` (located at first line)
2. edit `autostart` and comment all lines about lxpanel, pcmanfm and xscreensaver because we dont want lxde stuff in i3


Add this to the end of your i3 config file (usually located at ~/.config/i3/config)

```bash
bindsym $mod+x exec "i3-msg exit" # win+x -> exit i3
exec_always --no-startup-id bash infinitycam/start.sh # autostarts the camera gui when i3 starts
```

</details>

<details>
<summary>Python GUI (pygame)</summary>

```bash
git clone https://github.com/ankushKun/infinitycam
cd infinitycam
python3 -m venv --system-site-packages venv
source venv/bin/activate
pip3 install -r cam-py/requirements.txt --no-cache
```

</details>