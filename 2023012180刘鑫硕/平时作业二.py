
"""
@Author: 刘鑫硕
@File:生成随机样本
"""

import random
import string

def generator_sample(structure):
    """
    递归生成符合结构规范的样本数据
    
    参数:
    structure (dict): 描述数据结构的字典
    
    返回:
    根据structure生成的样本数据
    """
    # 基本类型直接返回（递归终止条件）
    if not isinstance(structure, dict):
        return structure
    
    # 处理容器类型（列表、元组、字典）
    if len(structure) == 1:
        container_type = next(iter(structure))
        container_spec = structure[container_type]
        
        if container_type == list:
            length = container_spec.get('length', random.randint(1, 5))
            element_spec = container_spec.copy()
            element_spec.pop('length', None)
            return [generator_sample(element_spec) for _ in range(length)]
        
        elif container_type == tuple:
            length = container_spec.get('length', random.randint(1, 5))
            element_spec = container_spec.copy()
            element_spec.pop('length', None)
            return tuple(generator_sample(element_spec) for _ in range(length))
        
        elif container_type == dict:
            length = container_spec.get('length', random.randint(1, 3))
            key_type = container_spec.get('key_type', int)  # 默认使用整数作为键
            value_spec = container_spec.copy()
            value_spec.pop('length', None)
            value_spec.pop('key_type', None)
            
            result = {}
            for _ in range(length):
                if key_type == int:
                    key = random.randint(0, 100)
                elif key_type == str:
                    key = ''.join(random.choices(string.ascii_lowercase, k=3))
                else:
                    key = _  # 默认使用索引作为键
                result[key] = generator_sample(value_spec)
            return result
    
    # 处理普通类型字段
    result = []
    for data_type, spec in structure.items():
        # 跳过特殊标记
        if data_type == 'num':
            continue
        
        constraint = spec.get('constraint', lambda x: True)
        max_attempts = 100  # 最大尝试次数，防止无限循环
        
        if data_type == int:
            min_val, max_val = spec['datarange']
            for _ in range(max_attempts):
                value = random.randint(min_val, max_val)
                if constraint(value):
                    result.append(value)
                    break
            else:
                # 尝试多次仍无法满足约束，使用默认值
                result.append(min_val)
                
        elif data_type == float:
            min_val, max_val = spec['datarange']
            for _ in range(max_attempts):
                value = random.uniform(min_val, max_val)
                if constraint(value):
                    result.append(value)
                    break
            else:
                result.append(min_val)
                
        elif data_type == str:
            char_set = spec['datarange']
            length = spec['len']
            for _ in range(max_attempts):
                value = ''.join(random.choices(char_set, k=length))
                if constraint(value):
                    result.append(value)
                    break
            else:
                # 生成一个满足最低要求的字符串
                value = ''.join(random.choices(char_set, k=length-1)) + random.choice(char_set)
                result.append(value)
                
        else:  # 嵌套结构，递归处理
            nested_value = generator_sample(spec)
            result.append(nested_value)
    
    return result

def generate(structure):
    """
    生成器函数，根据给定结构无限生成样本数据
    
    参数:
    structure (dict): 描述数据结构的字典
    
    返回:
    generator: 生成样本数据的生成器
    """
    while True:
        yield generator_sample(structure)

def main():
    """
    主函数：定义数据结构并生成10000个样本数据
    """
    # 定义复杂嵌套的数据结构规范
    struct = {
        tuple: {
            int: {
                'datarange': (-1000, 1000),
                'constraint': lambda x: x % 2 == 0  # 约束条件：偶数
            },
            float: {
                'datarange': (-100.0, 100.0),
                'constraint': lambda x: x > 0  # 约束条件：正数
            },
            str: {
                'datarange': string.ascii_letters + string.digits + string.punctuation,
                'len': 10,
                'constraint': lambda s: any(c.isdigit() for c in s)  # 约束条件：包含数字
            },
            list: {
                tuple: {
                    dict: {
                        int: {
                            'datarange': (0, 20),
                            'constraint': lambda x: x > 5  # 约束条件：大于5
                        },
                        str: {
                            'datarange': string.ascii_lowercase,
                            'len': 3,
                            'constraint': lambda s: s[0] in 'aeiou'  # 约束条件：首字母为元音
                        }
                    },
                    float: {
                        'datarange': (0.1, 10.0),
                        'constraint': lambda x: x < 5.0  # 约束条件：小于5.0
                    }
                },
                'length': 3  # 列表长度
            },
            dict: {
                str: {
                    'datarange': string.ascii_uppercase,
                    'len': 5,
                    'constraint': lambda s: s.isupper()  # 约束条件：全大写字母
                },
                list: {
                    int: {
                        'datarange': (1, 100),
                        'constraint': lambda x: x % 3 == 0  # 约束条件：能被3整除
                    },
                    'length': 5  # 列表长度
                }
            }
        }
    }
    
    # 创建样本生成器
    sample_generator = generate(struct)
    
    # 生成并打印10000个样本
    count = 0
    for sample in sample_generator:
        print(f"样本 {count+1}: {sample}")
        count += 1
        if count >= 10000:
            break

if __name__ == "__main__":
    main()
