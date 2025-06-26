import random
import string
def generate(kwargs):
        result = list()
        res = list()
        for k, v in kwargs.items():
            if k == int:
                it = iter(v['datarange'])
                res.append(random.randint(next(it), next(it)))
            elif k == float:
                it = iter(v['datarange'])
                res.append(random.uniform(next(it), next(it)))
            elif k == str:
                datarange, length = v['datarange'], v['len']
                tmp = ''.join(random.SystemRandom().choice(datarange) for _ in range(length))
                res.append(tmp)
            elif k == dict:
                elem = dict()
                elem[random.randint(0, 10)] = random.randint(0, 10)
                res.append(elem)
            elif k == list:
                res.append(list(generate(v)))
            elif k == tuple:
                res.append(tuple(generate(v)))
            else:
                continue
        result.append(res)
        yield result


def main():
    struct = {
        tuple: {
            str: {"datarange": string.ascii_uppercase, "len": 50},
            list: {
                int: {"datarange": (0, 10)},
                float: {"datarange": (0, 1.0)}
            },
            dict: {}
        }
    }
    for i in range(100000000):
        gen = generate(struct)
        print(next(gen))


if __name__ == '__main__':
    main()