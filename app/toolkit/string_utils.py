# app/toolkit/string_utils.py
import re
import secrets
import string
from typing import Optional


def is_valid_email(email: str) -> bool:
    """验证邮箱格式
    
    Args:
        email: 邮箱地址
        
    Returns:
        bool: 是否为有效邮箱
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def is_valid_phone(phone: str) -> bool:
    """验证手机号格式
    
    Args:
        phone: 手机号
        
    Returns:
        bool: 是否为有效手机号
    """
    pattern = r"^1[3-9]\d{9}$"
    return bool(re.match(pattern, phone))


def generate_random_string(length: int = 8, chars: str = None) -> str:
    """生成随机字符串
    
    Args:
        length: 字符串长度
        chars: 可选的字符集
        
    Returns:
        str: 随机字符串
    """
    if chars is None:
        chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


def mask_sensitive_info(info: str, start: int = 0, end: Optional[int] = None, mask_char: str = "*") -> str:
    """字符串脱敏
    
    Args:
        info: 要脱敏的字符串
        start: 开始保留的字符数
        end: 结束保留的字符数
        mask_char: 脱敏字符
        
    Returns:
        str: 脱敏后的字符串
    """
    if not info:
        return ""
    
    length = len(info)
    if end is None:
        end = length // 3
    
    if start + end >= length:
        return info
    
    return info[:start] + mask_char * (length - start - end) + info[-end:]


def remove_html_tags(text: str) -> str:
    """移除HTML标签
    
    Args:
        text: 包含HTML标签的文本
        
    Returns:
        str: 移除HTML标签后的文本
    """
    pattern = r"<[^>]*>"
    return re.sub(pattern, "", text)


def to_title_case(text: str) -> str:
    """首字母大写
    
    Args:
        text: 要转换的文本
        
    Returns:
        str: 首字母大写的文本
    """
    return text.title()


def to_camel_case(text: str) -> str:
    """转换为驼峰命名
    
    Args:
        text: 要转换的文本
        
    Returns:
        str: 驼峰命名的文本
    """
    words = text.replace("_", " ").replace("-", " ").split()
    return words[0].lower() + ''.join(word.title() for word in words[1:])


def to_snake_case(text: str) -> str:
    """转换为蛇形命名
    
    Args:
        text: 要转换的文本
        
    Returns:
        str: 蛇形命名的文本
    """
    # 添加下划线在大写字母前
    text = re.sub(r'(?<!^)(?=[A-Z])', '_', text)
    # 替换空格和连字符为下划线
    text = text.replace(" ", "_").replace("-", "_")
    return text.lower()


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """截断字符串
    
    Args:
        text: 要截断的文本
        max_length: 最大长度
        suffix: 后缀
        
    Returns:
        str: 截断后的文本
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def count_words(text: str) -> int:
    """计算单词数
    
    Args:
        text: 要计算的文本
        
    Returns:
        int: 单词数
    """
    if not text:
        return 0
    return len(text.split())


def remove_special_chars(text: str, keep_chars: str = "_") -> str:
    """移除特殊字符
    
    Args:
        text: 要处理的文本
        keep_chars: 要保留的特殊字符
        
    Returns:
        str: 移除特殊字符后的文本
    """
    pattern = f"[^{re.escape(string.ascii_letters + string.digits + keep_chars)}]"
    return re.sub(pattern, "", text)
