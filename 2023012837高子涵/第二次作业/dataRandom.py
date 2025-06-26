import string
import random
from typing import Generator, Any, Dict, Union, List, Tuple


class DataSampler:
    """A flexible data sampler that can generate various types of random data."""

    @staticmethod
    def generate_int(datarange: Tuple[int, int]) -> int:
        """Generate a random integer within the given range."""
        start, end = datarange
        return random.randint(start, end)

    @staticmethod
    def generate_float(datarange: Tuple[float, float], precision: Union[int, None] = None) -> float:
        """Generate a random float within the given range with optional precision."""
        start, end = datarange
        value = random.uniform(start, end)
        return round(value, precision) if precision is not None else value

    @staticmethod
    def generate_str(length: int, datarange: str = string.ascii_letters) -> str:
        """Generate a random string of specified length from given characters."""
        return ''.join(random.choice(datarange) for _ in range(length))

    @staticmethod
    def generate_bool() -> bool:
        """Generate a random boolean value."""
        return random.choice([True, False])

    @staticmethod
    def generate_choice(options: List[Any]) -> Any:
        """Randomly select an item from the given options."""
        return random.choice(options)

    @staticmethod
    def generate_sequence(sequence_type: type, elements: Dict[str, Dict]) -> Union[List, Tuple]:
        """Generate a sequence (list or tuple) of random elements."""
        elements_list = []
        for elem_type, elem_config in elements.items():
            if elem_type != 'num':
                generated = list(DataSampler.sample(elem_type, elem_config))
                elements_list.extend(generated)
        return sequence_type(elements_list)

    @staticmethod
    def generate_dict(pairs: Dict[str, Dict]) -> Dict[Any, Any]:
        """Generate a dictionary with random keys and values."""
        result = {}
        for pair_name, pair_config in pairs.items():
            if pair_name != 'num':
                key_config = pair_config.get('key', {})
                value_config = pair_config.get('value', {})

                keys = list(DataSampler.sample('key', key_config)) if key_config else []
                values = list(DataSampler.sample('value', value_config)) if value_config else []

                for key, value in zip(keys, values):
                    result[key] = value
        return result

    @staticmethod
    def sample(data_type: str, config: Dict[str, Any]) -> Generator[Any, None, None]:
        """Generate samples of the specified data type based on configuration."""
        count = config.get('num', 1)

        for _ in range(count):
            if data_type == 'int':
                yield DataSampler.generate_int(config['datarange'])
            elif data_type == 'float':
                yield DataSampler.generate_float(
                    config['datarange'],
                    config.get('precision')
                )
            elif data_type == 'str':
                yield DataSampler.generate_str(
                    config.get('len', 1),
                    config.get('datarange', string.ascii_letters)
                )
            elif data_type == 'bool':
                yield DataSampler.generate_bool()
            elif data_type == 'choice':
                yield DataSampler.generate_choice(config.get('options', []))
            elif data_type in ('list', 'tuple'):
                yield DataSampler.generate_sequence(
                    list if data_type == 'list' else tuple,
                    {k: v for k, v in config.items() if k != 'num'}
                )
            elif data_type == 'dict':
                yield DataSampler.generate_dict(
                    {k: v for k, v in config.items() if k != 'num'}
                )
            elif data_type in ('key', 'value'):
                # Handle nested key/value sampling
                for nested_type, nested_config in config.items():
                    yield from DataSampler.sample(nested_type, nested_config)


def sampling(**kwargs) -> Generator[Any, None, None]:
    """Main sampling interface that delegates to DataSampler."""
    for data_type, config in kwargs.items():
        yield from DataSampler.sample(data_type, config)


def batch_sampling(batch_size: int, **kwargs) -> List[Any]:
    """Generate a batch of samples."""
    gen = sampling(**kwargs)
    return [next(gen) for _ in range(batch_size)]


if __name__ == '__main__':
    print("示例1：生成两个元组")
    gen = sampling(tuple={
        'num': 2,
        'int': {'num': 3, 'datarange': (1, 10)},
        'str': {'num': 2, 'len': 5, "datarange": string.ascii_uppercase}
    })
    for item in gen:
        print(item)

    print("\n示例2：生成两个复杂列表")
    gen2 = sampling(list={
        'num': 2,
        'int': {'num': 2, 'datarange': (100, 200)},
        'float': {'num': 1, 'datarange': (1.5, 9.5), 'precision': 2},
        'str': {'num': 1, 'len': 4, 'datarange': string.ascii_lowercase},
        'tuple': {
            'num': 1,
            'int': {'num': 2, 'datarange': (0, 5)},
            'str': {'num': 1, 'len': 3, 'datarange': string.digits}
        }
    })
    for item in gen2:
        print(item)

    print("\n示例3：生成字典")
    gen3 = sampling(dict={
        'num': 1,
        'pair': {
            'key': {'str': {'num': 3, 'len': 2, 'datarange': string.ascii_uppercase}},
            'value': {'int': {'num': 3, 'datarange': (1, 100)}}
        }
    })
    for item in gen3:
        print(item)

    print("\n示例4：使用batch_sampling批量生成")
    samples = batch_sampling(3, bool={'num': 5})
    print(samples)