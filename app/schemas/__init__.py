from app.schemas.user import UserBase, UserCreate, UserUpdate, UserOut
from app.schemas.token import Token, TokenData
from app.schemas.health import HealthCheckResponse, HealthComponent
from app.schemas.student import StudentBase, StudentCreate, StudentUpdate, StudentOut

# 是否可以自动引入？
# 答案：可以自动引入，但是需要在 __all__ 中添加 HealthCheckResponse
__all__ = [
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserOut",
    "Token",
    "TokenData",
    "HealthCheckResponse",
    "HealthComponent",
    "StudentBase",
    "StudentCreate",
    "StudentUpdate",
    "StudentOut",
]
