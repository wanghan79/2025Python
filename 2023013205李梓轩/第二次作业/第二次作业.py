"""
    content:使用生成器生成随机样本
    author:Li Zixuan
    date:2025/5/8
"""
import random
import string


def generate_one(struct):
    """生成一个随机样本"""
    root = []
    for key, value in struct.items():
        if isinstance(value, dict):
            if key in ['tuple', 'list', 'dict']:
                container = []
                for k, v in value.items():
                    if k == 'str':
                        datarange = v.get('datarange', string.ascii_uppercase)
                        length = v.get('len', 10)
                        tmp = ''.join(random.choice(datarange) for _ in range(length))
                        container.append(tmp)
                    elif k == 'int':
                        datarange = v.get('datarange', (0, 100))
                        it = iter(datarange)
                        container.append(random.randint(next(it), next(it)))
                    elif k == 'float':
                        datarange = v.get('datarange', (0.0, 100.0))
                        it = iter(datarange)
                        container.append(random.uniform(next(it), next(it)))
                if key == 'tuple':
                    root.append(tuple(container))
                elif key == 'list':
                    root.append(container)
                elif key == 'dict':
                    dict_data = {}
                    for idx, item in enumerate(container):
                        if isinstance(item, str):
                            dict_data['str'] = item
                        elif isinstance(item, int):
                            dict_data['int'] = item
                        elif isinstance(item, float):
                            dict_data['float'] = item
                    root.append(dict_data)
            else:
                if key == 'str':
                    datarange = value.get('datarange', string.ascii_uppercase)
                    length = value.get('len', 10)
                    tmp = ''.join(random.choice(datarange) for _ in range(length))
                    root.append(tmp)
                elif key == 'int':
                    datarange = value.get('datarange', (0, 100))
                    it = iter(datarange)
                    root.append(random.randint(next(it), next(it)))
                elif key == 'float':
                    datarange = value.get('datarange', (0.0, 100.0))
                    it = iter(datarange)
                    root.append(random.uniform(next(it), next(it)))
        elif isinstance(value, list):
            container = []
            for item in value:
                if isinstance(item, dict):
                    for k, v in item.items():
                        if k == 'int':
                            datarange = v.get('datarange', (0, 100))
                            it = iter(datarange)
                            container.append(random.randint(next(it), next(it)))
                        elif k == 'float':
                            datarange = v.get('datarange', (0.0, 100.0))
                            it = iter(datarange)
                            container.append(random.uniform(next(it), next(it)))
                        elif k == 'str':
                            datarange = v.get('datarange', string.ascii_uppercase)
                            length = v.get('len', 10)
                            tmp = ''.join(random.choice(datarange) for _ in range(length))
                            container.append(tmp)
            root.append(container)
        else:
            root.append(value)
    return root


def main():
    # 固定数据结构定义
    struct = {
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

    print("==== 随机数据生成器 =====")

    while True:
        try:
            num = int(input("请输入要生成的样本数量: "))
            if num < 1:
                print("请输入大于0的整数")
                continue
            break
        except ValueError:
            print("无效输入，请输入整数")

    print(f"\n开始生成 {num} 个随机样本...\n")

    for i in range(num):
        data = generate_one(struct)
        print(f"样本 #{i + 1}:")
        print("-" * 50)
        for item in data:
            if isinstance(item, tuple):
                print(f"元组: {item}")
            elif isinstance(item, list):
                print(f"列表: {item}")
            elif isinstance(item, dict):
                print(f"字典: {item}")
            elif isinstance(item, int):
                print(f"整数: {item}")
            elif isinstance(item, float):
                print(f"浮点数: {item}")
            elif isinstance(item, str):
                if len(item) > 30:
                    print(f"字符串: {item[:30]}...")
                else:
                    print(f"字符串: {item}")
        print("-" * 50)

    print(f"\n成功生成 {num} 个样本!")


if __name__ == "__main__":
    main()