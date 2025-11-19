# app/toolkit/crypto.py
import hashlib
import hmac
import secrets
from typing import Tuple, Optional


def generate_password_hash(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    """生成密码哈希
    
    Args:
        password: 密码
        salt: 盐值
        
    Returns:
        Tuple[str, str]: (哈希值, 盐值)
    """
    if salt is None:
        salt = secrets.token_hex(16)
    # 使用pbkdf2_hmac算法
    password_bytes = password.encode('utf-8')
    salt_bytes = salt.encode('utf-8')
    
    # 生成哈希值
    hash_obj = hashlib.pbkdf2_hmac(
        'sha256',
        password_bytes,
        salt_bytes,
        100000  # 迭代次数
    )
    
    password_hash = hash_obj.hex()
    return password_hash, salt


def verify_password(password: str, password_hash: str, salt: str) -> bool:
    """验证密码
    
    Args:
        password: 密码
        password_hash: 密码哈希值
        salt: 盐值
        
    Returns:
        bool: 是否验证成功
    """
    computed_hash, _ = generate_password_hash(password, salt)
    return hmac.compare_digest(computed_hash, password_hash)


def generate_hmac_signature(data: str, key: str, algorithm: str = 'sha256') -> str:
    """生成HMAC签名
    
    Args:
        data: 要签名的数据
        key: 密钥
        algorithm: 哈希算法
        
    Returns:
        str: 签名
    """
    hash_func = getattr(hashlib, algorithm, hashlib.sha256)
    return hmac.new(
        key.encode('utf-8'),
        data.encode('utf-8'),
        hash_func
    ).hexdigest()


def verify_hmac_signature(data: str, signature: str, key: str, algorithm: str = 'sha256') -> bool:
    """验证HMAC签名
    
    Args:
        data: 数据
        signature: 签名
        key: 密钥
        algorithm: 哈希算法
        
    Returns:
        bool: 是否验证成功
    """
    computed_signature = generate_hmac_signature(data, key, algorithm)
    return hmac.compare_digest(computed_signature, signature)


def get_md5_hash(data: str) -> str:
    """获取MD5哈希值
    
    Args:
        data: 要哈希的数据
        
    Returns:
        str: MD5哈希值
    """
    return hashlib.md5(data.encode('utf-8')).hexdigest()


def get_sha256_hash(data: str) -> str:
    """获取SHA256哈希值
    
    Args:
        data: 要哈希的数据
        
    Returns:
        str: SHA256哈希值
    """
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def generate_random_token(length: int = 32) -> str:
    """生成随机令牌
    
    Args:
        length: 令牌长度
        
    Returns:
        str: 随机令牌
    """
    return secrets.token_hex(length // 2)