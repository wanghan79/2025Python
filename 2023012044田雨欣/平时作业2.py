import random

def random_sample_generator(sample_size, structure):
    for _ in range(sample_size):
        sample = {}
        for key, data_type in structure.items():
            if data_type == int:
                sample[key] = random.randint(0, 100)
            elif data_type == float:
                sample[key] = round(random.uniform(0, 100), 2)
            elif data_type == str:
                sample[key] = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
            else:
                sample[key] = None
        yield sample


if __name__ == "__main__":
    sample_structure = {
        "id": int,
        "score": float,
        "name": str,
        "age": int
    }

    generator = random_sample_generator(5, sample_structure)

    for sample in generator:
        print(sample)
"""
        sample_size: 样本数量
        structure: 样本结构
"""