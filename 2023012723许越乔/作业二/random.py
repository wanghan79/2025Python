import random
import string

class RandomSampleGenerator:
    def __init__(self, structure):
        """
        初始化随机样本生成器
        :param structure: 定义样本结构的字典
        """
        self.structure = structure

    def generate_sample(self):
        """
        根据结构生成单个随机样本
        """
        sample = {}
        for key, value_type in self.structure.items():
            if value_type == "int":
                sample[key] = random.randint(0, 100)  # 随机整数
            elif value_type == "float":
                sample[key] = round(random.uniform(0, 100), 2)  # 随机浮点数
            elif value_type == "string":
                sample[key] = ''.join(random.choices(string.ascii_letters + string.digits, k=10))  # 随机字符串
            elif value_type == "bool":
                sample[key] = random.choice([True, False])  # 随机布尔值
            else:
                raise ValueError(f"Unsupported type: {value_type}")
        return sample

    def generate_samples(self, num_samples):
        """
        生成指定数量的随机样本
        :param num_samples: 需要生成的样本数量
        :return: 包含所有样本的列表
        """
        return [self.generate_sample() for _ in range(num_samples)]

# 示例使用
if __name__ == "__main__":
    # 定义样本结构
    sample_structure = {
        "id": "int",
        "name": "string",
        "age": "int",
        "score": "float",
        "is_active": "bool"
    }

    # 创建生成器实例
    generator = RandomSampleGenerator(sample_structure)

    # 生成 5 个随机样本
    num_samples = 5
    samples = generator.generate_samples(num_samples)

    # 打印生成的样本
    for sample in samples:
        print(sample)