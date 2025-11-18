# app/core/response.py
from typing import TypeVar, Generic, Optional, List, Any
from pydantic import BaseModel, Field
from enum import Enum

T = TypeVar("T")


class CodeEnum(int, Enum):
    """响应状态码枚举"""
    OK = 200
    WARN = 601
    PARAM_ERROR = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    SERVER_ERROR = 500


class PageInfo(BaseModel, Generic[T]):
    """
    分页信息对象
    
    包含分页元数据：当前页、页大小、总数、总页数
    """
    page: int = Field(default=1, ge=1, description="当前页码")
    page_size: int = Field(default=10, ge=1, description="每页大小")
    total: int = Field(default=0, ge=0, description="总记录数")
    total_pages: int = Field(default=0, ge=0, description="总页数")
    items: List[T] = Field(default_factory=list, description="分页数据列表")
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_list(
        cls,
        items: List[T],
        page: int = 1,
        page_size: int = 10
    ) -> "PageInfo[T]":
        """从列表创建分页信息（假分页）"""
        total = len(items)
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0
        
        start = (page - 1) * page_size
        end = start + page_size
        page_items = items[start:end]
        
        return cls(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
            items=page_items
        )


class R(BaseModel, Generic[T]):
    """
    统一响应模型，融合了分页支持
    
    可用于：
    - 普通响应：R.ok(data=user)
    - 分页响应：R.ok(data=page_info)
    - 错误响应：R.fail(msg="错误信息")
    - 警告响应：R.warn(msg="警告信息")
    """
    code: int = Field(default=200, description="响应状态码")
    msg: str = Field(default="操作成功", description="响应消息")
    data: Optional[T] = Field(default=None, description="响应数据（支持泛型）")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "code": 200,
                "msg": "操作成功",
                "data": None
            }
        }
    
    # ==================== 成功响应 ====================
    
    @classmethod
    def ok(
        cls,
        data: Optional[T] = None,
        msg: str = "操作成功",
        code: int = CodeEnum.OK
    ) -> "R[T]":
        """
        返回成功响应
        
        :param data: 响应数据（可以是任何类型，包括 PageInfo）
        :param msg: 响应消息
        :param code: 状态码
        :return: R 对象
        """
        return cls(code=code, msg=msg, data=data)
    
    @classmethod
    def ok_page(
        cls,
        page_info: PageInfo[T],
        msg: str = "查询成功"
    ) -> "R[PageInfo[T]]":
        """
        返回分页成功响应
        
        :param page_info: PageInfo 分页对象
        :param msg: 响应消息
        :return: R[PageInfo[T]] 对象
        """
        return R[PageInfo[T]](code=CodeEnum.OK, msg=msg, data=page_info)
    
    # ==================== 错误响应 ====================
    
    @classmethod
    def fail(
        cls,
        msg: str = "操作失败",
        data: Optional[T] = None,
        code: int = CodeEnum.SERVER_ERROR
    ) -> "R[T]":
        """
        返回失败响应
        
        :param msg: 错误消息
        :param data: 错误详情数据（可选）
        :param code: 状态码
        :return: R 对象
        """
        return cls(code=code, msg=msg, data=data)
    
    @classmethod
    def param_error(
        cls,
        msg: str = "参数错误",
        data: Optional[T] = None
    ) -> "R[T]":
        """返回参数错误响应"""
        return cls.fail(msg=msg, data=data, code=CodeEnum.PARAM_ERROR)
    
    @classmethod
    def not_found(
        cls,
        msg: str = "资源不存在",
        data: Optional[T] = None
    ) -> "R[T]":
        """返回资源不存在响应"""
        return cls.fail(msg=msg, data=data, code=CodeEnum.NOT_FOUND)
    
    @classmethod
    def unauthorized(
        cls,
        msg: str = "未授权",
        data: Optional[T] = None
    ) -> "R[T]":
        """返回未授权响应"""
        return cls.fail(msg=msg, data=data, code=CodeEnum.UNAUTHORIZED)
    
    @classmethod
    def forbidden(
        cls,
        msg: str = "禁止访问",
        data: Optional[T] = None
    ) -> "R[T]":
        """返回禁止访问响应"""
        return cls.fail(msg=msg, data=data, code=CodeEnum.FORBIDDEN)
    
    # ==================== 警告响应 ====================
    
    @classmethod
    def warn(
        cls,
        msg: str = "警告",
        data: Optional[T] = None
    ) -> "R[T]":
        """
        返回警告响应
        
        :param msg: 警告消息
        :param data: 警告详情数据（可选）
        :return: R 对象
        """
        return cls(code=CodeEnum.WARN, msg=msg, data=data)
    
    # ==================== 工具方法 ====================
    
    @staticmethod
    def is_success(response: "R") -> bool:
        """判断响应是否成功"""
        return response.code == CodeEnum.OK
    
    @staticmethod
    def is_error(response: "R") -> bool:
        """判断响应是否错误"""
        return response.code != CodeEnum.OK


# ==================== 便捷函数 ====================

def page_success(
    items: List[T],
    page: int = 1,
    page_size: int = 10,
    msg: str = "查询成功"
) -> R[PageInfo[T]]:
    """
    快速构建分页成功响应
    
    :param items: 数据列表
    :param page: 当前页码
    :param page_size: 每页大小
    :param msg: 响应消息
    :return: R[PageInfo[T]] 对象
    """
    page_info = PageInfo.from_list(items, page, page_size)
    return R.ok_page(page_info, msg=msg)


def success(data: Optional[T] = None, msg: str = "操作成功") -> R[T]:
    """快速返回成功响应"""
    return R.ok(data=data, msg=msg)


def error(msg: str = "操作失败", code: int = CodeEnum.SERVER_ERROR) -> R:
    """快速返回错误响应"""
    return R.fail(msg=msg, code=code)


def warn(msg: str = "警告", data: Optional[T] = None) -> R[T]:
    """快速返回警告响应"""
    return R.warn(msg=msg, data=data)
