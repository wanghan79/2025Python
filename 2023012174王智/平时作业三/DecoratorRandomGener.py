import random
import string
from functools import wraps

def structDataSampling(num, **kwargs):
    """
    :param num: 生成器生成的数量
    :param kwargs: 生成器的参数
    :return: generator: 生成器
    """
    def generator():
        count = 0
        while count < num:
            element = []
            for key, value in kwargs.items():
                if key == "int":
                    element.append(random.randint(value['dataRange'][0], value['dataRange'][1]))
                elif key == "float":
                    element.append(random.uniform(value['dataRange'][0], value['dataRange'][1]))
                elif key == "str":
                    length = value.get('length', 5)
                    element.append(''.join(random.choices(list(value['dataRange']), k=length)))
            yield element
            count += 1
    return generator()

def generator_inner(**kwargs):
    """
    :param kwargs: 生成器的参数
    :return: generator: 生成器
    """
    for key, value in kwargs.items():
        if key == "int":
            yield random.randint(value['dataRange'][0], value['dataRange'][1])
        elif key == "float":
            yield random.uniform(value['dataRange'][0], value['dataRange'][1])
        elif key == "str":
            length = value.get('length', 5)
            yield ''.join(random.choices(list(value['dataRange']), k=length))

def dataStatistics(statistics):
    """
    根据传入的统计参数创建一个修饰器，用于统计生成器结果的SUM、AVG、MAX、MIN
    :param statistics: 一个字典，包含要计算的统计类型及其对应的数据位置
    :return: 修饰器函数
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 创建统计结果的容器
            stats = {}
            for stat_type in statistics:
                stats[stat_type] = []

            # 遍历生成器结果并填充统计容器
            for data in func(*args, **kwargs):
                for stat_type, data_pos in statistics.items():
                    stats[stat_type].append(data[data_pos])

            # 根据传入的统计类型计算相应结果
            result = {}
            for stat_type in statistics:
                if hasattr(stat_type, '__call__'):
                    result[stat_type.__name__] = stat_type(stats[stat_type])
                else:
                    if stat_type == 'SUM':
                        result[stat_type] = sum(stats[stat_type])
                    elif stat_type == 'AVG':
                        result[stat_type] = sum(stats[stat_type]) / len(stats[stat_type])
                    elif stat_type == 'MAX':
                        result[stat_type] = max(stats[stat_type])
                    elif stat_type == 'MIN':
                        result[stat_type] = min(stats[stat_type])
                    else:
                        print(f"Unsupported statistics type: {stat_type}")
            return result
        return wrapper
    return decorator

@dataStatistics({'SUM': 0, 'AVG': 0, 'MAX': 0, 'MIN': 0})
def apply(num=10, **kwargs):
    struct = {
        "num": num,
        "int": {"dataRange": (0, 100)},
        "float": {"dataRange": (0, 10000)},
        "str": {"dataRange": string.ascii_letters, "len": 10},
    }
    return structDataSampling(**struct)

# 示例调用，统计整数的第一列数据
if __name__ == '__main__':
    stats = apply(num=10)
    print(f"SUM: {stats['SUM']}, AVG: {stats['AVG']}, MAX: {stats['MAX']}, MIN: {stats['MIN']}")
