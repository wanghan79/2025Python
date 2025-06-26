import random
import string
import math
from typing import Callable, Dict, Any, Generator, List, Union, Tuple, Iterator
from collections import defaultdict

NUMBER_TYPE = {'int', 'float', 'double'}
BASIC_TYPE = {'int', 'float', 'double', 'str', 'bool', 'choice'}
CONTAINER_TYPE = {'list', 'tuple', 'dict', 'set'}

def avg(values: List[Union[int, float]]) -> float:
    return sum(values) / len(values) if values else 0

def std(values: List[Union[int, float]]) -> float:
    if not values:
        return 0
    mean = avg(values)
    return math.sqrt(sum((x - mean) ** 2 for x in values) / len(values))

def count(values: List[Any]) -> int:
    return len(values)

def StaticRes(*sargs: Callable):
    def decorator(func):
        def wrapper(*args, **kwargs):
            values = []
            
            type_grouped_data = defaultdict(list)
            
            for sample in func(*args, **kwargs):
                sample_type = type(sample).__name__
                type_grouped_data[sample_type].append(sample)
                
                if isinstance(sample, (int, float)):
                    values.append(sample)
            
            stats_result = {}
            
            # 全局统计
            if values:
                for static_func in sargs:
                    if static_func.__name__ in ['sum', 'max', 'min', 'avg', 'std', 'count']:
                        if static_func.__name__ in ['sum', 'max', 'min']:
                            stats_result[static_func.__name__] = static_func(values)
                        elif static_func.__name__ == 'avg':
                            stats_result['avg'] = avg(values)
                        elif static_func.__name__ == 'std':
                            stats_result['std'] = std(values)
                        elif static_func.__name__ == 'count':
                            stats_result['count'] = count(values)
            
            # 按类型统计
            type_stats = {}
            for data_type, data_list in type_grouped_data.items():
                if data_type in ['int', 'float']:
                    type_stats[data_type] = {
                        'count': len(data_list),
                        'sum': sum(data_list) if data_list else 0,
                        'avg': avg(data_list),
                        'min': min(data_list) if data_list else None,
                        'max': max(data_list) if data_list else None,
                        'std': std(data_list)
                    }
                else:
                    type_stats[data_type] = {
                        'count': len(data_list)
                    }
            
            return {
                'statistics': stats_result,
                'by_type': type_stats,
                'samples': values[:10] if len(values) > 10 else values  # 只返回前10个样本
            }
        return wrapper
    return decorator

def generateNumber(**kwargs) -> Generator[Union[int, float, str, bool], None, None]:
    _type, _info = next(iter(kwargs.items()))
    count = _info.get('num', 1)

    if _type == 'int':
        if 'datarange' not in _info:
            raise ValueError('int类型必须提供datarange参数')
        start, end = _info['datarange']
        for _ in range(count):
            yield random.randint(start, end)
            
    elif _type == 'float':
        if 'datarange' not in _info:
            raise ValueError('float类型必须提供datarange参数')
        start, end = _info['datarange']
        precision = _info.get('precision', None)
        for _ in range(count):
            value = random.uniform(start, end)
            if precision is not None:
                value = round(value, precision)
            yield value
            
    elif _type == 'str':
        datarange = _info.get('datarange', string.ascii_letters)
        length = _info.get('len', 5)
        for _ in range(count):
            yield ''.join(random.choice(datarange) for _ in range(length))
            
    elif _type == 'bool':
        for _ in range(count):
            yield random.choice([True, False])
            
    elif _type == 'choice':
        options = _info.get('options', [])
        if not options:
            raise ValueError('choice类型必须提供options参数')
        for _ in range(count):
            yield random.choice(options)

def generateContainer(**kwargs) -> Generator[Any, None, None]:
    _type, _info = next(iter(kwargs.items()))
    count = _info.get('num', 1)

    if _type == 'tuple' or _type == 'list' or _type == 'set':
        for _ in range(count):
            container_items = []
            for k, v in _info.items():
                if k != 'num':
                    if k in BASIC_TYPE:
                        container_items.extend(list(generateNumber(**{k: v})))
                    elif k in CONTAINER_TYPE:
                        container_items.extend(list(generateContainer(**{k: v})))
            
            # 展开容器内的所有元素
            for item in container_items:
                yield item
                
    elif _type == 'dict':
        for _ in range(count):
            for k, v in _info.items():
                if k != 'num':
                    if 'key' in v and 'value' in v:
                        # 生成键值对
                        keys = list(generateAType(**v['key']))
                        values = list(generateAType(**v['value']))
                        
                        # 只处理数值类型的值
                        for i in range(min(len(keys), len(values))):
                            if isinstance(values[i], (int, float)):
                                yield values[i]

def generateAType(**kwargs) -> Generator[Any, None, None]:
    if len(kwargs) != 1:
        raise ValueError('接收到的键值对个数不为1')

    _type, _info = next(iter(kwargs.items()))

    if _type in BASIC_TYPE:
        yield from generateNumber(**{_type: _info})
    elif _type in CONTAINER_TYPE:
        yield from generateContainer(**{_type: _info})

@StaticRes(sum, max, min, avg, std, count)
def sampling(**kwargs) -> Iterator[Any]:
    for k, v in kwargs.items():
        yield from generateAType(**{k: v})


if __name__=='__main__':
    # EXAMPLE 1
    print("示例1: 元组中的基本类型统计")
    result1 = sampling(tuple={
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
    print(result1)
    
    # EXAMPLE 2
    print("\n示例2: 嵌套元组统计")
    result2 = sampling(tuple={
        'num': 50,  # 减小数量以便快速运行
        'tuple': {
            'num': 3,
            'int': {
                'num': 2,
                'datarange': (1, 100)
            },
            'float': {
                'num': 2,
                'datarange': (1.0, 100.0),
                'precision': 2
            }
        }
    })
    print(result2)
    
    # EXAMPLE 3
    print("\n示例3: 包含布尔值和选择项的统计")
    result3 = sampling(list={
        'num': 1,
        'int': {
            'num': 10,
            'datarange': (1, 10)
        },
        'bool': {
            'num': 5
        },
        'choice': {
            'num': 3,
            'options': [10, 20, 30, 40, 50]
        }
    })
    print(result3)
