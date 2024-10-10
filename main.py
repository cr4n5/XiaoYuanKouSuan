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
    pass


def response(flow: http.HTTPFlow) -> None:
    print(f"Response: {flow.response.status_code} {flow.request.url}")
    if "https://xyks.yuanfudao.com/leo-math/android/exams?" in flow.request.url:
        answer = json.loads(flow.response.text)
        print(json.dumps(answer, indent=4))
        select_answer(answer, "练习")
    elif (
        "https://xyks.yuanfudao.com/leo-game-pk/android/math/pk/match?"
        in flow.request.url
    ):
        answer = json.loads(flow.response.text)
        print(json.dumps(answer, indent=4))
        select_answer(answer, "pk")


def answer_write(answer):
    for i in range(len(answer)):
        number_command.swipe_screen(answer[i])
        time.sleep(0.3)


def select_answer(answer, type):
    f = open("answer.txt", "w")
    select_answer = []

    if type == "练习":
        for question in answer["questions"]:
            answers = question["answers"]
            for i in range(len(answers)):
                if "." in answers[i]:
                    correct_answer = answers[i]
                    break
                if i == len(answers) - 1:
                    correct_answer = answers[0]
            select_answer.append(correct_answer)
            print(correct_answer, end="  ")
            f.write(str(correct_answer) + "  ")
    elif type == "pk":
        for question in answer["examVO"]["questions"]:
            answers = question["answers"]
            for i in range(len(answers)):
                if "." in answers[i]:
                    correct_answer = answers[i]
                    break
                if i == len(answers) - 1:
                    correct_answer = answers[0]
            select_answer.append(correct_answer)
            print(correct_answer, end="  ")
            f.write(str(correct_answer) + "  ")

    f.close()
    threading.Thread(target=gui_answer, args=(select_answer,)).start()


def gui_answer(answer):
    root = tk.Tk()
    root.title("继续执行")

    def on_button_click():
        root.destroy()
        answer_write(answer)

    button = tk.Button(root, text="点击继续", command=on_button_click)
    button.pack(pady=20)

    # 设置定时器，5秒后自动点击按钮
    root.after(12500, on_button_click)

    root.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mitmproxy script")
    parser.add_argument(
        "-P", "--port", type=int, default=8080, help="Port to listen on"
    )
    parser.add_argument(
        "-H", "--host", type=str, default="0.0.0.0", help="Host to listen on"
    )
    args = parser.parse_args()

    sys.argv = [
        "mitmdump",
        "-s",
        __file__,
        "--listen-host",
        args.host,
        "--listen-port",
        str(args.port),
    ]
    mitmdump()
