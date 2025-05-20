#!/usr/bin/python3
import random
import string
from functools import wraps
#from date import *

SUM = "SUM"
AVG = "AVG"
MAX = "MAX"
MIN = "MIN"

def _flatten(items):
    for item in items:
        if isinstance(item, (list, tuple)):
            yield from _flatten(item)
        elif isinstance(item, dict):
            yield from _flatten(item.values())
        elif isinstance(item, (int, float)):
            yield item

def dSum(data):
    return sum(_flatten(data))

def dAvg(data):
    flattened = list(_flatten(data))
    return sum(flattened)/len(flattened) if len(flattened) > 0 else 0

def dMAX(data):
    flattened = list(_flatten(data))
    return max(flattened) if len(flattened) > 0 else None

def dMIN(data):
    flattened = list(_flatten(data))
    return min(flattened) if len(flattened) > 0 else None

def StaticRes(*metrics):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            rtn = dict()
            D = list(func(*args, **kwargs))
            if SUM in metrics:
                rtn[SUM] = dSum(D)
            if AVG in metrics:
                rtn[AVG] = dAvg(D)
            if MAX in metrics:
                rtn[MAX] = dMAX(D)
            if MIN in metrics:
                rtn[MIN] = dMIN(D)
            return rtn
        return wrapper
    return decorator


@StaticRes(SUM, AVG, MAX, MIN)
def ranGen(**kwargs):
    for key, value in kwargs.items():
        num = value.get('num', 1)
        
        if key == 'int':
            it = iter(value['datarange'])
            first = next(it)
            second = next(it)
            yield tuple(random.randint(first, second) for _ in range(num))
        
        elif key == 'float':
            it = iter(value['datarange'])
            first = next(it)
            second = next(it)
            yield tuple(random.uniform(first, second)for _ in range(num))
        
        elif key == 'str':
            datarange, length = value['datarange'], value['len']
            yield tuple(''.join(random.SystemRandom().choice(datarange) for _ in range(length)) for _ in range(num))
        
        elif key == 'dict':
            key_gen = list(ranGen(**value['key']))
            item_gen = list(ranGen(**value['item']))
            yield dict(zip(key_gen, item_gen))
        
        elif key == 'list':
            yield list(ranGen(**value))
        
        elif key == 'tuple':
            yield tuple(ranGen(**value))
        
        else:
            continue

struct ={
    'int': {'datarange': (0,10), 'num': 5},
    'str': {"datarange": string.ascii_lowercase, "len": 5, 'num': 2}, 
    'list': {
        'int': {"datarange": (0, 10), 'num': 3},
        'float': {"datarange": (0, 1.0), 'num': 2}
    }, 
    'dict': {
        "key":{'int': {"datarange": (0, 10), 'num': 3} }, 
        "item":{'str': {"datarange": string.ascii_uppercase, "len": 10, 'num': 2} }
    }
}

if __name__ == '__main__':
    for _ in range(1):
        s = ranGen(**struct)
        print(s)