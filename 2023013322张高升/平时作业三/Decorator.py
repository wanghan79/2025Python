"""
@Author: Zhang Gaosheng
@Version: 1.0
@Description: 使用带参修饰器实现对随机样本生成函数的统计操作修饰，能够实现 
              SUM、AVG、MAX、MIN 四种统计操作的任意组合进行统计结果输出。
"""

###################################################################################
##
##  Import
##
###################################################################################

import random

###################################################################################
##
##  Functions
##
###################################################################################

def gen_str(data):
    """
    从 指定字符串 中随机生成 指定长度 的字符串
    """
    return ''.join(random.choices(data['datarange'], k=data['len']))

def gen_int(data):
    """
    从 随机数 范围 中生成 随机 int 数
    """
    return random.randint(data['datarange'][0], data['datarange'][1])

def gen_float(data):
    """
    从 随机数 范围 中生成 随机浮点数
    """
    return random.uniform(data['datarange'][0], data['datarange'][1])

def gen_list(data):
    """
    生成 列表
    """
    return [generate_sample({k: v}) for k, v in data.items()]

def gen_dict(data):
    """
    生成 字典
    """
    return {k: generate_sample({k: v}) for k, v in data.items()}

def gen_tuple(data):
    """
    生成 元组
    """
    return tuple(generate_sample({k: v}) for k, v in data.items())

"""
建立一个 将类型名称映射到相应的生成函数 的字典
"""
TYPE_TO_FUNC = {
    'str': gen_str,
    'int': gen_int,
    'float': gen_float,
    'list': gen_list,
    'dict': gen_dict,
    'tuple': gen_tuple,
} # 可以扩展新的生成函数

def extract_int(data):
    """
    提取出生成数据中的数值型数据
    """
    int_values = []

    # 1. 若是列表、元组、集合，则遍历元素递归调用本函数
    if isinstance(data, (list, tuple, set)):
        for item in data:
            int_values.extend(extract_int(item))

    # 2. 若是字典，则遍历字典的元素的 value 递归调用本函数
    elif isinstance(data, dict):
        for key, value in data.items():
            int_values.extend(extract_int(value))

    # 3. 若是数值型数据，则直接添加到结果列表中
    elif isinstance(data, int) or isinstance(data, float):
        int_values.append(data)
    return int_values

def StaticsResInt(**vargs):
    """
    装饰器函数，用于统计数值型数据
    统计 均值、中位数、众数、方差、标准差
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 1. 获取统计方法列表，支持多种统计方法
            method_list = vargs.get('name', [])
            
            # 2. 生成随机样本
            count = 0
            result = []
            for item in func(*args, **kwargs): # 调用 func 生成样本
                print(item)
                result.append(item)
                count += 1
            print(f"\nGenerated and printed {count} samples.\n")
            
            if not result:
                return None
            
            # 3. 提取出数值型数据
            int_values = []
            for item in result:
                int_values.extend(extract_int(item))
            
            if not int_values:
                return None
            
            # 4. 计算统计数据
            statics = []
            for stats_method in method_list:
                if stats_method == 'SUM':
                    statics.append(('SUM', sum(int_values)))
                elif stats_method == 'AVG':
                    statics.append(('AVG', sum(int_values) / len(int_values)))
                elif stats_method == 'VAR':
                    statics.append(('VAR', sum((x - sum(int_values) / len(int_values)) ** 2 
                                               for x in int_values) / len(int_values)))
                elif stats_method == 'RMSE':
                    statics.append(('RMSE', (sum((x - sum(int_values) / len(int_values)) ** 2 
                                                 for x in int_values) / len(int_values)) ** 0.5))
                else:
                    raise ValueError("Unsupported statistics method") # 不支持的统计方法
            return statics
        return wrapper
    return decorator

def generate_sample(struct):
    """
    生成指定结构配置的随机样本。
    """
    if len(struct) != 1:
        raise ValueError(f"结构配置必须包含且仅包含一个类型键：{struct}")
    type_name, data = next(iter(struct.items()))
    if type_name not in TYPE_TO_FUNC:
        raise ValueError(f"不支持的类型：'{type_name}'")
    return TYPE_TO_FUNC[type_name](data)    


@StaticsResInt(name=['SUM', 'AVG', 'VAR', 'RMSE']) # 装饰器
def random_sampler(**kwargs):
    """
    随机数生成器
    """
    number = kwargs.pop('number', 1)
    for _ in range(number):
        yield generate_sample(kwargs)

###################################################################################
##
##  Main
##
###################################################################################

if __name__ == '__main__':
    example = {
        'number': 10,
        'tuple': {
            'str': {
                'datarange': 'abcdefghijklmnopqrstuvwxyz', 
                'len': 8
            },
            'list': {
                'int': {
                    'datarange': [1, 10]
                }, 
                'float': {
                    'datarange': [1, 10]
                }
            },
            'dict': {
                'int': {
                    'datarange': [1, 10]
                }
            }
        }
    }

    result = random_sampler(**example)
    for static_method, data in result:
        print(f"The {static_method} of the integer: {data}")

    
'''
更加复杂的结构配置
将 example 进行替换即可

example = {
    'number': 3,
    'tuple': {
        'str': {
            'datarange': 'qwertyuiop', 
            'len': 8
        },
        'list': {
            'int': {
                'datarange': [1, 10]
            }, 
            'float': {
                'datarange': [1, 10]
            }
        },
        'dict': {
            'int': {
                'datarange': [1, 10]
            }
        },
        'float': {
            'datarange': [1, 10]
        },
        'tuple': {
            'str': {
                'datarange': 'qwertyuiop', 
                'len': 8
            },
            'dict': {
                'int': {
                    'datarange': [1, 10]
                },
                'tuple': {
                    'str': {
                        'datarange': 'qwertyuiop', 
                        'len': 8
                    },
                    'list': {
                        'int': {
                            'datarange': [1, 10]
                        },
                        'tuple': {
                            'str': {
                                'datarange': 'qwertyuiop', 
                                'len': 8
                            },
                        }
                    }
                }
            }
        }
    }
}
'''