import random
import string

def sample_generator(config, count=None):
    """
    随机样本生成器 (生成器版本)

    参数:
        config: 描述样本结构的配置字典
        count: 要生成的样本数量 (如果为None，则无限生成样本)
    """
    # 无限生成模式
    if count is None:
        while True:
            yield _generate_from_config(config)
    # 有限生成模式
    else:
        for _ in range(count):
            yield _generate_from_config(config)

def _generate_from_config(config):
    """根据配置生成单个样本"""
    data_type = config.get('type')

    if data_type == 'int':
        return random.randint(config['min'], config['max'])

    elif data_type == 'float':
        decimal_places = config.get('decimal', 2)
        return round(random.uniform(config['min'], config['max']), decimal_places)

    elif data_type == 'str':
        charset = config.get('chars', string.ascii_letters + string.digits)
        length = config.get('length', 8)
        return ''.join(random.choices(charset, k=length))

    elif data_type == 'bool':
        return random.choice([True, False])

    elif data_type == 'list':
        # 支持固定长度和随机长度列表
        length = config.get('length')
        if length is None:
            min_len = config.get('min_length', 1)
            max_len = config.get('max_length', 5)
            length = random.randint(min_len, max_len)

        return [_generate_from_config(config['element']) for _ in range(length)]

    elif data_type == 'dict':
        return {key: _generate_from_config(field_config)
                for key, field_config in config['fields'].items()}

    elif data_type == 'tuple':
        return tuple(_generate_from_config(element_config)
                    for element_config in config['elements'])

    else:
        raise ValueError(f"不支持的样本类型: {data_type}")


# 测试用例1: 生成随机用户数据
def generate_random_users(count):
    """生成随机用户数据"""
    user_config = {
        'type': 'dict',
        'fields': {
            'id': {'type': 'int', 'min': 1000, 'max': 9999},
            'username': {
                'type': 'str',
                'chars': string.ascii_lowercase,
                'length': random.randint(5, 10)
            },
            'email': {
                'type': 'str',
                'length': 10,
                'chars': string.ascii_lowercase + string.digits + '._-'
            },
            'age': {'type': 'int', 'min': 18, 'max': 65},
            'is_active': {'type': 'bool'},
            'registration_date': {'type': 'str', 'chars': string.digits, 'length': 8},  # YYYYMMDD
            'preferences': {
                'type': 'dict',
                'fields': {
                    'theme': {'type': 'str', 'chars': 'light dark', 'length': 1},
                    'notifications': {'type': 'bool'},
                    'language': {'type': 'str', 'chars': 'en fr es de', 'length': 1}
                }
            },
            'purchase_history': {
                'type': 'list',
                'min_length': 0,  # 允许空列表
                'max_length': 5,
                'element': {
                    'type': 'dict',
                    'fields': {
                        'order_id': {'type': 'str', 'chars': string.ascii_uppercase + string.digits, 'length': 8},
                        'amount': {'type': 'float', 'min': 5.0, 'max': 500.0, 'decimal': 2},
                        'items': {
                            'type': 'list',
                            'min_length': 1,
                            'max_length': 3,
                            'element': {
                                'type': 'dict',
                                'fields': {
                                    'product_id': {'type': 'str', 'chars': string.digits, 'length': 6},
                                    'quantity': {'type': 'int', 'min': 1, 'max': 5}
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    return sample_generator(user_config, count)


# 测试用例2: 生成传感器数据流
def generate_sensor_data_stream():
    """无限生成传感器数据流"""
    sensor_config = {
        'type': 'dict',
        'fields': {
            'sensor_id': {'type': 'str', 'length': 4, 'chars': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'},
            'timestamp': {'type': 'str', 'chars': string.digits, 'length': 10},  # Unix时间戳
            'temperature': {'type': 'float', 'min': -20.0, 'max': 50.0, 'decimal': 1},
            'humidity': {'type': 'float', 'min': 0.0, 'max': 100.0, 'decimal': 1},
            'pressure': {'type': 'float', 'min': 900.0, 'max': 1100.0, 'decimal': 1},
            'status': {
                'type': 'str',
                'chars': 'NORMAL WARNING CRITICAL',
                'length': 1
            }
        }
    }

    return sample_generator(sensor_config, None)  # 无限流


# 主程序：测试用例演示
if __name__ == '__main__':
    # 示例1: 生成有限数量的随机用户
    print("===== 测试用例1: 随机用户生成 =====")
    user_count = int(input("\n请输入要生成的用户数量: "))

    # 使用生成器创建用户
    user_gen = generate_random_users(user_count)

    # 打印前5个样本（或更少）
    print(f"\n生成 {user_count} 个用户样本:")
    max_display = min(5, user_count)
    displayed = 0

    for i, user in enumerate(user_gen, 1):
        if displayed < max_display:
            print(f"用户 {i}:")
            print(f"  ID: {user['id']}, 用户名: {user['username']}, 邮箱: {user['email']}@example.com")
            print(f"  年龄: {user['age']}, 活跃: {user['is_active']}")
            displayed += 1

    if user_count > max_display:
        print(f"\n... 省略了 {user_count - max_display} 个用户样本")

    # 示例2: 生成传感器数据流
    print("\n===== 测试用例2: 实时传感器数据流 =====")
    sensor_count = int(input("\n请输入要模拟的传感器数据点数: "))

    # 创建无限数据流
    sensor_stream = generate_sensor_data_stream()

    # 显示前5个传感器读数
    print(f"\n实时传感器数据流 (显示前 {min(5, sensor_count)} 个点):")
    for i, data in enumerate(sensor_stream):
        if i >= sensor_count:
            break
        if i < 5:
            print(f"数据点 {i+1}:")
            print(f"  传感器: {data['sensor_id']}, 时间: {data['timestamp']}")
            print(f"  温度: {data['temperature']}°C, 湿度: {data['humidity']}%")
            print(f"  气压: {data['pressure']}hPa, 状态: {data['status']}")

    print("\n=== 测试完成 ===")