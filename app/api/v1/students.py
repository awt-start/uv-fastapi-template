from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.logger import get_logger
from app.crud import (
    get_student,
    get_students,
    create_student,
    update_student,
    delete_student,
    get_student_by_student_id,
)
from app.models import User, Student
from app.schemas import StudentOut, StudentCreate, StudentUpdate
from app.models.response import success, error

# 获取日志实例
logger = get_logger(__name__)

router = APIRouter()


@router.get("/", response_model=List[StudentOut])
async def read_students(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    获取学生列表

    需要有效的JWT令牌
    """
    students = await get_students(db, skip=skip, limit=limit)
    logger.info(
        f"获取学生列表: 跳过 {skip} 条，限制 {limit} 条，共返回 {len(students)} 条"
    )
    return success(data=students)


@router.get("/{student_id}", response_model=StudentOut)
async def read_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    根据学生ID获取学生信息

    需要有效的JWT令牌
    """
    student = await get_student(db, student_id=student_id)
    if student is None:
        logger.warning(f"获取学生失败: 学生ID {student_id} 不存在")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生不存在",
        )
    logger.info(
        f"获取学生信息: 学生 {student.name} (学号: {student.student_id}, ID: {student.id})"
    )
    return success(data=student)


@router.post("/", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
async def create_new_student(
    student_in: StudentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    创建新学生

    需要有效的JWT令牌
    """
    # 检查学号是否已存在
    existing_student = await get_student_by_student_id(
        db, student_id=student_in.student_id
    )
    if existing_student:
        logger.warning(f"创建学生失败: 学号 {student_in.student_id} 已被使用")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该学号已被使用",
        )

    student = await create_student(db, student_in=student_in)
    logger.info(
        f"创建学生成功: {student.name} (学号: {student.student_id}, ID: {student.id})"
    )
    return success(data=student)


@router.put("/{student_id}", response_model=StudentOut)
async def update_student_info(
    student_id: int,
    student_in: StudentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    更新学生信息

    需要有效的JWT令牌
    """
    student = await get_student(db, student_id=student_id)
    if student is None:
        logger.warning(f"更新学生信息失败: 学生ID {student_id} 不存在")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生不存在",
        )

    student = await update_student(db, student=student, student_in=student_in)
    logger.info(
        f"更新学生信息成功: {student.name} (学号: {student.student_id}, ID: {student.id})"
    )
    return success(data=student)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student_info(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    删除学生信息

    需要有效的JWT令牌
    """
    student = await get_student(db, student_id=student_id)
    if student is None:
        logger.warning(f"删除学生失败: 学生ID {student_id} 不存在")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生不存在",
        )

    await delete_student(db, student=student)
    logger.info(
        f"删除学生成功: {student.name} (学号: {student.student_id}, ID: {student.id})"
    )
    return success(msg="学生删除成功")
