import random
import string

def generate(struct):
    result = []
    num = struct.get('num', 1)  # 使用 get 方法安全地获取 'num'，默认值为 1
    for _ in range(num):
        res = []
        for k, v in struct.items():
            if k == 'num':
                continue  # 跳过 'num' 键
            elif k == int:
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
                elem = {random.randint(0, 10): random.randint(0, 10)}
                res.append(elem)
            elif k == list:
                res.append(generate(v))  # 递归生成列表
            elif k == tuple:
                res.append(tuple(generate(v)))  # 递归生成元组
            else:
                continue
        result.append(res)
    return result

def main():
    struct = {
        'num': 2,  # 生成 2 组数据
        int: {"datarange": (1, 100)},  # 生成一个 1 到 100 的随机整数
        float: {"datarange": (0.0, 1.0)},  # 生成一个 0.0 到 1.0 的随机浮点数
        str: {"datarange": string.ascii_uppercase, "len": 5},  # 生成一个长度为 5 的随机大写字母字符串
        list: {  # 生成一个列表
            int: {"datarange": (100, 200)},  # 列表中包含一个 100 到 200 的随机整数
            float: {"datarange": (1.0, 2.0)}  # 列表中包含一个 1.0 到 2.0 的随机浮点数
        },
        tuple: {  # 生成一个元组
            int: {"datarange": (1, 10)},  # 元组中包含一个 1 到 10 的随机整数
            str: {"datarange": string.ascii_lowercase, "len": 3}  # 元组中包含一个长度为 3 的随机小写字母字符串
        },
        dict: {}  # 生成一个随机字典
    }
    print(generate(struct))

if __name__ == "__main__":
    main()  