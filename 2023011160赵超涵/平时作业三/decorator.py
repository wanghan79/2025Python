import random
import string
from functools import wraps


def StaticRes(*stats):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 1. 调用原始函数获取数据
            samples = list(func(*args, **kwargs))

            # 2. 提取所有数值型数据(整型和浮点型)
            numbers = []
            for sample in samples:
                for item in sample:
                    if isinstance(item, (int, float)):
                        numbers.append(item)
                    elif isinstance(item, (list, tuple)):
                        numbers.extend([x for x in item if isinstance(x, (int, float))])

            # 3. 计算请求的统计指标
            result = {}
            if not numbers:  # 如果没有数值数据
                return {"error": "No numeric data found"}

            for stat in stats:
                stat = stat.upper()
                if stat == 'SUM':
                    result['SUM'] = sum(numbers)
                elif stat == 'AVG':
                    result['AVG'] = sum(numbers) / len(numbers)
                elif stat == 'MAX':
                    result['MAX'] = max(numbers)
                elif stat == 'MIN':
                    result['MIN'] = min(numbers)

            return result

        return wrapper

    return decorator


def dataSampling(**kwargs):
    num = kwargs.pop('num', 1)

    for _ in range(num):
        res = []
        for key, value in kwargs.items():
            if key == "int":
                res.append(random.randint(value['datarange'][0], value['datarange'][1]))
            elif key == "float":
                res.append(random.uniform(value['datarange'][0], value['datarange'][1]))
            elif key == "str":
                datarange, length = value['datarange'], value['len']
                res.append(''.join(random.choices(datarange, k=length)))
            else:
                res.append(list(next(dataSampling(**value))))
        yield res
@StaticRes('SUM', 'AVG', 'MAX', 'MIN')
def dataSamplingDecorated(**kwargs):
    return dataSampling(**kwargs)

def main():
    struct = {
        'num': 3,
        "list": {
            "int": {"datarange": (0, 100)},
            "float": {"datarange": (0, 10.0)},
            "str": {"datarange": string.ascii_lowercase, "len": 5},
            "dict": {
                "pair1": {
                    "key": {
                        "tuple": {
                            "int": {"datarange": (1, 10)},
                            "str": {"datarange": string.ascii_letters, "len": 2}
                        }
                    },
                    "value": {
                        "str": {"datarange": string.ascii_uppercase, "len": 4}
                    }
                },
                "pair2": {
                    "key": {
                        "int": {"datarange": (0, 5)}
                    },
                    "value": {
                        "float": {"datarange": (0, 1.0)}
                    }
                }
            },
            "list": {
                "tuple": {
                    "float": {"datarange": (0, 1.0)},
                    "dict": {
                        "pair1": {
                            "key": {
                                "str": {"datarange": "abc", "len": 1}
                            },
                            "value": {
                                "int": {"datarange": (100, 200)}
                            }
                        }
                    }
                }
            }
        }
    }

    stats = dataSamplingDecorated(**struct)
    print("统计结果:")
    print(stats)

    print("\n数据样本:")
    samples = dataSampling(**struct)
    for i, sample in enumerate(samples):
        print(f"Sample {i + 1}:", sample)


if __name__ == "__main__":
    main()