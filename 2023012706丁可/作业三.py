import random
import string
import datetime
from functools import wraps
from typing import Dict, List, Tuple, Union, Any, Generator, Optional

# 各数据类型的默认取值范围
DEFAULT_RANGES = {
    'int': (1, 100),
    'float': (0.0, 100.0),
    'double': (0.0, 100.0),
    'long': (1, 1000000),
    'date': (datetime.date(2000, 1, 1), datetime.date(2023, 12, 31)),
    'str': (5, 20)  # 字符串长度范围
}


def generate_random_value(data_type: str, datarange: Optional[Tuple[Any, Any]] = None) -> Any:
    """根据数据类型和范围生成随机值"""
    if datarange is None:
        datarange = DEFAULT_RANGES.get(data_type.lower(), (0, 100))

    data_type = data_type.lower()

    if data_type == 'int':
        return random.randint(datarange[0], datarange[1])
    elif data_type in ('float', 'double'):
        return random.uniform(datarange[0], datarange[1])
    elif data_type == 'long':
        return random.randint(datarange[0], datarange[1])
    elif data_type == 'date':
        start, end = datarange
        delta = end - start
        random_days = random.randint(0, delta.days)
        return start + datetime.timedelta(days=random_days)
    elif data_type == 'str':
        length = random.randint(datarange[0], datarange[1])
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    elif data_type == 'array':
        return [generate_random_value(item['type'], item.get('datarange')) for item in datarange]
    elif data_type == 'tuple':
        return tuple(generate_random_value(item['type'], item.get('datarange')) for item in datarange)
    elif data_type == 'dict':
        return {k: generate_random_value(v['type'], v.get('datarange')) for k, v in datarange.items()}
    else:
        raise ValueError(f"不支持的数据类型: {data_type}")


def recursive_data_generator(data_structure: Dict[str, Any], *args, **kwargs) -> Dict[str, Any]:
    """递归生成随机数据结构"""
    result = {}
    for key, value in data_structure.items():
        if isinstance(value, dict):
            if 'type' in value:
                result[key] = generate_random_value(value['type'], value.get('datarange'))
            else:
                result[key] = recursive_data_generator(value, *args, **kwargs)
        elif isinstance(value, list):
            if value and isinstance(value[0], dict) and 'type' in value[0]:
                result[key] = [generate_random_value(item['type'], item.get('datarange')) for item in value]
            else:
                result[key] = random.choice(value)
        else:
            result[key] = value
    return result


def extract_numeric_values(data: Any, numeric_values: List[Union[int, float]]) -> None:
    """递归提取数据结构中的所有数值"""
    if isinstance(data, (int, float)):
        numeric_values.append(data)
    elif isinstance(data, (list, tuple)):
        for item in data:
            extract_numeric_values(item, numeric_values)
    elif isinstance(data, dict):
        for value in data.values():
            extract_numeric_values(value, numeric_values)


def data_generator(data_structure: Dict[str, Any], total_count: int = 100000000, *args, **kwargs) -> Generator[
    Dict[str, Any], None, None]:
    """大数据量生成器"""
    count = 0
    while count < total_count:
        data = recursive_data_generator(data_structure, *args, **kwargs)
        numeric_values = []
        extract_numeric_values(data, numeric_values)
        yield {'data': data, 'numeric_values': numeric_values}
        count += 1


def stats_decorator(*stats_args):
    """带参数的统计装饰器"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            stats = {
                'sum': 0,
                'avg': 0,
                'max': -float('inf'),
                'min': float('inf'),
                'count': 0
            }

            all_numeric = []
            gen = func(*args, **kwargs)

            for item in gen:
                all_numeric.extend(item['numeric_values'])

            if all_numeric:
                stats.update({
                    'sum': sum(all_numeric),
                    'avg': sum(all_numeric) / len(all_numeric),
                    'max': max(all_numeric),
                    'min': min(all_numeric),
                    'count': len(all_numeric)
                })

            # 只返回请求的统计项
            result = {}
            for stat in stats_args:
                if stat in stats:
                    result[stat] = stats[stat]

            return result if result else stats

        return wrapper

    return decorator


@stats_decorator('sum', 'avg', 'max', 'min')
def generate_data_with_stats(*args, **kwargs) -> Generator[Dict[str, Any], None, None]:
    """生成带统计功能的数据"""
    for item in data_generator(*args, **kwargs):
        yield item


# 示例数据结构
example_structure = {
    "id": {"type": "int", "datarange": (1, 10000)},
    "name": {"type": "str", "datarange": (5, 15)},
    "price": {"type": "float", "datarange": (10.0, 1000.0)},
    "quantity": {"type": "int", "datarange": (1, 100)},
    "metadata": {
        "weight": {"type": "float", "datarange": (0.1, 50.0)},
        "dimensions": {
            "type": "tuple",
            "datarange": [
                {"type": "float", "datarange": (1.0, 10.0)},
                {"type": "float", "datarange": (1.0, 10.0)},
                {"type": "float", "datarange": (1.0, 10.0)}
            ]
        }
    },
    "tags": {
        "type": "array",
        "datarange": [
            {"type": "str", "datarange": (3, 8)},
            {"type": "int", "datarange": (1, 100)}
        ]
    },
    "created_at": {"type": "date", "datarange": (datetime.date(2010, 1, 1), datetime.date(2023, 12, 31))}
}

if __name__ == "__main__":
    # 生成2条记录并计算统计信息
    stats = generate_data_with_stats(example_structure, 2)
    print("2条记录的统计信息:")
    print(stats)

    # 生成2条示例数据(不计算统计信息)
    print("\n示例数据记录:")
    gen = data_generator(example_structure, 2)  # 只生成2条记录作为示例
    for i, record in enumerate(gen):
        print(f"\n记录 {i + 1}:")
        print(record['data'])