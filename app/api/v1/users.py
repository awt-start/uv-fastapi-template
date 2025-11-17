from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.core.deps import get_current_user
from app.crud import get_user, get_users, update_user
from app.models import User
from app.schemas import UserOut, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserOut)
async def read_users_me(
    current_user: User = Depends(get_current_user),
):
    """
    获取当前用户信息

    需要有效的JWT令牌
    """
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
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
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限更新该用户信息",
        )

    user = await get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )

    user = await update_user(db, user=user, user_in=user_in)
    return user
