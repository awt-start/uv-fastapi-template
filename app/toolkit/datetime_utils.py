# app/toolkit/datetime.py
import datetime
import time
import calendar
from typing import Union, Tuple


def get_timestamp(ms: bool = False) -> int:
    """获取当前时间戳
    
    Args:
        ms: 是否返回毫秒级时间戳
        
    Returns:
        int: 当前时间戳
    """
    if ms:
        return int(time.time() * 1000)
    return int(time.time())


def format_datetime(dt: datetime.datetime = None, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """格式化日期时间
    
    Args:
        dt: 日期时间对象
        fmt: 格式化字符串
        
    Returns:
        str: 格式化后的日期时间字符串
    """
    if dt is None:
        dt = datetime.datetime.now()
    return dt.strftime(fmt)


def parse_datetime(date_str: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> datetime.datetime:
    """解析日期时间字符串
    
    Args:
        date_str: 日期时间字符串
        fmt: 格式化字符串
        
    Returns:
        datetime.datetime: 日期时间对象
    """
    return datetime.datetime.strptime(date_str, fmt)


def get_relative_time(dt: datetime.datetime = None) -> str:
    """获取相对时间
    
    Args:
        dt: 日期时间对象
        
    Returns:
        str: 相对时间描述
    """
    if dt is None:
        dt = datetime.datetime.now()
    now = datetime.datetime.now()
    diff = now - dt
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return f"{int(seconds)}秒前"
    elif seconds < 3600:
        return f"{int(seconds / 60)}分钟前"
    elif seconds < 86400:
        return f"{int(seconds / 3600)}小时前"
    elif seconds < 2592000:
        return f"{int(seconds / 86400)}天前"
    else:
        return dt.strftime("%Y-%m-%d")


def get_month_days(year: int, month: int) -> int:
    """获取指定月份的天数
    
    Args:
        year: 年份
        month: 月份
        
    Returns:
        int: 指定月份的天数
    """
    return calendar.monthrange(year, month)[1]


def get_date_diff(start_date: Union[str, datetime.datetime], end_date: Union[str, datetime.datetime]) -> Tuple[int, int, int]:
    """计算两个日期之间的差值
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
        
    Returns:
        Tuple[int, int, int]: (天数, 小时数, 分钟数)
    """
    if isinstance(start_date, str):
        start_date = parse_datetime(start_date)
    if isinstance(end_date, str):
        end_date = parse_datetime(end_date)
    
    diff = end_date - start_date
    days = diff.days
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    return days, hours, minutes


def format_time_delta(seconds: int) -> str:
    """格式化时间间隔
    
    Args:
        seconds: 秒数
        
    Returns:
        str: 格式化后的时间间隔
    """
    if seconds < 60:
        return f"{seconds}秒"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}分{secs}秒" if secs else f"{minutes}分"
    elif seconds < 86400:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}小时{minutes}分" if minutes else f"{hours}小时"
    else:
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        return f"{days}天{hours}小时" if hours else f"{days}天"


def get_first_day_of_month(dt: datetime.datetime = None) -> datetime.datetime:
    """获取当月第一天
    
    Args:
        dt: 日期时间对象
        
    Returns:
        datetime.datetime: 当月第一天的日期时间对象
    """
    if dt is None:
        dt = datetime.datetime.now()
    return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def get_last_day_of_month(dt: datetime.datetime = None) -> datetime.datetime:
    """获取当月最后一天
    
    Args:
        dt: 日期时间对象
        
    Returns:
        datetime.datetime: 当月最后一天的日期时间对象
    """
    if dt is None:
        dt = datetime.datetime.now()
    next_month = dt.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)


def add_days(dt: datetime.datetime = None, days: int = 1) -> datetime.datetime:
    """在指定日期上添加天数
    
    Args:
        dt: 日期时间对象
        days: 要添加的天数
        
    Returns:
        datetime.datetime: 添加天数后的日期时间对象
    """
    if dt is None:
        dt = datetime.datetime.now()
    return dt + datetime.timedelta(days=days)


def is_between_dates(dt: datetime.datetime = None, start_date: datetime.datetime = None, end_date: datetime.datetime = None) -> bool:
    """判断日期是否在指定范围内
    
    Args:
        dt: 要判断的日期时间对象
        start_date: 开始日期时间对象
        end_date: 结束日期时间对象
        
    Returns:
        bool: 是否在指定范围内
    """
    if dt is None:
        dt = datetime.datetime.now()
    if start_date is None or end_date is None:
        return False
    return start_date <= dt <= end_date
