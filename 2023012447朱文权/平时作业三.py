import random
import string
def StaticRes(*args):
    def decorator(func):
        def wrapper(kwargs):
            res=dict()
            if 'SUM' in args:
                res['SUM']=0
            generator=func(kwargs)
            for data in generator:
                if 'SUM' in args:
                    res['SUM']+=data[0]
                if 'MAX' in args:
                    if res.get('MAX') is None or res['MAX']<data[0]:
                        res['MAX']=data[0]
                if 'MIN' in args:
                    if res.get('MIN') is None or res['MIN']>data[0]:
                        res['MIN']=data[0]
            if 'ADV' in args:
                res['ADV']=res['SUM']/kwargs['num']
            return res
        return wrapper
    return decorator

@StaticRes('SUM','ADV','MAX','MIN')
def create(kwargs):
    num = kwargs['num'] if 'num' in kwargs else 1
    for i in range(num):
        resp = list()
        for key, value in kwargs.items():
            if key == 'num':
                continue
            elif key is int:
                index = iter(value['datarange'])
                resp.append(random.randint(next(index), next(index)))
            elif key is float:
                index = iter(value['datarange'])
                resp.append(random.uniform(next(index), next(index)))
            elif key is str:
                tmp = ''.join(random.SystemRandom().choice(value['datarange']) for _ in range(value['len']))
                resp.append(tmp)
            elif key is dict:
                dictionary = dict()
                dictionary[random.SystemRandom] = random.choice(value['datarange'])
                resp.append(dictionary)
            elif key is list:
                resp.append(create(value))
            elif key is tuple:
                resp.append(tuple(create(value)))
            else:
                continue
        yield resp

def main():
    struct = {"num": 10, int: {"datarange": (0, 100)}, float: {"datarange": (0, 10000)},
              str: {"datarange": string.ascii_uppercase, "len": 50}}

    res = create(struct)
    print (res)
if __name__ == '__main__':
    main()