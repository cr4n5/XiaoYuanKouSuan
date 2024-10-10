import json
import threading
from mitmproxy import http

from adb import adb_status
from log import logger
from action import perform_actions
from utils import check_continue_ui
from ui import init_ui, get_ui_label

url_prefix = "https://xyks.yuanfudao.com/leo-game-pk/android/math/pk/match"
flag = True


adb_status()


def response(flow: http.HTTPFlow) -> None:

    if flow.request.pretty_url.startswith(url_prefix):
        logger.info(f"匹配到目标请求: {flow.request.pretty_url}")

        response_data = flow.response.text

        try:
            data = json.loads(response_data)

            point_name = data.get("examVO", {}).get("pointName", "未知")
            logger.info(f"比赛名称: {point_name}")

            other_user_name = data.get("otherUser", {}).get("userName", "未知")
            other_user_id = data.get("otherUser", {}).get("userId", "未知")

            logger.info(f"对手用户名: {other_user_name} ID: {other_user_id}")

            questions = data.get("examVO", {}).get("questions", [])
            logger.info("题目答案：")
            left_num, right_num, result, left_label, right_label, result_label, status_label = get_ui_label()
            left_label.config(text=f"比赛名称: {point_name}")
            right_label.config(text=f"对手用户名: {other_user_name}")
            result_label.config(text=f"对手用户ID: {other_user_id}")
            for idx, question in enumerate(questions):
                answer = question.get("answer", "未知")
                content = question.get("content", "未知题目")
                logger.info(f"题目 {idx + 1}: {content}，答案: {answer}")

            threading.Thread(target=perform_actions, args=(questions, point_name,)).start()

        except json.JSONDecodeError:
            logger.info("响应数据不是合法的 JSON 格式")
        except Exception as e:
            logger.info(f"解析响应数据时发生错误: {str(e)}")


threading.Thread(target=check_continue_ui, daemon=True).start()
threading.Thread(target=init_ui, daemon=True).start()
