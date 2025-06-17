"""
改进版随机样本生成器与统计装饰器
@Author: Yang Haoda
@Version: 2.1
@Description:
1. 生成各种数据类型的随机样本
2. 使用装饰器添加统计功能
3. 支持SUM、AVG、MAX、MIN、VAR、RMSE六种统计操作

"""

import random
import math
from typing import Any, Dict, Generator, List, Tuple, Union


#  数据生成函数


def gen_str(data: Dict[str, Any]) -> str:
    """从指定字符串中随机生成指定长度的字符串"""
    return ''.join(random.choices(data['datarange'], k=data['len']))

def gen_int(data: Dict[str, Any]) -> int:
    """从随机数范围中生成随机int数"""
    return random.randint(data['datarange'][0], data['datarange'][1])

def gen_float(data: Dict[str, Any]) -> float:
    """从随机数范围中生成随机浮点数"""
    return random.uniform(data['datarange'][0], data['datarange'][1])

def gen_list(data: Dict[str, Any]) -> list:
    """生成列表"""
    return [generate_sample(item) for item in data['elements']]

def gen_dict(data: Dict[str, Any]) -> dict:
    """生成字典"""
    return {key: generate_sample(config) for key, config in data['fields'].items()}

def gen_tuple(data: Dict[str, Any]) -> tuple:
    """生成元组"""
    return tuple(generate_sample(item) for item in data['elements'])

# 类型映射字典
TYPE_TO_FUNC = {
    'str': gen_str,
    'int': gen_int,
    'float': gen_float,
    'list': gen_list,
    'dict': gen_dict,
    'tuple': gen_tuple,
}



def generate_sample(config: Dict[str, Any]) -> Any:
    """
    生成指定结构配置的随机样本。

    参数:
        config: 描述要生成数据结构的字典，格式为 {'type': ..., ...}

    返回:
        随机生成的样本数据
    """
    if 'type' not in config:
        raise ValueError(f"配置必须包含 'type' 键：{config}")

    type_name = config['type']

    if type_name not in TYPE_TO_FUNC:
        raise ValueError(f"不支持的类型：'{type_name}'")

    return TYPE_TO_FUNC[type_name](config)

def extract_numbers(data: Any) -> List[Union[int, float]]:
    """
    递归提取数据结构中的所有数值（整数和浮点数）

    参数:
        data: 任意数据结构

    返回:
        包含所有数值的列表
    """
    numbers = []

    # 处理列表、元组、集合
    if isinstance(data, (list, tuple, set)):
        for item in data:
            numbers.extend(extract_numbers(item))

    # 处理字典
    elif isinstance(data, dict):
        for value in data.values():
            numbers.extend(extract_numbers(value))

    # 处理数值型数据
    elif isinstance(data, (int, float)):
        numbers.append(data)

    return numbers

def statistics(*methods: str):
    """
    统计装饰器函数，用于统计数值型数据

    参数:
        methods: 要应用的统计方法列表，支持 'SUM', 'AVG', 'MAX', 'MIN', 'VAR', 'RMSE'

    返回:
        装饰器函数
    """
    valid_methods = {'SUM', 'AVG', 'MAX', 'MIN', 'VAR', 'RMSE'}
    invalid = set(methods) - valid_methods
    if invalid:
        raise ValueError(f"不支持的统计方法: {invalid}")

    def decorator(func):
        def wrapper(*args, **kwargs):
            # 1. 生成随机样本
            count = 0
            result = []
            for item in func(*args, **kwargs):
                print(item)
                result.append(item)
                count += 1

            print(f"\nGenerated {count} samples.\n")

            if not result:
                return None

            # 2. 提取出数值型数据
            numeric_values = []
            for item in result:
                numeric_values.extend(extract_numbers(item))

            if not numeric_values:
                print("警告: 没有找到可统计的数值数据")
                return None

            # 3. 计算统计数据
            stats_results = []

            # 数值统计基础
            total = sum(numeric_values)
            length = len(numeric_values)
            mean = total / length if length > 0 else 0
            variance = sum((x - mean) ** 2 for x in numeric_values) / length if length > 0 else 0

            # 应用请求的统计方法
            for method in methods:
                if method == 'SUM':
                    stats_results.append(('SUM', total))
                elif method == 'AVG':
                    stats_results.append(('AVG', mean))
                elif method == 'MAX':
                    stats_results.append(('MAX', max(numeric_values)))
                elif method == 'MIN':
                    stats_results.append(('MIN', min(numeric_values)))
                elif method == 'VAR':
                    stats_results.append(('VAR', variance))
                elif method == 'RMSE':
                    stats_results.append(('RMSE', math.sqrt(variance)))

            return stats_results
        return wrapper
    return decorator



@statistics('SUM', 'AVG', 'MAX', 'MIN', 'VAR', 'RMSE')
def random_sampler(**kwargs) -> Generator[Any, None, None]:
    """
    随机数生成器，带统计功能

    参数:
        ​**kwargs: 生成配置，包含 'number' 和样本结构描述

    返回:
        生成器，每次迭代产生一个随机样本
    """
    number = kwargs.pop('number', 1)
    sample_config = kwargs

    for _ in range(number):
        yield generate_sample(sample_config)


##  示例


def basic_example():
    """基本使用示例"""
    print("=" * 50)
    print("基本使用示例")
    print("=" * 50)

    config = {
        'number': 10,  # 生成10个样本
        'type': 'dict',
        'fields': {
            'id': {
                'type': 'int',
                'datarange': [1000, 9999]
            },
            'score': {
                'type': 'float',
                'datarange': [60.0, 100.0]
            },
            'attempts': {
                'type': 'int',
                'datarange': [1, 5]
            },
            'info': {
                'type': 'tuple',
                'elements': [
                    {
                        'type': 'int',
                        'datarange': [18, 40]
                    },
                    {
                        'type': 'float',
                        'datarange': [160.0, 190.0]
                    }
                ]
            }
        }
    }

    print("生成样本并计算统计量:")
    stats = random_sampler(**config)

    print("\n统计结果:")
    for method, value in stats:
        if isinstance(value, float):
            print(f"{method}: {value:.4f}")
        else:
            print(f"{method}: {value}")

def complex_example():
    """复杂结构示例"""
    print("\n" + "=" * 50)
    print("复杂结构示例")
    print("=" * 50)

    config = {
        'number': 5,
        'type': 'tuple',
        'elements': [
            {
                'type': 'str',
                'datarange': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                'len': 6
            },
            {
                'type': 'list',
                'elements': [
                    {
                        'type': 'int',
                        'datarange': [10, 100]
                    },
                    {
                        'type': 'float',
                        'datarange': [0.1, 1.0]
                    }
                ]
            },
            {
                'type': 'dict',
                'fields': {
                    'value': {
                        'type': 'int',
                        'datarange': [100, 200]
                    },
                    'nested': {
                        'type': 'list',
                        'elements': [
                            {
                                'type': 'float',
                                'datarange': [5.0, 10.0]
                            }
                        ]
                    }
                }
            }
        ]
    }

    print("生成复杂结构样本并计算统计量:")
    stats = random_sampler(**config)

    print("\n统计结果:")
    for method, value in stats:
        if isinstance(value, float):
            print(f"{method}: {value:.4f}")
        else:
            print(f"{method}: {value}")

def custom_statistics_example():
    """自定义统计方法示例"""
    print("\n" + "=" * 50)
    print("自定义统计方法示例")
    print("=" * 50)

    # 自定义统计装饰器
    @statistics('AVG', 'MAX', 'MIN')
    def custom_sampler(**kwargs):
        number = kwargs.pop('number', 1)
        sample_config = kwargs
        for _ in range(number):
            yield generate_sample(sample_config)

    config = {
        'number': 8,
        'type': 'list',
        'elements': [
            {
                'type': 'int',
                'datarange': [1, 100]
            },
            {
                'type': 'float',
                'datarange': [0.0, 1.0]
            }
        ]
    }

    print("生成样本并计算平均值、最大值、最小值:")
    stats = custom_sampler(**config)

    print("\n统计结果:")
    for method, value in stats:
        if isinstance(value, float):
            print(f"{method}: {value:.4f}")
        else:
            print(f"{method}: {value}")

if __name__ == '__main__':
    basic_example()
    complex_example()
    custom_statistics_example()
