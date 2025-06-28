import random
import string
from typing import Dict, Any, Tuple, Generator

GENERATOR_FUNCTIONS = {
    int: lambda args: random.randint(args[0], args[1]),
    float: lambda args: round(random.uniform(args[0], args[1]), 2),
    str: lambda args: ''.join(random.choices(string.ascii_lowercase, k=args[0])),
    bool: lambda _: random.choice([True, False]),
}

def generate_random_sample(structure: Dict[str, Tuple[type, tuple]]) -> Dict[str, Any]:
    return {
        field: GENERATOR_FUNCTIONS[datatype](args)
        for field, (datatype, args) in structure.items()
    }

def sample_generator(sample_count: int, structure: Dict[str, Tuple[type, tuple]]) -> Generator[
    Dict[str, Any], None, None]:
    for _ in range(sample_count):
        yield generate_random_sample(structure)

if __name__ == "__main__":
    '''
    定义样本结构
    '''
    SAMPLE_STRUCTURE = {
        "structure1": (int, (10, 100)),
        "structure2": (float, (1.5, 2.0)),
        "structure3": (str, (15,)),
        "structure4": (bool, ()),
    }

    '''
    定义样本数量
    '''
    SAMPLE_COUNT = 5

    for i, sample in enumerate(sample_generator(SAMPLE_COUNT, SAMPLE_STRUCTURE), 1):
        print(f"样本 {i}: {sample}")
