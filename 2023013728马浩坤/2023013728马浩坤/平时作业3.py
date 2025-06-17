import random


def gen_str(data):
    return ''.join(random.choices(data['datarange'], k=data['len']))


def gen_int(data):
    return random.randint(data['datarange'][0], data['datarange'][1])


def gen_float(data):
    return random.uniform(data['datarange'][0], data['datarange'][1])


def gen_list(data):
    return [generate_sample({k: v}) for k, v in data.items()]


def gen_dict(data):
    return {k: generate_sample({k: v}) for k, v in data.items()}


def gen_tuple(data):
    return tuple(generate_sample({k: v}) for k, v in data.items())


TYPE_TO_FUNC = {
    'str': gen_str,
    'int': gen_int,
    'float': gen_float,
    'list': gen_list,
    'dict': gen_dict,
    'tuple': gen_tuple,
}


def extract_int(data):
    int_values = []

    if isinstance(data, (list, tuple, set)):
        for item in data:
            int_values.extend(extract_int(item))

    elif isinstance(data, dict):
        for key, value in data.items():
            int_values.extend(extract_int(value))

    elif isinstance(data, int) or isinstance(data, float):
        int_values.append(data)
    return int_values


def StaticsResInt(**vargs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            method_list = vargs.get('name', [])

            count = 0
            result = []
            for item in func(*args, **kwargs):
                print(item)
                result.append(item)
                count += 1
            print(f"\nGenerated and printed {count} samples.\n")

            if not result:
                return None

            int_values = []
            for item in result:
                int_values.extend(extract_int(item))

            if not int_values:
                return None

            statics = []
            for stats_method in method_list:
                if stats_method == 'SUM':
                    statics.append(('SUM', sum(int_values)))
                elif stats_method == 'AVG':
                    statics.append(('AVG', sum(int_values) / len(int_values)))
                elif stats_method == 'VAR':
                    statics.append(('VAR', sum((x - sum(int_values) / len(int_values)) ** 2
                                               for x in int_values) / len(int_values)))
                elif stats_method == 'RMSE':
                    statics.append(('RMSE', (sum((x - sum(int_values) / len(int_values)) ** 2
                                                 for x in int_values) / len(int_values)) ** 0.5))
                else:
                    raise ValueError("Unsupported statistics method")  # 不支持的统计方法
            return statics

        return wrapper

    return decorator


def generate_sample(struct):
    if len(struct) != 1:
        raise ValueError(f"结构配置必须包含且仅包含一个类型键：{struct}")
    type_name, data = next(iter(struct.items()))
    if type_name not in TYPE_TO_FUNC:
        raise ValueError(f"不支持的类型：'{type_name}'")
    return TYPE_TO_FUNC[type_name](data)


@StaticsResInt(name=['SUM', 'AVG', 'VAR', 'RMSE'])  # 装饰器
def random_sampler(**kwargs):
    number = kwargs.pop('number', 1)
    for _ in range(number):
        yield generate_sample(kwargs)


if __name__ == '__main__':
    example = {
        'number': 10,
        'tuple': {
            'str': {
                'datarange': 'abcdefghijklmnopqrstuvwxyz',
                'len': 8
            },
            'list': {
                'int': {
                    'datarange': [1, 10]
                },
                'float': {
                    'datarange': [1, 10]
                }
            },
            'dict': {
                'int': {
                    'datarange': [1, 10]
                }
            }
        }
    }

    result = random_sampler(**example)
    for static_method, data in result:
        print(f"The {static_method} of the integer: {data}")
