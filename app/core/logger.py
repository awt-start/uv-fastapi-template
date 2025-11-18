"""
日志配置模块
提供统一的日志配置和获取日志实例的方法
"""

import logging
import sys
from typing import Optional
from logging.handlers import RotatingFileHandler
from app.core.config import settings

# 日志格式配置
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 日志文件配置
LOG_FILE = "app.log"
MAX_BYTES = 10 * 1024 * 1024  # 10MB
BACKUP_COUNT = 5  # 保留5个备份文件


def setup_logger() -> None:
    """
    设置全局日志配置
    - 控制台输出
    - 文件输出（支持滚动）
    - 根据环境设置日志级别
    """
    # 创建根日志器
    root_logger = logging.getLogger()

    # 清除已存在的处理器
    root_logger.handlers.clear()

    # 根据环境设置日志级别
    if settings.APP_ENV == "production":
        log_level = logging.INFO
    else:
        log_level = logging.DEBUG

    root_logger.setLevel(log_level)

    # 创建格式化器
    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # 创建文件处理器（仅在生产环境启用）
    if settings.APP_ENV == "production":
        file_handler = RotatingFileHandler(
            LOG_FILE, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT, encoding="utf-8"
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    # 设置第三方库的日志级别（可根据需要调整）
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    获取日志实例

    Args:
        name: 日志名称，默认为None（返回根日志器）

    Returns:
        logging.Logger: 日志实例
    """
    return logging.getLogger(name)
