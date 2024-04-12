# Clickoor Camera



<details>
<summary> <h3 style="display:inline;">Components</h2> </summary>

<details>
<summary>Hardware</summary>

- [Raspberry Pi 4b](https://robu.in/product/raspberry-pi-4-model-b-with-2-gb-ram/)
- [Raspberry Pi HQ Camera](https://robu.in/product/raspberry-pi-hq-camera/) (or any compatible camera module)
- [Raspi HQ Cam C mount lens](https://robu.in/product/16mm-telephoto-lens-for-raspberry-pi-high-quality-camera/) (optional depending on what camera module you use)
- [Waveshare 4.3" touchscreen DSI display](https://robu.in/product/waveshare-4-3-inch-capacitive-touch-display-for-raspberry-pi-800x480/) (or any compatible display)
- [18650 Li-ion battery](https://robu.in/product/panasonic-ncr18650ga-3300mah-3c-li-ion-battery/)
- [Powerbank charger module](https://amzn.in/d/1pB2MlH) with LCD (generic)
- [R13-507 button](https://robu.in/product/red-r13-507-16mm-no-lock-push-button-momentary-switch-3a-250v/) for shutter
- [Slide switch](https://robu.in/product/slide-switch-ss-12f15-1p2t/) for power

Other common components such as microSD card, keyboard, mouse, hdmi display etc.
</details>

<details>
<summary>Software</summary>

- [Raspberry Pi OS](https://www.raspberrypi.com/software/)
- [i3](https://i3wm.org/) (window manager)
- [pygame_gui](https://pygame-gui.readthedocs.io/en/), [pygame-ce](https://pyga.me/)
- [Picamera2](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)
- [gpiozero](https://gpiozero.readthedocs.io/en/stable/)

</details>
</details>


## Setup

<details>
<summary>Wifi (using `nmtui` if not already setup)</summary>
    
```bash
sudo nmtui
```

Has a nice ncurses interface to connect to wifi networks

</details>

<details>
<summary>Update and Upgrade always</summary>

```bash
sudo apt update
sudo apt upgrade
```

</details>

<details>
<summary>Pi HQ Camera</summary>

Connect the camera module to the camera port using the provided ribbon cable.

No specific setup is needed in case of pi 4b, the camera module should be detected automatically.

</details>

<details>
<summary>Touchscreen Display</summary>

No setup needed for the 4.3" Waveshare touchscreen display, it should be detected automatically.

If using a cheaper 3.5" display, follow these steps:

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
<summary>Python GUI (pygame)</summary>

```bash
cd clickoor
bash scripts/setup.sh
bash scripts/start.sh
```

</details>

<details>
<summary>i3</summary>

install i3wm

```bash
sudo apt install i3
sudo apt remove i3lock # we dont want lockscreen
```

Configure to boot into cli and autologin using raspi-config

run `sudo raspi-config` -> Boot Options -> Desktop / CLI -> Console Autologin

Configure to use i3 instead of lxde

open `.bashrc` and add this line at the end

```bash
startx /usr/bin/i3
```

<details>
<summary>Different method (Better way but doesnot always work, skill issue)</summary>

```bash
cd /etc/xdg/lxsession/LXDE-pi
```

1. edit `desktop.conf` and set `window_manager=i3` (located at first line)
2. edit `autostart` and comment all lines about lxpanel, pcmanfm and xscreensaver because we dont want lxde stuff in i3
</details>


Add this to the end of your i3 config file (located at ~/.config/i3/config)

```bash
bindsym $mod+x exec "i3-msg exit"
bindsym $mod+c exec "bash /home/pi/clickoor/scripts/start.sh"
bindsym $mod+i exec "x-terminal-emulator -e nmtui"
exec_always --no-startup-id "bash /home/pi/clickoor/scripts/start.sh"
```

or copy the config file in `configuration/config` to `~/.config/i3/config`

</details>

## TODO:

- [ ] Automated setup.sh script for configuring everything
- [ ] Changable resolution
- [ ] Video recording option
- [ ] Options for creation of jwk for first time users
- [ ] Turbo sdk integration (through ardrive-cli?)
- [ ] Image compression under 500kb
- [x] Save each image as new timestamped file instead of overwriting
- [x] Gallery images view, incl. local and onchain images
- [x] Wallet options for change seed, upload jwk file (through a webserver)
- [x] Upload selected images from gallery to Arweave
- [x] Wifi connection from Wifi Screen
- [x] Pull latest code whenever there is an update
