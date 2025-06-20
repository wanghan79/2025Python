# 作业三：统计操作修饰器

import random
import string
from functools import wraps

def statistics_decorator(*operations):

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 获取生成的样本
            samples = list(func(*args, **kwargs))

            # 提取所有数值
            all_numbers = []
            for sample in samples:
                for value in sample.values():
                    if isinstance(value, (int, float)):
                        all_numbers.append(value)
                    elif isinstance(value, list):
                        all_numbers.extend([v for v in value if isinstance(v, (int, float))])

            # 计算统计值
            stats = {}
            if all_numbers:
                if 'SUM' in operations:
                    stats['SUM'] = sum(all_numbers)
                if 'AVG' in operations:
                    stats['AVG'] = sum(all_numbers) / len(all_numbers)
                if 'MAX' in operations:
                    stats['MAX'] = max(all_numbers)
                if 'MIN' in operations:
                    stats['MIN'] = min(all_numbers)

            return {'samples': samples, 'statistics': stats}

        return wrapper

    return decorator

# 简化的数据生成器（用于测试修饰器）
def simple_data_generator(config):

    count = config.get('count', 1)

    for _ in range(count):
        sample = {}
        for field_name, field_config in config.items():
            if field_name == 'count':
                continue

            data_type = field_config['type']

            if data_type == 'int':
                sample[field_name] = random.randint(field_config['min'], field_config['max'])
            elif data_type == 'float':
                sample[field_name] = random.uniform(field_config['min'], field_config['max'])
            elif data_type == 'str':
                length = field_config['length']
                chars = field_config.get('chars', string.ascii_letters)
                sample[field_name] = ''.join(random.choice(chars) for _ in range(length))
            elif data_type == 'list':
                size = field_config['size']
                min_val = field_config['min']
                max_val = field_config['max']
                sample[field_name] = [random.randint(min_val, max_val) for _ in range(size)]

        yield sample

# 测试函数定义
@statistics_decorator('SUM', 'AVG', 'MAX', 'MIN')
def generate_student_data():
    """生成学生数据"""
    config = {
        'count': 5,
        'score': {'type': 'int', 'min': 70, 'max': 100},
        'rate': {'type': 'float', 'min': 0.8, 'max': 1.0},
        'name': {'type': 'str', 'length': 5},
        'grades': {'type': 'list', 'size': 3, 'min': 80, 'max': 95}
    }
    return simple_data_generator(config)


@statistics_decorator('SUM', 'AVG')
def generate_simple_data():
    """生成简单数据"""
    config = {
        'count': 3,
        'value1': {'type': 'int', 'min': 1, 'max': 10},
        'value2': {'type': 'float', 'min': 1.0, 'max': 5.0}
    }
    return simple_data_generator(config)


@statistics_decorator('MAX', 'MIN')
def generate_range_data():
    """生成范围数据（"""
    config = {
        'count': 4,
        'temperature': {'type': 'int', 'min': -10, 'max': 40},
        'humidity': {'type': 'float', 'min': 30.0, 'max': 90.0},
        'measurements': {'type': 'list', 'size': 5, 'min': 0, 'max': 100}
    }
    return simple_data_generator(config)

def print_result(result, title):
    print(f"\n=== {title} ===")
    print(f"生成样本数: {len(result['samples'])}")

    for i, sample in enumerate(result['samples'], 1):
        print(f"  样本{i}: {sample}")

    print(f"\n统计结果:")
    for stat_name, stat_value in result['statistics'].items():
        if isinstance(stat_value, float):
            print(f"  {stat_name}: {stat_value:.2f}")
        else:
            print(f"  {stat_name}: {stat_value}")

if __name__ == "__main__":
    print("=== 统计操作修饰器测试 ===")

    # 测试1：完整统计操作
    result1 = generate_student_data()
    print_result(result1, "学生数据 - 完整统计")

    # 测试2：部分统计操作
    result2 = generate_simple_data()
    print_result(result2, "简单数据 - 部分统计")

    # 测试3：最大最小统计
    result3 = generate_range_data()
    print_result(result3, "范围数据 - 最大最小统计")

    @statistics_decorator('SUM')
    def generate_sum_only():
        config = {
            'count': 2,
            'numbers': {'type': 'list', 'size': 3, 'min': 1, 'max': 5}
        }
        return simple_data_generator(config)

    result_sum = generate_sum_only()
    print_result(result_sum, "仅计算总和")