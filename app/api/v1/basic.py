# app/api/v1/basic.py 或 main.py
import asyncio
import time
from datetime import datetime
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db
from app.core.config import settings
from app.core.logger import get_logger
from app.models.response import R

logger = get_logger(__name__)

router = APIRouter()


async def check_database(db: AsyncSession) -> dict:
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "latency_ms": 0}
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {"status": "error", "error": str(e)}


""" async def check_redis() -> dict:
    # 可选：如果你用了 Redis
    try:
        from app.core.redis import redis_client  # 假设你有 redis_client
        start = time.time()
        await redis_client.ping()
        latency = int((time.time() - start) * 1000)
        return {"status": "ok", "latency_ms": latency}
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        return {"status": "error", "error": str(e)}
 """


async def check_external_service() -> dict:
    # 可选：检查你依赖的外部服务（如 AI API、支付网关）
    try:
        import httpx

        async with httpx.AsyncClient(timeout=5.0) as client:
            start = time.time()
            response = await client.get(
                "https://api.example.com/health"
            )  # 替换为实际地址
            latency = int((time.time() - start) * 1000)
            if response.status_code == 200:
                return {"status": "ok", "latency_ms": latency}
            else:
                return {"status": "error", "http_status": response.status_code}
    except Exception as e:
        logger.error(f"External service health check failed: {e}")
        return {"status": "error", "error": str(e)}


@router.get(
    "/health",
    tags=["基础"],
    summary="健康检查",
    description="动态检查数据库、缓存、外部服务等依赖状态",
    status_code=status.HTTP_200_OK,
    response_model=R,
)
async def health_check(db: AsyncSession = Depends(get_db)) -> R:
    """增强版健康检查：动态探测关键依赖"""
    start_time = time.time()

    # 并发检查（不阻塞）
    checks = {
        "database": check_database(db),
    }

    # 按需启用其他检查（通过配置开关）
    """ if settings.ENABLE_REDIS_HEALTH_CHECK:
        checks["redis"] = check_redis()
    if settings.ENABLE_EXTERNAL_HEALTH_CHECK:
        checks["external_service"] = check_external_service() """

    # 等待所有检查完成
    results = await asyncio.gather(*checks.values(), return_exceptions=True)
    health_info = {}
    overall_status = "healthy"

    for i, key in enumerate(checks.keys()):
        result = results[i]
        if isinstance(result, Exception):
            health_info[key] = {"status": "error", "error": str(result)}
            overall_status = "unhealthy"
        else:
            health_info[key] = result
            """ if result.get("status") != "ok":
                overall_status = "unhealthy" """

    response = R.ok(
        data={
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "uptime_seconds": int(time.time() - start_time) + 1,
            "info": health_info,
        }
    )

    # 若整体不健康，返回 503（可选）
    if overall_status != "healthy":
        from fastapi.responses import JSONResponse

        return R.fail(
            msg="Some dependencies are unhealthy",
            code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    logger.info("Health check passed")
    return response
