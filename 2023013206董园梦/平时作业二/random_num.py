import random
import string
from typing import Dict, List, Tuple, Union, Generator, Any

def generate_random_sample_generator(structure: Union[Dict, List, Tuple, str, int, float]) -> Generator[Any, None, None]:
    """生成随机样本的生成器"""
    if isinstance(structure, dict):
        while True:
            yield {k: next(generate_random_sample_generator(v)) for k, v in structure.items()}
    elif isinstance(structure, list):
        first_element = structure[0] if structure else ""
        while True:
            yield [next(generate_random_sample_generator(first_element)) for _ in range(random.randint(1, 3))]
    elif isinstance(structure, tuple):
        while True:
            yield tuple(next(generate_random_sample_generator(item)) for item in structure)
    elif isinstance(structure, str):
        while True:
            if structure:
                yield ''.join(random.choices(string.ascii_letters + string.digits, k=len(structure)))
            else:
                yield ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 15)))
    elif isinstance(structure, int):
        while True:
            yield random.randint(1, 100)  # id范围：1-100
    elif isinstance(structure, float):
        while True:
            yield round(random.uniform(0.01, 1.0), 4)  # price范围：0.01-1.0，保留4位小数
    else:
        raise TypeError(f"Unsupported data type: {type(structure)}")

def generate_batch_samples(generator: Generator[Any, None, None], batch_size: int, print_samples: bool = True) -> List[Any]:
    samples = [next(generator) for _ in range(batch_size)]
    if print_samples:
        print("生成的随机数据样本:")
        for i, sample in enumerate(samples):
            print(f"样本{i+1}: {sample}")
    return samples

if __name__ == "__main__":
    unified_structure = {
        "id": 0,
        "value": 0.0,
        "items": [{
            "price": 0.0,
            "quantity": 0
        }]
    }
    generator = generate_random_sample_generator(unified_structure)
    generate_batch_samples(generator, 10)  #生成样本数