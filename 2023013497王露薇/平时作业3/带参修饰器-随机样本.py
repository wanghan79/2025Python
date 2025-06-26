import random
import string
from functools import wraps


def StaticRes(*stats):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 获取生成器
            generator = func(*args, **kwargs)

            # 初始化统计数据结构
            statistics = {stat.upper(): [] for stat in stats}

            # 处理一定数量的样本进行统计（这里设为1000个样本）
            sample_count = 0
            max_samples = 1000  # 防止无限循环

            for _ in range(max_samples):
                try:
                    data = next(generator)
                    # 只处理数值数据（int和float）
                    numeric_data = [x for x in data if isinstance(x, (int, float))]

                    if not numeric_data:
                        continue

                    sample_count += 1

                    for stat in stats:
                        stat = stat.upper()
                        if stat == 'SUM':
                            statistics['SUM'].append(sum(numeric_data))
                        elif stat == 'AVG':
                            statistics['AVG'].append(sum(numeric_data) / len(numeric_data))
                        elif stat == 'MAX':
                            statistics['MAX'].append(max(numeric_data))
                        elif stat == 'MIN':
                            statistics['MIN'].append(min(numeric_data))
                except StopIteration:
                    break

            if sample_count == 0:
                return {"error": "No numeric data found in samples"}

            # 计算最终统计结果
            result = {}
            for stat, values in statistics.items():
                if not values:
                    continue
                if stat == 'SUM':
                    # SUM的SUM没有意义，这里返回所有样本的和的总和
                    # 或者可以返回平均值，根据需求调整
                    result[stat] = sum(values)
                elif stat == 'AVG':
                    result[stat] = sum(values) / len(values)
                elif stat == 'MAX':
                    result[stat] = max(values)
                elif stat == 'MIN':
                    result[stat] = min(values)

            return result

        return wrapper

    return decorator


def structDataSampling(**kwargs):
    while True:  # 无限循环，生成无穷样本
        element = list()
        for key, value in kwargs.items():
            if key == "num":
                continue
            if key == "int":
                it = iter(value['datarange'])
                tmp = random.randint(next(it), next(it))
                element.append(tmp)
            elif key == "float":
                it = iter(value['datarange'])
                tmp = random.uniform(next(it), next(it))
                element.append(tmp)
            elif key == "str":
                tmp = ''.join(random.SystemRandom().choice(value["datarange"]) for _ in range(value["len"]))
                element.append(tmp)
            else:
                # 递归调用生成器函数
                generated = next(structDataSampling(**value))  # 使用 next 获取下一个生成的值
                element.extend(generated if isinstance(generated, list) else [generated])
        yield element


# 定义修饰函数
@StaticRes('SUM', 'AVG', 'MAX', 'MIN')
def sampled_data(**kwargs):
    return structDataSampling(**kwargs)


# 测试
if __name__ == "__main__":
    # 定义数据结构
    data_structure = {
        "num":100000000,
        "list":{
            "list": {
                "int": {"datarange": (0, 10)},
                "float": {"datarange": (0, 10000)}
            },
            "str": {"datarange": string.ascii_letters, "len": 10},
            "int": {"datarange": (0, 10)},
            "float": {"datarange": (0, 10000)}
        },
        "tuple":{
            "str":{"datarange":string.ascii_letters,"len":10},
            "list":{
                "int":{"datarange":(0,10)},
                "float":{"datarange":(0,10000)}
            },
            "dict":{
                "str":{"datarange":string.ascii_letters,"len":10},
                "int":{"datarange":(0,10)}
            }
        }
    }

    # 调用修饰后的函数
    result = sampled_data(**data_structure)
    print("统计结果:", result)