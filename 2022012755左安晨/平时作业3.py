
"""
  Author:  Zuoanchen
  Created: 10/6/2025
"""


import random
import string
from functools import wraps


def StaticRes(*stat_funcs):
    def decorator(func):
        # 保存未装饰的函数
        original_func = func
        def wrapper(*args, **kwargs):
            # 在递归调用时使用原始函数
            def recursive_call(**kwargs):
                return original_func(**kwargs)

            # 1. 生成数据
            data_generator = func(*args, **kwargs)
            data = list(data_generator)

            # 2. 收集所有叶子节点的数值
            leaf_values = []

            def collect_values(item):
                if isinstance(item, (int, float)):
                    leaf_values.append(item)
                elif isinstance(item, (list, tuple)):
                    for subitem in item:
                        collect_values(subitem)
                elif isinstance(item, dict):
                    for value in item.values():
                        collect_values(value)

            for item in data:
                collect_values(item)

            # 3. 计算结果
            stats = {}
            if "Max" in stat_funcs:
                stats["Max"] = max(leaf_values) if leaf_values else None
            if "Min" in stat_funcs:
                stats["Min"] = min(leaf_values) if leaf_values else None
            if "AVG" in stat_funcs:
                stats["AVG"] = sum(leaf_values) / len(leaf_values) if leaf_values else None
            if "SUM" in stat_funcs:
                stats["SUM"] = sum(leaf_values) if leaf_values else None

            return {"data": data, "stats": stats}

        # 将递归调用方法附加到包装函数上
        wrapper.recursive_call = original_func
        return wrapper

    return decorator


@StaticRes("Max", "Min", "AVG", "SUM")
def dataSampling(**kwargs):
    type_, nested_data = list(kwargs.items())[0]

    if type_ == "tuple":
        yield tuple(next(dataSampling.recursive_call(**item)) for item in nested_data)
    elif type_ == "list":
        yield [next(dataSampling.recursive_call(**item)) for item in nested_data]
    elif type_ == "dict":
        yield {key: next(dataSampling.recursive_call(**value)) for key, value in nested_data.items()}
    elif type_ == "int":
        yield random.randint(nested_data["datarange"][0], nested_data["datarange"][1])
    elif type_ == "float":
        yield random.uniform(nested_data["datarange"][0], nested_data["datarange"][1])
    elif type_ == "str":
        yield ''.join(random.SystemRandom().choice(nested_data["datarange"]) for _ in range(nested_data["len"]))


# 示例用法
if __name__ == "__main__":
    data = {
        "dict": {
            "tuple": {
                "tuple": [
                    {"str": {"datarange": string.ascii_uppercase, "len": 5}},
                    {"int": {"datarange": (0, 10)}},
                    {
                        "tuple": [
                            {"int": {"datarange": (0, 10)}},
                            {"float": {"datarange": (0, 1.0)}},
                            {"str": {"datarange": string.ascii_uppercase, "len": 5}}
                        ]
                    }
                ]
            },
            "list": {
                "list": [
                    {"int": {"datarange": (0, 10)}},
                    {"float": {"datarange": (0, 1.0)}},
                    {"str": {"datarange": string.ascii_uppercase, "len": 5}}
                ]
            },
            "dict": {
                "dict": {
                    "list": {
                        "list": [
                            {"int": {"datarange": (0, 10)}},
                            {"str": {"datarange": string.ascii_uppercase, "len": 5}},
                            {
                                "tuple": [
                                    {"float": {"datarange": (0, 1.0)}},
                                    {"int": {"datarange": (0, 10)}}
                                ]
                            }
                        ]
                    }
                }
            }
        }
    }
    result = dataSampling(**data)
    print("生成的数据:")
    print(result['data'])
    print("\n统计结果:")
    print(result['stats'])
