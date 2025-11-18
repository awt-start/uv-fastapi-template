"""
结构化日志系统 - 完整版本
支持 JSON 格式、审计日志、性能监控、请求追踪等功能
"""
import json
import logging
import sys
import time
from datetime import datetime
from enum import Enum
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional, Any, Dict
from uuid import uuid4

from app.core.config import settings


class LogLevel(str, Enum):
    """日志级别枚举"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogType(str, Enum):
    """日志类型枚举"""
    APPLICATION = "APPLICATION"  # 应用日志
    AUDIT = "AUDIT"              # 审计日志
    PERFORMANCE = "PERFORMANCE"  # 性能日志
    REQUEST = "REQUEST"          # 请求日志
    DATABASE = "DATABASE"        # 数据库日志
    SECURITY = "SECURITY"        # 安全日志


class StructuredFormatter(logging.Formatter):
    """结构化日志格式化器 - 输出 JSON 格式"""
    
    def format(self, record: logging.LogRecord) -> str:
        """格式化日志记录为 JSON"""
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # 添加自定义属性
        if hasattr(record, "log_type"):
            log_data["log_type"] = getattr(record, "log_type", None)
        if hasattr(record, "request_id"):
            log_data["request_id"] = getattr(record, "request_id", None)
        if hasattr(record, "user_id"):
            log_data["user_id"] = getattr(record, "user_id", None)
        if hasattr(record, "duration"):
            log_data["duration_ms"] = getattr(record, "duration", None) 
        if hasattr(record, "extra_data"):
            log_data["extra"] = getattr(record, "extra_data", None)
        
        # 异常信息
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)


class PlainFormatter(logging.Formatter):
    """普通文本格式化器 - 用于开发环境"""
    
    FORMATS = {
        logging.DEBUG: "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        logging.INFO: "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        logging.WARNING: "%(asctime)s - %(name)s - %(levelname)s - ⚠️  %(message)s",
        logging.ERROR: "%(asctime)s - %(name)s - %(levelname)s - ❌ %(message)s",
        logging.CRITICAL: "%(asctime)s - %(name)s - %(levelname)s - �� %(message)s",
    }
    
    def format(self, record: logging.LogRecord) -> str:
        fmt = self.FORMATS.get(record.levelno, self.FORMATS[logging.INFO])
        formatter = logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


class LogConfig:
    """日志配置类"""
    
    LOG_DIR = Path("logs")
    LOG_FILES = {
        "app": "app.log",
        "error": "app.error.log",
        "audit": "app.audit.log",
        "performance": "app.performance.log",
        "request": "app.request.log",
    }
    
    MAX_BYTES = 10 * 1024 * 1024  # 10MB
    BACKUP_COUNT = 5
    
    THIRD_PARTY_LOGGERS = {
        "uvicorn": "WARNING",
        "uvicorn.access": "INFO",
        "fastapi": "WARNING",
        "sqlalchemy": "WARNING",
        "sqlalchemy.engine": "WARNING",
    }
    
    @classmethod
    def get_log_level(cls) -> str:
        """根据环境获取日志级别"""
        if settings.APP_ENV == "production":
            return "INFO"
        elif settings.APP_ENV == "testing":
            return "DEBUG"
        return "DEBUG"
    
    @classmethod
    def use_json_format(cls) -> bool:
        """是否使用 JSON 格式（生产环境使用）"""
        return settings.APP_ENV == "production"


class LoggerManager:
    """日志管理器 - 单例模式"""
    
    _instance: Optional["LoggerManager"] = None
    _initialized = False
    
    def __new__(cls) -> "LoggerManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not LoggerManager._initialized:
            self._setup()
            LoggerManager._initialized = True
    
    def _setup(self) -> None:
        """初始化日志系统"""
        LogConfig.LOG_DIR.mkdir(exist_ok=True)
        
        root_logger = logging.getLogger()
        root_logger.handlers.clear()
        
        log_level = LogConfig.get_log_level()
        root_logger.setLevel(log_level)
        
        # 添加处理器
        self._add_console_handler(root_logger, log_level)
        if settings.APP_ENV == "production":
            self._add_file_handlers(root_logger, log_level)
        
        # 配置第三方库日志
        self._setup_third_party_loggers()
    
    def _add_console_handler(
        self,
        logger: logging.Logger,
        log_level: str
    ) -> None:
        """添加控制台处理器"""
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        
        if LogConfig.use_json_format():
            formatter = StructuredFormatter()
        else:
            formatter = PlainFormatter()
        
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    def _add_file_handlers(
        self,
        logger: logging.Logger,
        log_level: str
    ) -> None:
        """添加文件处理器"""
        # 主日志文件
        self._add_rotating_file_handler(
            logger,
            LogConfig.LOG_DIR / LogConfig.LOG_FILES["app"],
            log_level,
            StructuredFormatter() if LogConfig.use_json_format() else PlainFormatter()
        )
        
        # 错误日志文件
        error_handler = RotatingFileHandler(
            LogConfig.LOG_DIR / LogConfig.LOG_FILES["error"],
            maxBytes=LogConfig.MAX_BYTES,
            backupCount=LogConfig.BACKUP_COUNT,
            encoding="utf-8"
        )
        error_handler.setLevel("ERROR")
        error_handler.setFormatter(
            StructuredFormatter() if LogConfig.use_json_format() else PlainFormatter()
        )
        logger.addHandler(error_handler)
        
        # 审计日志文件
        audit_logger = logging.getLogger("audit")
        self._add_rotating_file_handler(
            audit_logger,
            LogConfig.LOG_DIR / LogConfig.LOG_FILES["audit"],
            "INFO",
            StructuredFormatter()
        )
        audit_logger.propagate = False
        
        # 性能日志文件
        perf_logger = logging.getLogger("performance")
        self._add_rotating_file_handler(
            perf_logger,
            LogConfig.LOG_DIR / LogConfig.LOG_FILES["performance"],
            "INFO",
            StructuredFormatter()
        )
        perf_logger.propagate = False
        
        # 请求日志文件
        request_logger = logging.getLogger("request")
        self._add_rotating_file_handler(
            request_logger,
            LogConfig.LOG_DIR / LogConfig.LOG_FILES["request"],
            "INFO",
            StructuredFormatter()
        )
        request_logger.propagate = False
    
    @staticmethod
    def _add_rotating_file_handler(
        logger: logging.Logger,
        file_path: Path,
        level: str,
        formatter: logging.Formatter
    ) -> None:
        """添加滚动文件处理器"""
        handler = RotatingFileHandler(
            file_path,
            maxBytes=LogConfig.MAX_BYTES,
            backupCount=LogConfig.BACKUP_COUNT,
            encoding="utf-8"
        )
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    def _setup_third_party_loggers(self) -> None:
        """配置第三方库日志级别"""
        for logger_name, log_level in LogConfig.THIRD_PARTY_LOGGERS.items():
            logging.getLogger(logger_name).setLevel(log_level)
    
    @staticmethod
    def get_logger(name: Optional[str] = None) -> logging.Logger:
        """获取日志实例"""
        return logging.getLogger(name)


class StructuredLogger:
    """结构化日志包装类 - 提供丰富的日志记录方法"""
    
    def __init__(self, name: Optional[str] = None):
        self.logger = logging.getLogger(name)
        self.request_id = str(uuid4())
    
    def set_request_id(self, request_id: str) -> None:
        """设置请求 ID"""
        self.request_id = request_id
    
    def _log_with_extra(
        self,
        level: int,
        msg: str,
        log_type: Optional[str] = None,
        user_id: Optional[int] = None,
        extra_data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> None:
        """带附加信息的日志记录"""
        extra = {
            "request_id": self.request_id,
            "log_type": log_type or LogType.APPLICATION.value,
        }
        
        if user_id:
            extra["user_id"] = str(user_id)
        if extra_data:
            extra["extra_data"] = str(extra_data)
        
        self.logger.log(level, msg, extra=extra, **kwargs)
    
    def debug(
        self,
        msg: str,
        user_id: Optional[int] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> None:
        """调试日志"""
        self._log_with_extra(
            logging.DEBUG, msg, LogType.APPLICATION.value, user_id, extra_data
        )
    
    def info(
        self,
        msg: str,
        log_type: Optional[str] = None,
        user_id: Optional[int] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> None:
        """信息日志"""
        self._log_with_extra(
            logging.INFO, msg, log_type or LogType.APPLICATION.value, user_id, extra_data
        )
    
    def warning(
        self,
        msg: str,
        user_id: Optional[int] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> None:
        """警告日志"""
        self._log_with_extra(
            logging.WARNING, msg, LogType.APPLICATION.value, user_id, extra_data
        )
    
    def error(
        self,
        msg: str,
        user_id: Optional[int] = None,
        extra_data: Optional[Dict[str, Any]] = None,
        exc_info: bool = True
    ) -> None:
        """错误日志"""
        self._log_with_extra(
            logging.ERROR, msg, LogType.APPLICATION.value, user_id, extra_data, exc_info=exc_info
        )
    
    def critical(
        self,
        msg: str,
        user_id: Optional[int] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> None:
        """严重错误日志"""
        self._log_with_extra(
            logging.CRITICAL, msg, LogType.APPLICATION.value, user_id, extra_data
        )
    
    def audit(
        self,
        msg: str,
        action: str,
        user_id: int,
        resource: str,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> None:
        """审计日志"""
        audit_logger = logging.getLogger("audit")
        extra = {
            "request_id": self.request_id,
            "log_type": LogType.AUDIT.value,
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "extra_data": extra_data or {},
        }
        audit_logger.info(msg, extra=extra)
    
    def performance(
        self,
        msg: str,
        operation: str,
        duration_ms: float,
        user_id: Optional[int] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> None:
        """性能日志"""
        perf_logger = logging.getLogger("performance")
        extra = {
            "request_id": self.request_id,
            "log_type": LogType.PERFORMANCE.value,
            "operation": operation,
            "duration": duration_ms,
        }
        if user_id:
            extra["user_id"] = user_id
        if extra_data:
            extra["extra_data"] = extra_data
        
        perf_logger.info(msg, extra=extra)
    
    def request(
        self,
        method: str,
        path: str,
        status_code: int,
        duration_ms: float,
        user_id: Optional[int] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> None:
        """请求日志"""
        request_logger = logging.getLogger("request")
        msg = f"{method} {path} - {status_code}"
        extra = {
            "request_id": self.request_id,
            "log_type": LogType.REQUEST.value,
            "method": method,
            "path": path,
            "status_code": status_code,
            "duration": duration_ms,
        }
        if user_id:
            extra["user_id"] = user_id
        if extra_data:
            extra["extra_data"] = extra_data
        
        request_logger.info(msg, extra=extra)
    
    def database(
        self,
        msg: str,
        query: str,
        duration_ms: float,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> None:
        """数据库日志"""
        extra = {
            "request_id": self.request_id,
            "log_type": LogType.DATABASE.value,
            "query": query[:500],  # 限制长度
            "duration": duration_ms,
            "extra_data": extra_data or {},
        }
        self.logger.info(msg, extra=extra)
    
    def security(
        self,
        msg: str,
        event_type: str,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> None:
        """安全日志"""
        extra = {
            "request_id": self.request_id,
            "log_type": LogType.SECURITY.value,
            "event_type": event_type,
            "ip_address": ip_address,
        }
        if user_id:
            extra["user_id"] = user_id
        if extra_data:
            extra["extra_data"] = extra_data
        
        self.logger.warning(msg, extra=extra)


# 全局便捷函数
def setup_logging() -> None:
    """初始化日志系统"""
    LoggerManager()


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """获取标准日志实例"""
    LoggerManager()
    return LoggerManager.get_logger(name)


def get_structured_logger(name: Optional[str] = None) -> StructuredLogger:
    """获取结构化日志实例"""
    LoggerManager()
    return StructuredLogger(name)
