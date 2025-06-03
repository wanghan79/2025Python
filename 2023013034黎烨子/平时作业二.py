import random


def random_sample_generator(sample_count, sample_structure):
    """
    随机样本生成器
    参数:
        sample_count: 生成样本的数量
        sample_structure: 样本结构，字典形式，如 {'int': (1, 100), 'float': (0.0, 1.0), 'str': 5}
                         'int'表示生成整数，(min, max)范围
                         'float'表示生成浮点数，(min, max)范围
                         'str'表示生成长度为n的随机字符串
    """
    for _ in range(sample_count):
        sample = {}
        for key, value in sample_structure.items():
            if key == 'int':
                sample['int'] = random.randint(value[0], value[1])
            elif key == 'float':
                sample['float'] = random.uniform(value[0], value[1])
            elif key == 'str':
                length = value
                sample['str'] = ''.join(
                    random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=length))
        yield sample


# 示例使用
if __name__ == "__main__":
    # 定义样本结构: 包含一个整数(1-100), 一个浮点数(0.0-1.0), 一个5字符的字符串
    sample_structure = {
        'int': (1, 100),
        'float': (0.0, 1.0),
        'str': 5
    }

    # 生成10个样本
    generator = random_sample_generator(10, sample_structure)

    print("生成的随机样本:")
    for i, sample in enumerate(generator, 1):
        print(f"样本{i}: {sample}")