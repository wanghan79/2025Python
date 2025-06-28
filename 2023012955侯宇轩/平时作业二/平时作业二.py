import random
import string

"""生成随机字符串"""
def generate_random_string(datarange, length):
    return ''.join(random.choices(datarange, k=length))


"""生成随机列表"""
def generate_random_list(data_type, datarange, length):
    if data_type == int:
        return [random.randint(datarange[0], datarange[1]) for _ in range(length)]
    elif data_type == float:
        return [random.uniform(datarange[0], datarange[1]) for _ in range(length)]

"""动态生成随机字典"""
def generate_random_dict(struct):
    data = {}
    for key, value in struct.items():
        data_type = value.get('type', 'str')  # 默认为字符串类型
        if data_type == 'int':
            data[key] = random.randint(value['datarange'][0], value['datarange'][1])
        elif data_type == 'float':
            data[key] = random.uniform(value['datarange'][0], value['datarange'][1])
        elif data_type == 'str':
            data[key] = generate_random_string(value['datarange'], value['len'])
        elif data_type == 'list':
            data[key] = generate_random_list(
                eval(value['subtype']), value['datarange'], value.get('len', 10)
            )
        elif data_type == 'dict':
            data[key] = generate_random_dict(value['subdict'])
    return data

"""根据给定的结构描述生成单个数据实例"""
def dataSampling(*args, **kwargs):
    struct = args[0] if args else kwargs.get("struct")
    num_instances = args[1] if len(args) > 1 else kwargs.get("num_instances",1)

    def generator():
        for _ in range(num_instances):
            data = {}
            for key, value in struct.items():
                if key == 'num':
                    continue
                elif key == 'tuple':
                    data[key] = generate_random_string(value['str']['datarange'], value['str']['len'])
                elif key == 'list':
                    data[key] = {}
                    for list_key, list_value in value.items():
                        # 将字符串 'int' 或 'float' 转换为实际的数据类型
                        if list_key == 'int':
                            data_type = int
                        elif list_key == 'float':
                            data_type = float
                        data[key][list_key] = generate_random_list(
                            data_type, list_value['datarange'], list_value.get('len', 10)
                        )
                elif key == 'dict':
                    data[key] = generate_random_dict(value)
            yield data

    return generator()



"""给定的结构描述"""
struct = {
    'num': 100,
    'tuple': {
        'str': {
            'datarange': string.ascii_uppercase,
            'len': 50
        }
    },
    'list': {
        'int': {
            'datarange': (0, 10),
            'len':1
        },
        'float': {
            'datarange': (0, 10000),
            'len':1
        }
    },
    'dict': {
        'key1': {
            'type': 'int',
            'datarange': (0, 100)
        },
        'key2': {
            'type': 'str',
            'datarange': string.ascii_letters,
            'len': 10
        }
    }
}


"""生成100个数据实例"""
num = struct['num']  # 获取需要生成的实例数量
generator = dataSampling(struct, num)

for counter, data in enumerate(generator, start=1):
    print(f"Data {counter}: {data}")
    if counter >= num:
        break