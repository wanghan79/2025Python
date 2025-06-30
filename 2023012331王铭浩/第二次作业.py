作业二：使用生成器生成随机样本，配套生成器使用范例代码，随机样本的数量和结构由调用者输入。
import random
import string

def random_sample_generator(field_spec, num_samples):
    """
    生成随机样本数据

    :param field_spec: 字段结构规范，如：
           {
               'name': ('str', 5),
               'age': ('int', 18, 60),
               'score': ('float', 0, 100)
           }
    :param num_samples: 要生成的样本数
    :return: 生成器对象
    """
    for _ in range(num_samples):
        sample = {}
        for field, spec in field_spec.items():
            if spec[0] == 'int':
                sample[field] = random.randint(spec[1], spec[2])
            elif spec[0] == 'float':
                sample[field] = round(random.uniform(spec[1], spec[2]), 2)
            elif spec[0] == 'str':
                sample[field] = ''.join(random.choices(string.ascii_letters, k=spec[1]))
            elif spec[0] == 'choice':
                sample[field] = random.choice(spec[1])
            else:
                raise ValueError(f"Unsupported field type: {spec[0]}")
        yield sample



structure = {
    'id': ('int', 1000, 9999),
    'name': ('str', 6),
    'age': ('int', 18, 35),
    'score': ('float', 0.0, 100.0),
    'gender': ('choice', ['Male', 'Female'])
}

# 调用生成器生成 5 个样本
gen = random_sample_generator(structure, 5)

# 遍历并打印样本
for sample in gen:
print(sample)
代码运行结果如下：
{'id': 6562, 'name': 'KcysXb', 'age': 23, 'score': 69.32, 'gender': 'Male'}
{'id': 7819, 'name': 'HwTsRM', 'age': 29, 'score': 13.81, 'gender': 'Female'}
{'id': 6656, 'name': 'JEFNah', 'age': 21, 'score': 51.84, 'gender': 'Male'}
{'id': 2028, 'name': 'nBvlGI', 'age': 24, 'score': 73.71, 'gender': 'Female'}
{'id': 1611, 'name': 'iaKSsL', 'age': 25, 'score': 9.72, 'gender': 'Female'}
这段程序的运行结果展示了使用生成器随机生成的5条模拟用户数据，每条数据包含用户编号（id）、随机姓名（name）、年龄（age）、成绩（score）和性别（gender）等字段。各字段的取值范围和类型由调用者预先设定，程序会根据这些规则自动生成结构化的随机样本，
