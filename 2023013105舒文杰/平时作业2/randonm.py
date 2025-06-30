
import random

# 映射类型到生成函数
GENERATOR_MAP = {}

def string_gen(config):
    chars = config.get('chars', 'abcdefghijklmnopqrstuvwxyz')
    length = config.get('length', 6)
    return ''.join(random.choices(chars, k=length))

def int_gen(config):
    low, high = config.get('range', [0, 100])
    return random.randint(low, high)

def float_gen(config):
    low, high = config.get('range', [0.0, 1.0])
    return random.uniform(low, high)

def list_gen(config):
    return [generate_value({k: v}) for k, v in config.items()]

def dict_gen(config):
    return {key: generate_value({k: v}) for key, (k, v) in enumerate(config.items())}

def tuple_gen(config):
    return tuple(generate_value({k: v}) for k, v in config.items())

# 注册生成函数
GENERATOR_MAP['str'] = string_gen
GENERATOR_MAP['int'] = int_gen
GENERATOR_MAP['float'] = float_gen
GENERATOR_MAP['list'] = list_gen
GENERATOR_MAP['dict'] = dict_gen
GENERATOR_MAP['tuple'] = tuple_gen

def generate_value(spec):
    """
    根据单个结构说明生成随机数据
    """
    if len(spec) != 1:
        raise Exception("结构定义应只包含一个类型键")
    data_type, config = next(iter(spec.items()))
    if data_type not in GENERATOR_MAP:
        raise Exception(f"暂不支持的数据类型: {data_type}")
    return GENERATOR_MAP[data_type](config)

def data_generator(schema, amount=1):
    """
    随机样本生成器（生成器形式）
    :param schema: 数据结构定义
    :param amount: 生成的样本数量
    """
    for _ in range(amount):
        yield generate_value(schema)


if __name__ == '__main__':
    # 示例结构定义
    config = {
        'tuple': {
            'str': {
                'chars': 'abcxyz',
                'length': 5
            },
            'list': {
                'int': {
                    'range': [1, 10]
                },
                'float': {
                    'range': [1.0, 10.0]
                }
            },
            'dict': {
                'int': {
                    'range': [100, 200]
                }
            }
        }
    }

    count = 0
    for item in data_generator(config, amount=5):
        print(item)
        count += 1
    print(f"\n共生成样本：{count} 个")
