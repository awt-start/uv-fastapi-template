# app/core/response.py

from typing import TypeVar, Generic, Optional, Any
from pydantic import BaseModel

T = TypeVar("T")


class R(BaseModel, Generic[T]):
    """
    统一响应模型，对标 Java 的 R<T>
    """

    code: int
    msg: str
    data: Optional[T] = None

    class Config:
        # 允许返回 ORM 模型等非 dict 对象（自动序列化）
        from_attributes = True  # Pydantic v2 语法（旧版为 orm_mode = True）

    @classmethod
    def ok(cls, data: T = None, msg: str = "操作成功") -> "R[T]":
        return cls(code=200, msg=msg, data=data)

    @classmethod
    def fail(cls, data: T = None, msg: str = "操作失败", code: int = 500) -> "R[T]":
        return cls(code=code, msg=msg, data=data)

    @classmethod
    def warn(cls, data: T = None, msg: str = "警告") -> "R[T]":
        return cls(code=601, msg=msg, data=data)  # 601 为自定义警告码，可按需调整

    @staticmethod
    def is_success(response: "R") -> bool:
        return response.code == 200

    @staticmethod
    def is_error(response: "R") -> bool:
        return not R.is_success(response)
