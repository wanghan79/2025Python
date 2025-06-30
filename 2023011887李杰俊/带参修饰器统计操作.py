import random
import xml.etree.ElementTree as ET
from functools import wraps
from typing import List, Dict, Any, Tuple, Generator
import statistics
import io


def random_sample_generator(sample_count: int, structure: Dict[str, Any]) -> Generator[Dict, None, None]:
    """
    随机样本生成器

    参数:
        sample_count: 样本数量
        structure: 样本结构定义
                  例如: {
                      'name': ('string', 5),  # 字符串类型，长度5
                      'age': ('int', 18, 80), # 整数类型，范围18-80
                      'score': ('float', 0.0, 100.0), # 浮点数类型，范围0.0-100.0
                      'active': ('bool',)     # 布尔类型
                  }

    生成器: 每次yield一个符合结构的样本字典
    """

    def generate_value(field_def):
        """根据字段定义生成随机值"""
        if field_def[0] == 'string':
            length = field_def[1] if len(field_def) > 1 else 10
            chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            return ''.join(random.choice(chars) for _ in range(length))

        elif field_def[0] == 'int':
            min_val = field_def[1] if len(field_def) > 1 else 0
            max_val = field_def[2] if len(field_def) > 2 else 100
            return random.randint(min_val, max_val)

        elif field_def[0] == 'float':
            min_val = field_def[1] if len(field_def) > 1 else 0.0
            max_val = field_def[2] if len(field_def) > 2 else 100.0
            return round(random.uniform(min_val, max_val), 2)

        elif field_def[0] == 'bool':
            return random.choice([True, False])

        else:
            raise ValueError(f"不支持的数据类型: {field_def[0]}")

    for _ in range(sample_count):
        sample = {}
        for field_name, field_def in structure.items():
            sample[field_name] = generate_value(field_def)
        yield sample


def use_sample_generator():
    """生成器使用范例代码"""
    print("=== 生成器使用范例 ===")

    # 定义样本结构
    structure = {
        'name': ('string', 8),
        'age': ('int', 18, 65),
        'salary': ('float', 3000.0, 15000.0),
        'is_manager': ('bool',)
    }

    # 生成5个样本
    print("生成的随机样本:")
    generator = random_sample_generator(5, structure)

    for i, sample in enumerate(generator, 1):
        print(f"样本{i}: {sample}")

    return generator


# ==================== 作业三：带参修饰器统计操作 ====================

def statistics_decorator(*stats_ops):
    """
    带参修饰器：对随机样本生成函数进行统计操作

    参数:
        *stats_ops: 统计操作列表，可包含 'SUM', 'AVG', 'MAX', 'MIN'
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 收集所有样本
            samples = list(func(*args, **kwargs))

            print(f"\n=== 统计结果 (共{len(samples)}个样本) ===")

            # 获取数值字段
            numeric_fields = {}
            if samples:
                for field, value in samples[0].items():
                    if isinstance(value, (int, float)):
                        numeric_fields[field] = [sample[field] for sample in samples]

            # 执行统计操作
            for field, values in numeric_fields.items():
                print(f"\n字段 '{field}' 的统计:")

                for op in stats_ops:
                    if op == 'SUM':
                        result = sum(values)
                        print(f"  总和: {result}")

                    elif op == 'AVG':
                        result = statistics.mean(values)
                        print(f"  平均值: {result:.2f}")

                    elif op == 'MAX':
                        result = max(values)
                        print(f"  最大值: {result}")

                    elif op == 'MIN':
                        result = min(values)
                        print(f"  最小值: {result}")

            return samples

        return wrapper

    return decorator


@statistics_decorator('SUM', 'AVG', 'MAX', 'MIN')
def generate_statistical_samples(count: int, structure: Dict[str, Any]):
    """被修饰的随机样本生成函数"""
    return random_sample_generator(count, structure)

def test_all_assignments():
    print("\n" + "=" * 60)
    print("作业三：带参修饰器测试")
    print("=" * 60)

    # 测试统计修饰器
    structure = {
        'id': ('int', 1, 100),
        'score': ('float', 60.0, 100.0),
        'age': ('int', 20, 30)
    }

    samples = generate_statistical_samples(5, structure)
    print("\n" + "=" * 60)

test_all_assignments()
