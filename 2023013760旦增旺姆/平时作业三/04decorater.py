import random
import string
import math

# 随机数据生成函数
def generate(struct):
    result = []
    num = struct.get('num', 1)  # 使用 get 方法安全地获取 'num'，默认值为 1
    for _ in range(num):
        res = {}
        for k, v in struct.items():
            if k == 'num':
                continue  # 跳过 'num' 键
            elif k == int:
                it = iter(v['datarange'])
                res['int'] = random.randint(next(it), next(it))
            elif k == float:
                it = iter(v['datarange'])
                res['float'] = random.uniform(next(it), next(it))
            elif k == str:
                datarange, length = v['datarange'], v['len']
                res['str'] = ''.join(random.SystemRandom().choice(datarange) for _ in range(length))
            elif k == list:
                res['list'] = generate(v)  # 递归生成列表
            elif k == tuple:
                res['tuple'] = tuple(generate(v))  # 递归生成元组
            elif k == dict:
                res['dict'] = {random.randint(0, 10): random.randint(0, 10)}
            else:
                continue
        result.append(res)
    return result

# 统计装饰器
def StaticRes(*stats):
    def decorator(func):
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)  # 调用被装饰的函数生成数据
            results = {stat: [] for stat in stats}  # 初始化统计结果字典

            for sample in data:
                int_val = sample.get('int', 0)
                float_val = sample.get('float', 0)
                combined = [int_val, float_val]

                for stat in stats:
                    if stat == 'SUM':
                        results[stat].append(sum(combined))
                    elif stat == 'AVG':
                        results[stat].append(sum(combined) / len(combined))
                    elif stat == 'VAR':
                        avg = sum(combined) / len(combined)
                        results[stat].append(sum((x - avg) ** 2 for x in combined) / len(combined))
                    elif stat == 'RMSE':
                        avg = sum(combined) / len(combined)
                        results[stat].append(math.sqrt(sum((x - avg) ** 2 for x in combined) / len(combined)))

            # 计算最终的统计结果
            final_results = {stat: sum(values) / len(values) for stat, values in results.items()}
            return final_results
        return wrapper
    return decorator

# 被装饰的函数
@StaticRes('SUM', 'AVG', 'VAR', 'RMSE')  # 指定需要统计的指标
def dataSampling(struct):
    return generate(struct)

# 主函数
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

    result = dataSampling(struct)  # 调用装饰后的函数
    print(result)  # 输出统计结果

if __name__ == "__main__":
    main()