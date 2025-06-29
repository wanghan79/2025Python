import random
import string
from typing import Any, Dict, List, Union


class RandomSampleGenerator:
    def __init__(self):
        self.functions = {
            'int': self._generate_random_int,
            'float': self._generate_random_float,
            'str': self._generate_random_str,
            'bool': self._generate_random_bool,
            'list': self._generate_random_list,
            'dict': self._generate_random_dict
        }

    def generate_samples(self, count: int, structure: Union[Dict, str]) -> List[Any]:
        return [self._generate_sample(structure) for _ in range(count)]

    def _generate_sample(self, structure: Union[Dict, str]) -> Any:
        if isinstance(structure, str):
            return self.functions[structure]()
        elif isinstance(structure, dict):
            return {key: self._generate_sample(value) for key, value in structure.items()}
        else:
            raise ValueError("Unsupported structure type")

    def _generate_random_int(self, min_val: int = -100, max_val: int = 100) -> int:
        return random.randint(min_val, max_val)

    def _generate_random_float(self, min_val: float = -100.0, max_val: float = 100.0) -> float:
        return random.uniform(min_val, max_val)

    def _generate_random_str(self, min_len: int = 3, max_len: int = 10) -> str:
        length = random.randint(min_len, max_len)
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def _generate_random_bool(self) -> bool:
        return random.choice([True, False])

    def _generate_random_list(self, min_len: int = 1, max_len: int = 5) -> list:
        length = random.randint(min_len, max_len)
        element_type = random.choice(['int', 'float', 'str', 'bool'])
        return [self.functions[element_type]() for _ in range(length)]

    def _generate_random_dict(self, min_keys: int = 1, max_keys: int = 5) -> dict:
        num_keys = random.randint(min_keys, max_keys)
        keys = [self._generate_random_str(3, 8) for _ in range(num_keys)]
        return {key: self._generate_sample(random.choice(['int', 'float', 'str', 'bool']))
                for key in keys}


if __name__ == "__main__":
    generator = RandomSampleGenerator()

    int_samples = generator.generate_samples(10, 'int')
    print("Random integers:", int_samples)

    str_samples = generator.generate_samples(5, 'str')
    print("Random strings:", str_samples)

    complex_structure = {
        'id': 'int',
        'name': 'str',
        'price': 'float',
        'in_stock': 'bool',
        'tags': ['str'],
        'metadata': {
            'color': 'str',
            'weight': 'float'
        }
    }
    complex_samples = generator.generate_samples(3, complex_structure)
    print("Complex samples:")
    for sample in complex_samples:
        print(sample)

    random_dict_samples = generator.generate_samples(2, generator._generate_random_dict())
    print("Random dict samples:")
    for sample in random_dict_samples:
        print(sample)