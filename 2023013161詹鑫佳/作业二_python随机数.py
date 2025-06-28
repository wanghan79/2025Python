import random
import string

def SampleData(**kwargs):
    num = kwargs.get('num', 1)  # 使用 get 方法获取 num，默认值为 1
    for _ in range(num):
        answer = list()
        for k, v in kwargs.items():
            if k == 'num':
                continue
            elif k == 'int':
                it = iter(v['datarange'])
                answer.append(random.randint(next(it), next(it)))
            elif k == 'float':
                it = iter(v['datarange'])
                answer.append(random.uniform(next(it), next(it)))
            elif k == 'str':
                datarange, length = v['datarange'], v['len']
                tmp = ''.join(random.SystemRandom().choice(datarange) for _ in range(length))
                answer.append(tmp)
            elif k == 'dict':
                elem = dict()
                elem[random.randint(0, 10)] = random.randint(0, 10)
                answer.append(elem)
            elif k == 'list':
                answer.append(list(SampleData(**v)))  # 递归调用，注意传递字典
            elif k == 'tuple':
                answer.append(tuple(SampleData(**v)))  # 递归调用，注意传递字典
            else:
                continue
        yield answer

def main():
    struct = {
        'num': 1000,  # 随机样本数量：用户自定义，这里取1000
        'tuple': {    # 用户自定义随机样本结构
            'str': {"datarange": string.ascii_uppercase, "len": 3},
            'list': {
                'int': {"datarange": (0, 10)},
                'float': {"datarange": (0, 1.0)}
            },
            'dict': {}
        }
    }
    gen = SampleData(**struct)
    for sample in gen:
        # 处理每个样本，例如打印或保存到文件
        print(sample)

if __name__ == "__main__":
    main()
