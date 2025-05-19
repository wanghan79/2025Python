#!/usr/bin/python3
import random
import string

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
    'tuple': { 
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
}

if __name__ == '__main__':
    for _ in range(5):
        s = ranGen(**struct)
        print(next(s))