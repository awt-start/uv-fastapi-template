# app/utils/string.py
import re
from typing import Optional

def is_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_phone(phone: str) -> bool:
    """验证手机号(中国)"""
    pattern = r'^1[3-9]\d{9}$'
    return re.match(pattern, phone) is not None

def slugify(text: str) -> str:
    """将文本转换为URL友好格式"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    return re.sub(r'[-\s]+', '-', text).strip('-')

def truncate(text: str, length: int = 100, suffix: str = "...") -> str:
    """截断文本到指定长度"""
    if len(text) <= length:
        return text
    return text[:length - len(suffix)] + suffix