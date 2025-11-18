"""
FastAPI 应用主入口
提供应用初始化、生命周期管理和基础路由
"""

from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.config import settings
from app.core.database import engine
from app.core.logger import get_structured_logger, setup_logging, get_logger
from app.models import Base
from app.models.response import R, PageInfo

# 设置日志
setup_logging()
logger = get_logger(__name__)
from app.middleware.LoggingMiddleware import LoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理

    启动时：
    - 创建数据库表

    关闭时：
    - 释放资源（如需要）
    """
    # 启动逻辑
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✓ 数据库表创建成功")
    except Exception as e:
        logger.error(f"✗ 数据库初始化失败: {e}")
        raise

    yield

    # 关闭逻辑
    await engine.dispose()
    logger.info("✓ 应用已关闭，资源已释放")


def create_application() -> FastAPI:
    """
    创建并配置 FastAPI 应用实例

    Returns:
        配置完成的 FastAPI 应用
    """
    application = FastAPI(
        title=settings.PROJECT_NAME,
        description=f"{settings.PROJECT_NAME} API 文档",
        version="1.0.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc",
        lifespan=lifespan,
    )

    # 添加日志中间件
    application.add_middleware(LoggingMiddleware)

    # 配置 CORS
    configure_cors(application)

    # 注册路由
    register_routes(application)

    return application


def configure_cors(application: FastAPI) -> None:
    """
    配置跨域资源共享 (CORS)

    Args:
        application: FastAPI 应用实例
    """
    if settings.BACKEND_CORS_ORIGINS:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=[
                str(origin).rstrip("/") for origin in settings.BACKEND_CORS_ORIGINS
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["*"],
            max_age=3600,  # 预检请求缓存时间
        )


def register_routes(application: FastAPI) -> None:
    """
    注册应用路由

    Args:
        application: FastAPI 应用实例
    """
    # 注册 API 路由
    application.include_router(api_router, prefix=settings.API_V1_STR)

    # 注册基础路由
    @application.get(
        "/",
        tags=["基础"],
        summary="根路径",
        description="API 欢迎页面和基本信息",
        response_model=R[Dict[str, Any]],
    )
    async def index() -> R:
        """根路径健康检查"""
        return R.ok(
            data={
                "version": "1.0.0",
                "author": "芒星",
                "description": "这是一个基于 FastAPI 的 RESTful API 服务",
                "docs": f"{settings.API_V1_STR}/docs",
            }
        )


# 创建应用实例
app = create_application()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
