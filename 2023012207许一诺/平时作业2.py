import string
import random
from typing import Generator, Any, Dict, Union, List, Tuple

def sampling(**kwargs) -> Generator[Any, None, None]:
    for _type, _info in kwargs.items():
        count = _info.get('num', 1)

        for _ in range(count):
            if _type == 'int':
                it = iter(_info['datarange'])
                start, end = next(it), next(it)
                yield random.randint(start, end)

            elif _type == 'float':
                it = iter(_info['datarange'])
                start, end = next(it), next(it)
                precision = _info.get('precision', None)
                value = random.uniform(start, end)
                if precision is not None:
                    value = round(value, precision)
                yield value

            elif _type == 'str':
                length = _info.get('len', 1)
                datarange = _info.get('datarange', string.ascii_letters)
                yield ''.join(random.choice(datarange) for _ in range(length))

            elif _type == 'bool':
                yield random.choice([True, False])

            elif _type == 'choice':
                options = _info.get('options', [])
                yield random.choice(options)

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
                
            elif _type == 'dict':
                result = {}
                for k, v in _info.items():
                    if k != 'num':
                        key_template = v.get('key', {})
                        value_template = v.get('value', {})
                        
                        keys = list(sampling(**key_template))
                        values = list(sampling(**value_template))
                        
                        for i in range(min(len(keys), len(values))):
                            result[keys[i]] = values[i]
                yield result


def batch_sampling(batch_size: int, **kwargs) -> List[Any]:
    result = []
    gen = sampling(**kwargs)
    for _ in range(batch_size):
        try:
            result.append(next(gen))
        except StopIteration:
            break
    return result


if __name__ == '__main__':
    print("示例1：生成两个元组")
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
        
    print("\n示例2：生成两个复杂列表")
    gen2 = sampling(list={
        'num': 2, 
        'int': {
            'num': 2,
            'datarange': (100, 200)
        },
        'float': {
            'num': 1,
            'datarange': (1.5, 9.5),
            'precision': 2
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
    
    for item in gen2:
        print(item)
        
    print("\n示例3：生成字典")
    gen3 = sampling(dict={
        'num': 1,
        'pair': {
            'key': {'str': {'num': 3, 'len': 2, 'datarange': string.ascii_uppercase}},
            'value': {'int': {'num': 3, 'datarange': (1, 100)}}
        }
    })
    
    for item in gen3:
        print(item)
        
    print("\n示例4：使用batch_sampling批量生成")
    samples = batch_sampling(3, bool={'num': 5})
    print(samples)

