import random
import string


def generate(kwargs):
    result = list()
    num = kwargs['num'] if 'num' in kwargs else 1
    for _ in range(num):
        res = list()
        for k, v in kwargs.items():
            if k == 'num':
                continue
            elif isinstance(k, type):
                if k is int:
                    it = iter(v['datarange'])
                    res.append(random.randint(next(it), next(it)))
                elif k is float:
                    it = iter(v['datarange'])
                    res.append(random.uniform(next(it), next(it)))
                elif k is str:
                    datarange, length = v['datarange'], v['len']
                    tmp = ''.join(random.SystemRandom().choice(datarange) for _ in range(length))
                    res.append(tmp)
                elif k is dict:
                    elem = dict()
                    elem[random.randint(0, 10)] = random.randint(0, 10)
                    res.append(elem)
                elif k is list:
                    res.append(generate(v))
                elif k is tuple:
                    res.append(tuple(generate(v)))
            else:
                continue
        result.append(res)
    return result


def main():
    struct = {'num': 2, tuple: {str: {"datarange": string.ascii_uppercase, "len": 50},
                               list: {int: {"datarange": (0, 10)},
                                      float: {"datarange": (0, 1.0)}},
                               dict: {}}}
    print(generate(struct))


if __name__ == '__main__':
    main()