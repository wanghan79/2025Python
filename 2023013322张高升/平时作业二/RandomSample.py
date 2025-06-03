"""
@Author: Zhang Gaosheng
@Version: 1.0
@Description: 使用生成器生成随机样本，配套生成器使用范例代码，随机样本的数量和结构由调用者输入。
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


def random_sampler(**kwargs):
    """
    随机数生成器
    """
    number = kwargs.pop('number', 1)
    for _ in range(number):
        yield generate_sample(kwargs) # 使用生成器

###################################################################################
##
##  Main
##
###################################################################################

if __name__ == '__main__':
    example = {
        'number': 100000000, # 设置一个较大的数量
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

    
    count = 0
    for item in random_sampler(**example): # 返回的是生成器，需要用 for 循环迭代
        print(item)
        count += 1
    print(f"\nGenerated and printed {count} samples.")


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