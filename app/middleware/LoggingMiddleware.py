"""
日志中间件 - 自动记录请求日志、性能日志、错误日志
"""

import time
from typing import Callable
from uuid import uuid4

from fastapi import Request, Response
from fastapi.responses import StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logger import get_structured_logger, StructuredLogger


class LoggingMiddleware(BaseHTTPMiddleware):
    """日志中间件 - 记录所有 HTTP 请求"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """处理请求并记录日志"""
        # 生成或获取请求 ID
        request_id = request.headers.get("X-Request-ID", str(uuid4()))

        # 创建日志实例
        logger = get_structured_logger(__name__)
        logger.set_request_id(request_id)

        # 添加请求 ID 到请求状态（供后续使用）
        request.state.request_id = request_id
        request.state.logger = logger

        # 获取请求信息
        method = request.method
        path = request.url.path
        query_params = dict(request.query_params)
        client_ip = self._get_client_ip(request)
        user_agent = request.headers.get("user-agent", "")

        # 记录请求日志
        logger.info(
            f"Incoming request: {method} {path}",
            log_type="REQUEST",
            extra_data={
                "method": method,
                "path": path,
                "query_params": query_params,
                "client_ip": client_ip,
                "user_agent": user_agent,
            },
        )

        # 记录请求体（仅在开发环境）
        try:
            if method in ["POST", "PUT", "PATCH"]:
                body = await request.body()
                if body:
                    logger.debug(
                        f"Request body: {body.decode()[:500]}",
                        extra_data={"body_size": len(body)},
                    )
                # 重新设置 body（因为 await request.body() 会消耗流）
                request._body = body
        except Exception as e:
            logger.error(f"Failed to read request body: {str(e)}")

        # 记录开始时间
        start_time = time.time()

        try:
            # 调用下一个中间件或路由
            response = await call_next(request)

            # 计算处理时间
            duration_ms = (time.time() - start_time) * 1000

            # 记录响应日志
            logger.request(
                method=method,
                path=path,
                status_code=response.status_code,
                duration_ms=duration_ms,
                extra_data={
                    "client_ip": client_ip,
                    "response_headers": dict(response.headers),
                },
            )

            # 如果是慢查询（>500ms），记录性能警告
            if duration_ms > 500:
                logger.performance(
                    f"Slow request detected: {method} {path}",
                    operation=f"{method} {path}",
                    duration_ms=duration_ms,
                    extra_data={"threshold_ms": 500},
                )

            # 在响应头中添加 request_id
            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as e:
            # 记录异常
            duration_ms = (time.time() - start_time) * 1000
            logger.error(
                f"Request failed: {method} {path}",
                extra_data={
                    "error": str(e),
                    "duration_ms": duration_ms,
                    "client_ip": client_ip,
                },
            )
            raise

    @staticmethod
    def _get_client_ip(request: Request) -> str:
        """获取客户端 IP"""
        # 检查代理头
        if "x-forwarded-for" in request.headers:
            return request.headers["x-forwarded-for"].split(",")[0].strip()
        if "x-real-ip" in request.headers:
            return request.headers["x-real-ip"]
        # 直接连接
        return request.client.host if request.client else "unknown"


class PerformanceLogContext:
    """性能日志上下文管理器"""

    def __init__(self, operation: str, logger: StructuredLogger, user_id: int):
        self.operation = operation
        self.logger = logger
        self.user_id = user_id
        self.start_time = None

    async def __aenter__(self):
        """进入上下文"""
        self.start_time = time.time()
        self.logger.debug(f"Starting operation: {self.operation}")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        duration_ms = (time.time() - (self.start_time or 0)) * 1000

        if exc_type:
            self.logger.error(
                f"Operation failed: {self.operation}",
                extra_data={
                    "error": str(exc_val),
                    "duration_ms": duration_ms,
                },
            )
        else:
            self.logger.performance(
                f"Operation completed: {self.operation}",
                operation=self.operation,
                duration_ms=duration_ms,
                user_id=self.user_id,
            )


class DatabaseOperationLogger:
    """数据库操作日志记录器"""

    def __init__(self, logger: StructuredLogger):
        self.logger = logger

    async def log_query(
        self,
        operation: str,
        table: str,
        query: str,
        duration_ms: float,
        rows_affected: int,
    ) -> None:
        """记录数据库查询"""
        extra_data = {
            "operation": operation,
            "table": table,
            "rows_affected": rows_affected,
        }

        self.logger.database(
            f"Database {operation}: {table}",
            query=query,
            duration_ms=duration_ms,
            extra_data=extra_data,
        )

        # 如果是慢查询，记录警告
        if duration_ms > 100:
            self.logger.warning(
                f"Slow database query detected: {operation} on {table}",
                extra_data={
                    "duration_ms": duration_ms,
                    "threshold_ms": 100,
                    "query": query[:500],
                },
            )
