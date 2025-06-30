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

def test_all_assignments():
    print("\n" + "=" * 60)
    print("作业二：生成器测试")
    print("=" * 60)

    use_sample_generator()

    print("\n" + "=" * 60)

test_all_assignments()
