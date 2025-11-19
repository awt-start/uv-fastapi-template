# Toolkit 工具包

本模块提供了各种实用工具函数，用于简化日常开发中的常见操作。

## 模块结构

- **const**: 常量定义
- **converter**: 数据转换工具
- **datetime**: 日期时间处理
- **file**: 文件操作
- **string**: 字符串处理
- **crypto**: 加密解密工具

## 使用方法

直接从toolkit模块导入所需的函数：

```python
from app.toolkit import get_timestamp, generate_password_hash, is_valid_email
```

## 各模块功能说明

### const 模块

定义了统一的响应码和默认消息：

```python
ResponseCode.SUCCESS  # 2000
ResponseCode.INVALID_PARAM  # 4001
ResponseCode.NOT_FOUND  # 4004
ResponseCode.INTERNAL_ERROR  # 5000
```

### converter 模块

提供数据转换功能：

- `dict_to_json_str`: 将字典转换为JSON字符串
- `remove_none_values`: 移除字典中的None值
- `flatten_dict`: 扁平化字典
- `list_to_dict`: 将列表转换为字典
- `model_to_dict`: 将SQLAlchemy模型转换为字典
- `camel_to_snake`: 驼峰命名转蛇形命名
- `snake_to_camel`: 蛇形命名转驼峰命名
- `snake_to_pascal`: 蛇形命名转帕斯卡命名

### datetime 模块

提供日期时间处理功能：

- `get_timestamp`: 获取当前时间戳
- `format_datetime`: 格式化日期时间
- `parse_datetime`: 解析日期时间字符串
- `get_relative_time`: 获取相对时间（如"3天前"）
- `get_month_days`: 获取指定月份的天数
- `get_date_diff`: 计算两个日期之间的差值
- `format_time_delta`: 格式化时间间隔
- `get_first_day_of_month`: 获取指定月份的第一天
- `get_last_day_of_month`: 获取指定月份的最后一天
- `add_days`: 给日期添加指定天数
- `is_between_dates`: 检查日期是否在指定范围内

### file 模块

提供文件操作功能：

- `get_file_size`: 获取文件大小（字节）
- `get_file_size_str`: 获取文件大小（带单位）
- `get_file_hash`: 计算文件哈希值
- `copy_file`: 复制文件
- `move_file`: 移动文件
- `create_directory`: 创建目录
- `delete_file`: 删除文件
- `list_files`: 列出目录下的文件
- `get_file_extension`: 获取文件扩展名
- `is_file_exists`: 检查文件是否存在
- `is_directory_exists`: 检查目录是否存在
- `get_file_name`: 获取文件名（不含扩展名）

### string 模块

提供字符串处理功能：

- `is_valid_email`: 验证邮箱格式
- `is_valid_phone`: 验证手机号格式
- `generate_random_string`: 生成随机字符串
- `mask_sensitive_info`: 敏感信息脱敏
- `remove_html_tags`: 移除HTML标签
- `to_title_case`: 转换为首字母大写
- `to_camel_case`: 转换为驼峰命名
- `to_snake_case`: 转换为蛇形命名
- `truncate_string`: 截断字符串
- `count_words`: 统计单词数量
- `remove_special_chars`: 移除特殊字符

### crypto 模块

提供加密解密功能：

- `generate_password_hash`: 生成密码哈希
- `verify_password`: 验证密码
- `generate_hmac_signature`: 生成HMAC签名
- `verify_hmac_signature`: 验证HMAC签名
- `get_md5_hash`: 计算MD5哈希
- `get_sha256_hash`: 计算SHA256哈希
- `generate_random_token`: 生成随机令牌

## 示例

### 日期时间处理

```python
from app.toolkit import get_timestamp, format_datetime, get_relative_time

# 获取当前时间戳
timestamp = get_timestamp()

# 格式化日期时间
formatted = format_datetime(datetime.now(), format="%Y-%m-%d %H:%M:%S")

# 获取相对时间
relative = get_relative_time(datetime.now() - timedelta(days=3))
# 输出: "3天前"
```

### 加密解密

```python
from app.toolkit import generate_password_hash, verify_password, get_md5_hash

# 生成密码哈希
hashed_pwd = generate_password_hash("password123")

# 验证密码
is_valid = verify_password("password123", hashed_pwd)

# 计算文件哈希
md5_hash = get_md5_hash("test.txt")
```

### 文件操作

```python
from app.toolkit import copy_file, create_directory, list_files

# 创建目录
create_directory("output")

# 复制文件
copy_file("input.txt", "output/input.txt")

# 列出目录下的文件
files = list_files("output")
```

## 注意事项

1. 所有函数都经过测试，确保可靠性
2. 函数命名遵循一致的命名规范（蛇形命名）
3. 提供了详细的函数文档和类型提示
4. 支持Python 3.8+