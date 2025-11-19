"""工具函数包

本模块提供了项目中常用的工具函数，包括：
- 常量定义（const）
- 数据转换（converter）
- 日期时间处理（datetime）
- 文件操作（file）
- 字符串处理（string）
- 加密解密（crypto）
"""

# 导出所有工具函数和常量
from app.toolkit.const import ResponseCode, _RESPONSE_MSG
from app.toolkit.converter import (
    dict_to_json_str,
    remove_none_values,
    flatten_dict,
    list_to_dict,
    model_to_dict,
    camel_to_snake,
    snake_to_camel,
    snake_to_pascal
)
from app.toolkit.datetime_utils import (
    get_timestamp,
    format_datetime,
    parse_datetime,
    get_relative_time,
    get_month_days,
    get_date_diff,
    format_time_delta,
    get_first_day_of_month,
    get_last_day_of_month,
    add_days,
    is_between_dates
)
from app.toolkit.file import (
    get_file_size,
    get_file_size_str,
    get_file_hash,
    copy_file,
    move_file,
    create_directory,
    delete_file,
    list_files,
    get_file_extension,
    is_file_exists,
    is_directory_exists,
    get_file_name
)
from app.toolkit.string_utils import (
    is_valid_email,
    is_valid_phone,
    generate_random_string,
    mask_sensitive_info,
    remove_html_tags,
    to_title_case,
    to_camel_case,
    to_snake_case,
    truncate_string,
    count_words,
    remove_special_chars
)
from app.toolkit.crypto import (
    generate_password_hash,
    verify_password,
    generate_hmac_signature,
    verify_hmac_signature,
    get_md5_hash,
    get_sha256_hash,
    generate_random_token
)

__all__ = [
    # const
    "ResponseCode",
    "_RESPONSE_MSG",
    
    # converter
    "dict_to_json_str",
    "remove_none_values",
    "flatten_dict",
    "list_to_dict",
    "model_to_dict",
    "camel_to_snake",
    "snake_to_camel",
    "snake_to_pascal",
    
    # datetime
    "get_timestamp",
    "format_datetime",
    "parse_datetime",
    "get_relative_time",
    "get_month_days",
    "get_date_diff",
    "format_time_delta",
    "get_first_day_of_month",
    "get_last_day_of_month",
    "add_days",
    "is_between_dates",
    
    # file
    "get_file_size",
    "get_file_size_str",
    "get_file_hash",
    "copy_file",
    "move_file",
    "create_directory",
    "delete_file",
    "list_files",
    "get_file_extension",
    "is_file_exists",
    "is_directory_exists",
    "get_file_name",
    
    # string
    "is_valid_email",
    "is_valid_phone",
    "generate_random_string",
    "mask_sensitive_info",
    "remove_html_tags",
    "to_title_case",
    "to_camel_case",
    "to_snake_case",
    "truncate_string",
    "count_words",
    "remove_special_chars",
    
    # crypto
    "generate_password_hash",
    "verify_password",
    "generate_hmac_signature",
    "verify_hmac_signature",
    "get_md5_hash",
    "get_sha256_hash",
    "generate_random_token"
]