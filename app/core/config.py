from pydantic_settings import BaseSettings
from typing import Any, List
from pydantic import AnyHttpUrl


class Settings(BaseSettings):
    """应用配置类"""

    # 应用基本信息
    PROJECT_NAME: str = "UV FastAPI Template"
    API_V1_STR: str = "/api/v1"

    # 应用环境
    APP_ENV: str = "development"
    # 安全密钥
    SECRET_KEY: str = "your-secret-key-here"
    # 访问令牌过期时间（分钟）
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS配置
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]

    # 数据库配置
    DATABASE_URL: str = "sqlite:///./test.db"

    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()
