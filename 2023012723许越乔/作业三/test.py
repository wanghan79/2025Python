import random
import string
from functools import wraps


def statistics_decorator(*stats):
    """
    带参装饰器，用于对随机样本生成函数进行统计操作
    :param stats: 统计操作的组合，支持 'SUM', 'AVG', 'MAX', 'MIN'
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 调用原函数生成样本
            samples = func(*args, **kwargs)

            # 初始化统计结果字典
            results = {stat: {} for stat in stats}

            # 遍历每个样本
            for key in samples[0].keys():
                values = [sample[key] for sample in samples if isinstance(sample[key], (int, float))]

                if 'SUM' in stats:
                    results['SUM'][key] = sum(values)
                if 'AVG' in stats:
                    results['AVG'][key] = sum(values) / len(values) if values else 0
                if 'MAX' in stats:
                    results['MAX'][key] = max(values) if values else None
                if 'MIN' in stats:
                    results['MIN'][key] = min(values) if values else None

            # 打印统计结果
            print("统计结果：")
            for stat, result in results.items():
                print(f"{stat}: {result}")

            # 返回原始样本数据
            return samples

        return wrapper

    return decorator


# 随机样本生成函数
def generate_random_samples(num_samples, structure):
    """
    根据结构生成指定数量的随机样本
    :param num_samples: 样本数量
    :param structure: 样本结构
    :return: 包含所有样本的列表
    """
    samples = []
    for _ in range(num_samples):
        sample = {}
        for key, value_type in structure.items():
            if value_type == "int":
                sample[key] = random.randint(0, 100)
            elif value_type == "float":
                sample[key] = round(random.uniform(0, 100), 2)
            elif value_type == "string":
                sample[key] = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            elif value_type == "bool":
                sample[key] = random.choice([True, False])
            else:
                raise ValueError(f"Unsupported type: {value_type}")
        samples.append(sample)
    return samples


# 使用装饰器
@statistics_decorator('SUM', 'AVG', 'MAX', 'MIN')
def generate_and_statistics_samples(num_samples, structure):
    return generate_random_samples(num_samples, structure)


# 示例使用
if __name__ == "__main__":
    # 定义样本结构
    sample_structure = {
        "id": "int",
        "name": "string",
        "age": "int",
        "score": "float",
        "is_active": "bool"
    }

    # 生成 5 个随机样本并进行统计
    generate_and_statistics_samples(5, sample_structure)