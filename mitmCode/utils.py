import subprocess
import time
import traceback

import cv2
import numpy as np
from PIL import Image, ImageTk

from log import logger
from ui import get_config_auto, get_ui_label

template_kaixin = cv2.imread('src/kaixin.png', 0)
template_tryagain = cv2.imread('src/tryagain.png', 0)
template_jixu = cv2.imread('./src/jixu.png', 0)
template_again = cv2.imread('./src/again.png', 0)

status_win = cv2.imread('./src/win.png', 0)
status_lose = cv2.imread('./src/lose.png', 0)
status_draw = cv2.imread('./src/draw.png', 0)
status_running = cv2.imread('./src/running.png', 0)
status_get_rewards = cv2.imread('./src/get_rewards.png', 0)
status_matching = cv2.imread('./src/matching.png', 0)
status_retry = cv2.imread('./src/retry.png', 0)


def match_template(screen_image, template):
    """在屏幕截图中查找模板图像的位置"""
    try:
        result = cv2.matchTemplate(screen_image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > 0.8:
            return max_loc
        else:
            return None
    except Exception as e:
        logger.error(f"Error in match_template: {e}")
        return None


def touch(matched_location):
    click_x = matched_location[0] + 25
    click_y = matched_location[1] + 25
    subprocess.check_output(f"adb shell input tap {click_x} {click_y}", shell=True)


def check_continue_ui():
    while True:
        try:
            left_num, right_num, result, left_label, right_label, result_label, status_label = get_ui_label()
            time.sleep(1)
            subprocess.check_output("adb exec-out screencap -p > screenshot.png", shell=True)
            image = Image.open("screenshot.png")

            screen_image_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            screen_image_gray = cv2.cvtColor(screen_image_np, cv2.COLOR_BGR2GRAY)
            if get_config_auto().get():
                matched_location = match_template(screen_image_gray, template_kaixin)
                matched_location1 = match_template(screen_image_gray, template_tryagain)
                jixu_location = match_template(screen_image_gray, template_jixu)
                again_location = match_template(screen_image_gray, template_again)
                if matched_location:
                    touch(matched_location)
                if matched_location1:
                    touch(matched_location1)
                if jixu_location:
                    touch(jixu_location)
                if again_location:
                    touch(again_location)
                    status_label.config(text=f"状态:等待开始")

            matched_win = match_template(screen_image_gray, status_win)
            matched_lose = match_template(screen_image_gray, status_lose)
            matched_draw = match_template(screen_image_gray, status_draw)
            matched_running = match_template(screen_image_gray, status_running)
            matched_get_rewards = match_template(screen_image_gray, status_get_rewards)
            matched_matching = match_template(screen_image_gray, status_matching)
            matched_retry = match_template(screen_image_gray, status_retry)
            if matched_win:
                status_label.config(text=f"状态:胜利")
                logger.info('比赛胜利')
            elif matched_lose:
                status_label.config(text=f"状态:失败")
                logger.info('比赛失败')
            elif matched_running:
                status_label.config(text="状态:运行答题中")
            elif matched_get_rewards:
                status_label.config(text="状态:答题结束")
                logger.info('比赛结束')
            elif matched_matching:
                status_label.config(text="状态:匹配中")
                logger.info('匹配中')
            elif matched_retry:
                status_label.config(text="状态:小猿口算错误")
                logger.info('小猿口算错误')
                subprocess.run(["adb", "shell", "input", "keyevent", "4"])
            elif matched_draw:
                status_label.config(text="状态:平局")
                logger.info('比赛平局')
        except Exception as e:
            logger.error(traceback.format_exc())
