import random
import string


def generate(**kwargs):
    num = kwargs.get('num', 1)
    for _ in range(num):
        res = list()
        for k, v in kwargs.items():
            if k == 'num':
                continue
            elif k == "int":
                it = iter(v['datarange'])
                res.append(random.randint(next(it), next(it)))
            elif k == "float":
                it = iter(v['datarange'])
                res.append(random.uniform(next(it), next(it)))
            elif k == "str":
                res.append(''.join(random.SystemRandom().choice(v['datarange']) for _ in range(v['len'])))
            elif k == "dict":
                key = ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(3))
                value = random.randint(0, 100)
                res.append({key: value})
            elif k == "list":
                res.append(list(generate(**v)))
            elif k == "tuple":
                res.append(tuple(generate(**v)))
            else:
                continue
        yield res


def main():
    # 获取用户输入的样本数量和结构
    sample_count = int(input("请输入要生成的样本数量："))
    print("请输入样本结构（以字典形式表示，例如：{'num': 1, 'tuple': {'str': {'datarange': string.ascii_uppercase, 'len': 50}, 'list': {'int': {'datarange': (0, 10)}, 'float': {'datarange': (0, 1.0)}}, 'dict': {}}}）：")
    struct = eval(input())

    # 使用生成器生成随机样本
    sample_generator = generate(**struct)
    for _ in range(sample_count):
        sample = next(sample_generator)
        print(sample)


if __name__ == "__main__":
    main()