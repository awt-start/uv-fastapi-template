#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Toolkit模块测试脚本
"""

import os
import sys
import datetime
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.toolkit import (
    # const模块
    ResponseCode, _RESPONSE_MSG,
    
    # converter模块
    dict_to_json_str, remove_none_values, flatten_dict, list_to_dict,
    model_to_dict, camel_to_snake, snake_to_camel, snake_to_pascal,
    
    # datetime_utils模块
    get_timestamp, format_datetime, parse_datetime, get_relative_time,
    get_month_days, get_date_diff, format_time_delta, get_first_day_of_month,
    get_last_day_of_month, add_days, is_between_dates,
    
    # file模块
    get_file_size, get_file_size_str, get_file_hash, copy_file, move_file,
    create_directory, delete_file, list_files, get_file_extension,
    is_file_exists, is_directory_exists, get_file_name,
    
    # string模块
    is_valid_email, is_valid_phone, generate_random_string, mask_sensitive_info,
    remove_html_tags, to_title_case, to_camel_case, to_snake_case,
    truncate_string, count_words, remove_special_chars,
    
    # crypto模块
    generate_password_hash, verify_password, generate_hmac_signature,
    verify_hmac_signature, get_md5_hash, get_sha256_hash, generate_random_token
)


def test_const():
    """测试const模块"""
    print("=== 测试const模块 ===")
    print(f"响应码: SUCCESS={ResponseCode.SUCCESS}, FAIL={ResponseCode.FAIL}")
    print(f"默认消息: {_RESPONSE_MSG[ResponseCode.SUCCESS]}")
    print()


def test_converter():
    """测试converter模块"""
    print("=== 测试converter模块 ===")
    
    # 测试字典转JSON
    test_dict = {"name": "test", "value": 123}
    json_str = dict_to_json_str(test_dict)
    print(f"字典转JSON: {json_str}")
    
    # 测试移除None值
    test_dict_with_none = {"name": "test", "value": None, "age": 20}
    cleaned = remove_none_values(test_dict_with_none)
    print(f"移除None值: {cleaned}")
    
    # 测试命名转换
    camel_case = "userName"
    snake_case = "user_name"
    print(f"驼峰转蛇形({camel_case}): {camel_to_snake(camel_case)}")
    print(f"蛇形转驼峰({snake_case}): {snake_to_camel(snake_case)}")
    print(f"蛇形转帕斯卡({snake_case}): {snake_to_pascal(snake_case)}")
    print()


def test_datetime():
    """测试datetime模块"""
    print("=== 测试datetime模块 ===")
    
    # 测试获取时间戳
    timestamp = get_timestamp()
    print(f"当前时间戳: {timestamp}")
    
    # 测试格式化日期时间
    now = datetime.datetime.now()
    formatted = format_datetime(now)
    print(f"格式化日期: {formatted}")
    
    # 测试相对时间
    past_time = now - datetime.timedelta(days=2)
    relative = get_relative_time(past_time)
    print(f"相对时间: {relative}")
    
    # 测试月份天数
    days = get_month_days(2023, 2)
    print(f"2023年2月天数: {days}")
    print()


def test_file():
    """测试file模块"""
    print("=== 测试file模块 ===")
    
    # 创建测试文件
    test_file = "test_temp.txt"
    with open(test_file, "w") as f:
        f.write("测试文件内容")
    
    # 测试文件大小
    size = get_file_size(test_file)
    size_str = get_file_size_str(test_file)
    print(f"文件大小: {size}字节, {size_str}")
    
    # 测试文件哈希
    md5_hash = get_md5_hash(test_file)
    print(f"文件MD5: {md5_hash}")
    
    # 测试文件操作
    create_directory("test_dir")
    copy_file(test_file, "test_dir/test_copy.txt")
    print(f"文件是否存在: {is_file_exists("test_dir/test_copy.txt")}")
    
    # 清理测试文件
    delete_file(test_file)
    delete_file("test_dir/test_copy.txt")
    if is_directory_exists("test_dir"):
        import shutil
        shutil.rmtree("test_dir")
    
    print()


def test_string():
    """测试string模块"""
    print("=== 测试string模块 ===")
    
    # 测试邮箱验证
    email = "test@example.com"
    invalid_email = "invalid-email"
    print(f"邮箱验证 {email}: {is_valid_email(email)}")
    print(f"邮箱验证 {invalid_email}: {is_valid_email(invalid_email)}")
    
    # 测试手机号验证
    phone = "13800138000"
    invalid_phone = "1234567890"
    print(f"手机号验证 {phone}: {is_valid_phone(phone)}")
    print(f"手机号验证 {invalid_phone}: {is_valid_phone(invalid_phone)}")
    
    # 测试随机字符串
    random_str = generate_random_string(10)
    print(f"随机字符串: {random_str}")
    
    # 测试敏感信息脱敏
    card_number = "6222021234567890123"
    masked = mask_sensitive_info(card_number, start=4, end=4)
    print(f"信用卡脱敏: {masked}")
    print()


def test_crypto():
    """测试crypto模块"""
    print("=== 测试crypto模块 ===")
    
    # 测试密码哈希
    password = "password123"
    password_hash, salt = generate_password_hash(password)
    print(f"密码哈希: ({password_hash}, {salt})")
    print(f"验证密码: {verify_password(password, password_hash, salt)}")
    print(f"验证错误密码: {verify_password("wrong", password_hash, salt)}")
    
    # 测试随机令牌
    token = generate_random_token(32)
    print(f"随机令牌: {token}")
    
    # 测试HMAC签名
    message = "test message"
    secret = "secret_key"
    signature = generate_hmac_signature(message, secret)
    print(f"HMAC签名: {signature}")
    print(f"验证HMAC: {verify_hmac_signature(message, secret, signature)}")
    print()


def main():
    """运行所有测试"""
    print("开始测试toolkit模块...")
    print("=" * 50)
    
    try:
        test_const()
        test_converter()
        test_datetime()
        test_file()
        test_string()
        test_crypto()
        
        print("=" * 50)
        print("所有测试完成!")
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()