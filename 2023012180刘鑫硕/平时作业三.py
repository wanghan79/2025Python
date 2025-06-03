"""
@Author: 刘鑫硕
@File:装饰器
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

def generate_sample(structure):
    """
    递归生成样本数据
    
    参数:
    structure (dict): 描述数据结构的字典
    
    返回:
    根据structure生成的样本数据
    """
    if not isinstance(structure, dict):
        return structure
    
    # 处理特殊类型
    if len(structure) == 1 and list(structure.keys())[0] in (list, tuple, dict):
        data_type = list(structure.keys())[0]
        params = list(structure.values())[0]
        
        if data_type == list:
            length = params.get('length', random.randint(1, 5))
            element_structure = params.copy()
            element_structure.pop('length', None)
            return [generate_sample(element_structure) for _ in range(length)]
        
        elif data_type == tuple:
            length = params.get('length', random.randint(1, 5))
            element_structure = params.copy()
            element_structure.pop('length', None)
            return tuple(generate_sample(element_structure) for _ in range(length))
        
        elif data_type == dict:
            length = params.get('length', random.randint(1, 3))
            key_type = params.get('key_type', int)
            value_structure = params.copy()
            value_structure.pop('length', None)
            value_structure.pop('key_type', None)
            
            result = {}
            for _ in range(length):
                if key_type == int:
                    key = random.randint(0, 100)
                elif key_type == str:
                    key = ''.join(random.choices(string.ascii_lowercase, k=3))
                else:
                    key = _
                result[key] = generate_sample(value_structure)
            return result
    
    # 处理普通类型
    result = {}
    for data_type, params in structure.items():
        if data_type == 'num':
            continue  # 跳过特殊标记
        
        if data_type == int:
            min_val, max_val = params['datarange']
            value = random.randint(min_val, max_val)
            constraint = params.get('constraint', lambda x: True)
            while not constraint(value):
                value = random.randint(min_val, max_val)
            result[data_type] = value
            
        elif data_type == float:
            min_val, max_val = params['datarange']
            value = random.uniform(min_val, max_val)
            constraint = params.get('constraint', lambda x: True)
            while not constraint(value):
                value = random.uniform(min_val, max_val)
            result[data_type] = value
            
        elif data_type == str:
            char_set = params['datarange']
            length = params['len']
            value = ''.join(random.choices(char_set, k=length))
            constraint = params.get('constraint', lambda x: True)
            while not constraint(value):
                value = ''.join(random.choices(char_set, k=length))
            result[data_type] = value
            
        else:  # 嵌套结构
            result[data_type] = generate_sample(params)
    
    return result

# 在此配置需要的统计操作
OPERATIONS = ['SUM', 'AVG', 'MAX', 'MIN']

@statistics_decorator(operations=OPERATIONS)
def generate(structure):
    """
    生成器函数，根据给定结构无限生成样本数据（已添加统计装饰器）
    
    参数:
    structure (dict): 描述数据结构的字典
    
    返回:
    generator: 生成样本数据的生成器
    """
    while True:
        yield generate_sample(structure)

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
