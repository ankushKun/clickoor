import subprocess
import time


def run_cmd(cmd: str):
    res = subprocess.run(cmd, shell=True, capture_output=True)
    try:
        res.check_returncode()
        return res.stdout.decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        return e.stderr.decode("utf-8").strip()


def get_wifi_signal_strength():
    """Get the signal strength of the connected Wi-Fi network.

    Returns:
        The signal strength in dBm.
    """

    try:
        output = run_cmd("iwconfig")
        x = output.split("Link Quality=")[
            1].split("  Signal level=")[0].split("/")
        # print(x)
        return int(int(x[0])/int(x[1])*100)
    except Exception as e:
        # print(e)
        return 0


def connect_to_wifi(ssid: str, password: str):
    """Connects to a WiFi network.

    Args:
        ssid: The name of the WiFi network.
        password: The password for the WiFi network.
    """

    subprocess.call(f"sudo iwconfig wlan0 essid {ssid}")
    # subprocess.call(["sudo", "iwconfig", "wlan0", "key", password])
    subprocess.call(f"sudo iwconfig wlan0 key s:{password}")
    time.sleep(5)
    subprocess.call(["sudo", "dhclient", "wlan0"])
