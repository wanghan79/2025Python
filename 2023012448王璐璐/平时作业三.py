import random

def deco(*ops):
    def outer(func):
        def inner(*args, **kwargs):
            data = list(func(*args, **kwargs))
            if 'SUM' in ops:
                print('SUM:', sum(data))
            if 'AVG' in ops:
                print('AVG:', sum(data) / len(data))
            if 'MAX' in ops:
                print('MAX:', max(data))
            if 'MIN' in ops:
                print('MIN:', min(data))
            return data
        return inner
    return outer

@deco('SUM', 'AVG', 'MAX', 'MIN')
def gen_nums(n):
    i = 0
    while i < n:
        yield random.randint(1, 100)
        i += 1

for x in gen_nums(10):
    print(x)
