"""
@Author: Weizhi Wang
@Date: 2025-05-20
@Description: 使用生成器生成随机样本，配套生成器使用范例代码，随机样本的数量和结构由调用者输入。
"""

import random
import string

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
        # 跳过总数量控制参数
        if k == 'num':
            continue
        # 生成整数类型数据
        elif k is int:
            it = iter(v['datarange'])
            res.append(random.randint(next(it), next(it)))
        # 生成浮点数类型数据
        elif k is float:
            it = iter(v['datarange'])
            res.append(random.uniform(next(it), next(it)))
        # 生成字符串类型数据
        elif k is str:
            datarange, length = v['datarange'], v['len']
            tmp = ''.join(random.SystemRandom().choice(datarange) for _ in range(length))
            res.append(tmp)
        # 生成字典类型数据（固定结构：随机整数键值对）
        elif k is dict:
            elem = dict()
            elem[random.randint(0, 10)] = random.randint(0, 10)
            res.append(elem)
        # 生成列表类型数据（递归调用）
        elif k is list:
            res.append(generator_sample(v))
        # 生成元组类型数据（递归调用并转换为元组）
        elif k is tuple:
            res.append(tuple(generator_sample(v)))
        else:
            continue
    return res

def generate(kwargs):
    """
    生成器函数，根据给定结构无限生成样本数据
    
    参数:
    kwargs (dict): 描述数据结构的字典
    
    返回:
    generator: 生成样本数据的生成器
    """
    while True:
        yield generator_sample(kwargs)

def main():
    """
    主函数：定义数据结构并生成100个样本数据
    """
    # 定义复杂嵌套的数据结构规范
    struct = {
        # 'num': 300,  # 未使用的总数量控制参数
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
        print(sample)
        count += 1
        if count >= 10000:
            break

if __name__ == "__main__":
    main()
