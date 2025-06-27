import random
from functools import wraps

# 带参修饰器，接受操作类型作为参数
def StaticRes(*args):

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 调用原始函数生成样本数据
            samples = func(*args, **kwargs)
            results = {}
            
            # 根据传入的操作进行统计
            for operation in args:
                if operation == 'SUM':
                    results['SUM'] = sum([sample['salary'] for sample in samples])
                elif operation == 'AVG':
                    results['AVG'] = sum([sample['salary'] for sample in samples]) / len(samples) if samples else 0
                elif operation == 'MAX':
                    results['MAX'] = max([sample['salary'] for sample in samples], default=None)
                elif operation == 'MIN':
                    results['MIN'] = min([sample['salary'] for sample in samples], default=None)
            
            # 返回统计结果
            return results, samples
        return wrapper
    return decorator

# 随机样本生成函数
def dataSampling(num_samples, structure):

    samples = []
    for _ in range(num_samples):
        sample = {}
        for field, value_range in structure.items():
            if isinstance(value_range, range):
                sample[field] = random.choice(value_range)
            elif isinstance(value_range, list):
                sample[field] = random.choice(value_range)
            elif isinstance(value_range, tuple) and len(value_range) == 2:
                sample[field] = random.randint(value_range[0], value_range[1])
        samples.append(sample)
    return samples

# 使用装饰器修饰函数，并指定需要统计的操作
@StaticRes('SUM', 'AVG', 'MAX')  # 选择进行SUM, AVG, MAX三种统计操作
def generate_samples(num_samples, structure):
    return dataSampling(num_samples, structure)

# 样本数据结构
structure = {
    "age": range(18, 65),  # 年龄范围
    "name": ["Alice", "Bob", "Charlie", "David", "Eva"],  # 名字列表
    "salary": (3000, 10000),  # 工资范围
}

# 生成并输出统计结果
num_samples = 5
result, samples = generate_samples(num_samples, structure)

# 输出结果
print("统计结果:", result)
print("生成的样本:", samples)