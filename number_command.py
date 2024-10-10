import subprocess
from functools import lru_cache

# 以作者的测试平板分辨率为基准（1800x2880）
# 已在小米 13 测试（1080x2400）
BASE_COORDINATES = {
    "1": [[1480, 1050], [1440, 1470]],
    "2": [[1255, 1100], [1700, 1100], [1255, 1470], [1700, 1470]],
    "3": [[1344, 1040], [1600, 1200], [1270, 1323], [1635, 1379], [1249, 1588]],
    "4": [[1716, 1274], [1245, 1296], [1450, 1030], [1450, 1466]],
    "5": [[1558, 1020], [1290, 1211], [1600, 1348], [1300, 1472]],
    "6": [[1533, 1027], [1265, 1428], [1663, 1439]],
    ">": [[[1350, 1080], [1545, 1172], [1295, 1297]]],
    "<": [[[1578, 1058], [1308, 1231], [1560, 1292]]],
    "=": [[[1284, 1122], [1700, 1122], [1280, 1300], [1700, 1300]]]
}

@lru_cache()
def get_device_resolution():
    result = subprocess.run(["adb", "shell", "wm", "size"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = result.stdout
    if "Physical size" in output:
        resolution_str = output.split(":")[-1].strip()
        width, height = map(int, resolution_str.split("x"))
        return width, height
    else:
        raise Exception("无法获取设备分辨率")

def run_adb_command(command):
    # 使用 Popen 打开一个持久的 adb shell 会话并发送所有命令
    try:
        with subprocess.Popen(["adb", "shell"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
            stdout, stderr = process.communicate(command)
            if stderr:
                print(f"ADB 错误: {stderr}")
            return stdout
    except Exception as e:
        print(f"ADB 命令执行失败: {e}")
        return None

def swipe_screen(command_str, base_resolution=(1800, 2880)):
    current_resolution = get_device_resolution()
    scale_factor_x = current_resolution[0] / base_resolution[0]
    scale_factor_y = current_resolution[1] / base_resolution[1]

    xy_paths = str_to_xy(command_str, scale_factor_x, scale_factor_y)
    all_commands = ""
    if xy_paths:
        for path in xy_paths:
            for i in range(len(path) - 1):
                command = f"input swipe {path[i][0]} {path[i][1]} {path[i+1][0]} {path[i+1][1]} 0"
                all_commands += command + "\n"
        run_adb_command(all_commands)

def scale_coordinates(base_coordinates, scale_x, scale_y):
    # 缩放所有坐标
    return [[(int(x * scale_x), int(y * scale_y)) for (x, y) in path] for path in base_coordinates]

def str_to_xy(command_str, scale_x, scale_y):
    if command_str in BASE_COORDINATES:
        return scale_coordinates(BASE_COORDINATES[command_str], scale_x, scale_y)
    else:
        return None

if __name__ == "__main__":
    # 执行滑动操作
    swipe_screen("<")
    swipe_screen("=")
