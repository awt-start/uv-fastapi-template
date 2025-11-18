# app/utils/converter.py
from typing import Any, Dict, List
from datetime import datetime

def dict_to_json_str(data: Dict) -> str:
    """字典转JSON字符串"""
    import json
    return json.dumps(data, ensure_ascii=False, default=str)

def remove_none_values(data: Dict) -> Dict:
    """移除字典中的None值"""
    return {k: v for k, v in data.items() if v is not None}

def flatten_dict(d: Dict, parent_key: str = '', sep: str = '_') -> Dict:
    """扁平化嵌套字典"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def list_to_dict(items: List, key_field: str) -> Dict:
    """列表转字典(以指定字段作为键)"""
    return {item[key_field]: item for item in items if key_field in item}