import random
import string
from typing import Any, Dict, List, Union, Callable
from functools import wraps


def stats_operations(*operations: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            samples = func(*args, **kwargs)
            results = {'samples': samples}

            if 'SUM' in operations:
                results['SUM'] = sum(samples) if all(isinstance(x, (int, float)) for x in samples) else "N/A"
            if 'AVG' in operations:
                results['AVG'] = sum(samples) / len(samples) if all(
                    isinstance(x, (int, float)) for x in samples) else "N/A"
            if 'MAX' in operations:
                results['MAX'] = max(samples) if all(isinstance(x, (int, float)) for x in samples) else "N/A"
            if 'MIN' in operations:
                results['MIN'] = min(samples) if all(isinstance(x, (int, float)) for x in samples) else "N/A"

            return results

        return wrapper

    return decorator


class RandomSampleGenerator:
    def __init__(self):
        self.functions = {
            'int': self._generate_random_int,
            'float': self._generate_random_float,
            'str': self._generate_random_str,
            'bool': self._generate_random_bool
        }

    @stats_operations('SUM', 'AVG', 'MAX', 'MIN')
    def generate_numeric_samples(self, count: int, type_: str) -> List[Union[int, float]]:
        return [self.functions[type_]() for _ in range(count)]

    def _generate_random_int(self, min_val: int = -100, max_val: int = 100) -> int:
        return random.randint(min_val, max_val)

    def _generate_random_float(self, min_val: float = -100.0, max_val: float = 100.0) -> float:
        return random.uniform(min_val, max_val)

    def _generate_random_str(self, min_len: int = 3, max_len: int = 10) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(min_len, max_len)))

    def _generate_random_bool(self) -> bool:
        return random.choice([True, False])


if __name__ == "__main__":
    generator = RandomSampleGenerator()

    print(generator.generate_numeric_samples(10, 'int'))


    @stats_operations('SUM', 'AVG')
    def generate_sum_avg(count, type_):
        return [generator._generate_random_int() if type_ == 'int' else generator._generate_random_float() for _ in
                range(count)]


    print(generate_sum_avg(5, 'float'))


    @stats_operations('MAX', 'MIN')
    def generate_max_min(count, type_):
        return [generator._generate_random_int() if type_ == 'int' else generator._generate_random_float() for _ in
                range(count)]


    print(generate_max_min(8, 'int'))