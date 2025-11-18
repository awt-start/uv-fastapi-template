# app/models/student.py
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.models.base import BaseModel
from app.models.user import User  # 假设 User 也升级为 2.0 风格


class Student(BaseModel):
    """学生模型"""

    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[str] = mapped_column(
        String(20), unique=True, index=True, comment="学号"
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="姓名")
    grade: Mapped[str] = mapped_column(
        String(20), nullable=True, comment="年级，如 '2023级'"
    )
    major: Mapped[str] = mapped_column(String(100), nullable=True, comment="专业")
    class_name: Mapped[str] = mapped_column(String(50), nullable=True, comment="班级")
