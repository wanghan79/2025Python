
import random
import string

def dataSampling(config):
    """
    根据配置 config 生成一个随机样本。
    支持 int, float, str, list, tuple, dict 类型。
    每生成一个样本即 yield 返回（或直接 print 输出）。
    """

    def generate_item(k, v):
        if k == 'int':
            it = iter(v['datarange'])
            return random.randint(next(it), next(it))
        elif k == 'float':
            it = iter(v['datarange'])
            return random.uniform(next(it), next(it))
        elif k == 'str':
            datarange = v.get('datarange', string.ascii_letters)
            length = v.get('len', 8)
            return ''.join(random.choices(datarange, k=length))
        elif k == 'list':
            return list(dataSampling(v))
        elif k == 'tuple':
            return tuple(dataSampling(v))
        elif k == 'dict':
            return {key: generate_item(key, val) for key, val in v.items()}
        return None

    num = config.get('num', 1)

    for _ in range(num):
        sample = {}
        for key, value in config.items():
            if key == 'num':
                continue
            sample[key] = generate_item(key, value)
        yield sample


if __name__ == '__main__':
    struct = {
        'num': 10000,
        'tuple': {
            'str': {"datarange": string.ascii_uppercase, "len": 10}
        },
        'dict': {
            'list': {
                'int': {"datarange": (0, 10)}
            }
        },
        'int': {"datarange": (0, 10)},
        'float': {"datarange": (0, 10)}
    }

    for sample in dataSampling(struct):
        print(sample)  # 每生成一个样本就换行输出
