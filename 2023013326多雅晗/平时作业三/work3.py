"""
数据生成与统计工具

模块功能：
1. 提供了数据生成器的核心实现，支持生成多种数据类型（int、float、str、list、tuple、dict、set）的随机数据。
2. 提供了灵活的接口，允许用户通过嵌套字典定义复杂的数据结构。
3. 提供了装饰器 StaticRes，用于统计生成数据的多个指标，如总和、平均值、最大值、最小值等。
4. 支持生成具有特定范围和长度的随机数据，适用于测试和数据模拟场景。

作者：多雅晗
"""
import random
import string
from functools import reduce

NUMBER_TYPES = {'int', 'float', 'double', 'str'}
CONTAINER_TYPES = {'list', 'tuple', 'dict', 'set'}


def StaticRes(*stats):
    """
    装饰器：用于统计生成数据的多个指标

    参数:
        stats: 统计函数或统计指标名称集合

    返回:
        包含统计结果的字典
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            # 收集所有数值数据
            numeric_data = []

            # 处理生成器或普通函数返回的数据
            data = func(*args, **kwargs)

            # 如果是生成器，遍历所有元素
            if hasattr(data, '__iter__') and not isinstance(data, (list, dict)):
                for item in data:
                    if isinstance(item, (int, float)):
                        numeric_data.append(item)
                    elif isinstance(item, (list, tuple, dict)):
                        # 递归提取数值
                        def extract_numbers(obj):
                            if isinstance(obj, (int, float)):
                                return [obj]
                            elif isinstance(obj, (list, tuple)):
                                numbers = []
                                for i in obj:
                                    numbers.extend(extract_numbers(i))
                                return numbers
                            elif isinstance(obj, dict):
                                numbers = []
                                for v in obj.values():
                                    numbers.extend(extract_numbers(v))
                                return numbers
                            return []

                        numeric_data.extend(extract_numbers(item))
            else:
                # 处理普通函数返回的数据
                if isinstance(data, (int, float)):
                    numeric_data.append(data)
                elif isinstance(data, (list, tuple, dict)):
                    def extract_numbers(obj):
                        if isinstance(obj, (int, float)):
                            return [obj]
                        elif isinstance(obj, (list, tuple)):
                            numbers = []
                            for i in obj:
                                numbers.extend(extract_numbers(i))
                            return numbers
                        elif isinstance(obj, dict):
                            numbers = []
                            for v in obj.values():
                                numbers.extend(extract_numbers(v))
                            return numbers
                        return []

                    numeric_data.extend(extract_numbers(data))

            # 计算统计指标
            results = {}
            if not numeric_data:
                return results

            for stat in stats:
                if stat == 'SUM' or stat == 'sum' or stat == 3:
                    results['sum'] = sum(numeric_data)
                elif stat == 'AVG' or stat == 'avg' or stat == 4:
                    results['avg'] = sum(numeric_data) / len(numeric_data)
                elif stat == 'MAX' or stat == 'max' or stat == 1:
                    results['max'] = max(numeric_data)
                elif stat == 'MIN' or stat == 'min' or stat == 2:
                    results['min'] = min(numeric_data)
                elif callable(stat):
                    # 处理传入的函数
                    results[stat.__name__] = reduce(stat, numeric_data)

            return results

        return wrapper

    return decorator


def generate_number(**kwargs):
    """
    生成基础类型数据

    参数:
        kwargs: 数据类型及参数设置

    生成:
        对应类型的随机值
    """
    data_type, config = next(iter(kwargs.items()))

    if 'datarange' not in config:
        raise ValueError(f"Missing 'datarange' parameter for {data_type}")

    num = config.get('num', 1)

    if data_type == 'int':
        start, end = config['datarange']
        for _ in range(num):
            yield random.randint(start, end)
    elif data_type == 'float':
        start, end = config['datarange']
        for _ in range(num):
            yield random.uniform(start, end)
    elif data_type == 'str':
        chars = config['datarange']
        length = config['len']
        for _ in range(num):
            yield ''.join(random.choices(chars, k=length))


def generate_container(**kwargs):
    """
    递归生成容器类型数据

    参数:
        kwargs: 容器类型及其配置

    生成:
        容器内部的所有元素
    """
    container_type, config = next(iter(kwargs.items()))

    num = config.get('num', 1)

    for _ in range(num):
        elements = []
        for key, value in config.items():
            if key in NUMBER_TYPES:
                elements.extend(list(generate_number(**{key: value})))
            elif key in CONTAINER_TYPES:
                elements.extend(list(generate_container(**{key: value})))

        if container_type == 'list':
            yield elements
        elif container_type == 'tuple':
            yield tuple(elements)
        elif container_type == 'dict':
            yield {f'key_{i}': elem for i, elem in enumerate(elements)}
        elif container_type == 'set':
            yield set(elements)


def generate_data(**kwargs):
    """
    根据数据类型分发给不同的生成函数

    参数:
        kwargs: 单个键值对，表示需要生成的类型

    生成:
        随机数据项
    """
    if len(kwargs) != 1:
        raise ValueError("Expected exactly one key-value pair")

    data_type = next(iter(kwargs.keys()))

    if data_type in NUMBER_TYPES:
        yield from generate_number(**kwargs)
    elif data_type in CONTAINER_TYPES:
        yield from generate_container(**kwargs)


@StaticRes('sum', 'avg', 'max', 'min')
def sampling(**kwargs):
    """
    样本生成函数，支持通过StaticRes统计数值型样本的各种统计量

    参数:
        kwargs: 数据生成配置

    生成:
        随机数据项
    """
    for data_type, config in kwargs.items():
        yield from generate_data(**{data_type: config})


if __name__ == '__main__':
    # 示例1: 生成包含多种类型的元组数据并统计
    print("示例1结果:")
    result1 = sampling(tuple={
        'num': 100,
        'int': {
            'num': 2,
            'datarange': (0, 1000)
        },
        'float': {
            'num': 2,
            'datarange': (0, 1000.0)
        },
        'str': {
            'num': 3,
            'datarange': string.ascii_letters,
            'len': 5
        }
    })
    print(result1)

    # 示例2: 生成嵌套容器数据并统计
    print("\n示例2结果:")
    result2 = sampling(tuple={
        'num': 1000,
        'tuple': {
            'num': 3,
            'int': {
                'num': 2,
                'datarange': (1, 100)
            },
            'str': {
                'num': 1,
                'datarange': string.ascii_lowercase,
                'len': 6
            }
        }
    })
    print(result2)

    # 示例3: 生成字典数据并统计
    print("\n示例3结果:")
    result3 = sampling(dict={
        'num': 50,
        'int': {
            'num': 2,
            'datarange': (10, 20)
        },
        'float': {
            'num': 2,
            'datarange': (5.0, 15.0)
        }
    })
    print(result3)