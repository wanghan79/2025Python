import random
import string


def create_random_sample_generator(data_type, num_samples):
    """
    生成随机样本的生成器。

    Args:
        data_type (str): 数据类型，可选值为：
            - 'int'：生成随机整数
            - 'char'：生成随机单个字符
            - 'str'：生成随机字符串
            - 'float'：生成随机浮点数
        num_samples (int): 生成的样本数量

    Yields:
        随机生成的数据，类型根据data_type参数决定
    """
    if data_type == 'int':
        # 生成随机整数，默认范围为1到1000000
        min_int = 1
        max_int = 1000000
        for _ in range(num_samples):
            yield random.randint(min_int, max_int)
    elif data_type == 'char':
        # 生成随机单个字符，从所有可打印的ASCII字符中选择
        characters = string.printable
        for _ in range(num_samples):
            yield random.choice(characters)
    elif data_type == 'str':
        # 生成随机字符串，长度为5，由小写字母组成
        str_length = 5
        for _ in range(num_samples):
            yield ''.join(random.choices(string.ascii_lowercase, k=str_length))
    elif data_type == 'float':
        # 生成随机浮点数，默认范围为0.0到1.0
        min_float = 0.0
        max_float = 1.0
        for _ in range(num_samples):
            yield random.uniform(min_float, max_float)
    else:
        raise ValueError(f"不支持的数据类型：{data_type}")


def generate_data(data_type, num_samples, **kwargs):
    """
    输出全部的数据，但测试的样本量太大没选择使用
    """
    generator = create_random_sample_generator(data_type, num_samples, **kwargs)
    data = []
    for item in generator:
        data.append(item)
    return data


if __name__ == "__main__":
    print("生成10000000个随机整数：")
    int_generator = create_random_sample_generator('int', 10000000)
    # 由于生成数量较大，这里仅打印前5个样本
    for i, num in enumerate(int_generator):
        if i >= 5:
            break
        print(num)

    print("\n生成45678个随机字符：")
    char_generator = create_random_sample_generator('char', 45678)
    # 打印前10个样本
    for i, char in enumerate(char_generator):
        if i >= 10:
            break
        print(char, end=' ')
    print()

    print("\n生成500个随机字符串：")
    str_generator = create_random_sample_generator('str', 500)
    # 打印前5个样本
    for i, s in enumerate(str_generator):
        if i >= 5:
            break
        print(s)

    print("\n生成100个随机浮点数：")
    float_generator = create_random_sample_generator('float', 100)
    # 打印前5个样本
    for i, f in enumerate(float_generator):
        if i >= 5:
            break
        print(f)