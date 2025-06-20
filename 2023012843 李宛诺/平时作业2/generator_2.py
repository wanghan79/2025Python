# 作业二：随机样本生成器
import random
import string

def random_data_generator(config):

    count = config.get('count', 1)

    for _ in range(count):
        sample = {}
        for field_name, field_config in config.items():
            if field_name == 'count':
                continue

            data_type = field_config['type']

            if data_type == 'int':
                sample[field_name] = random.randint(field_config['min'], field_config['max'])
            elif data_type == 'float':
                sample[field_name] = random.uniform(field_config['min'], field_config['max'])
            elif data_type == 'str':
                length = field_config['length']
                chars = field_config.get('chars', string.ascii_letters)
                sample[field_name] = ''.join(random.choice(chars) for _ in range(length))
            elif data_type == 'list':
                size = field_config['size']
                min_val = field_config['min']
                max_val = field_config['max']
                sample[field_name] = [random.randint(min_val, max_val) for _ in range(size)]

        yield sample

def print_samples(samples):
    print(f"共生成 {len(samples)} 个样本:")
    for i, sample in enumerate(samples, 1):
        print(f"  样本{i}: {sample}")


if __name__ == "__main__":
    print("=== 随机样本生成器测试 ===")

    # 测试配置1：学生信息生成
    config1 = {
        'count': 5,
        'score': {'type': 'int', 'min': 70, 'max': 100},
        'rate': {'type': 'float', 'min': 0.8, 'max': 1.0},
        'name': {'type': 'str', 'length': 5},
        'grades': {'type': 'list', 'size': 3, 'min': 80, 'max': 95}
    }

    print("配置1 - 学生信息:")
    print(f"配置: {config1}")
    samples1 = list(random_data_generator(config1))
    print_samples(samples1)

    print("\n" + "=" * 50 + "\n")

    # 测试配置2：产品信息生成
    config2 = {
        'count': 3,
        'product_id': {'type': 'int', 'min': 1000, 'max': 9999},
        'price': {'type': 'float', 'min': 10.0, 'max': 500.0},
        'product_name': {'type': 'str', 'length': 8, 'chars': string.ascii_uppercase},
        'ratings': {'type': 'list', 'size': 5, 'min': 1, 'max': 5}
    }

    print("配置2 - 产品信息:")
    print(f"配置: {config2}")
    samples2 = list(random_data_generator(config2))
    print_samples(samples2)

    print("\n" + "=" * 50 + "\n")

    # 测试配置3：用户数据生成
    config3 = {
        'count': 4,
        'user_id': {'type': 'int', 'min': 1, 'max': 100},
        'balance': {'type': 'float', 'min': 0.0, 'max': 10000.0},
        'username': {'type': 'str', 'length': 6, 'chars': string.ascii_lowercase + string.digits},
        'login_times': {'type': 'list', 'size': 7, 'min': 0, 'max': 10}
    }

    print("配置3 - 用户数据:")
    print(f"配置: {config3}")
    samples3 = list(random_data_generator(config3))
    print_samples(samples3)

    # 演示生成器特性
    print("\n演示生成器特性:")
    generator = random_data_generator({'count': 3, 'value': {'type': 'int', 'min': 1, 'max': 10}})
    for i, sample in enumerate(generator, 1):
        print(f"  生成样本{i}: {sample}")