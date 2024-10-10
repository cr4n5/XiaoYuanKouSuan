import subprocess

from log import logger

adb_ip = "127.0.0.1"
adb_port = 16384


def adb_status():
    _result = subprocess.check_output("adb devices", shell=True).decode()
    if "device" in _result and "List of devices attached" in _result:
        lines = _result.splitlines()
        for line in lines:
            if "device" in line and not line.startswith("List"):
                logger.info(f"已连接到:{line}")
                return True
    return subprocess.run(["adb", "connect", f"{adb_ip}:{adb_port}"])


def get_device_resolution():
    result = subprocess.run(["adb", "shell", "wm", "size"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = result.stdout
    if "Physical size" in output:
        resolution_str = output.split(":")[-1].strip()
        width, height = map(int, resolution_str.split("x"))
        return width, height
    else:
        raise Exception("无法获取设备分辨率")


def run_adb_command(commands):
    for command in commands:
        result = subprocess.run(["adb", "shell", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            logger.error(f"命令执行失败: {result.stderr}")
