from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.models import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from typing import Union, List


async def get_user(db: AsyncSession, user_id: int) -> Union[User, None]:
    """
    根据用户ID获取用户

    Args:
        db: 数据库会话
        user_id: 用户ID

    Returns:
        用户对象或None
    """
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Union[User, None]:
    """
    根据邮箱获取用户

    Args:
        db: 数据库会话
        email: 用户邮箱

    Returns:
        用户对象或None
    """
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    """
    创建新用户

    Args:
        db: 数据库会话
        user_in: 用户创建数据

    Returns:
        创建的用户对象
    """
    # 检查邮箱是否已存在
    existing_user = await get_user_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被注册",
        )

    # 创建用户对象
    hashed_password = get_password_hash(user_in.password)
    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=hashed_password,
    )

    # 保存到数据库
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def update_user(db: AsyncSession, user: User, user_in: UserUpdate) -> User:
    """
    更新用户信息

    Args:
        db: 数据库会话
        user: 原用户对象
        user_in: 用户更新数据

    Returns:
        更新后的用户对象
    """
    # 更新用户字段
    update_data = user_in.model_dump(exclude_unset=True)

    # 如果包含密码，需要重新哈希
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    # 更新用户对象
    for field, value in update_data.items():
        setattr(user, field, value)

    # 保存到数据库
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def authenticate_user(
    db: AsyncSession, email: str, password: str
) -> Union[User, None]:
    """
    验证用户身份

    Args:
        db: 数据库会话
        email: 用户邮箱
        password: 用户密码

    Returns:
        验证成功返回用户对象，否则返回None
    """
    user = await get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    """
    获取用户列表

    Args:
        db: 数据库会话
        skip: 跳过的记录数
        limit: 返回的最大记录数

    Returns:
        用户对象列表
    """
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()
