"""
此为 Python 程序设计课平时作业二：随机数据生成

作者：梁博芳
用途：Python 程序设计课平时作业二
"""

import random
import string

def sampling(**kwargs):
    """
    使用生成器生成随机样本

    参数:
        kwargs: 描述数据结构的嵌套字典，例如：
            {
                'tuple': {
                    'num': 2,
                    'int': {'num': 3, 'datarange': (1, 10)},
                    'str': {'num': 2, 'len': 5, 'datarange': string.ascii_uppercase}
                }
            }

    返回:
        每次 yield 一个生成的数据项
    """
    for data_type, config in kwargs.items():
        total_num = config.get('num', 1)  # 总生成次数

        for _ in range(total_num):
            if data_type == 'int':
                data_range = config['datarange']
                yield random.randint(*data_range)

            elif data_type == 'float':
                data_range = config['datarange']
                yield random.uniform(*data_range)

            elif data_type == 'str':
                length = config['len']
                char_set = config['datarange']
                yield ''.join(random.SystemRandom().choice(char_set) for _ in range(length))

            elif data_type in ['list', 'tuple']:
                elements = []
                for sub_type, sub_config in config.items():
                    if sub_type != 'num':
                        sub_elements = list(sampling(**{sub_type: sub_config}))
                        elements.extend(sub_elements)

                if data_type == 'list':
                    yield elements
                else:
                    yield tuple(elements)

if __name__ == '__main__':
    # 示例 1：生成两个元组，每个包含 3 个 int 和 2 个 5 位大写字母字符串
    gen = sampling(tuple={
        'num': 2,
        'int': {
            'num': 3,
            'datarange': (1, 10)
        },
        'str': {
            'num': 2,
            'len': 5,
            'datarange': string.ascii_uppercase
        }
    })
    for item in gen:
        print(item)
