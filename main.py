from mitmproxy import http
import json
from mitmproxy.tools.main import mitmdump
import sys
import threading
import os
import subprocess
import number_command
import time
import tkinter as tk
from tkinter import messagebox
import argparse

def request(flow: http.HTTPFlow) -> None:
    # 处理请求
    # print(f"Request: {flow.request.method} {flow.request.url}")
    pass

def response(flow: http.HTTPFlow) -> None:
    # 处理响应
    
    print(f"Response: {flow.response.status_code} {flow.request.url}")
    # 如果url中包含指定的关键字，则打印响应信息
    if "https://xyks.yuanfudao.com/leo-math/android/exams?" in flow.request.url:
        # 将响应信息转换为json格式
        answer = json.loads(flow.response.text)
        # 格式化输出
        print(json.dumps(answer, indent=4))
        # 保存到文件
        # with open("answer.json", "w") as f:
        #     f.write(json.dumps(answer, indent=4))
        select_answer(answer,"练习")
    elif "https://xyks.yuanfudao.com/leo-game-pk/android/math/pk/match?" in flow.request.url:
        # 将响应信息转换为json格式
        answer = json.loads(flow.response.text)
        # 格式化输出
        print(json.dumps(answer, indent=4))
        # 保存到文件
        # with open("answer.json", "w") as f:
        #     f.write(json.dumps(answer, indent=4))
        select_answer(answer,"pk")

def answer_write(answer):
    
    for i in range(len(answer)):
        number_command.swipe_screen(answer[i])
        # time.sleep(0.16)
        time.sleep(0.3)

def select_answer(answer, type):
    # 关闭notepad
    # os.system("taskkill /f /im notepad.exe")

    # 并保存到txt文件
    f = open("answer.txt", "w")

    select_answer = []

    if type == "练习":
        for question in answer["questions"]:
            answers=question["answers"]
            for i in range(len(answers)):
                if "." in answers[i]:
                    correct_answer = answers[i]
                    break
                if i == len(answers)-1:
                    correct_answer = answers[0]
                
            select_answer.append(correct_answer)
            print(correct_answer, end="  ")
            f.write(str(correct_answer) + "  ")
    elif type == "pk":
        for question in answer["examVO"]["questions"]:
            answers=question["answers"]
            for i in range(len(answers)):
                if "." in answers[i]:
                    correct_answer = answers[i]
                    break
                if i == len(answers)-1:
                    correct_answer = answers[0]
                
            select_answer.append(correct_answer)
            print(correct_answer, end="  ")
            f.write(str(correct_answer) + "  ")
    
    # 关闭文件
    f.close()

    threading.Thread(target=gui_answer, args=(select_answer,)).start()

    # 用记事本打开文件
    # os.system("notepad answer.txt")
    # threading.Thread(target=os.system, args=("notepad answer.txt",)).start()
    
def gui_answer(answer):
    # 创建一个GUI
    root = tk.Tk()
    root.title("继续执行")
    
    def on_button_click():
        root.destroy()  # 关闭窗口
        answer_write(answer)  # 继续执行代码
    
    # 创建一个按钮
    button = tk.Button(root, text="点击继续", command=on_button_click)
    button.pack(pady=20)
    
    # 运行 GUI 界面
    root.mainloop()

    # time.sleep(4)
    # answer_write(answer)
    # time.sleep(7)
    # command = "input tap 1445 1272"
    # number_command.run_adb_command(command)
    # time.sleep(0.1)
    # command = "input tap 2144 1694"
    # number_command.run_adb_command(command)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mitmproxy script")
    parser.add_argument("-p", "--port", type=int, default=8080, help="Port to listen on")
    parser.add_argument("-h", "--host", type=str, default="0.0.0.0", help="Host to listen on")
    args = parser.parse_args()

    sys.argv = ["mitmdump", "-s", __file__, "--listen-host", args.host, "--listen-port", str(args.port)]
    mitmdump()