import os
import tkinter as tk

from loguru import logger

left_image = None
right_image = None
left_num = None
right_num = None
result = None
image = None
status = None
left_label, right_label, result_label = None, None, None
root = None
match_enabled = None
log_text, status_label = None, None


class TkinterLogHandler:
    global log_text

    def __init__(self):
        self.text_widget = log_text

    def write(self, message):
        if message.strip():  # 只写入非空消息
            self.text_widget.config(state=tk.NORMAL)
            self.text_widget.insert(tk.END, message)
            self.text_widget.yview(tk.END)
            self.text_widget.config(state=tk.DISABLED)

    def flush(self):
        pass


def init_ui():
    global left_num, right_num, result, left_label, right_label, result_label, root, match_enabled, status_label, log_text
    root = tk.Tk()
    root.wm_attributes("-topmost", True)
    root.resizable(0, 0)
    root.attributes("-toolwindow", 2)
    root.title("小猿口算-MIMT")

    match_enabled = tk.BooleanVar(value=False)

    match_checkbox = tk.Checkbutton(root, text="启用自动循环", variable=match_enabled)
    match_checkbox.pack()

    left_label = tk.Label(root, text="比赛名称: None", font=("Helvetica", 16))
    left_label.pack()

    right_label = tk.Label(root, text="对手用户名: None", font=("Helvetica", 16))
    right_label.pack()

    result_label = tk.Label(root, text="对手用户ID: None", font=("Helvetica", 16))
    result_label.pack()

    status_label = tk.Label(root, text="状态：初始化", font=("Helvetica", 16))
    status_label.pack()

    log_text = tk.Text(root, height=10, width=50, state=tk.DISABLED)
    log_text.pack()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    tkinter_handler = TkinterLogHandler()
    logger.add(
        tkinter_handler.write,
        level="INFO",
        format="{time:MM-DD HH:mm:ss} | {level} | {message}")

    root.mainloop()


def get_ui_label():
    global left_num, right_num, result, left_label, right_label, result_label, status_label
    return left_num, right_num, result, left_label, right_label, result_label, status_label


def on_closing():
    global root
    os.system("mitmweb --stop")
    os.system('taskkill /f /t /im adb.exe')
    root.destroy()


def get_config_auto():
    global match_enabled
    return match_enabled

