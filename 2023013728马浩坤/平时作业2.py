import random

def gen_str(data):
    return ''.join(random.choices(data['datarange'], k=data['len']))

def gen_int(data):
    return random.randint(data['datarange'][0], data['datarange'][1])

def gen_float(data):
    return random.uniform(data['datarange'][0], data['datarange'][1])

def gen_list(data):
    return [generate_sample({k: v}) for k, v in data.items()]

def gen_dict(data):
    return {k: generate_sample({k: v}) for k, v in data.items()}

def gen_tuple(data):
    return tuple(generate_sample({k: v}) for k, v in data.items())

TYPE_TO_FUNC = {
    'str': gen_str,
    'int': gen_int,
    'float': gen_float,
    'list': gen_list,
    'dict': gen_dict,
    'tuple': gen_tuple,
}

def generate_sample(struct):
    if len(struct) != 1:
        raise ValueError(f"结构配置必须包含且仅包含一个类型键：{struct}")
    type_name, data = next(iter(struct.items()))
    if type_name not in TYPE_TO_FUNC:
        raise ValueError(f"不支持的类型是：'{type_name}'")
    return TYPE_TO_FUNC[type_name](data)

def random_sampler(**kwargs):
    number = kwargs.pop('number', 1)
    for _ in range(number):
        yield generate_sample(kwargs)

if __name__ == '__main__':
    example = {
        'number': 100000000,
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
    for item in random_sampler(**example):
        print(item)
        count += 1
    print(f"\nGenerated and printed {count} samples.")

'''
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