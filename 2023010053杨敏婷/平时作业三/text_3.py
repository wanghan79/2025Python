import random
import string
from collections import defaultdict

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
    num_instances = args[1] if len(args) > 1 else kwargs.get("num_instances", 1)

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


"""修饰器函数"""
def StatisticsRes(*stats_types):
    all_stats_types = [ 'SUM', 'AVG','MAX', 'MIN']
    stats_types = [stat for stat in stats_types if stat in all_stats_types]

    def decorator(func):
        def wrapper(*func_args, **func_kwargs):
            data = list(func(*func_args, **func_kwargs))
            stats_result = defaultdict(lambda: defaultdict(list))

            for result in data:
                for key, value in result.items():
                    if key == 'list':
                        for sub_key, sub_list in value.items():
                            for stat in stats_types:
                                if stat =='SUM':
                                    stats_result[sub_key][stat].append(sum(sub_list))
                                elif stat == 'AVG':
                                    stats_result[sub_key][stat].append(sum(sub_list) / len(sub_list))
                                elif stat == 'MAX':
                                    stats_result[sub_key][stat].append(max(sub_list))
                                elif stat == 'MIN':
                                    stats_result[sub_key][stat].append(min(sub_list))


            final_result = {}
            for key, stats in stats_result.items():
                final_result[key] = {}
                for stat in stats_types:
                    if stat == 'SUM':
                        final_result[key][stat] = sum(stats[stat])
                    elif stat == 'AVG':
                        final_result[key][stat] = sum(stats[stat]) / len(stats[stat])
                    elif stat == 'MAX':
                        final_result[key][stat] = max(stats[stat])
                    elif stat == 'MIN':
                        final_result[key][stat] = min(stats[stat])

            return data, final_result
        return wrapper
    return decorator


"""给定的结构描述"""
struct = {
    'num': 10,
    'tuple': {
        'str': {
            'datarange': string.ascii_uppercase,
            'len': 50
        }
    },
    'list': {
        'int': {
            'datarange': (0, 10),
            'len': 1
        },
        'float': {
            'datarange': (0, 10000),
            'len': 1
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

#指定需要计算的统计类型
@StatisticsRes('SUM','AVG','MAX','MIN' )
def dataSamplingWithStats(struct, num_instances):
    return dataSampling(struct, num_instances)

# 生成数据实例
num = struct['num']
all_data, all_results = dataSamplingWithStats(struct, num)

# 打印生成的数据
for counter, data in enumerate(all_data, start=1):
    print(f"Data {counter}: {data}")
    if counter >= num:
        break

print("Statistics Result:", all_results)