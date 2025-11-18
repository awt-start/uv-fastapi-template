from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from app.core import security
from app.core.config import settings
from app.core.database import get_db
from app.core.logger import get_logger
from app.crud import authenticate_user, create_user
from app.schemas import Token, UserCreate, UserOut
from app.models.response import success, error,CodeEnum,R
# 获取日志实例
logger = get_logger(__name__)

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """
    用户登录接口

    使用OAuth2密码模式进行认证，返回访问令牌
    """
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"登录失败: 邮箱 {form_data.username} 密码错误")
        return R.fail(msg="邮箱或密码错误",code=CodeEnum.PARAM_ERROR)
  
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )

    logger.info(f"登录成功: 用户 {user.email} (ID: {user.id})")
    return  {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user,
    }


@router.post("/register", response_model=UserOut)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    用户注册接口

    创建新用户并返回用户信息
    """
    user = await create_user(db, user_in=user_in)
    logger.info(f"用户注册成功: {user.email} (ID: {user.id})")
    return success(data=user)
