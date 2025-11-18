from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.models import Student
from app.schemas.student import StudentCreate, StudentUpdate
from app.core.logger import get_logger
from typing import Union, List

# 获取日志实例
logger = get_logger(__name__)


async def get_student(db: AsyncSession, student_id: int) -> Union[Student, None]:
    """
    根据学生ID获取学生

    Args:
        db: 数据库会话
        student_id: 学生ID

    Returns:
        学生对象或None
    """
    result = await db.execute(select(Student).where(Student.id == student_id))
    return result.scalar_one_or_none()


async def get_student_by_student_id(
    db: AsyncSession, student_id: str
) -> Union[Student, None]:
    """
    根据学号获取学生

    Args:
        db: 数据库会话
        student_id: 学号

    Returns:
        学生对象或None
    """
    result = await db.execute(select(Student).where(Student.student_id == student_id))
    return result.scalar_one_or_none()


async def create_student(db: AsyncSession, student_in: StudentCreate) -> Student:
    """
    创建新学生

    Args:
        db: 数据库会话
        student_in: 学生创建数据

    Returns:
        创建的学生对象
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

    # 创建学生对象
    student = Student(**student_in.model_dump())

    # 保存到数据库
    db.add(student)
    await db.commit()
    await db.refresh(student)

    logger.info(
        f"创建学生成功: {student.name} (学号: {student.student_id}, ID: {student.id})"
    )
    return student


async def update_student(
    db: AsyncSession, student: Student, student_in: StudentUpdate
) -> Student:
    """
    更新学生信息

    Args:
        db: 数据库会话
        student: 原学生对象
        student_in: 学生更新数据

    Returns:
        更新后的学生对象
    """
    # 更新学生字段
    update_data = student_in.model_dump(exclude_unset=True)

    # 如果包含学号，需要检查是否已被其他学生使用
    if "student_id" in update_data and update_data["student_id"] != student.student_id:
        existing_student = await get_student_by_student_id(
            db, student_id=update_data["student_id"]
        )
        if existing_student:
            logger.warning(f"更新学生失败: 学号 {update_data['student_id']} 已被使用")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该学号已被使用",
            )

    # 更新学生对象
    for field, value in update_data.items():
        setattr(student, field, value)

    # 保存到数据库
    db.add(student)
    await db.commit()
    await db.refresh(student)

    logger.info(
        f"更新学生成功: {student.name} (学号: {student.student_id}, ID: {student.id})"
    )
    return student


async def get_students(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[Student]:
    """
    获取学生列表

    Args:
        db: 数据库会话
        skip: 跳过的记录数
        limit: 返回的最大记录数

    Returns:
        学生对象列表
    """
    result = await db.execute(select(Student).offset(skip).limit(limit))
    return result.scalars().all()


async def delete_student(db: AsyncSession, student: Student) -> None:
    """
    删除学生

    Args:
        db: 数据库会话
        student: 要删除的学生对象

    Returns:
        None
    """
    await db.delete(student)
    await db.commit()
    logger.info(
        f"删除学生成功: {student.name} (学号: {student.student_id}, ID: {student.id})"
    )
