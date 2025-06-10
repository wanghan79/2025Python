import random
import string


class RandomSampleGenerator:
    def __init__(self, num_samples, structure):
        self.num_samples = num_samples
        self.structure = structure

    def generate_data(self, structure):
        if 'type' not in structure:
            return None

        data_type = structure['type']

        if data_type == 'int':
            dr = structure.get('datarange', [0, 100])
            return random.randint(dr[0], dr[1])

        elif data_type == 'float':
            dr = structure.get('datarange', [0.0, 100.0])
            return round(random.uniform(dr[0], dr[1]), 2)

        elif data_type == 'str':
            dr = structure.get('datarange', string.ascii_letters)
            length = structure.get('len', 8)
            return ''.join(random.choices(dr, k=length))

        elif data_type == 'list':
            elements = structure.get('elements', [])
            size = structure.get('size', random.randint(1, 10))
            if elements:
                return [self.generate_data(elements[0]) for _ in range(size)]
            else:
                return []

        elif data_type == 'dict':
            keys = structure.get('keys', {})
            return {k: self.generate_data(v) for k, v in keys.items()}

        elif data_type == 'tuple':
            elements = structure.get('elements', [])
            return tuple(self.generate_data(e) for e in elements)

        else:
            return None

    def generate_samples(self):
        samples = []
        for _ in range(self.num_samples):
            sample = {}
            for key, value in self.structure.items():
                sample[key] = self.generate_data(value)
            samples.append(sample)
        return samples

    @classmethod
    def from_manual_config(cls, num_samples, structure):
        return cls(num_samples, structure)


# 示例用法
if __name__ == "__main__":
    # 定义结构
    structure = {
        "int_field": {"type": "int", "datarange": [1, 100]},
        "float_field": {"type": "float", "datarange": [0.0, 100.0]},
        "str_field": {"type": "str", "datarange": string.ascii_uppercase, "len": 8},
        "list_field": {
            "type": "list",
            "elements": [{"num": {"type": "int", "datarange": [1, 10]}}],
            "size": 5
        },
        "dict_field": {
            "type": "dict",
            "keys": {
                "key1": {"type": "int", "datarange": [1, 10]},
                "key2": {"type": "str", "datarange": string.ascii_lowercase, "len": 5}
            }
        },
        "tuple_field": {
            "type": "tuple",
            "elements": [
                {"type": "int", "datarange": [1, 10]},
                {"type": "str", "datarange": string.digits, "len": 4}
            ]
        }
    }

    # 创建生成器并生成样本
    generator = RandomSampleGenerator.from_manual_config(10, structure)
    samples = generator.generate_samples()

    # 打印生成的样本
    for i, sample in enumerate(samples):
        print(f"样本 {i + 1}: {sample}")
