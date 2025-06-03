import string
import random


def StaticRes(*stats_methods):
    def decorator(func):
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)

            def extract_numbers(item):
                numbers = []
                if isinstance(item, (int, float)):
                    numbers.append(item)
                elif isinstance(item, (list, tuple)):
                    for sub_item in item:
                        numbers.extend(extract_numbers(sub_item))
                elif isinstance(item, dict):
                    for sub_item in item.values():
                        numbers.extend(extract_numbers(sub_item))
                return numbers

            numbers = extract_numbers(data)
            stats = {}
            if not numbers:
                for method in stats_methods:
                    stats[method] = None
                return stats

            sum_val = sum(numbers)
            avg_val = sum_val / len(numbers)
            max_val = max(numbers)
            min_val = min(numbers)

            for method in stats_methods:
                if method == 'SUM':
                    stats['SUM'] = sum_val
                elif method == 'AVE':
                    stats['AVE'] = avg_val
                elif method == 'MAX':
                    stats['MAX'] = max_val
                elif method == 'MIN':
                    stats['MIN'] = min_val

            return stats

        return wrapper

    return decorator


@StaticRes('SUM', 'AVE', 'MAX', 'MIN')  # 修改装饰器参数
def DataSampling(**kwargs):
    element = []
    for key, value in kwargs.items():
        if key == "int":
            element.append(random.randint(*value['datarange']))
        elif key == "float":
            element.append(random.uniform(*value['datarange']))
        elif key == "str":
            chars = value['datarange']
            length = value.get('len', 5)
            element.append(''.join(random.choices(chars, k=length)))
        elif key == "list":
            sub_element = DataSampling(**value)
            element.append(sub_element)
        elif key == "dict":
            sub_element = DataSampling(**value)
            element.append(dict(enumerate(sub_element)))
        elif key == "tuple":
            sub_element = DataSampling(**value)
            element.append(tuple(sub_element))
        else:
            print(f"警告：不支持的键 '{key}'")
    return element

    # 数据生成结构定义



struct = {
    "int": {"datarange": (0, 100)},
    "float": {"datarange": (0, 10000)},
    "str": {"datarange": string.ascii_uppercase, "len": 50},
    "list": {
        "int": {"datarange": (100, 200)},
        "float": {"datarange": (1000, 2000)},
        "str": {"datarange": string.ascii_lowercase, "len": 10}
    },
    "dict": {
        "int": {"datarange": (500, 600)},
        "float": {"datarange": (5000, 6000)},
        "str": {"datarange": string.digits, "len": 8}
    },
    "tuple": {
        "int": {"datarange": (700, 800)},
        "float": {"datarange": (7000, 8000)},
        "str": {"datarange": string.punctuation, "len": 5}
    }
}

# 测试输出
result = DataSampling(**struct)
print("统计结果:", result)