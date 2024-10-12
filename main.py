from mitmproxy import http
from mitmproxy.tools.main import mitmdump
import re
import threading
import number_command
import tkinter as tk
from tkinter import messagebox
import argparse
import sys
import time
import subprocess
import getExerciseJs
import json
import os

# CONFIG
is_dialog_shown = False
ANSWER_COUNT = 30
WAITING_TIME = 12.5
APP_PACKAGE_NAME = "com.fenbi.android.leo"
CONFIG_FILE = "user_config.json"
FIRST_RUN_KEY = "first_run"

class UserConfig:
    def __init__(self, config_file=CONFIG_FILE):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        # 加载配置文件
        if not os.path.exists(self.config_file):
            return {FIRST_RUN_KEY: True}
        with open(self.config_file, "r") as f:
            return json.load(f)

    def save_config(self):
        # 保存配置文件
        with open(self.config_file, "w") as f:
            json.dump(self.config, f)

    def is_first_run(self):
        # 检查是否为首次运行
        return self.config.get(FIRST_RUN_KEY, True)

    def mark_first_run_done(self):
        # 标记首次运行已完成
        self.config[FIRST_RUN_KEY] = False
        self.save_config()

def request(flow: http.HTTPFlow) -> None:
    pass

def response(flow: http.HTTPFlow) -> None:

    global is_dialog_shown
    url = flow.request.url
    print(f"Response: {flow.response.status_code} {url}")

    if is_target_url(url):
        handle_target_response(flow, url)
    elif "https://xyks.yuanfudao.com/leo-game-pk/android/math/pk/match/v2?" in url:
        if not is_dialog_shown:
            is_dialog_shown = True
            threading.Thread(target=gui_answer).start()

def is_target_url(url):
    return re.search(r"leo\.fbcontent\.cn/bh5/leo-web-oral-pk/exercise_.*\.js", url)

def handle_target_response(flow, url):
    print(f"匹配到指定的 URL: {url}")
    responsetext = flow.response.text
    funname = extract_function_name(responsetext)

    if funname:
        update_response_text(flow, responsetext, funname)
    else:
        print("未找到匹配的函数名，无法进行替换。")

def extract_function_name(responsetext):
    match = re.search(r"(?<=isRight:)[^,]*?\(.*?\).*?(?=\|)", responsetext)
    return match.group() if match else None

def update_response_text(flow, responsetext, funname):
    print(f"找到函数名: {funname}")
    updated_text = responsetext.replace(funname, f"{funname}||true")
    flow.response.text = updated_text
    print(f"替换后的响应: {updated_text}")
    threading.Thread(target=show_message_box, args=("过滤成功", f"函数 {funname} 替换成功!")).start()

def show_message_box(title, message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title, message)
    root.destroy()

def answer_write(prepared_commands):
    start_time = time.time()
    # 一次性发送准备好的 ADB 命令
    number_command.run_adb_command(prepared_commands)
    end_time = time.time()
    print(f"点击操作耗时: {end_time - start_time:.3f}秒")

def gui_answer():
    # 预先准备 ADB 命令
    prepared_commands = number_command.prepare_tap_commands(".", ANSWER_COUNT)

    root = tk.Tk()
    root.title("继续执行")
    button = tk.Button(root, text="点击继续", command=lambda: answer_write(prepared_commands))
    button.pack(pady=20)

    # 设置定时器自动执行
    threading.Timer(WAITING_TIME, auto_click_and_close, args=(root, prepared_commands)).start()
    
    root.mainloop()

def auto_click_and_close(root, prepared_commands):
    answer_write(prepared_commands)
    global is_dialog_shown
    is_dialog_shown = False
    root.destroy()

# 检查 adb 是否安装
def check_adb_installed():
    try:
        result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"ADB 检查失败: {result.stderr}")
            sys.exit(1)
    except FileNotFoundError:
        print("ADB 未找到，请先安装 ADB 工具。")
        sys.exit(1)

# ADB 连接设备
def connect_adb_wireless(adb_ip):
    try:
        result = subprocess.run(["adb", "connect", adb_ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "connected" not in result.stdout:
            print(f"ADB 连接失败: {result.stderr}")
            sys.exit(1)
        print(f"已连接到 {adb_ip}")
    except subprocess.CalledProcessError as e:
        print(f"ADB 连接错误: {e}")
        sys.exit(1)

def clear_and_restart_app(package_name):
    # 清除应用数据并重启应用
    subprocess.run(["adb", "shell", "am", "force-stop", package_name])
    # 还没想到如何仅清除缓存，先暂时用清除全部数据方式替换
    subprocess.run(["adb", "shell", "pm", "clear", package_name])
    subprocess.run(["adb", "shell", "am", "start", "-n", f"{package_name}/.activity.RouterActivity"])
    print(f"已清除缓存并重启应用: {package_name}")


if __name__ == "__main__":
    check_adb_installed()
    config = UserConfig()

    # 检查是否为首次运行
    if config.is_first_run():
        clear_and_restart_app(APP_PACKAGE_NAME)
        config.mark_first_run_done()
        show_message_box("首次运行", "应用已停止并清除缓存，现在重新启动...")

    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Mitmproxy script")
    parser.add_argument("-P", "--port", type=int, default=8080, help="Port to listen on")
    parser.add_argument("-H", "--host", type=str, default="0.0.0.0", help="Host to listen on")
    parser.add_argument("-AI", "--adb-ip", type=str, help="IP and port for ADB wireless connection (e.g., 192.168.0.101:5555)")
    args = parser.parse_args()

    # 如果指定了 ADB IP，进行无线调试连接
    if args.adb_ip:
        connect_adb_wireless(args.adb_ip)

    # 运行 mitmdump
    sys.argv = ["mitmdump", "-s", __file__, "--listen-host", args.host, "--listen-port", str(args.port)]
    mitmdump()