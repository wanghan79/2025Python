import random
import string

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def random_integer(min_value=0, max_value=100):
    return random.randint(min_value, max_value)

def random_sample_generator(sample_count, sample_structure):
    for _ in range(sample_count):
        sample = {}
        for field, field_type in sample_structure.items():
            if field_type == 'str':
                sample[field] = random_string()
            elif field_type == 'int':
                sample[field] = random_integer()
            else:
                raise ValueError(f"Unsupported field type: {field_type}")
        yield sample

if __name__ == "__main__":
    sample_count = int(input("请输入需要生成的样本数量："))
    sample_structure = {
        'name': 'str',
        'age': 'int',
        'city': 'str'
    }
    
    generator = random_sample_generator(sample_count, sample_structure)
    
    for sample in generator:
        print(sample)
