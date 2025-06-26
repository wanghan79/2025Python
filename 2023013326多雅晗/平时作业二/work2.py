"""
数据生成器实现

功能：
1. 提供了数据生成器的核心实现，支持生成多种数据类型（int、float、str、list、tuple、dict）的随机数据。
2. 提供了灵活的接口，允许用户通过嵌套字典定义复杂的数据结构。
3. 支持生成具有特定范围和长度的随机数据，适用于测试和数据模拟场景。

作者：多雅晗
"""
import random
import string
from typing import Any, Dict, Generator, Iterable, Union


def data_generator(**kwargs: Dict[str, Any]) -> Generator[Union[int, float, str, list, tuple, dict], None, None]:
    """
    生成随机数据的生成器函数

    参数:
        kwargs: 描述数据结构的嵌套字典

    返回:
        生成器，每次yield一个生成的数据项
    """
    for data_type, type_info in kwargs.items():
        count = type_info.get('num', 1)

        for _ in range(count):
            if data_type == 'int':
                it = iter(type_info['datarange'])
                yield random.randint(next(it), next(it))

            elif data_type == 'float':
                it = iter(type_info['datarange'])
                yield random.uniform(next(it), next(it))

            elif data_type == 'str':
                datarange = type_info.get('datarange', string.ascii_letters)
                length = type_info.get('len', 10)
                yield ''.join(random.SystemRandom().choice(datarange) for _ in range(length))

            elif data_type == 'list':
                elements = []
                for elem_type, elem_info in type_info.items():
                    if elem_type != 'num':
                        inner = list(data_generator(**{elem_type: elem_info}))
                        elements.extend(inner)
                yield elements

            elif data_type == 'tuple':
                elements = []
                for elem_type, elem_info in type_info.items():
                    if elem_type != 'num':
                        inner = list(data_generator(**{elem_type: elem_info}))
                        elements.extend(inner)
                yield tuple(elements)

            elif data_type == 'dict':
                elements = {}
                for elem_type, elem_info in type_info.items():
                    if elem_type != 'num':
                        if elem_type == 'str':
                            datarange = elem_info.get('datarange', string.ascii_letters)
                            length = elem_info.get('len', 10)
                            key = ''.join(random.SystemRandom().choice(datarange) for _ in range(length))
                        else:
                            key = elem_type
                        value = next(data_generator(**{elem_type: elem_info}))
                        elements[key] = value
                yield elements


def main():
    # 示例1：生成两个元组，每个包含3个int和2个5位大写字母字符串
    print("示例1:")
    gen1 = data_generator(tuple={
        'num': 2,
        'int': {
            'num': 3,
            'datarange': (1, 10)
        },
        'str': {
            'num': 2,
            'len': 5,
            "datarange": string.ascii_uppercase
        }
    })

    for item in gen1:
        print(item)

    # 示例2：生成复杂嵌套结构
    print("\n示例2:")
    gen2 = data_generator(list={
        'num': 2,
        'int': {
            'num': 2,
            'datarange': (100, 200)
        },
        'float': {
            'num': 1,
            'datarange': (1.5, 9.5)
        },
        'str': {
            'num': 1,
            'len': 4,
            'datarange': string.ascii_lowercase
        },
        'tuple': {
            'num': 1,
            'int': {
                'num': 2,
                'datarange': (0, 5)
            },
            'str': {
                'num': 1,
                'len': 3,
                'datarange': string.digits
            }
        }
    })

    for item in gen2:
        print(item)

    # 示例3：生成包含字典的复杂结构
    print("\n示例3:")
    gen3 = data_generator(dict={
        'num': 3,
        'str': {
            'datarange': string.ascii_letters,
            'len': 5
        },
        'int': {
            'datarange': (0, 100)
        },
        'list': {
            'num': 2,
            'float': {
                'datarange': (0.0, 1.0)
            }
        }
    })

    for item in gen3:
        print(item)


if __name__ == "__main__":
    main()