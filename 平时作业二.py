import random

def random_sample_generator(sample_count, field_structure):
    for _ in range(sample_count):
        sample = {}
        for field, config in field_structure.items():
            if config[0] == 'int':
                sample[field] = random.randint(config[1], config[2])
            elif config[0] == 'float':
                sample[field] = round(random.uniform(config[1], config[2]), 2)
            elif config[0] == 'str':
                sample[field] = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=config[1]))
        yield sample

# 使用
structure = {'age': ('int', 18, 30), 'score': ('float', 50, 100), 'name': ('str', 5)}
for item in random_sample_generator(5, structure):
    print(item)
