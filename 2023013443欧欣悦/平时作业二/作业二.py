import random
import string

def random_sample_generator(num_samples, structure):
    """
    生成随机样本的生成器函数。

    参数：
    num_samples (int): 需要生成的随机样本数量。
    structure (dict): 定义样本结构的字典，键为字段名，值为字段类型。

    生成器返回值：
    每次迭代返回一个符合指定结构的随机样本（字典形式）。
    """
    for _ in range(num_samples):
        sample = {}
        for field, field_type in structure.items():
            if field_type == "int":
                sample[field] = random.randint(0, 100)  # 随机整数范围0到100
            elif field_type == "float":
                sample[field] = round(random.uniform(0, 100), 2)  # 随机浮点数范围0到100，保留2位小数
            elif field_type == "str":
                sample[field] = ''.join(random.choices(string.ascii_letters + string.digits, k=8))  # 随机8位字符串
            elif field_type == "bool":
                sample[field] = random.choice([True, False])  # 随机布尔值
            else:
                raise ValueError(f"不支持的字段类型：{field_type}")
        yield sample
# 定义样本结构
sample_structure = {
    "id": "int",
    "name": "str",
    "age": "int",
    "score": "float",
    "is_active": "bool"
}

# 调用者输入的随机样本数量
num_samples = int(input("请输入随机样本数量："))

# 使用生成器生成随机样本
print("生成的随机样本如下：")
for sample in random_sample_generator(num_samples, sample_structure):
    print(sample)