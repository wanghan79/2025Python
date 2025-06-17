"""
本程序实现一个带统计功能的通用数据生成器框架。
使用装饰器 StaticRes 可以对生成的数值型数据进行统计（如 sum、max、min）。

作者：李超平
用途：Python 程序设计课平时作业三
"""
import random
import string

NUMBER_TYPE = {'int', 'float', 'double', 'str'}
CONTAINER_TYPE = {'list', 'tuple', 'dict'}

def StaticRes(*sargs):
    """
    装饰器：用于统计 sampling 函数中生成的数值数据的多个指标，如 sum, max, min

    参数:
        sargs: 统计函数集合（如 sum, max, min）等。

    返回:
        包含每个统计函数结果的字典
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            res = dict()
            cnt = 0
            pres = [0 for _ in range(len(sargs))]
            for sample in func(*args, **kwargs):
                if isinstance(sample, int) or isinstance(sample, float):
                    for i in range(len(sargs)):
                        pres[i] = sargs[i]([pres[i], sample]) if cnt != 0 else sample
                    cnt += 1
            for static in sargs:
                res[static.__name__] = pres[sargs.index(static)]
            return res
        return wrapper
    return decorator

def generateNumber(**kwargs):
    """
    用于生成基础类型数据：int、float、str（通过 yield 返回）

    参数:
        kwargs: 数据类型及参数设置（如 datarange、num、len）

    生成:
        对应类型的随机值
    """
    _type, _info = next(iter(kwargs.items()))

    if 'datarange' not in _info:
        raise Exception('没有找到datarange参数')

    if _type == 'int':
        start, end = _info['datarange']
        for _ in range(_info['num']):
            yield random.randint(start, end)
    if _type == 'float':
        start, end = _info['datarange']
        for _ in range(_info['num']):
            yield random.uniform(start, end)
    if _type == 'str':
        for _ in range(_info['num']):
            datarange, length = _info["datarange"], _info["len"]
            elem = "".join(random.SystemRandom().choice(datarange) for __ in range(length))
            yield elem

def generateContainer(**kwargs):
    """
    递归生成容器类型内的所有元素，使用 yield

    参数:
        kwargs: 描述容器类型及其包含的元素生成方式

    生成:
        容器内部展开的所有元素
    """
    _type, _info = next(iter(kwargs.items()))

    if _type == 'tuple':
        for _ in range(_info['num']):
            for k, v in _info.items():
                if k in NUMBER_TYPE:
                    yield from generateNumber(**{k: v})
                elif k in CONTAINER_TYPE:
                    yield from generateContainer(**{k: v})

def generateAType(**kwargs):
    """
    根据数据类型分发给不同的生成函数

    参数:
        kwargs: 单个键值对，表示一个需要生成的类型

    生成:
        随机数据项
    """
    if len(kwargs) != 1:
        raise Exception('接收到的键值对个数不为1')

    _type, _info = next(iter(kwargs.items()))

    if _type in NUMBER_TYPE:
        yield from generateNumber(**{_type: _info})
    elif _type in CONTAINER_TYPE:
        yield from generateContainer(**{_type: _info})

@StaticRes(sum, max, min)
def sampling(**kwargs):
    """
    样本生成函数，支持通过 StaticRes 统计数值型样本的各种统计量

    参数:
        kwargs: 数据生成配置
    """
    for k, v in kwargs.items():
        yield from generateAType(**{k: v})


if __name__=='__main__':
    # EXAMPLE 1
    print(sampling(tuple={
        'num': 100,
        'int': {
            'num': 2,
            'datarange': (0, 1000)
        },
        'float': {
            'num': 2,
            'datarange': (0, 1000.0)
        },
        'str': {
            'num': 3,
            'datarange': string.ascii_letters,
            'len': 5
        }
    }))

"""
EXAMPLE 1
    sampling(tuple={
        'num': 100,
        'int': {
            'num': 2,
            'datarange': (0, 1000)
        },
        'float': {
            'num': 2,
            'datarange': (0, 1000.0)
        },
        'str': {
            'num': 3,
            'datarange': string.ascii_letters,
            'len': 5
        }
    })

EXAMPLE 2
    sampling(tuple={
        'num': 10000,  # 如果 num 太大程序会跑不完
        'tuple': {
            'num': 3,
            'int': {
                'num': 2,
                'datarange': (1, 100)
            },
            'str': {
                'num': 1,
                'datarange': string.ascii_lowercase,
                'len': 6
            }
        }
    })
"""