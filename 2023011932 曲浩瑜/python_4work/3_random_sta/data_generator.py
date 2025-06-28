import random
import uuid
import datetime
import functools
import collections
from dateutil import parser
from typing import Any, Dict, List, Union, Optional, Callable, Iterable, Set, Tuple
from faker import Faker

fake = Faker('zh_CN')


def generate_data(length: int, **kwargs) -> List[Dict[str, Any]]:
    for _ in range(length):
        item = {}
        for field_name, field_config in kwargs.items():
            item[field_name] = generate_field_value(field_config)
        yield item


def generate_field_value(field_config: Dict[str, Any]) -> Any:
    # 默认为string
    field_type = field_config.get('type', 'string')
    if field_type == 'int':
        return generate_int(field_config)
    elif field_type == 'float':
        return generate_float(field_config)
    elif field_type == 'bool':
        return generate_bool(field_config)
    elif field_type == 'string':
        return generate_string(field_config)
    elif field_type == 'datetime':
        return generate_datetime(field_config)
    elif field_type == 'uuid':
        return generate_uuid()
    elif field_type == 'sequence':
        return generate_sequence(field_config)
    elif field_type == 'list':
        return generate_list(field_config)
    elif field_type == 'dict':
        return generate_dict(field_config)
    else:
        raise ValueError(f"不支持的字段类型: {field_type}")


def generate_int(config: Dict[str, Any]) -> int:
    """生成整数"""
    min_val = config.get('min', 0)
    max_val = config.get('max', 100)
    return random.randint(min_val, max_val)


def generate_float(config: Dict[str, Any]) -> float:
    """生成浮点数"""
    min_val = config.get('min', 0.0)
    max_val = config.get('max', 1.0)
    precision = config.get('precision', 2)
    value = random.uniform(min_val, max_val)
    return round(value, precision)


def generate_bool(config: Dict[str, Any]) -> bool:
    """生成布尔值"""
    weight = config.get('weight', 0.5)
    return random.random() < weight


def generate_string(config: Dict[str, Any]) -> str:
    """生成字符串"""
    if 'values' in config:
        return random.choice(config['values'])
    length = config.get('length', 10)
    charset = config.get('charset', 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    if charset == 'chinese':
        if length < 5:
            return fake.name()[:length]
        else:
            return fake.text(max_nb_chars=length)[:length]
    else:
        return ''.join(random.choice(charset) for _ in range(length))


def generate_datetime(config: Dict[str, Any]) -> str:
    """生成日期时间"""
    start_date = config.get('start', '1949-01-01')
    end_date = config.get('end', '2099-12-31')
    format_str = config.get('format', '%Y-%m-%d %H:%M:%S')
    if isinstance(start_date, str):
        start_date = parser.parse(start_date)
    if isinstance(end_date, str):
        end_date = parser.parse(end_date)
    time_diff = int((end_date - start_date).total_seconds())
    # 随机生成一个时间点
    random_seconds = random.randint(0, time_diff)
    random_date = start_date + datetime.timedelta(seconds=random_seconds)
    return random_date.strftime(format_str)


def generate_uuid() -> str:
    """生成UUID"""
    return str(uuid.uuid4())


_sequence_counters = {}


def generate_sequence(config: Dict[str, Any]) -> int:
    """生成序列值"""
    start = config.get('start', 1)
    step = config.get('step', 1)
    # 使用配置的哈希作为计数器的键
    config_hash = str(hash(frozenset(config.items())))
    if config_hash not in _sequence_counters:
        _sequence_counters[config_hash] = start - step
    _sequence_counters[config_hash] += step
    return _sequence_counters[config_hash]


def generate_list(config: Dict[str, Any]) -> List[Any]:
    """生成列表"""
    element_config = config.get('of', {'type': 'string'})
    if 'length' in config:
        length = config['length']
    elif 'min_length' in config and 'max_length' in config:
        length = random.randint(config['min_length'], config['max_length'])
    else:
        length = random.randint(1, 5)
    return [generate_field_value(element_config) for _ in range(length)]


def generate_dict(config: Dict[str, Any]) -> Dict[str, Any]:
    """生成字典"""
    schema = config.get('schema', {})
    result = {}
    for field_name, field_config in schema.items():
        result[field_name] = generate_field_value(field_config)
    return result


def stats_decorator(*operations):
    """
    带参数的装饰器，用于对数据生成函数进行统计操作
    
    Args:
        operations: 统计操作列表，可选值为'SUM'、'AVG'、'MAX'、'MIN'
        
    Returns:
        装饰器函数
    """
    valid_operations = {'SUM', 'AVG', 'MAX', 'MIN'}
    
    # 验证输入的操作是否有效
    for op in operations:
        if op not in valid_operations:
            raise ValueError(f"不支持的统计操作: {op}，有效操作: {', '.join(valid_operations)}")
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 收集生成器生成的所有数据
            data = list(func(*args, **kwargs))
            
            # 如果没有指定任何操作，直接返回数据
            if not operations:
                return data
            
            # 定义统计函数
            stats_funcs = {
                'SUM': lambda values: sum(values),
                'AVG': lambda values: sum(values) / len(values) if values else 0,
                'MAX': lambda values: max(values) if values else None,
                'MIN': lambda values: min(values) if values else None
            }
            
            # 统计结果
            stats_results = {}
            
            # 检查数据是否非空
            if data:
                # 获取数据的所有字段
                all_fields = set()
                for item in data:
                    all_fields.update(item.keys())
                
                # 对每个字段进行统计
                for field in all_fields:
                    # 收集所有可以进行数值统计的值
                    numeric_values = []
                    for item in data:
                        if field in item:
                            value = item[field]
                            # 只对数值类型进行统计
                            if isinstance(value, (int, float)):
                                numeric_values.append(value)
                    
                    # 如果有数值可以统计
                    if numeric_values:
                        field_stats = {}
                        for op in operations:
                            field_stats[op] = stats_funcs[op](numeric_values)
                        
                        stats_results[field] = field_stats
            
            # 返回原始数据和统计结果
            return {
                'data': data,
                'stats': stats_results
            }
        
        return wrapper
    
    return decorator
