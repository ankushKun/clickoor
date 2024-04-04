import subprocess


def run_cmd(cmd: str):
    res = subprocess.run(cmd, shell=True, capture_output=True)
    res.check_returncode()
    try:
        return res.stdout.decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        return e.stderr.decode("utf-8").strip()
