import random
import string
from collections import namedtuple

def random_sample_generator(sample_count, structure):
    def generate_random_data(field_type):
        if field_type == 'int':
            return random.randint(0, 1000)
        elif field_type.startswith('int('):
            min_val, max_val = map(int, field_type[4:-1].split(','))
            return random.randint(min_val, max_val)
        elif field_type == 'float':
            return round(random.uniform(0, 100), 2)
        elif field_type == 'str':
            length = random.randint(5, 15)
            return ''.join(random.choices(string.ascii_letters, k=length))
        elif field_type == 'email':
            name = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 10)))
            domain = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 6)))
            return f"{name}@{domain}.com"
        elif field_type == 'bool':
            return random.choice([True, False])
        else:
            return None
    
    Sample = namedtuple('Sample', structure.keys())
    
    for _ in range(sample_count):
        data = {}
        for field, field_type in structure.items():
            data[field] = generate_random_data(field_type)
        yield Sample(**data)

if __name__ == "__main__":
    sample_structure = {
        'id': 'int',
        'username': 'str',
        'email': 'email',
        'age': 'int(18,65)',
        'score': 'float',
        'is_active': 'bool'
    }
    
    try:
        num_samples = int(input("请输入要生成的样本数量: "))
    except ValueError:
        num_samples = 5
    
    print("\n生成的随机样本:")
    for i, sample in enumerate(random_sample_generator(num_samples, sample_structure), 1):
        print(f"样本 {i}:")
        print(f"  ID: {sample.id}")
        print(f"  用户名: {sample.username}")
        print(f"  邮箱: {sample.email}")
        print(f"  年龄: {sample.age}")
        print(f"  分数: {sample.score}")
        print(f"  是否活跃: {sample.is_active}")
        print("-" * 30)
