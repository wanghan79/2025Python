import random
import string

def random_sample_generator(count, structure):
    """
    生成器，生成随机样本
   
    """
    for _ in range(count):
        sample = {}
        for field, config in structure.items():
            if config[0] == 'int':
                sample[field] = random.randint(config[1], config[2])
            elif config[0] == 'float':
                sample[field] = round(random.uniform(config[1], config[2]), 2)
            elif config[0] == 'str':
                sample[field] = ''.join(random.choices(string.ascii_letters, k=config[1]))
        yield sample
#使用范例
# 定义结构
structure = {
    'age': ('int', 18, 30),
    'score': ('float', 0, 100),
    'name': ('str', 6)
}

# 调用生成器
generator = random_sample_generator(5, structure)

# 遍历输出
for item in generator:
    print(item)