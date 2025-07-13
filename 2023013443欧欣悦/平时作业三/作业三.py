import random
import string
from functools import wraps

def random_sample_generator(num_samples, structure):
    """
    生成随机样本的生成器函数。

    参数：
    num_samples (int): 需要生成的随机样本数量。
    structure (dict): 定义样本结构的字典，键为字段名，值为字段类型。

    生成器返回值：
    每次迭代返回一个符合指定结构的随机样本（字典形式）。
    """
    for _ in range(num_samples):
        sample = {}
        for field, field_type in structure.items():
            if field_type == "int":
                sample[field] = random.randint(0, 100)  # 随机整数范围0到100
            elif field_type == "float":
                sample[field] = round(random.uniform(0, 100), 2)  # 随机浮点数范围0到100，保留2位小数
            elif field_type == "str":
                sample[field] = ''.join(random.choices(string.ascii_letters + string.digits, k=8))  # 随机8位字符串
            elif field_type == "bool":
                sample[field] = random.choice([True, False])  # 随机布尔值
            else:
                raise ValueError(f"不支持的字段类型：{field_type}")
        yield sample

def statistics_decorator(*stats):
    """
    带参装饰器，用于对随机样本生成函数进行统计操作修饰。

    参数：
    *stats (str): 支持的统计操作，可以是 'SUM', 'AVG', 'MAX', 'MIN' 的任意组合。
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            samples = list(func(*args, **kwargs))  # 获取所有样本
            results = {}
            for stat in stats:
                if stat == 'SUM':
                    results['SUM'] = {field: sum(sample[field] for sample in samples if isinstance(sample[field], (int, float))) for field in samples[0]}
                elif stat == 'AVG':
                    results['AVG'] = {field: sum(sample[field] for sample in samples if isinstance(sample[field], (int, float))) / len(samples) for field in samples[0]}
                elif stat == 'MAX':
                    results['MAX'] = {field: max(sample[field] for sample in samples if isinstance(sample[field], (int, float))) for field in samples[0]}
                elif stat == 'MIN':
                    results['MIN'] = {field: min(sample[field] for sample in samples if isinstance(sample[field], (int, float))) for field in samples[0]}
                else:
                    raise ValueError(f"不支持的统计操作：{stat}")
            print("统计结果：")
            for stat, result in results.items():
                print(f"{stat}: {result}")
            return samples
        return wrapper
    return decorator

# 使用带参装饰器修饰随机样本生成函数
@statistics_decorator('SUM', 'AVG', 'MAX', 'MIN')
def generate_random_samples(num_samples, structure):
    return random_sample_generator(num_samples, structure)

# 定义样本结构
sample_structure = {
    "id": "int",
    "name": "str",
    "age": "int",
    "score": "float",
    "is_active": "bool"
}

# 调用者输入的随机样本数量
num_samples = int(input("请输入随机样本数量："))

# 生成随机样本并输出统计结果
print("生成的随机样本如下：")
for sample in generate_random_samples(num_samples, sample_structure):
    print(sample)