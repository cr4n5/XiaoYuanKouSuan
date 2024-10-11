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
import getExerciseJs
# CONFIG #
tick_time = 0.3    # 每题间隔时间
start_time = 12.5    # 开始做题前摇时间


def request(flow: http.HTTPFlow) -> None:
    # 处理请求
    # print(f"Request: {flow.request.method} {flow.request.url}")
    pass

def response(flow: http.HTTPFlow) -> None:
    # 处理响应

    print(f"Response: {flow.response.status_code} {flow.request.url}")

    ''' 原方案
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
    
    '''

    if "https://leo.fbcontent.cn/bh5/leo-web-oral-pk/exercise_" in flow.request.url:
        # 初始化 text 变量
        text = None
    
    # 查询本地是否有 exercise.js
        try:
            with open("exercise.js", "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            # 如果没有则下载
            print("未找到 exercise.js，正在下载")
            with open("original.js", "w", encoding="utf-8") as f:
                f.write(flow.response.text)
            getExerciseJs.replace_and_change_js("original.js", "exercise.js")
        
            # 重新读取生成的 exercise.js
            with open("exercise.js", "r", encoding="utf-8") as f:
                text = f.read()
    
        # 确保 text 变量有值
        if text is not None:
            flow.response.text = text
            print("修改成功")
        else:
            print("未能修改响应文本")

    

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

    q_num = len(select_answer)
    threading.Thread(target=gui_answer, args=(select_answer,q_num,)).start()

    # 用记事本打开文件
    # os.system("notepad answer.txt")
    # threading.Thread(target=os.system, args=("notepad answer.txt",)).start()
    
def gui_answer(answer,q_num):
    # 创建一个GUI
    root = tk.Tk()
    root.title("继续执行")
    
    def on_button_click():
        answer_write(answer)  # 继续执行代码

    def on_button2_click():
        number_command.next_round()  # 继续执行代码
        root.destroy()
    
    # 创建一个按钮
    button = tk.Button(root, text="点击继续", command=on_button_click)
    button2 = tk.Button(root, text="下一把", command=on_button2_click)
    button.pack(pady=20)
    button2.pack(pady=20)
    
    # 设置定时器，若干秒后自动点击按钮
    time = int(start_time * 1000)
    root.after(time, on_button_click)
    time2 = int((start_time + tick_time * 1.15 * q_num + 5) * 1000)
    root.after(time2, on_button2_click)
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
    parser.add_argument("-P", "--port", type=int, default=8080, help="Port to listen on")
    parser.add_argument("-H", "--host", type=str, default="0.0.0.0", help="Host to listen on")
    args = parser.parse_args()

    sys.argv = ["mitmdump", "-s", __file__, "--listen-host", args.host, "--listen-port", str(args.port)]

    mitmdump()
