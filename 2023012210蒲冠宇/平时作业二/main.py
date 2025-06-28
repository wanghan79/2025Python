import random
import string


def create_random_sample(struct_def):
    sample = []
    for field, spec in struct_def.items():
        if isinstance(spec, dict):
            if field in ('tuple', 'list', 'dict'):
                container = []
                for data_type, params in spec.items():
                    if data_type == 'str':
                        char_set = params.get('datarange', string.ascii_uppercase)
                        str_len = params.get('len', 10)
                        rand_str = ''.join(random.choice(char_set) for _ in range(str_len))
                        container.append(rand_str)
                    elif data_type == 'int':
                        num_range = params.get('datarange', (0, 100))
                        start, end = num_range
                        rand_int = random.randint(start, end)
                        container.append(rand_int)
                    elif data_type == 'float':
                        num_range = params.get('datarange', (0.0, 100.0))
                        start, end = num_range
                        rand_float = random.uniform(start, end)
                        container.append(rand_float)
                if field == 'tuple':
                    sample.append(tuple(container))
                elif field == 'list':
                    sample.append(container)
                elif field == 'dict':
                    dict_data = {}
                    for idx, val in enumerate(container):
                        if isinstance(val, str):
                            dict_data['str'] = val
                        elif isinstance(val, int):
                            dict_data['int'] = val
                        elif isinstance(val, float):
                            dict_data['float'] = val
                    sample.append(dict_data)
            else:
                if field == 'str':
                    char_set = spec.get('datarange', string.ascii_uppercase)
                    str_len = spec.get('len', 10)
                    rand_str = ''.join(random.choice(char_set) for _ in range(str_len))
                    sample.append(rand_str)
                elif field == 'int':
                    num_range = spec.get('datarange', (0, 100))
                    start, end = num_range
                    rand_int = random.randint(start, end)
                    sample.append(rand_int)
                elif field == 'float':
                    num_range = spec.get('datarange', (0.0, 100.0))
                    start, end = num_range
                    rand_float = random.uniform(start, end)
                    sample.append(rand_float)
        elif isinstance(spec, list):
            collection = []
            for item_spec in spec:
                if isinstance(item_spec, dict):
                    for data_type, params in item_spec.items():
                        if data_type == 'int':
                            num_range = params.get('datarange', (0, 100))
                            start, end = num_range
                            collection.append(random.randint(start, end))
                        elif data_type == 'float':
                            num_range = params.get('datarange', (0.0, 100.0))
                            start, end = num_range
                            collection.append(random.uniform(start, end))
                        elif data_type == 'str':
                            char_set = params.get('datarange', string.ascii_uppercase)
                            str_len = params.get('len', 10)
                            collection.append(''.join(random.choice(char_set) for _ in range(str_len)))
            sample.append(collection)
        else:
            sample.append(spec)
    return sample


def run_generator():
    structure = {
        'tuple': {
            'str': {'datarange': string.ascii_uppercase, 'len': 50},
            'int': {'datarange': (0, 10)},
            'float': {'datarange': (0.0, 1.0)}
        },
        'list': {
            'float': {'datarange': (0.0, 1.0)},
            'str': {'datarange': string.ascii_lowercase, 'len': 10}
        },
        'dict': {
            'str': {'datarange': string.ascii_lowercase, 'len': 10},
            'float': {'datarange': (0.0, 1.0)}
        },
        'int': {'datarange': (0, 10)},
        'float': {'datarange': (0.0, 1.0)},
        'str': {'datarange': string.ascii_letters, 'len': 20}
    }

    print("==== 随机数据生成器 ===")

    while True:
        try:
            count = int(input("请输入要生成的样本数量: "))
            if count < 1:
                print("请输入大于0的整数")
                continue
            break
        except ValueError:
            print("无效输入，请输入整数")

    print(f"\n开始生成 {count} 个随机样本...\n")

    for i in range(count):
        generated = create_random_sample(structure)
        print(f"样本 #{i + 1}:")
        print("-" * 50)
        for elem in generated:
            if isinstance(elem, tuple):
                print(f"元组: {elem}")
            elif isinstance(elem, list):
                print(f"列表: {elem}")
            elif isinstance(elem, dict):
                print(f"字典: {elem}")
            elif isinstance(elem, int):
                print(f"整数: {elem}")
            elif isinstance(elem, float):
                print(f"浮点数: {elem}")
            elif isinstance(elem, str):
                if len(elem) > 30:
                    print(f"字符串: {elem[:30]}...")
                else:
                    print(f"字符串: {elem}")
        print("-" * 50)

    print(f"\n成功生成 {count} 个样本!")


if __name__ == "__main__":
    run_generator()
