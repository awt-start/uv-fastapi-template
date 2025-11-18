# app/utils/datetime.py
from datetime import datetime, timedelta, timezone
from typing import Optional

def get_current_timestamp() -> int:
    """获取当前时间戳(秒)"""
    return int(datetime.now(timezone.utc).timestamp())

def format_datetime(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """格式化日期时间"""
    return dt.strftime(fmt)

def parse_datetime(date_str: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """解析日期字符串"""
    return datetime.strptime(date_str, fmt)

def get_date_range(start_date: datetime, end_date: datetime) -> list:
    """获取日期范围内的所有日期"""
    current = start_date
    dates = []
    while current <= end_date:
        dates.append(current.date())
        current += timedelta(days=1)
    return dates

def days_until(target_date: datetime) -> int:
    """计算距离目标日期还有多少天"""
    return (target_date.date() - datetime.now().date()).days