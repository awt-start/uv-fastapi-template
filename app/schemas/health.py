# app/schemas/health.py
from pydantic import BaseModel
from typing import Dict, Any

# 增加上swagger 信息
from fastapi import status
from datetime import datetime


# 增加上swagger 信息
class HealthComponent(BaseModel):
    status: str  # "ok" / "error"
    details: Dict[str, Any] = {}


class HealthCheckResponse(BaseModel):
    status: str  # "healthy" / "unhealthy"
    timestamp: str
    info: Dict[str, HealthComponent] = {}
