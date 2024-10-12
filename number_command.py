import subprocess
from functools import lru_cache

# 以作者的测试平板分辨率为基准（1800x2880）
# 已在小米 13 测试（1080x2400）
BASE_RESOLUTION = (1800, 2880)

# 坐标点信息
BASE_COORDINATES = {
    "1": [[1480, 1050], [1440, 1470]],
    "2": [[1255, 1100], [1700, 1100], [1255, 1470], [1700, 1470]],
    "3": [[1344, 1040], [1600, 1200], [1270, 1323], [1635, 1379], [1249, 1588]],
    "4": [[1716, 1274], [1245, 1296], [1450, 1030], [1450, 1466]],
    "5": [[1558, 1020], [1290, 1211], [1600, 1348], [1300, 1472]],
    "6": [[1533, 1027], [1265, 1428], [1663, 1439]],
    ">": [[[1350, 1080], [1545, 1172], [1295, 1297]]],
    "<": [[[1578, 1058], [1308, 1231], [1560, 1292]]],
    "=": [[[1284, 1122], [1700, 1122], [1280, 1300], [1700, 1300]]],
    ".": [1350, 1080]  # 单独的点
}

@lru_cache()
def get_device_resolution():
    # 获取设备的物理分辨率，并缓存
    result = subprocess.run(["adb", "shell", "wm", "size"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = result.stdout
    if "Physical size" in output:
        resolution_str = output.split(":")[-1].strip()
        width, height = map(int, resolution_str.split("x"))
        return width, height
    else:
        raise Exception("无法获取设备分辨率")

def run_adb_command(commands):
    # 执行 ADB 命令，减少 subprocess 调用次数
    try:
        command_str = "\n".join(commands) + "\n"
        result = subprocess.run(["adb", "shell"], input=command_str, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.stderr:
            print(f"ADB 错误: {result.stderr}")
        return result.stdout
    except Exception as e:
        print(f"ADB 命令执行失败: {e}")
        return None

def tap_screen(command_str):
    current_resolution = get_device_resolution()
    scale_x = current_resolution[0] / BASE_RESOLUTION[0]
    scale_y = current_resolution[1] / BASE_RESOLUTION[1]

    xy_paths = str_to_xy(command_str, scale_x, scale_y)
    if xy_paths:
        adb_commands = []
        # 处理单个点或多个点路径
        if isinstance(xy_paths[0], tuple):
            adb_commands.append(f"input tap {xy_paths[0][0]} {xy_paths[0][1]}")
        else:
            for path in xy_paths:
                adb_commands.extend([f"input tap {x} {y}" for (x, y) in path])
        # 一次性发送所有命令，减少 subprocess 开销
        run_adb_command(adb_commands)

def scale_coordinates(base_coordinates, scale_x, scale_y):
    # 根据设备分辨率缩放坐标
    if isinstance(base_coordinates[0], list):
        return [[(int(x * scale_x), int(y * scale_y)) for (x, y) in path] for path in base_coordinates]
    else:
        x, y = base_coordinates
        return [(int(x * scale_x), int(y * scale_y))]

def str_to_xy(command_str, scale_x, scale_y):
    # 将指令转换为坐标
    if command_str in BASE_COORDINATES:
        return scale_coordinates(BASE_COORDINATES[command_str], scale_x, scale_y)
    return None

if __name__ == "__main__":
    # 确保以 root 权限运行
    subprocess.run(["adb", "root"])  # 启动 adb root 权限
    subprocess.run(["adb", "wait-for-device"])  # 等待设备准备好
    # 执行点击操作
    tap_screen("<")
    tap_screen("=")
