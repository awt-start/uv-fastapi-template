from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.logger import get_logger
from app.crud import get_user, get_users, update_user
from app.models import User
from app.schemas import UserOut, UserUpdate

# 获取日志实例
logger = get_logger(__name__)

router = APIRouter()


@router.get("/me", response_model=UserOut)
async def read_users_me(
    current_user: User = Depends(get_current_user),
):
    """
    获取当前用户信息

    需要有效的JWT令牌
    """
    logger.info(f"获取当前用户信息: {current_user.email} (ID: {current_user.id})")
    return current_user


@router.get("/{user_id}", response_model=UserOut)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    根据用户ID获取用户信息

    需要有效的JWT令牌
    """
    user = await get_user(db, user_id=user_id)
    if user is None:
        logger.warning(f"获取用户失败: 用户ID {user_id} 不存在")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    logger.info(f"获取用户信息: 用户 {user.email} (ID: {user.id})")
    return user


@router.get("/", response_model=List[UserOut])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    获取用户列表

    需要有效的JWT令牌
    """
    users = await get_users(db, skip=skip, limit=limit)
    logger.info(f"获取用户列表: 跳过 {skip} 条，限制 {limit} 条，共返回 {len(users)} 条")
    return users


@router.put("/{user_id}", response_model=UserOut)
async def update_user_info(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    更新用户信息

    需要有效的JWT令牌，只能更新自己的信息
    """
    # 只能更新自己的信息
    if current_user.id != user_id:
        logger.warning(f"更新用户信息失败: 用户 {current_user.email} (ID: {current_user.id}) 尝试更新用户 ID {user_id} 的信息，权限不足")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限更新该用户信息",
        )

    user = await get_user(db, user_id=user_id)
    if user is None:
        logger.warning(f"更新用户信息失败: 用户ID {user_id} 不存在")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )

    user = await update_user(db, user=user, user_in=user_in)
    logger.info(f"更新用户信息成功: 用户 {user.email} (ID: {user.id})")
    return user