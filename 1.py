"""
简化版随机样本生成器


"""

import random

def generate_sample(config):
    """
    根据配置生成随机样本

    参数:
        config: 描述要生成数据结构的字典

    返回:
        随机生成的样本数据
    """
    # 基本类型生成
    if config.get('type') == 'int':
        return random.randint(config['min'], config['max'])

    elif config.get('type') == 'float':
        return round(random.uniform(config['min'], config['max']), config.get('decimal', 2))

    elif config.get('type') == 'str':
        chars = config.get('chars', 'abcdefghijklmnopqrstuvwxyz0123456789')
        length = config.get('length', 8)
        return ''.join(random.choices(chars, k=length))

    elif config.get('type') == 'bool':
        return random.choice([True, False])

    # 容器类型生成
    elif config.get('type') == 'list':
        length = config.get('length', random.randint(1, 5))
        return [generate_sample(config['element']) for _ in range(length)]

    elif config.get('type') == 'dict':
        return {key: generate_sample(value_config) for key, value_config in config['fields'].items()}

    elif config.get('type') == 'tuple':
        return tuple(generate_sample(element) for element in config['elements'])

    else:
        raise ValueError(f"不支持的类型: {config.get('type')}")


def generate_samples(count, config):
    """
    生成多个样本

    参数:
        count: 要生成的样本数量
        config: 描述样本结构的配置

    返回:
        包含所有样本的列表
    """
    return [generate_sample(config) for _ in range(count)]


def print_samples(samples, max_display=5):
    """
    打印样本

    参数:
        samples: 样本列表
        max_display: 最大显示数量
    """
    print(f"\n生成了 {len(samples)} 个样本:")

    if len(samples) <= max_display:
        for i, sample in enumerate(samples):
            print(f"样本 {i+1}: {sample}")
    else:
        for i in range(max_display):
            print(f"样本 {i+1}: {samples[i]}")
        print(f"... 和另外 {len(samples) - max_display} 个样本")


def test_generator():
    """测试生成器功能"""
    print("随机样本生成器测试")
    print("=" * 50)

    while True:
        print("\n请选择测试类型:")
        print("1: 生成随机整数")
        print("2: 生成随机浮点数")
        print("3: 生成随机字符串")
        print("4: 生成随机布尔值")
        print("5: 生成列表")
        print("6: 生成字典")
        print("7: 生成元组")
        print("8: 生成嵌套结构")
        print("9: 退出测试")

        choice = input("请输入选项 (1-9): ")

        if choice == '9':
            print("\n测试结束!")
            break

        count = int(input("请输入要生成的样本数量: "))

        if choice == '1':
            # 整数测试
            min_val = int(input("最小值: "))
            max_val = int(input("最大值: "))
            config = {'type': 'int', 'min': min_val, 'max': max_val}

        elif choice == '2':
            # 浮点数测试
            min_val = float(input("最小值: "))
            max_val = float(input("最大值: "))
            decimal = int(input("小数位数 (默认为2): ") or 2)
            config = {'type': 'float', 'min': min_val, 'max': max_val, 'decimal': decimal}

        elif choice == '3':
            # 字符串测试
            chars = input("字符集 (默认为a-z0-9): ") or 'abcdefghijklmnopqrstuvwxyz0123456789'
            length = int(input("长度 (默认为8): ") or 8)
            config = {'type': 'str', 'chars': chars, 'length': length}

        elif choice == '4':
            # 布尔值测试
            config = {'type': 'bool'}

        elif choice == '5':
            # 列表测试
            print("\n配置列表元素:")
            element_type = input("元素类型 (int/float/str/bool): ")
            if element_type == 'int':
                min_val = int(input("最小值: "))
                max_val = int(input("最大值: "))
                element_config = {'type': 'int', 'min': min_val, 'max': max_val}
            elif element_type == 'float':
                min_val = float(input("最小值: "))
                max_val = float(input("最大值: "))
                element_config = {'type': 'float', 'min': min_val, 'max': max_val}
            elif element_type == 'str':
                chars = input("字符集 (默认为a-z0-9): ") or 'abcdefghijklmnopqrstuvwxyz0123456789'
                length = int(input("长度 (默认为8): ") or 8)  # 修复了这里
                element_config = {'type': 'str', 'chars': chars, 'length': length}
            elif element_type == 'bool':
                element_config = {'type': 'bool'}
            else:
                print("无效的元素类型!")
                continue

            list_length = int(input("列表长度 (默认为3): ") or 3)  # 修复了这里
            config = {'type': 'list', 'element': element_config, 'length': list_length}

        elif choice == '6':
            # 字典测试
            fields = {}
            print("\n添加字典字段 (输入q完成):")
            while True:
                key = input("字段名称: ")
                if key == 'q':
                    break

                field_type = input(f"{key} 类型 (int/float/str/bool): ")
                if field_type == 'int':
                    min_val = int(input(f"{key} 最小值: "))
                    max_val = int(input(f"{key} 最大值: "))
                    fields[key] = {'type': 'int', 'min': min_val, 'max': max_val}
                elif field_type == 'float':
                    min_val = float(input(f"{key} 最小值: "))
                    max_val = float(input(f"{key} 最大值: "))
                    fields[key] = {'type': 'float', 'min': min_val, 'max': max_val}
                elif field_type == 'str':
                    chars = input(f"{key} 字符集 (默认为a-z0-9): ") or 'abcdefghijklmnopqrstuvwxyz0123456789'
                    length = int(input(f"{key} 长度 (默认为8): ") or 8)  # 修复了这里
                    fields[key] = {'type': 'str', 'chars': chars, 'length': length}
                elif field_type == 'bool':
                    fields[key] = {'type': 'bool'}
                else:
                    print("无效的类型!")

            config = {'type': 'dict', 'fields': fields}

        elif choice == '7':
            # 元组测试
            elements = []
            print("\n添加元组元素 (输入q完成):")
            i = 1
            while True:
                element_type = input(f"元素 {i} 类型 (int/float/str/bool): ")
                if element_type == 'q':
                    break

                if element_type == 'int':
                    min_val = int(input(f"元素 {i} 最小值: "))
                    max_val = int(input(f"元素 {i} 最大值: "))
                    elements.append({'type': 'int', 'min': min_val, 'max': max_val})
                elif element_type == 'float':
                    min_val = float(input(f"元素 {i} 最小值: "))
                    max_val = float(input(f"元素 {i} 最大值: "))
                    elements.append({'type': 'float', 'min': min_val, 'max': max_val})
                elif element_type == 'str':
                    chars = input(f"元素 {i} 字符集 (默认为a-z0-9): ") or 'abcdefghijklmnopqrstuvwxyz0123456789'
                    length = int(input(f"元素 {i} 长度 (默认为8): ") or 8)  # 修复了这里
                    elements.append({'type': 'str', 'chars': chars, 'length': length})
                elif element_type == 'bool':
                    elements.append({'type': 'bool'})
                else:
                    print("无效的类型!")
                    continue

                i += 1

            config = {'type': 'tuple', 'elements': elements}

        elif choice == '8':
            # 嵌套结构测试
            print("创建一个嵌套结构（例如字典中包含列表）")
            # 这里创建了一个用户信息结构
            config = {
                'type': 'dict',
                'fields': {
                    'id': {'type': 'int', 'min': 1000, 'max': 9999},
                    'name': {'type': 'str', 'chars': 'abcdefghijklmnopqrstuvwxyz', 'length': 6},
                    'active': {'type': 'bool'},
                    'scores': {
                        'type': 'list',
                        'element': {'type': 'float', 'min': 0.0, 'max': 100.0},
                        'length': 3
                    },
                    'metadata': {
                        'type': 'tuple',
                        'elements': [
                            {'type': 'str', 'chars': 'XYZ', 'length': 3},
                            {'type': 'int', 'min': 1, 'max': 10}
                        ]
                    }
                }
            }
            print("使用预定义的用户信息结构配置")

        else:
            print("无效的选项!")
            continue

        # 生成并显示样本
        samples = generate_samples(count, config)
        print_samples(samples)


if __name__ == '__main__':
    test_generator()
