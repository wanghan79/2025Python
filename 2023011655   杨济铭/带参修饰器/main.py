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


def statistical_decorator(statistics):
    def decorator(func):
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            results = {}

            # 执行统计操作
            if 'SUM' in statistics:
                results['SUM'] = sum(data)
            if 'AVG' in statistics:
                results['AVG'] = sum(data) / len(data)
            if 'MAX' in statistics:
                results['MAX'] = max(data)
            if 'MIN' in statistics:
                results['MIN'] = min(data)

            # 打印统计结果
            print("\n统计结果：")
            for stat, value in results.items():
                print(f"{stat}: {value}")

            return data

        return wrapper

    return decorator


@statistical_decorator(['SUM', 'AVG', 'MAX', 'MIN'])
def generate_data(data_type, num_samples, **kwargs):
    generator = create_random_sample_generator(data_type, num_samples, **kwargs)
    data = []
    for item in generator:
        data.append(item)
    return data


if __name__ == "__main__":
    # 示例1：生成10000000个随机整数，并执行统计操作
    int_data = generate_data('int', 10000000)
    print("生成的整数数量：", len(int_data))
    print("前5个整数：", int_data[:5])

    # 示例2：生成45678个随机字符，并执行统计操作
    char_data = generate_data('char', 45678)
    print("\n生成的字符数量：", len(char_data))
    print("前10个字符：", char_data[:10])

    # 示例3：生成500个随机字符串，长度为10，并执行统计操作
    str_data = generate_data('str', 500, str_length=10)
    print("\n生成的字符串数量：", len(str_data))
    print("前5个字符串：", str_data[:5])

    # 示例4：生成100个随机浮点数，范围为-10.0到10.0，并执行统计操作
    float_data = generate_data('float', 100, min_float=-10.0, max_float=10.0)
    print("\n生成的浮点数数量：", len(float_data))
    print("前5个浮点数：", float_data[:5])