import random
import string
import datetime


def random_sample_generator(sample_count, structure):
    """
    生成指定数量和结构的随机样本

    参数:
    sample_count (int): 要生成的样本数量
    structure (dict): 样本结构，格式为 {字段名: 字段类型}
                     支持的字段类型: 'int', 'float', 'str', 'date', 'bool', 'choice'
                     对于'int'和'float'类型，可以指定范围，如 'int:0:100'
                     对于'str'类型，可以指定长度，如 'str:10'
                     对于'choice'类型，可以指定选项，如 'choice:A,B,C,D'

    返回:
    generator: 生成指定结构的随机样本的生成器
    """

    def generate_random_value(field_type):
        if field_type.startswith('int:'):
            parts = field_type.split(':')
            min_val = int(parts[1]) if len(parts) > 1 else 0
            max_val = int(parts[2]) if len(parts) > 2 else 1000
            return random.randint(min_val, max_val)

        elif field_type.startswith('float:'):
            parts = field_type.split(':')
            min_val = float(parts[1]) if len(parts) > 1 else 0.0
            max_val = float(parts[2]) if len(parts) > 2 else 1000.0
            return round(random.uniform(min_val, max_val), 2)

        elif field_type.startswith('str:'):
            length = int(field_type.split(':')[1]) if len(field_type.split(':')) > 1 else 10
            return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

        elif field_type == 'date':
            start_date = datetime.date(2000, 1, 1)
            end_date = datetime.date(2023, 12, 31)
            delta = end_date - start_date
            random_days = random.randint(0, delta.days)
            return (start_date + datetime.timedelta(days=random_days)).isoformat()

        elif field_type == 'bool':
            return random.choice([True, False])

        elif field_type.startswith('choice:'):
            choices = field_type.split(':', 1)[1].split(',')
            return random.choice(choices)

        elif field_type == 'int':
            return random.randint(0, 1000)

        elif field_type == 'float':
            return round(random.uniform(0, 1000), 2)

        elif field_type == 'str':
            return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

        else:
            return None

    for _ in range(sample_count):
        sample = {field_name: generate_random_value(field_type) for field_name, field_type in structure.items()}
        yield sample


# 使用示例:
if __name__ == "__main__":
    # 示例1: 生成用户数据
    user_structure = {
        'id': 'int:1:1000',
        'name': 'str:8',
        'email': 'str:15',
        'age': 'int:18:65',
        'is_active': 'bool',
        'registration_date': 'date',
        'user_type': 'choice:free,premium,enterprise'
    }

    print("生成10个用户数据样本:")
    for i, user in enumerate(random_sample_generator(10, user_structure), 1):
        print(f"用户 {i}: {user}")

    # 示例2: 生成产品数据
    product_structure = {
        'product_id': 'str:6',
        'price': 'float:10:1000',
        'inventory': 'int:0:500',
        'category': 'choice:electronics,clothing,food,books',
        'is_available': 'bool'
    }

    print("\n生成5个产品数据样本:")
    for i, product in enumerate(random_sample_generator(5, product_structure), 1):
        print(f"产品 {i}: {product}")
