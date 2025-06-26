import random
import string
#可以生成很大数据
def generate(**kwargs):
    num = kwargs.get('num', 1)  # 使用 get 方法获取 num，默认值为 1
    for _ in range(num):
        res = list()
        for k, v in kwargs.items():
            if k == 'num':
                continue
            elif k == 'int':
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
                res.append(generate(**v))  # 递归调用，注意传递字典
            elif k == 'tuple':
                res.append(tuple(generate(**v)))  # 递归调用，注意传递字典
            else:
                continue
        yield res  # 使用 yield 逐个生成结果

def main():
    struct = {
        'num': 100000000,  # 生成一亿个样本
        'tuple': {
            'str': {"datarange": string.ascii_uppercase, "len": 3},
            'list': {
                'int': {"datarange": (0, 10)},
                'float': {"datarange": (0, 1.0)}
            },
            'dict': {}
        }
    }
    generator = generate(**struct)
    for sample in generator:
        print(sample)  # 打印生成的样本
        # 注意：由于生成一亿个样本会占用大量时间和资源，建议在实际使用中限制打印数量或进行其他处理

if __name__ == "__main__":
    main()