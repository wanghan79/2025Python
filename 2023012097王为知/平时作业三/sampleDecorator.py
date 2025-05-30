"""
@Author: Weizhi Wang
@Date: 2025-05-20
@Description: 使用带参修饰器实现对随机样本生成函数的统计操作修饰，能够实现SUM、AVG、MAX、MIN四种统计操作的任意组合进行统计结果输出。
"""

import random
import string
from functools import wraps
import atexit

# 全局变量用于存储所有样本的数值
all_numbers = []

def extract_numbers(data):
    """
    递归提取数据结构中的所有数值（整数和浮点数）
    
    参数:
    data: 任意数据结构（支持嵌套）
    
    返回:
    list: 提取到的数值列表
    """
    numbers = []
    if isinstance(data, (int, float)):
        numbers.append(data)
    elif isinstance(data, (list, tuple)):
        for item in data:
            numbers.extend(extract_numbers(item))
    elif isinstance(data, dict):
        for key, value in data.items():
            numbers.extend(extract_numbers(key))
            numbers.extend(extract_numbers(value))
    return numbers

def statistics_decorator(operations):
    """
    带参装饰器工厂函数，用于添加全局统计功能
    
    参数:
    operations (list): 包含统计操作名的列表（可选'SUM','AVG','MAX','MIN'）
    
    返回:
    decorator: 装饰器函数
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            gen = func(*args, **kwargs)
            for sample in gen:
                # 提取当前样本中的所有数值并添加到全局列表
                all_numbers.extend(extract_numbers(sample))
                yield sample
        return wrapper
    return decorator

def print_global_statistics(operations):
    """
    打印全局统计结果
    
    参数:
    operations (list): 需要执行的统计操作列表
    """
    if not all_numbers:
        print("没有收集到任何数值数据")
        return
    
    print("\n" + "="*50)
    print("全局统计结果（所有样本）：")
    print("="*50)
    
    stats = {}
    if 'SUM' in operations:
        stats['SUM'] = sum(all_numbers)
    if 'AVG' in operations:
        stats['AVG'] = sum(all_numbers) / len(all_numbers)
    if 'MAX' in operations:
        stats['MAX'] = max(all_numbers)
    if 'MIN' in operations:
        stats['MIN'] = min(all_numbers)
    
    for op, value in stats.items():
        print(f"{op}: {value:.4f}" if isinstance(value, float) else f"{op}: {value}")
    
    print(f"统计样本数量: {len(all_numbers)}个数值")
    print("="*50)

def generator_sample(kwargs):
    """
    根据给定的结构规范生成单个样本数据
    
    参数:
    kwargs (dict): 描述数据结构的字典，键为数据类型，值为该类型的生成规则
    
    返回:
    list: 生成的样本数据列表
    """
    res = list()
    for k, v in kwargs.items():
        if k == 'num':
            continue
        elif k is int:
            it = iter(v['datarange'])
            res.append(random.randint(next(it), next(it)))
        elif k is float:
            it = iter(v['datarange'])
            res.append(random.uniform(next(it), next(it)))
        elif k is str:
            datarange, length = v['datarange'], v['len']
            tmp = ''.join(random.SystemRandom().choice(datarange) for _ in range(length))
            res.append(tmp)
        elif k is dict:
            elem = dict()
            elem[random.randint(0, 10)] = random.randint(0, 10)
            res.append(elem)
        elif k is list:
            res.append(generator_sample(v))
        elif k is tuple:
            res.append(tuple(generator_sample(v)))
        else:
            continue
    return res

# 在此配置需要的统计操作
OPERATIONS = ['SUM', 'AVG', 'MAX', 'MIN']

@statistics_decorator(operations=OPERATIONS)
def generate(kwargs):
    """
    生成器函数，根据给定结构无限生成样本数据（已添加统计装饰器）
    
    参数:
    kwargs (dict): 描述数据结构的字典
    
    返回:
    generator: 生成样本数据的生成器
    """
    while True:
        yield generator_sample(kwargs)

def main():
    """
    主函数：定义数据结构并生成10000个样本数据
    """
    # 注册退出处理函数，在程序结束时打印全局统计
    atexit.register(print_global_statistics, OPERATIONS)
    
    struct = {
        tuple: {
            int: {
                'datarange': (-1000, 1000),
                'constraint': lambda x: x % 2 == 0
            },
            float: {
                'datarange': (-100.0, 100.0),
                'constraint': lambda x: x > 0
            },
            str: {
                'datarange': string.ascii_letters + string.digits + string.punctuation,
                'len': 10,
                'constraint': lambda s: any(c.isdigit() for c in s)
            },
            list: {
                tuple: {
                    dict: {
                        int: {
                            'datarange': (0, 20),
                            'constraint': lambda x: x > 5
                        },
                        str: {
                            'datarange': string.ascii_lowercase,
                            'len': 3,
                            'constraint': lambda s: s[0] in 'aeiou'
                        }
                    },
                    float: {
                        'datarange': (0.1, 10.0),
                        'constraint': lambda x: x < 5.0
                    }
                },
                'length': 3
            },
            dict: {
                str: {
                    'datarange': string.ascii_uppercase,
                    'len': 5,
                    'constraint': lambda s: s.isupper()
                },
                list: {
                    int: {
                        'datarange': (1, 100),
                        'constraint': lambda x: x % 3 == 0
                    },
                    'length': 5
                }
            }
        }
    }
    
    sample_generator = generate(struct)
    count = 0
    for sample in sample_generator:
        print(f"样本 {count+1}: {sample}")
        count += 1
        if count >= 10000:
            print(f"\n已生成 {count} 个样本，程序即将退出...")
            break

if __name__ == "__main__":
    main()
