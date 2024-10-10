import time

from log import logger
from swipe import swipe_screen


allowed_point_keyword = ["大小"]


def contains_keyword(input_str):
    for keyword in allowed_point_keyword:
        if keyword in input_str:
            return True
    return False


def perform_actions(questions, point_name):
    """已经是最佳参数，请勿随意调整"""
    logger.info("已找到比赛，等待比赛开始")
    time.sleep(12.2)

    if not contains_keyword(point_name):
        logger.error("不在符合的比赛范围内")
        return

    for idx, question in enumerate(questions):
        answer = question.get("answer", None)
        swipe_screen(answer)
        logger.info(f"完成题目{idx + 1}|答案：{answer}")
        time.sleep(0.2)

