import re
import threading
import number_command
import time
from tkinter import messagebox
import tkinter as tk
from mitmproxy import http
import config


def is_target_url(url):
    return re.search(r"leo\.fbcontent\.cn/bh5/leo-web-oral-pk/exercise_.*\.js", url)

class ResponseHandler:
    def __init__(self):
        self.is_dialog_shown = False
        self.function_name_pattern = re.compile(r"(?<=isRight:)[^,]*?\(.*?\).*?(?=\|)")

    def request(self, flow: http.HTTPFlow):
        pass

    def response(self, flow: http.HTTPFlow):
        url = flow.request.url
        print(f"Response: {flow.response.status_code} {url}")

        if is_target_url(url):
            self.handle_target_response(flow, url)
        elif "https://xyks.yuanfudao.com/leo-game-pk/android/math/pk/match/v2?" in url:
            if not self.is_dialog_shown:
                self.is_dialog_shown = True
                threading.Thread(target=self.gui_answer).start()

    def handle_target_response(self, flow, url):
        print(f"匹配到指定的 URL: {url}")
        self.update_response_text(flow, flow.response.text)

    def update_response_text(self, flow, rt):
        # 1. 取消PK准备动画
        text = re.sub(r'"readyGoEnd"\)\}\),.{1,4}\)\}\),.{1,4}\)\}\),.{1,4}\)\}\)',
                      r'"readyGoEnd")}),20)}),20)}),20)})', rt)

        # 2. case 0 替换
        text = re.sub(r'case 0:if(.{0,14})\.challengeCode(.{200,300})([a-zA-Z]{1,2})\("startExercise"\);',
                      r'case 0:\3("startExercise");if\1.challengeCode\2', text)

        # 3. 判断任何答案正确
        text = re.sub(r'return .{3,5}\)\?1:0\},', r'return 1},', text)

        # 4. 自动触发答题
        text = re.sub(r'=function\(([a-zA-Z]{1,2}),([a-zA-Z]{1,2})\)\{([a-zA-Z]{1,2})&&\(([a-zA-Z]{1,2})\.value=',
                      r"=function(\1,\2){\2({ recognizeResult: '', pathPoints: [[]], answer: 1, showReductionFraction: 0 });\3&&(\4.value=",
                      text)

        # 5. 直接判断所有答题完成
        text = re.sub(r'\.value\+1>=[a-zA-Z]{1,2}\.value\.length\?([a-zA-Z]{1,2})\("finishExercise"\)',
                      r'.value+1>=0?\1("finishExercise")', text)

        # 6. 好友挑战PK修改时间为0.001
        text = re.sub(r"correctCnt:(.{1,5}),costTime:(.{1,15}),updatedTime:(.{1,120})([a-zA-Z]{1,2})\.challengeCode",
                      r"correctCnt:\1,costTime:\4.challengeCode?1:\2,updatedTime:\3\4.challengeCode", text)

        # 7. 所有PK场次修改时间为0.001
        text = re.sub(r"correctCnt:(.{1,5}),costTime:(.{1,15}),updatedTime:(.{1,120})([a-zA-Z]{1,2})\.challengeCode",
                      r"correctCnt:\1,costTime:1,updatedTime:\3\4.challengeCode", text)

        flow.response.text = text
        print(f"替换后的响应: {text}")
        threading.Thread(target=self.show_message_box, args=("过滤成功", f"替换成功!")).start()


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