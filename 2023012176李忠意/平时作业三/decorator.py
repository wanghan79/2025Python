import random
import string
from functools import wraps

# 装饰器：对生成器结果进行 SUM、AVG、MAX、MIN 的统计
def StaticRes(*stats_args):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            def flatten(data):
                numeric_values = []
                if isinstance(data, (int, float)):
                    numeric_values.append(data)
                elif isinstance(data, list):
                    for item in data:
                        numeric_values.extend(flatten(item))
                return numeric_values

            data_generator = func(*args, **kwargs)
            all_numeric_values = []
            for data in data_generator:
                all_numeric_values.extend(flatten(data))

            result = {}
            if 'SUM' in stats_args:
                result['SUM'] = sum(all_numeric_values)
            if 'AVG' in stats_args and all_numeric_values:
                result['AVG'] = sum(all_numeric_values) / len(all_numeric_values)
            if 'MAX' in stats_args:
                result['MAX'] = max(all_numeric_values)
            if 'MIN' in stats_args:
                result['MIN'] = min(all_numeric_values)
            return result

        return wrapper
    return decorator

def dataSampling(**kwargs):
    num = kwargs.get('num', 1)
    for _ in range(num):
        res = []
        for key, value in kwargs.items():
            if key == 'num':
                continue
            elif key == 'int':
                res.append(random.randint(value['datarange'][0], value['datarange'][1]))
            elif key == 'float':
                res.append(random.uniform(value['datarange'][0], value['datarange'][1]))
            elif key == 'str':
                s = value['datarange']
                length = value['len']
                res.append(''.join(random.choices(s, k=length)))
            else:
                res.append(list(next(dataSampling(**value))))
        yield res

@StaticRes('SUM', 'AVG', 'MAX', 'MIN')
def dataSamplingDecorated(**kwargs):
    return dataSampling(**kwargs)

def output():
    struct = {
        'num': 2,
        'list': {
            'int': {"datarange": (0, 100)},
            'float': {"datarange": (0, 10.0)},
            'str': {"datarange": string.ascii_lowercase, "len": 5}
        },
        'tuple': {
            'tuple': {
                'int': {"datarange": (1, 10)},
                'list': {
                    'str': {"datarange": string.digits, "len": 3}
                }
            }
        },
        'dict': {
            'list': {
                'float': {"datarange": (0, 1.0)},
                'dict': {
                    'str': {"datarange": string.ascii_uppercase, "len": 4}
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
        print(f"Sample {i+1}:", sample)

if __name__ == '__main__':
    output()
