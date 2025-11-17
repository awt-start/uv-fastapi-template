# app/core/const.py

from enum import IntEnum


class ResponseCode(IntEnum):
    """业务响应码（非 HTTP 状态码）"""

    SUCCESS = 0
    FAIL = 1
    UNAUTHORIZED = 2
    FORBIDDEN = 3
    USER_NOT_FOUND = 1001
    USER_EXISTS = 1002
    INVALID_TOKEN = 1003
    TOKEN_EXPIRED = 1004
    VALIDATION_ERROR = 1005
    SYSTEM_ERROR = 5000


# 可选：映射默认消息
_RESPONSE_MSG = {
    ResponseCode.SUCCESS: "成功",
    ResponseCode.FAIL: "失败",
    ResponseCode.UNAUTHORIZED: "未登录或会话过期",
    ResponseCode.FORBIDDEN: "权限不足",
    ResponseCode.USER_NOT_FOUND: "用户不存在",
    ResponseCode.USER_EXISTS: "用户已存在",
    ResponseCode.INVALID_TOKEN: "无效的令牌",
    ResponseCode.TOKEN_EXPIRED: "登录已过期，请重新登录",
    ResponseCode.VALIDATION_ERROR: "参数校验失败",
    ResponseCode.SYSTEM_ERROR: "系统异常，请稍后重试",
}
