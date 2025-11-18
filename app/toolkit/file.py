# app/utils/file.py
import os
import hashlib
from pathlib import Path
from typing import Optional


def get_file_size(file_path: str) -> int:
    """获取文件大小(字节)"""
    return os.path.getsize(file_path)


def file_exists(file_path: str) -> bool:
    """检查文件是否存在"""
    return os.path.isfile(file_path)


def get_file_hash(file_path: str, algorithm: str = "md5") -> str:
    """计算文件哈希值"""
    hash_func = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def safe_path_join(*parts: str) -> str:
    """安全地拼接路径(防止目录穿越)"""
    base = Path(parts[0]).resolve()
    for part in parts[1:]:
        full_path = (base / part).resolve()
        if not str(full_path).startswith(str(base)):
            raise ValueError(f"Path traversal detected: {full_path}")
    return str(base)
