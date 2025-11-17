from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Union


class UserBase(BaseModel):
    """用户基础模型"""

    email: EmailStr


class UserCreate(UserBase):
    """用户创建模型"""

    password: str
    full_name: Union[str, None] = None


class UserUpdate(UserBase):
    """用户更新模型"""

    password: Union[str, None]


class UserOut(UserBase):
    """用户输出模型"""

    id: int
    is_active: bool
    created_at: datetime
    full_name: Union[str, None] = None

    class Config:
        from_attributes = True
