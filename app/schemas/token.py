from pydantic import BaseModel
from typing import Union


class Token(BaseModel):
    """令牌响应模型"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """令牌数据模型"""

    email: Union[str, None] = None
