from datetime import datetime, timedelta
from typing import Any, Optional, Union

import bcrypt
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# 创建密码上下文，用于密码哈希和验证
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码是否匹配

    bcrypt算法要求密码长度不超过72字节，超过部分将被截断
    """
    # 基于字节长度截断密码
    plain_password_bytes = plain_password.encode("utf-8")[:72]
    hashed_password_bytes = hashed_password.encode("utf-8")

    # 使用bcrypt库直接验证密码
    try:
        return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """生成密码哈希值

    bcrypt算法要求密码长度不超过72字节，超过部分将被截断
    """
    # 基于字节长度截断密码
    password_bytes = password.encode("utf-8")[:72]

    # 使用bcrypt库直接生成哈希
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)

    return hashed.decode("utf-8")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建JWT访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt