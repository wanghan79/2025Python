import random
import string

def Generator(**kwargs):
    # 初始化
    num = kwargs.get("num", 1)

    # 使用生成器逐个生成数据
    for _ in range(num):
        res = list()
        for k, v in kwargs.items():
            if k == "num":
                continue
            elif k == "int":
                it = iter(v['datarange'])
                res.append(random.randint(next(it), next(it)))
            elif k == "float":
                it = iter(v['datarange'])
                res.append(random.uniform(next(it), next(it)))
            elif k == "str":
                res.append(''.join([random.SystemRandom().choice(v['datarange']) for _ in range(v['len'])]))
            elif k == "dict":
                key = ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(3))
                value = random.randint(0, 100)
                res.append({key: value})
            elif k == "list":
                # 递归展开生成器
                res.append(list(Generator(**v)))
            elif k == "tuple":
                # 递归展开生成器
                res.append(tuple(Generator(**v)))
            else:
                continue
        yield res

def main():
    struct = {
        'num': 100000000, 
        "tuple": {
            "str": {
                "datarange": string.ascii_uppercase, 
                "len": 50
            },
            "list": {
                "int": {
                    "datarange": (0, 10)
                }, 
                "float": {
                    "datarange": (0, 1.0)
                }
            }, 
            "dict": {}
        }
    }

    # 迭代生成样本
    sample_generator = Generator(**struct)
    for sample in sample_generator:
        # 打印结果
        print(sample)
        # break

main()
