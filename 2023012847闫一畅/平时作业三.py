import random
import string


def StaticRes(*stats):
    def decorator(func):
        def wrapper(*args, **kwargs):
            numbers = func(*args, **kwargs)
            result = {}

            if 1 in stats:
                result['max'] = max(numbers)
            if 2 in stats:
                result['min'] = min(numbers)
            if 3 in stats:
                result['sum'] = sum(numbers)
            if 4 in stats:
                result['avg'] = sum(numbers) / len(numbers)

            return result

        return wrapper

    return decorator


def DataSampling(**kwargs):
    num = kwargs.get('num', 1)
    results = []

    for _ in range(num):
        sample = []
        for data_type, config in kwargs.items():
            if data_type == 'num':
                continue

            if data_type == "int":
                start, end = config['datarange']
                sample.append(random.randint(start, end))

            elif data_type == "float":
                start, end = config['datarange']
                sample.append(random.uniform(start, end))

            elif data_type == "str":
                chars = config['datarange']
                length = config['len']
                sample.append(''.join(random.choices(chars, k=length)))

            elif data_type == "dict":
                key = ''.join(random.choices(string.ascii_letters, k=3))
                value = random.randint(0, 100)
                sample.append({key: value})

            elif data_type in ("list", "tuple"):
                nested_data = DataSampling(**config)
                sample.append(nested_data if data_type == "list" else tuple(nested_data))

        results.append(sample if len(sample) > 1 else sample[0])

    return results[0] if num == 1 else results


# 示例数据结构
sample_struct = {
    'num': 5,
    "int": {"datarange": (0, 100)},
    "float": {"datarange": (0, 100.0)},
    "str": {
        "datarange": string.ascii_uppercase,
        "len": 5
    },
    "dict": {},
    "list": {
        "int": {"datarange": (0, 10)},
        "float": {"datarange": (0, 1.0)}
    }
}
count = {2, 4}  # 统计操作组合：MIN 和 AVG


@StaticRes(*count)
def sampling(**kwargs):
    data = DataSampling(**kwargs)

    # 只提取数值
    def flatten(items):
        for item in items:
            if isinstance(item, (list, tuple)):
                yield from flatten(item)
            elif isinstance(item, dict):
                yield from flatten(item.values())
            else:
                yield item

    return [x for x in flatten([data]) if isinstance(x, (int, float))]


if __name__ == '__main__':
    data = DataSampling(**sample_struct)
    print("生成的数据：", data)
    print("统计结果：", sampling(**sample_struct))