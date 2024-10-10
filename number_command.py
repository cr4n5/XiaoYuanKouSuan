import time
import subprocess
from functools import lru_cache

# 以作者的测试平板分辨率为基准（1800x2880）
# 已在小米 13 测试（1080x2400）
BASE_COORDINATES = {
    "1": [[[1480, 1050], [1440, 1470]]],
    "2": [[[1255, 1100], [1700, 1100], [1255, 1470], [1700, 1470]]],
    "3": [[[1344, 1040], [1600, 1200], [1270, 1323], [1635, 1379], [1249, 1588]]],
    "4": [[[1716, 1274], [1245, 1296], [1450, 1030], [1450, 1466]]],
    "5": [[[1558, 1020], [1290, 1211], [1600, 1348], [1300, 1472]]],
    "6": [[[1533, 1027], [1265, 1428], [1663, 1439]]],
    ">": [[[1350, 1080], [1545, 1172], [1295, 1297]]],
    "<": [[[1578, 1058], [1308, 1231], [1560, 1292]]],
    "=": [[[1284, 1122], [1700, 1122], [1280, 1300], [1700, 1300]]]
}

NEXT_BUTTON_COORDINATES = {
    "next_1": [1400, 900], 
    "next_2": [2160, 1720], 
    "next_3": [1475, 1490], 
}

scale_x = 1
scale_y = 1

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

def run_adb_command(commands):
    # 批量执行 ADB 命令
    for command in commands:
        result = subprocess.run(["adb", "shell", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"命令执行失败: {result.stderr}")

def swipe_screen(command_str, base_resolution=(1800, 2880)):
    current_resolution = get_device_resolution()
    global scale_x
    global scale_y
    scale_x = current_resolution[0] / base_resolution[0]
    scale_y = current_resolution[1] / base_resolution[1]

    xy_paths = str_to_xy(command_str, scale_x, scale_y)
    if xy_paths:
        adb_commands = []
        for path in xy_paths:
            for i in range(len(path) - 1):
                adb_commands.append(f"input swipe {path[i][0]} {path[i][1]} {path[i+1][0]} {path[i+1][1]} 0")
        # 批量执行命令
        run_adb_command(adb_commands)

def scale_coordinates(base_coordinates, scale_x, scale_y):
    # 缩放所有坐标
    return [[(int(x * scale_x), int(y * scale_y)) for (x, y) in path] for path in base_coordinates]

def scale_coordinates_for_tap(coordinate, scale_x, scale_y):
    # 缩放一个点坐标
    return [int(coordinate[0] * scale_x), int(coordinate[1] * scale_y)]

def str_to_xy(command_str, scale_x, scale_y):
    if command_str in BASE_COORDINATES:
        return scale_coordinates(BASE_COORDINATES[command_str], scale_x, scale_y)
    else:
        return None

def click_screen(xy):
    command = [f"input tap {xy[0]} {xy[1]}"]
    run_adb_command(command)

def next_round():
    click_screen( scale_coordinates_for_tap(NEXT_BUTTON_COORDINATES["next_1"], scale_x, scale_y) )
    time.sleep(0.5)
    click_screen( scale_coordinates_for_tap(NEXT_BUTTON_COORDINATES["next_2"], scale_x, scale_y) )
    time.sleep(0.5)
    click_screen( scale_coordinates_for_tap(NEXT_BUTTON_COORDINATES["next_3"], scale_x, scale_y) )

if __name__ == "__main__":
    # 执行滑动操作
    swipe_screen("<")
    swipe_screen("=")
    swipe_screen("1")
    # swipe_screen("7")
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    
    # # 依次执行手写，每个数字之间延迟1秒
    # for number in numbers:
    #     print(f"Drawing number {number}")
    #     swipe_screen(number)
    #     time.sleep(1)  # 延迟1秒
    
    
