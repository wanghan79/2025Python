import random
import string

def structDataSampling(num, **kwargs):
    """
    使用生成器递归生成随机数据
    :param num: 生成样本数量
    :param kwargs: 结构定义
    :yield: 每个样本
    """

    def generate_sample(config):
        if isinstance(config, dict):
            if 'datarange' in config:
                if 'len' in config and isinstance(config['datarange'], str):
                    return ''.join(random.choice(config['datarange']) for _ in range(config['len']))
                else:
                    it = iter(config['datarange'])
                    low, high = next(it), next(it)
                    if isinstance(low, int) and isinstance(high, int):
                        return random.randint(low, high)
                    else:
                        return random.uniform(low, high)
            else:
                return {key: generate_sample(value) for key, value in config.items()}
        elif isinstance(config, list):
            return [generate_sample(item) for item in config]
        elif isinstance(config, tuple):
            return tuple(generate_sample(item) for item in config)
        else:
            return config

    # yield
    for _ in range(num):
        yield generate_sample(kwargs)


def print_values(data, indent=0):
    """
    递归打印样本内容
    """
    if isinstance(data, (int, float, str)):
        print(' ' * indent + str(data))
    elif isinstance(data, dict):
        for key, value in data.items():
            print(' ' * indent + f"{key}:")
            print_values(value, indent + 2)
    elif isinstance(data, (list, tuple)):
        for i, item in enumerate(data):
            print(' ' * indent + f"[{i}]:")
            print_values(item, indent + 2)


def apply():
    struct = {
        "int": {"datarange": (0, 100)},
        "float": {"datarange": (0, 10000)},
        "str": {"datarange": string.ascii_uppercase, "len": 10},
        "tuple": (
            {"datarange": string.ascii_lowercase, "len": 5},
            {"datarange": (10, 20)}  
        ),
        "list": [
            {"datarange": (0, 10)}, 
            {"datarange": "ABCDEFG", "len": 3} 
        ],
        "dict": {
            "name": {"datarange": string.ascii_letters, "len": 8},
            "age": {"datarange": (18, 60)}
        }
    }

    print("生成样本如下：")
    for i, sample in enumerate(structDataSampling(5, **struct), 1):
        print(f"\nSample {i}:")
        print_values(sample)


apply()
