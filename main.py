import json
import sys
import threading
import subprocess
import time
import argparse
import tkinter as tk
from mitmproxy import http
from mitmproxy.tools.main import mitmdump
import number_command

# 请求处理函数
def request(flow: http.HTTPFlow) -> None:
    pass

# 响应处理函数
def response(flow: http.HTTPFlow) -> None:
    url = flow.request.url
    if "https://xyks.yuanfudao.com/leo-math/android/exams?" in url:
        handle_response(flow.response.text, "练习")
    elif "https://xyks.yuanfudao.com/leo-game-pk/android/math/pk/match?" in url:
        handle_response(flow.response.text, "pk")

# 处理并解析响应信息
def handle_response(response_text, answer_type):
    try:
        answer = json.loads(response_text)
        print(json.dumps(answer, indent=4))  # 格式化输出
        save_answers(answer, answer_type)
    except json.JSONDecodeError:
        print("JSON 解析错误")

# 保存答案
def save_answers(answer, answer_type):
    select_answer = parse_answers(answer, answer_type)
    
    # 保存到txt文件
    with open("answer.txt", "w") as f:
        f.write("  ".join(select_answer))
    
    # 启动GUI线程
    threading.Thread(target=gui_answer, args=(select_answer,)).start()

# 解析答案
def parse_answers(answer, answer_type):
    select_answer = []
    questions = answer["questions"] if answer_type == "练习" else answer["examVO"]["questions"]
    
    for question in questions:
        correct_answer = next((ans for ans in question["answers"] if "." in ans), question["answers"][0])
        select_answer.append(correct_answer)
        print(correct_answer, end="  ")
    
    return select_answer

# 执行滑动操作
def answer_write(answer):
    for ans in answer:
        number_command.swipe_screen(ans)
        time.sleep(0.3)  # 可根据需求调整

# GUI界面控制
def gui_answer(answer):
    root = tk.Tk()
    root.title("继续执行")

    label = tk.Label(root, text="请待可作答时点击继续", font=("Helvetica", 14))
    label.pack(pady=10, anchor="center")

    def on_button_click():
        root.destroy()  # 关闭窗口
        answer_write(answer)  # 继续执行代码

    button = tk.Button(root, text="点击继续", command=on_button_click)
    button.pack(pady=20)

    # 12.5秒后自动点击按钮
    root.after(12500, on_button_click)
    root.mainloop()

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

# 主程序
if __name__ == "__main__":
    check_adb_installed()

    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Mitmproxy script")
    parser.add_argument("-P", "--port", type=int, default=8080, help="Port to listen on")
    parser.add_argument("-H", "--host", type=str, default="0.0.0.0", help="Host to listen on")
    args = parser.parse_args()

    # 运行mitmdump
    sys.argv = ["mitmdump", "-s", __file__, "--listen-host", args.host, "--listen-port", str(args.port)]
    mitmdump()
