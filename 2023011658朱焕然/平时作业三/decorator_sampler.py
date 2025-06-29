import random
import string
from math import sqrt

# 装饰器：可选统计项
def StaticRes(*stats):
    def decorator(func):
        def wrapper(*args, **kwargs):
            data_generator = func(*args, **kwargs)

            # 初始化统计
            result = {
                'SUM': 0,
                'AVG': 0,
                'VAR': 0,
                'RMSE': 0,
                'count': 0
            }

            for item in data_generator:
                print("Generated:", item)
                numbers = extract_numbers(item)
                if numbers:
                    result['count'] += len(numbers)
                    result['SUM'] += sum(numbers)
                    avg = result['SUM'] / result['count']
                    squared_diffs = [(x - avg) ** 2 for x in numbers]
                    result['VAR'] += sum(squared_diffs)
                    result['RMSE'] += sum(squared_diffs)

            if result['count'] > 0:
                result['AVG'] = result['SUM'] / result['count']
                if result['count'] > 1:
                    result['VAR'] /= result['count']
                    result['RMSE'] = sqrt(result['RMSE'] / result['count'])
                else:
                    result['VAR'] = 0
                    result['RMSE'] = 0

            # 输出结果
            final_result = {}
            if 'SUM' in stats:
                final_result['SUM'] = result['SUM']
            if 'AVG' in stats:
                final_result['AVG'] = result['AVG']
            if 'VAR' in stats:
                final_result['VAR'] = result['VAR']
            if 'RMSE' in stats:
                final_result['RMSE'] = result['RMSE']

            return final_result
        return wrapper
    return decorator

# 提取结构中的数值型数据
def extract_numbers(element):
    numbers = []
    if isinstance(element, (int, float)):
        numbers.append(element)
    elif isinstance(element, (list, tuple, set)):
        for item in element:
            numbers.extend(extract_numbers(item))
    elif isinstance(element, dict):
        for _, value in element.items():
            numbers.extend(extract_numbers(value))
    return numbers

# 内部递归生成器
def generator_inner(**kwargs):
    for key, value in kwargs.items():
        if key == "list" or key == "dict":
            for k, v in value.items():
                if k in ["list", "dict"]:
                    yield list(generator_inner(**v))
                elif k == "int":
                    yield random.randint(v['datarange'][0], v['datarange'][1])
                elif k == "float":
                    yield random.uniform(v['datarange'][0], v['datarange'][1])
                elif k == "str":
                    length = v.get('len', 5)
                    yield ''.join(random.choices(list(v['datarange']), k=length))
                elif k == "tuple":
                    yield tuple(generator_inner(**v))
                else:
                    print(f"Warning: Unsupported key '{k}' encountered.")
        elif key == "int":
            yield random.randint(value['datarange'][0], value['datarange'][1])
        elif key == "float":
            yield random.uniform(value['datarange'][0], value['datarange'][1])
        elif key == "str":
            length = value.get('len', 5)
            yield ''.join(random.choices(list(value['datarange']), k=length))
        elif key == "tuple":
            yield tuple(generator_inner(**value))
        else:
            print(f"Warning: Unsupported key '{key}' encountered.")

# 外层结构生成器
@StaticRes('SUM', 'AVG', 'VAR', 'RMSE')
def structDataSampling(**kwargs):
    num = kwargs.get('num', 1)
    kwargs.pop('num', None)

    def generator():
        count = 0
        while count < num:
            element = []
            for key, value in kwargs.items():
                if key == "list":
                    element.append(list(generator_inner(**value)))
                elif key == "dict":
                    element.append(dict(generator_inner(**value)))
                elif key == "int":
                    element.append(random.randint(value['datarange'][0], value['datarange'][1]))
                elif key == "float":
                    element.append(random.uniform(value['datarange'][0], value['datarange'][1]))
                elif key == "str":
                    length = value.get('len', 5)
                    element.append(''.join(random.choices(list(value['datarange']), k=length)))
                elif key == "tuple":
                    element.append(tuple(generator_inner(**value)))
                else:
                    print(f"Warning: Unsupported key '{key}' encountered.")
            yield element
            count += 1

    return generator()

# 测试
if __name__ == "__main__":
    struct = {
        "num": 10,
        "list": {
            "str": {"datarange": string.ascii_letters, "len": 5},
            "int": {"datarange": (0, 10)}
        },
        "tuple": {
            "float": {"datarange": (0, 100)},
            "dict": {
                "int": {"datarange": (10, 50)}
            }
        }
    }
    result = structDataSampling(**struct)
    print("\nStatistics:", result)
