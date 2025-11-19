# app/toolkit/file.py
import os
import hashlib
import shutil
from pathlib import Path
from typing import List, Optional


def get_file_size(file_path: str) -> int:
    """获取文件大小
    
    Args:
        file_path: 文件路径
        
    Returns:
        int: 文件大小(字节)
    """
    return os.path.getsize(file_path)


def get_file_size_str(file_path: str) -> str:
    """获取文件大小(带单位)
    
    Args:
        file_path: 文件路径
        
    Returns:
        str: 文件大小(带单位)
    """
    size = get_file_size(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"


def get_file_hash(file_path: str, hash_type: str = "md5") -> str:
    """获取文件哈希值
    
    Args:
        file_path: 文件路径
        hash_type: 哈希算法类型
        
    Returns:
        str: 文件哈希值
    """
    hash_func = getattr(hashlib, hash_type, hashlib.md5)
    h = hash_func()
    with open(file_path, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            h.update(data)
    return h.hexdigest()


def safe_path_join(*parts: str) -> str:
    """安全地拼接路径(防止目录穿越)"""
    base = Path(parts[0]).resolve()
    for part in parts[1:]:
        full_path = (base / part).resolve()
        if not str(full_path).startswith(str(base)):
            raise ValueError(f"Path traversal detected: {full_path}")
    return str(base)


def copy_file(src: str, dst: str) -> None:
    """复制文件
    
    Args:
        src: 源文件路径
        dst: 目标文件路径
        
    Returns:
        None
    """
    shutil.copy2(src, dst)


def move_file(src: str, dst: str) -> None:
    """移动文件
    
    Args:
        src: 源文件路径
        dst: 目标文件路径
        
    Returns:
        None
    """
    shutil.move(src, dst)


def create_directory(directory: str) -> None:
    """创建目录(如果不存在)
    
    Args:
        directory: 目录路径
        
    Returns:
        None
    """
    os.makedirs(directory, exist_ok=True)


def delete_file(file_path: str) -> None:
    """删除文件
    
    Args:
        file_path: 文件路径
        
    Returns:
        None
    """
    if os.path.exists(file_path):
        os.remove(file_path)


def list_files(directory: str, extension: Optional[str] = None) -> List[str]:
    """列出目录中的文件
    
    Args:
        directory: 目录路径
        extension: 文件扩展名(如: ".txt")
        
    Returns:
        List[str]: 文件路径列表
    """
    files = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            if extension is None or filename.endswith(extension):
                files.append(filepath)
    return files


def get_file_extension(file_path: str) -> str:
    """获取文件扩展名
    
    Args:
        file_path: 文件路径
        
    Returns:
        str: 文件扩展名
    """
    return os.path.splitext(file_path)[1].lower()


def is_file_exists(file_path: str) -> bool:
    """检查文件是否存在
    
    Args:
        file_path: 文件路径
        
    Returns:
        bool: 文件是否存在
    """
    return os.path.isfile(file_path)


def is_directory_exists(directory: str) -> bool:
    """检查目录是否存在
    
    Args:
        directory: 目录路径
        
    Returns:
        bool: 目录是否存在
    """
    return os.path.isdir(directory)


def get_file_name(file_path: str, with_extension: bool = True) -> str:
    """获取文件名
    
    Args:
        file_path: 文件路径
        with_extension: 是否包含扩展名
        
    Returns:
        str: 文件名
    """
    if with_extension:
        return os.path.basename(file_path)
    return os.path.splitext(os.path.basename(file_path))[0]
