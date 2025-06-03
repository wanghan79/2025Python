"""
@Author: Li Xiang
@Version: 1.0
@Description: 使用生成器生成随机样本，配套生成器使用范例代码，随机样本的数量和结构由调用者输入。
"""

import random
import string


def gen_str(data):
    """
    从指定字符串中随机生成指定长度的字符串。
    """
    return ''.join(random.choices(data['datarange'], k=data.get('len', 8)))


def gen_int(data):
    """
    生成指定范围内的随机整数。
    """
    return random.randint(data['datarange'][0], data['datarange'][1])


def gen_float(data):
    """
    生成指定范围内的随机浮点数。
    """
    return random.uniform(data['datarange'][0], data['datarange'][1])


def gen_list(data):
    """
    生成列表，支持多个字段。
    每个字段会递归调用 generate_sample。
    """
    result = []
    for key, value in data.items():
        result.append(generate_sample({key: value}))
    return result


def gen_dict(data):
    """
    生成字典，键值对递归生成。
    """
    return {k: generate_sample({k: v}) for k, v in data.items()}


def gen_tuple(data):
    """
    生成元组，内容递归生成。
    """
    return tuple(generate_sample({k: v}) for k, v in data.items())


# 类型到生成函数的映射表
TYPE_TO_FUNC = {
    'str': gen_str,
    'int': gen_int,
    'float': gen_float,
    'list': gen_list,
    'dict': gen_dict,
    'tuple': gen_tuple,
}


def generate_sample(struct):
    """
    根据配置生成单个样本。
    struct 应该是一个只有一个键值对的 dict，表示数据类型和参数。
    """
    if len(struct) != 1:
        raise ValueError(f"结构配置必须且仅能包含一个类型键：{struct}")

    type_name, data = next(iter(struct.items()))

    if type_name not in TYPE_TO_FUNC:
        raise ValueError(f"不支持的类型：'{type_name}'")

    return TYPE_TO_FUNC[type_name](data)


def random_sampler(number=1, **kwargs):
    """
    随机样本生成器。
    number: 要生成的样本数量。
    kwargs: 样本结构定义。
    """
    for _ in range(number):
        yield generate_sample(kwargs)


if __name__ == '__main__':
    example = {
        'number': 10,  # 设置样本数量
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
            },
            'float': {
                'datarange': [1, 10]
            }
        }
    }

    count = 0
    for item in random_sampler(**example):
        print(item)
        count += 1
    print(f"\nGenerated and printed {count} samples.")
