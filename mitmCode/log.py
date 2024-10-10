from loguru import logger
import sys

logger.remove()

# 配置控制台输出
logger.add(
    sys.stdout,
    level="DEBUG",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{"
           "line}</cyan> - <level>{message}</level>",
    colorize=True
)

# 配置文件输出
logger.add(
    "logs/app_{time}.log",
    rotation="10 MB",
    retention="10 days",
    compression="zip",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{line} - {message}",
    encoding="utf-8"
)

