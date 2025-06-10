import random
import string
def StaticRes(*args):
    def decorator(func):
        def wrapper(kwargs):
            res = dict()
            count = 0
            total = 0
            if 'SUM' in args:
                res['SUM'] = 0
            generator = func(kwargs)
            for data in generator:
                count += 1
                total += data[0]
                if 'SUM' in args:
                    res['SUM'] += data[0]
                if 'MAX' in args:
                    if res.get('MAX') is None or res['MAX'] < data[0]:
                        res['MAX'] = data[0]
                if 'MIN' in args:
                    if res.get('MIN') is None or res['MIN'] > data[0]:
                        res['MIN'] = data[0]
                if 'AVG' in args and count > 0:
                    res['AVG'] = total/count
            return res
        return wrapper
    return decorator

@StaticRes('SUM','MAX','MIN','AVG')
def generate(kwargs):
    num = kwargs.get('num', 1)
    for _ in range(num):
        resp = list()
        for key, value in kwargs.items():
            if key == 'num':
                continue

            if key is int:
                start, end = iter(value['datarange'])
                resp.append(random.randint(start, end))
            elif key is float:
                start, end = iter(value['datarange'])
                resp.append(random.uniform(start, end))
            elif key is str:
                chars = value['datarange']
                length = value['len']
                tmp = ''.join(random.SystemRandom().choice(chars) for _ in range(length))
                resp.append(tmp)
            elif key is dict:
                dictionary = {random.choice[value['datarange']]: random.choice(value['datarange'])}
                resp.append(dictionary)
            elif key is list:
                resp.append(list(generate(value)))
            elif key is tuple:
                resp.append(tuple(generate(value)))

        yield resp

def main():
    struct = {"num": 1000, int: {"datarange": (1, 100)}, float: {"datarange": (1.0, 1000)},
              str: {"datarange": string.ascii_uppercase, "len": 10}}

    resp = generate(struct)

    count = 0
    for item in resp:
        count += 1
        if count % 1000 == 0:
            print(f"已生成 {count:,} 条数据")

    print(resp)

if __name__ == '__main__':
    main()
