"""
本程序实现使用生成器生成随机样本

作者：李超平
用途：Python 程序设计课平时作业二
"""
import string
import random

def sampling(**kwargs):
    """
    使用生成器生成随机样本

    参数:
        kwargs: 描述数据结构的嵌套字典

    返回:
        每次 yield 一个生成的数据项
    """
    for _type, _info in kwargs.items():
        count = _info.get('num', 1)

        for _ in range(count):
            if _type == 'int':
                it = iter(_info['datarange'])
                yield random.randint(next(it), next(it))

            elif _type == 'float':
                it = iter(_info['datarange'])
                yield random.uniform(next(it), next(it))

            elif _type == 'str':
                yield ''.join(random.SystemRandom().choice(_info['datarange']) for _ in range(_info['len']))

            elif _type == 'list':
                elem = []
                for k, v in _info.items():
                    if k != 'num':
                        inner = list(sampling(**{k: v}))
                        elem.extend(inner)
                yield elem

            elif _type == 'tuple':
                elem = []
                for k, v in _info.items():
                    if k != 'num':
                        inner = list(sampling(**{k: v}))
                        elem.extend(inner)
                yield tuple(elem)


if __name__ == '__main__':
    # EXAMPLE 1：生成两个元组，每个包含3个int和2个5位大写字母字符串
    gen = sampling(tuple={
        'num': 2,
        'int': {
            'num': 3,
            'datarange': (1, 10)
        },
        'str': {
            'num': 2,
            'len': 5,
            "datarange": string.ascii_uppercase
        }
    })

    for item in gen:
        print(item)

""" 
EXAMPLE 1
    sampling(tuple={
        'num': 2,
        'int': {
            'num': 3,
            'datarange': (1, 10)
        },
        'str': {
            'num': 2,
            'len': 5,
            "datarange": string.ascii_uppercase
        }
    })

EXAMPLE 2
    sampling(list={
        'num': 2,  # 生成两个列表
        'int': {
            'num': 2,
            'datarange': (100, 200)
        },
        'float': {
            'num': 1,
            'datarange': (1.5, 9.5)
        },
        'str': {
            'num': 1,
            'len': 4,
            'datarange': string.ascii_lowercase
        },
        'tuple': {
            'num': 1,
            'int': {
                'num': 2,
                'datarange': (0, 5)
            },
            'str': {
                'num': 1,
                'len': 3,
                'datarange': string.digits
            }
        }
    })
"""
