# app/db/base.py
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime, Integer, Text
from sqlalchemy.sql import func
from typing import Optional


class Base(DeclarativeBase):
    """SQLAlchemy 2.0 基类"""

    pass


class BaseModel(Base):
    """
    通用基础模型（抽象类）
    所有业务模型应继承此类
    """

    __abstract__ = True

    # 软删除
    is_deleted: Mapped[bool] = mapped_column(
        default=False, nullable=False, comment="软删除标志"
    )

    # 时间戳
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), comment="创建时间"
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="最后更新时间",
    )

    # 操作人（通常由业务层传入，如当前用户 ID 或 email）
    created_by: Mapped[Optional[str]] = mapped_column(String(255), comment="创建人")
    updated_by: Mapped[Optional[str]] = mapped_column(String(255), comment="最后更新人")

    # 通用业务字段
    status: Mapped[Optional[str]] = mapped_column(
        String(50), default="active", comment="状态（如：active, inactive, pending 等）"
    )
    sort_order: Mapped[int] = mapped_column(
        Integer, default=0, comment="排序序号，值越小越靠前"
    )
    remark: Mapped[Optional[str]] = mapped_column(
        Text, comment="备注信息，可用于记录额外说明"
    )
