from pydantic import BaseModel, Field
from datetime import datetime
from typing import Union


class StudentBase(BaseModel):
    """学生基础模型"""

    student_id: str = Field(..., max_length=20, description="学号")
    name: str = Field(..., max_length=50, description="姓名")
    grade: Union[str, None] = Field(None, max_length=20, description="年级")
    major: Union[str, None] = Field(None, max_length=100, description="专业")
    class_name: Union[str, None] = Field(None, max_length=50, description="班级")


class StudentCreate(StudentBase):
    """学生创建模型"""

    pass


class StudentUpdate(BaseModel):
    """学生更新模型"""

    student_id: Union[str, None] = Field(None, max_length=20, description="学号")
    name: Union[str, None] = Field(None, max_length=50, description="姓名")
    grade: Union[str, None] = Field(None, max_length=20, description="年级")
    major: Union[str, None] = Field(None, max_length=100, description="专业")
    class_name: Union[str, None] = Field(None, max_length=50, description="班级")


class StudentOut(StudentBase):
    """学生输出模型"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
