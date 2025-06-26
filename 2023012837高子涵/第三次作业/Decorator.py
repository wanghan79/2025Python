import random
import string
import math
from typing import Callable, Dict, Any, Generator, List, Union, Tuple, Iterator
from collections import defaultdict
from functools import wraps


class DataGenerator:
    """A comprehensive random data generator with statistical analysis capabilities."""

    NUMBER_TYPES = {'int', 'float'}
    BASIC_TYPES = {'int', 'float', 'str', 'bool', 'choice'}
    CONTAINER_TYPES = {'list', 'tuple', 'dict', 'set'}

    @staticmethod
    def calculate_statistics(values: List[Union[int, float]]) -> Dict[str, Any]:
        """Calculate basic statistics for numeric values."""
        if not values:
            return {}

        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)

        return {
            'count': len(values),
            'sum': sum(values),
            'avg': mean,
            'min': min(values),
            'max': max(values),
            'std': math.sqrt(variance),
            'range': max(values) - min(values)
        }

    @staticmethod
    def generate_number(data_type: str, config: Dict[str, Any]) -> Generator[Union[int, float, str, bool], None, None]:
        """Generate basic type values."""
        count = config.get('num', 1)

        if data_type == 'int':
            start, end = config['datarange']
            for _ in range(count):
                yield random.randint(start, end)

        elif data_type == 'float':
            start, end = config['datarange']
            precision = config.get('precision')
            for _ in range(count):
                value = random.uniform(start, end)
                yield round(value, precision) if precision is not None else value

        elif data_type == 'str':
            chars = config.get('datarange', string.ascii_letters)
            length = config.get('len', 5)
            for _ in range(count):
                yield ''.join(random.choice(chars) for _ in range(length))

        elif data_type == 'bool':
            for _ in range(count):
                yield random.choice([True, False])

        elif data_type == 'choice':
            options = config['options']
            for _ in range(count):
                yield random.choice(options)

    @staticmethod
    def generate_container(data_type: str, config: Dict[str, Any]) -> Generator[Any, None, None]:
        """Generate container type values."""
        count = config.get('num', 1)

        for _ in range(count):
            if data_type == 'dict':
                # Special handling for dictionaries
                key_config = config.get('key', {'str': {'num': 1, 'len': 3}})
                value_config = config.get('value', {'int': {'num': 1, 'datarange': (0, 100)}})

                # Generate key-value pairs
                keys = list(DataGenerator.generate_from_config(key_config))
                values = list(DataGenerator.generate_from_config(value_config))

                # Yield only the values for statistics
                for val in values:
                    if isinstance(val, (int, float)):
                        yield val
            else:
                # Handle lists, tuples, sets
                elements = []
                for elem_type, elem_config in config.items():
                    if elem_type != 'num':
                        elements.extend(list(DataGenerator.generate_from_config({elem_type: elem_config})))

                for item in elements:
                    yield item

    @staticmethod
    def generate_from_config(config: Dict[str, Any]) -> Generator[Any, None, None]:
        """Generate data based on configuration."""
        if len(config) != 1:
            raise ValueError("Configuration should specify exactly one data type")

        data_type, params = next(iter(config.items()))

        if data_type in DataGenerator.BASIC_TYPES:
            yield from DataGenerator.generate_number(data_type, params)
        elif data_type in DataGenerator.CONTAINER_TYPES:
            yield from DataGenerator.generate_container(data_type, params)
        else:
            raise ValueError(f"Unsupported data type: {data_type}")

    @staticmethod
    def statistics_decorator(func: Callable) -> Callable:
        """Decorator to add statistical analysis."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            numeric_values = []
            type_counts = defaultdict(int)
            samples = []

            for sample in func(*args, **kwargs):
                sample_type = type(sample).__name__
                type_counts[sample_type] += 1
                samples.append(sample)

                if isinstance(sample, (int, float)):
                    numeric_values.append(sample)

            stats = DataGenerator.calculate_statistics(numeric_values) if numeric_values else {}

            return {
                'statistics': stats,
                'type_distribution': dict(type_counts),
                'samples': samples[:10]
            }

        return wrapper

    @classmethod
    def sampling(cls, **kwargs) -> Iterator[Any]:
        """Main sampling interface."""
        for data_type, config in kwargs.items():
            yield from cls.generate_from_config({data_type: config})


# Decorated sampling function
@DataGenerator.statistics_decorator
def sampling(**kwargs) -> Iterator[Any]:
    return DataGenerator.sampling(**kwargs)


if __name__ == '__main__':
    # Example 1: Basic types in tuple
    print("Example 1: Tuple with basic types")
    result1 = sampling(tuple={
        'num': 100,
        'int': {'num': 2, 'datarange': (0, 1000)},
        'float': {'num': 2, 'datarange': (0, 1000.0)},
        'str': {'num': 3, 'datarange': string.ascii_letters, 'len': 5}
    })
    print(result1)

    # Example 2: Nested structures
    print("\nExample 2: Nested tuple with statistics")
    result2 = sampling(tuple={
        'num': 50,
        'tuple': {
            'num': 3,
            'int': {'num': 2, 'datarange': (1, 100)},
            'float': {'num': 2, 'datarange': (1.0, 100.0), 'precision': 2}
        }
    })
    print(result2)

    # Example 3: Mixed types with boolean and choices
    print("\nExample 3: Mixed types in list")
    result3 = sampling(list={
        'num': 1,
        'int': {'num': 10, 'datarange': (1, 10)},
        'bool': {'num': 5},
        'choice': {'num': 3, 'options': [10, 20, 30, 40, 50]}
    })
    print(result3)

    # Example 4: Dictionary generation - FIXED
    print("\nExample 4: Dictionary with key-value pairs")
    result4 = sampling(dict={
        'num': 1,
        'key': {'str': {'num': 3, 'len': 2}},
        'value': {'int': {'num': 3, 'datarange': (1, 100)}}
    })
    print(result4)