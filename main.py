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

# CONFIG
is_dialog_shown = False
ANSWER_COUNT = 30
WAITING_TIME = 12.5

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

def answer_write():
    for _ in range(ANSWER_COUNT):
        number_command.tap_screen(".")

def gui_answer():
    root = tk.Tk()
    root.title("继续执行")
    button = tk.Button(root, text="点击继续", command=answer_write)
    button.pack(pady=20)

    # 设置定时器自动点击
    threading.Timer(WAITING_TIME, auto_click_and_close, args=(root,)).start()

    root.mainloop()

def auto_click_and_close(root):
    answer_write()
    global is_dialog_shown
    is_dialog_shown = False
    root.destroy()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mitmproxy script")
    parser.add_argument("-P", "--port", type=int, default=8080, help="Port to listen on")
    parser.add_argument("-H", "--host", type=str, default="0.0.0.0", help="Host to listen on")
    args = parser.parse_args()

    sys.argv = ["mitmdump", "-s", __file__, "--listen-host", args.host, "--listen-port", str(args.port)]
    mitmdump()
