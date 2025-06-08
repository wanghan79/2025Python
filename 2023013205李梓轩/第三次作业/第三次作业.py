"""
    content:数据统计
    author:Li Zixuan
    date:2025/5/16
"""
import random
import string
from functools import wraps


# 带参修饰器，用于指定统计操作
def statistics_operations(operations):
    def decorator(func):
        @wraps(func)
        def wrapper(num_samples, struct):
            samples = []
            for _ in range(num_samples):
                sample = generate_one(struct)  # 修改这里，直接调用generate_one
                samples.append(sample)

            numeric_data = []
            for sample in samples:
                for item in sample:
                    if isinstance(item, tuple):
                        # 元组中的整数和浮点数
                        numeric_data.extend([elem for elem in item if isinstance(elem, (int, float))])
                    elif isinstance(item, list):
                        # 列表中的整数和浮点数
                        numeric_data.extend([elem for elem in item if isinstance(elem, (int, float))])
                    elif isinstance(item, dict):
                        # 字典中的整数和浮点数值
                        for value in item.values():
                            if isinstance(value, (int, float)):
                                numeric_data.append(value)
                    elif isinstance(item, (int, float)):
                        # 单独的整数或浮点数
                        numeric_data.append(item)

            print("\n" + "=" * 30 + " 统计结果 " + "=" * 30)
            if not numeric_data:
                print("没有可用的数值数据进行统计")
                return samples

            # 根据操作名称执行统计
            if 'SUM' in operations:
                print(f"总和 (SUM): {sum(numeric_data):.4f}")
            if 'AVG' in operations:
                print(f"平均值 (AVG): {sum(numeric_data) / len(numeric_data):.4f}")
            if 'MAX' in operations:
                print(f"最大值 (MAX): {max(numeric_data):.4f}")
            if 'MIN' in operations:
                print(f"最小值 (MIN): {min(numeric_data):.4f}")

            print("=" * 70)
            return samples

        return wrapper

    return decorator


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

    # 用户选择统计操作
    valid_ops = ['SUM', 'AVG', 'MAX', 'MIN']
    selected_ops = []
    print("\n请选择统计操作（输入数字选择，0结束选择）：")
    print("1: SUM（总和）")
    print("2: AVG（平均值）")
    print("3: MAX（最大值）")
    print("4: MIN（最小值）")
    print("0: 结束选择")

    while True:
        choice = input("请选择操作（输入数字）: ")
        if choice == '0':
            if not selected_ops:
                print("请至少选择一个统计操作")
                continue
            break
        elif choice == '1':
            if 'SUM' not in selected_ops:
                selected_ops.append('SUM')
                print("已添加SUM统计")
            else:
                print("SUM已添加")
        elif choice == '2':
            if 'AVG' not in selected_ops:
                selected_ops.append('AVG')
                print("已添加AVG统计")
            else:
                print("AVG已添加")
        elif choice == '3':
            if 'MAX' not in selected_ops:
                selected_ops.append('MAX')
                print("已添加MAX统计")
            else:
                print("MAX已添加")
        elif choice == '4':
            if 'MIN' not in selected_ops:
                selected_ops.append('MIN')
                print("已添加MIN统计")
            else:
                print("MIN已添加")
        else:
            print("无效选择，请输入0-4之间的数字")

    # 使用修饰器包装生成样本的函数
    decorated_generate = statistics_operations(selected_ops)(lambda n, s: [generate_one(s) for _ in range(n)])

    print(f"\n开始生成 {num} 个随机样本并进行统计...")
    samples = decorated_generate(num, struct)

    # 打印样本详情
    print(f"\n{num} 个样本的详细数据：")
    for i, sample in enumerate(samples):
        print(f"\n样本 #{i + 1}:")
        print("-" * 50)
        for item in sample:
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
        print("-" * 50)  # 缩进已修复

    print(f"\n成功生成 {num} 个样本并完成统计!")


if __name__ == "__main__":
    main()