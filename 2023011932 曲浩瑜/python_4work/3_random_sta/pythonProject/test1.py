import random
import uuid
import datetime
from dateutil import parser
from typing import Any, Dict, List, Union, Optional, Callable
from functools import wraps
from collections import defaultdict
from statistics import mean
from faker import Faker

fake = Faker('zh_CN')

# 全局变量存储统计信息
_statistics = defaultdict(dict)


def with_statistics(func: Callable) -> Callable:
    """装饰器，用于收集生成数据的统计信息"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        # 调用原始函数
        result = func(*args, **kwargs)

        # 如果是生成器，先转换为列表
        if hasattr(result, '__iter__') and not isinstance(result, (dict, list)):
            result = list(result)

        # 收集统计信息
        if isinstance(result, (list, dict)):
            collect_statistics(result, kwargs)

        return result

    return wrapper


def collect_statistics(data: Union[List[Dict], Dict], config: Dict) -> None:
    """收集数据的统计信息"""
    if isinstance(data, dict):
        data = [data]

    for field_name, field_config in config.items():
        field_type = field_config.get('type', 'string')

        if field_type in ('int', 'float'):
            values = []
            for item in data:
                if field_name in item:
                    # 处理嵌套结构
                    if isinstance(item[field_name], dict):
                        # 如果是字典类型，递归处理
                        nested_values = extract_numeric_values(item[field_name])
                        values.extend(nested_values)
                    elif isinstance(item[field_name], list):
                        # 如果是列表类型，检查元素是否为数值或包含数值的字典
                        for element in item[field_name]:
                            if isinstance(element, (int, float)):
                                values.append(element)
                            elif isinstance(element, dict):
                                nested_values = extract_numeric_values(element)
                                values.extend(nested_values)
                    else:
                        values.append(item[field_name])

            if values:
                _statistics[field_name]['max'] = max(values)
                _statistics[field_name]['min'] = min(values)
                _statistics[field_name]['avg'] = mean(values)
                _statistics[field_name]['count'] = len(values)


def extract_numeric_values(data: Dict) -> List[Union[int, float]]:
    """从字典中提取所有数值类型的值"""
    values = []
    for value in data.values():
        if isinstance(value, (int, float)):
            values.append(value)
        elif isinstance(value, dict):
            values.extend(extract_numeric_values(value))
        elif isinstance(value, list):
            for element in value:
                if isinstance(element, (int, float)):
                    values.append(element)
                elif isinstance(element, dict):
                    values.extend(extract_numeric_values(element))
    return values


def get_statistics() -> Dict:
    """获取统计信息"""
    return dict(_statistics)


def clear_statistics() -> None:
    """清除统计信息"""
    _statistics.clear()


# 应用装饰器
@with_statistics
def generate_data(length: int, **kwargs) -> List[Dict[str, Any]]:
    for _ in range(length):
        item = {}
        for field_name, field_config in kwargs.items():
            item[field_name] = generate_field_value(field_config)
        yield item


# 以下是原有代码保持不变...

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
