import random
import string


def generate_sample(kwargs):
    """
    生成单个样本
    """
    res = list()
    for k, v in kwargs.items():
        if k == 'int':
            it = iter(v['datarange'])
            res.append(random.randint(next(it), next(it)))
        elif k == 'float':
            it = iter(v['datarange'])
            res.append(random.uniform(next(it), next(it)))
        elif k == 'str':
            datarange, length = v['datarange'], v['len']
            tmp = ''.join(random.SystemRandom().choice(datarange) for _ in range(length))
            res.append(tmp)
        elif k == 'dict':
            elem = dict()
            elem[random.randint(0, 10)] = random.randint(0, 10)
            res.append(elem)
        elif k == 'list':
            res.append(list(generate_sample(v)))
        elif k == 'tuple':
            res.append(tuple(generate_sample(v)))
        else:
            continue
    return res


def generate_samples(kwargs, num_samples):
    """
    使用生成器生成大量样本
    """
    for _ in range(num_samples):
        yield generate_sample(kwargs)


def main():
    struct = {
        'int': {"datarange": (0, 100)},
        'float': {"datarange": (0.0, 1.0)},
        'str': {"datarange": string.ascii_uppercase, "len": 10},
        'list': { 'int': {"datarange": (0, 10)} },
        'tuple': { 'float': {"datarange": (0.0, 1.0)} },
        'dict': {}
    }
    num_samples = 100000000 # 一亿个样本
    for i, sample in enumerate(generate_samples(struct, num_samples)):
        print(f"Sample {i+1}: {sample}")
        if i >= 9:  # 仅打印前10个样本，避免过多输出
            break


if __name__ == "__main__":
    main()