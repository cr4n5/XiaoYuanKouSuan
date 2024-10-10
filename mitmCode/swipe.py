from adb import get_device_resolution, run_adb_command

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


def swipe_screen(command_str, base_resolution=(1800, 2880)):
    current_resolution = get_device_resolution()
    scale_factor_x = current_resolution[0] / base_resolution[0]
    scale_factor_y = current_resolution[1] / base_resolution[1]

    xy_paths = str_to_xy(command_str, scale_factor_x, scale_factor_y)
    if xy_paths:
        adb_commands = []
        for path in xy_paths:
            for i in range(len(path) - 1):
                adb_commands.append(f"input swipe {path[i][0]} {path[i][1]} {path[i + 1][0]} {path[i + 1][1]} 0")
        run_adb_command(adb_commands)


def scale_coordinates(base_coordinates, scale_x, scale_y):
    return [[(int(x * scale_x), int(y * scale_y)) for (x, y) in path] for path in base_coordinates]


def str_to_xy(command_str, scale_x, scale_y):
    if command_str in BASE_COORDINATES:
        return scale_coordinates(BASE_COORDINATES[command_str], scale_x, scale_y)
    else:
        return None

