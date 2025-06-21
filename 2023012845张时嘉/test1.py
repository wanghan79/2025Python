import random

def random_sample_generator(structure):
    """
    structure格式示例：{"int": (1, 100), "float": (0.0, 10.0), "str_len": 5}
    """
    while True:
        sample = {}
        for key, value in structure.items():
            if key == "int":
                sample[key] = random.randint(value[0], value[1])
            elif key == "float":
                sample[key] = round(random.uniform(value[0], value[1]), 2)
            elif key == "str":
                sample[key] = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=value))
        yield sample

if __name__ == "__main__":
    structure = {
        "id": ("int", 1, 1000),
        "score": ("float", 0.0, 100.0),
        "name": ("str", 8)
    }
    num_samples = 5
    
    gen = random_sample_generator(structure)
    
    for _ in range(num_samples):
        sample = next(gen)
        print(sample)
