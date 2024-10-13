import re
import threading
import number_command
import time
from tkinter import messagebox
import tkinter as tk
from mitmproxy import http
import config

class ResponseHandler:
    def __init__(self):
        self.is_dialog_shown = False
        self.function_name_pattern = re.compile(r"(?<=isRight:)[^,]*?\(.*?\).*?(?=\|)")

    def request(self, flow: http.HTTPFlow):
        pass

    def response(self, flow: http.HTTPFlow):
        url = flow.request.url
        print(f"Response: {flow.response.status_code} {url}")

        if self.is_target_url(url):
            self.handle_target_response(flow, url)
        elif "https://xyks.yuanfudao.com/leo-game-pk/android/math/pk/match/v2?" in url:
            if not self.is_dialog_shown:
                self.is_dialog_shown = True
                threading.Thread(target=self.gui_answer).start()

    def is_target_url(self, url):
        return re.search(r"leo\.fbcontent\.cn/bh5/leo-web-oral-pk/exercise_.*\.js", url)

    def handle_target_response(self, flow, url):
        print(f"匹配到指定的 URL: {url}")
        responsetext = flow.response.text
        funname = self.extract_function_name(responsetext)

        if funname:
            self.update_response_text(flow, responsetext, funname)
        else:
            print("未找到匹配的函数名，无法进行替换。")

    def extract_function_name(self, responsetext):
        match = self.function_name_pattern.search(responsetext)
        return match.group() if match else None

    def update_response_text(self, flow, responsetext, funname):
        print(f"找到函数名: {funname}")
        updated_text = responsetext.replace(funname, f"{funname}||true")
        flow.response.text = updated_text
        print(f"替换后的响应: {updated_text}")
        threading.Thread(target=self.show_message_box, args=("过滤成功", f"函数 {funname} 替换成功!")).start()

    def show_message_box(self, title, message):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(title, message)
        root.destroy()

    def answer_write(self, prepared_commands):
        start_time = time.time()
        number_command.run_adb_command(prepared_commands)
        print(f"点击操作耗时: {time.time() - start_time:.3f}秒")

    def gui_answer(self):
        prepared_commands = number_command.prepare_tap_commands(".", config.ANSWER_COUNT)

        root = tk.Tk()
        root.title("继续执行")
        button = tk.Button(root, text="点击继续", command=lambda: self.answer_write(prepared_commands))
        button.pack(pady=20)

        threading.Timer(config.WAITING_TIME, self.auto_click_and_close, args=(root, prepared_commands)).start()
        root.mainloop()

    def auto_click_and_close(self, root, prepared_commands):
        self.answer_write(prepared_commands)
        self.is_dialog_shown = False
        root.destroy()

addons = [
    ResponseHandler()
]