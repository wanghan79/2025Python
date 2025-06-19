"""
此为 Python 程序设计课平时作业三：装饰器修饰随机数据

作者：梁博芳
用途：Python 程序设计课平时作业三
"""

import random

# 支持的数据类型
NUMBER_TYPES = {'int', 'float'}
CONTAINER_TYPES = {'tuple'}

# 装饰器：用于统计数值型数据的多个指标
def static_res(*stats):
    """
    装饰器用于统计数值型数据的多个指标，如 sum, max, min.

    参数:
        *stats: 传入要统计的函数集合（如 sum, max, min 等）。

    返回:
        包含每个统计函数结果的字典。
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            numeric_data = []
            for sample in func(*args, **kwargs):
                if isinstance(sample, (int, float)):
                    numeric_data.append(sample)
            res = {stat.__name__: stat(numeric_data) if numeric_data else None for stat in stats}
            return res
        return wrapper
    return decorator

# 数据生成函数：根据数据类型分发给不同的生成逻辑
def generate_data(dtype, params):
    """
    根据数据类型生成相应的随机数据。

    参数:
        dtype: 数据类型（如 int, float, tuple）。
        params: 数据生成参数。

    返回:
        生成的随机数据列表。
    """
    if dtype == 'int':
        return [random.randint(*params['datarange']) for _ in range(params['num'])]
    elif dtype == 'float':
        return [random.uniform(*params['datarange']) for _ in range(params['num'])]
    elif dtype == 'tuple':
        elements = []
        for elem_dtype, elem_params in params.items():
            if elem_dtype in NUMBER_TYPES:
                elements.extend(generate_data(elem_dtype, elem_params))
            elif elem_dtype in CONTAINER_TYPES:
                elements.extend(generate_data(elem_dtype, elem_params))
        return elements
    return []

# 样本生成函数：支持通过 StaticRes 统计数值型样本的各种统计量
@static_res(sum, max, min)
def sampling(**kwargs):
    """
    样本生成函数，支持统计数值型样本的各种统计量。

    参数:
        **kwargs: 数据生成配置。

    返回:
        统计结果字典。
    """
    for dtype, params in kwargs.items():
        return generate_data(dtype, params)

if __name__ == '__main__':
    # 示例：生成一个嵌套元组，并统计其中的数值型数据
    res = sampling(tuple={
        'num': 1,
        'tuple': {
            'num': 3,
            'int': {
                'num': 2,
                'datarange': (1, 100)
            }
        }
    })
    print(f"统计结果：{res}")
