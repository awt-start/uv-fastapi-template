# app/toolkit/converter.py
from typing import Any, Dict, List, TypeVar, Union
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase

T = TypeVar('T', bound=DeclarativeBase)


def dict_to_json_str(data: Dict) -> str:
    """字典转JSON字符串
    
    Args:
        data: 要转换的字典数据
        
    Returns:
        str: JSON格式的字符串
    """
    import json
    return json.dumps(data, ensure_ascii=False, default=str)


def remove_none_values(data: Dict) -> Dict:
    """移除字典中的None值
    
    Args:
        data: 要处理的字典
        
    Returns:
        Dict: 移除None值后的字典
    """
    return {k: v for k, v in data.items() if v is not None}


def flatten_dict(d: Dict, parent_key: str = "", sep: str = "_") -> Dict:
    """扁平化嵌套字典
    
    Args:
        d: 要扁平化的字典
        parent_key: 父键名称
        sep: 键分隔符
        
    Returns:
        Dict: 扁平化后的字典
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            # 处理列表，将索引作为键的一部分
            for i, item in enumerate(v):
                list_key = f"{new_key}[{i}]"
                if isinstance(item, dict):
                    items.extend(flatten_dict(item, list_key, sep=sep).items())
                else:
                    items.append((list_key, item))
        else:
            items.append((new_key, v))
    return dict(items)


def list_to_dict(items: List, key_field: str) -> Dict:
    """列表转字典(以指定字段作为键)
    
    Args:
        items: 要转换的列表
        key_field: 作为键的字段名
        
    Returns:
        Dict: 以指定字段为键的字典
    """
    return {item[key_field]: item for item in items if key_field in item}


def model_to_dict(model: Union[T, List[T]], exclude_fields: List[str] = None) -> Union[Dict, List[Dict]]:
    """将SQLAlchemy模型转换为字典
    
    Args:
        model: SQLAlchemy模型实例或列表
        exclude_fields: 要排除的字段列表
        
    Returns:
        Union[Dict, List[Dict]]: 转换后的字典或字典列表
    """
    if exclude_fields is None:
        exclude_fields = []
    
    def _convert_single_model(m):
        if hasattr(m, "__dict__"):
            data = {k: v for k, v in m.__dict__.items() if not k.startswith("_") and k not in exclude_fields}
            # 处理datetime类型
            for k, v in data.items():
                if isinstance(v, datetime):
                    data[k] = v.isoformat()
            return data
        return {}
    
    if isinstance(model, list):
        return [_convert_single_model(m) for m in model]
    return _convert_single_model(model)


def camel_to_snake(s: str) -> str:
    """驼峰命名转蛇形命名
    
    Args:
        s: 驼峰命名的字符串
        
    Returns:
        str: 蛇形命名的字符串
    """
    import re
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()


def snake_to_camel(s: str) -> str:
    """蛇形命名转驼峰命名
    
    Args:
        s: 蛇形命名的字符串
        
    Returns:
        str: 驼峰命名的字符串
    """
    components = s.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def snake_to_pascal(s: str) -> str:
    """蛇形命名转帕斯卡命名
    
    Args:
        s: 蛇形命名的字符串
        
    Returns:
        str: 帕斯卡命名的字符串
    """
    components = s.split('_')
    return ''.join(x.title() for x in components)
