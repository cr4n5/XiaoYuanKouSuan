import subprocess

def run_adb_command(command):
    # 打开一个持久的 adb shell 会话
    shell_process = subprocess.Popen(["adb", "shell"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    shell_process.communicate(command)
    shell_process.stdin.close()

def swipe_screen(str):
    xy = str_to_xy(str)
    all_commands = "\n"
    if xy:
        for i in range(len(xy)):
            for j in range(len(xy[i]) - 1):
                command = f"input swipe {xy[i][j][0]} {xy[i][j][1]} {xy[i][j+1][0]} {xy[i][j+1][1]} 0"
                all_commands += command + "\n"
        all_commands += "exit\n"
        run_adb_command(all_commands)
        

def str_to_xy(str):
    match str:
        case "1":
            return [[1480, 1050], [1440, 1470]]
        case "2":
            return [[1255, 1100], [1700, 1100], [1255, 1470], [1700, 1470]]
        case "3":
            return [[1344, 1040], [1600, 1200], [1270, 1323], [1635, 1379], [1249, 1588]]
        case "4":
            return [[1716, 1274],[1245,1296],[1450,1030],[1450,1466]]
        case "5":
            return [[1558,1020],[1290,1211],[160,1348],[1300.1472]]
        case "6":
            return [[1533,1027],[1265,1428],[1663,1439]]
        case ">":
            return [[[1350, 1080], [1545, 1172], [1295, 1297]]]
        case "<":
            return [[[1578,1058],[1308,1231],[1560,1292]]]
        case "=":
            return [[[1284, 1122], [1700, 1122]],[[1280, 1300], [1700, 1300]]]

if __name__ == "__main__":
    
    # 执行滑动操作
    swipe_screen("<")
    swipe_screen("=")
    
