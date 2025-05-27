import random
import string
from functools import wraps


def random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


def random_list(element_type, length=5):
    if element_type == 'int':
        return [random.randint(0, 100) for _ in range(length)]
    elif element_type == 'float':
        return [round(random.uniform(0.0, 100.0), 2) for _ in range(length)]
    elif element_type == 'str':
        return [random_string(10) for _ in range(length)]
    else:
        raise ValueError(f"Unsupported list element type: {element_type}")


def random_tuple(element_types):
    elements = []
    for element_type in element_types:
        if element_type == 'int':
            elements.append(random.randint(0, 100))
        elif element_type == 'float':
            elements.append(round(random.uniform(0.0, 100.0), 2))
        elif element_type == 'str':
            elements.append(random_string(10))
        else:
            raise ValueError(f"Unsupported tuple element type: {element_type}")
    return tuple(elements)


def sample_generator(sample_count, sample_structure):
    for _ in range(sample_count):
        sample = {}
        for field_name, field_info in sample_structure.items():
            if isinstance(field_info, dict):
                sample[field_name] = next(sample_generator(1, field_info))['nested']
            elif isinstance(field_info, str):
                if field_info == 'int':
                    sample[field_name] = random.randint(0, 100)
                elif field_info == 'float':
                    sample[field_name] = round(random.uniform(0.0, 100.0), 2)
                elif field_info == 'str':
                    sample[field_name] = random_string(10)
                elif field_info == 'list':
                    sample[field_name] = random_list('int')
                elif field_info == 'tuple':
                    sample[field_name] = random_tuple(['int', 'float'])
                else:
                    raise ValueError(f"Unsupported field type: {field_info}")
            elif isinstance(field_info, list):
                sample[field_name] = random_tuple(field_info)
            else:
                raise ValueError(f"Unsupported field info format: {field_info}")
        yield {'nested': sample}


def statistics_decorator(*operations):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            samples = list(func(*args, **kwargs))
            results = [sample['nested'] for sample in samples]

            all_values = []

            def extract_numeric_values(data):
                if isinstance(data, (int, float)):
                    all_values.append(data)
                elif isinstance(data, dict):
                    for value in data.values():
                        extract_numeric_values(value)
                elif isinstance(data, list):
                    for item in data:
                        extract_numeric_values(item)
                elif isinstance(data, tuple):
                    for item in data:
                        extract_numeric_values(item)

            for result in results:
                extract_numeric_values(result)

            stats = {}
            for op in operations:
                if op == 'SUM':
                    stats[op] = sum(all_values)
                elif op == 'AVG':
                    stats[op] = sum(all_values) / len(all_values) if all_values else 0
                elif op == 'MAX':
                    stats[op] = max(all_values) if all_values else None
                elif op == 'MIN':
                    stats[op] = min(all_values) if all_values else None
                else:
                    raise ValueError(f"Unsupported operation: {op}")

            print("Generated Samples:")
            for sample in results:
                print(sample)

            for key, value in stats.items():
                print(f"{key}: {value}")

            return samples

        return wrapper

    return decorator


if __name__ == "__main__":
    structure = {
        'id': 'int',
        'value': 'float',
        'description': 'str',
        'attributes': ['int', 'float'],
        'tags': 'list',
        'info': {
            'nested_id': 'int',
            'nested_value': 'float'
        }
    }


    @statistics_decorator('SUM', 'AVG', 'MAX', 'MIN')
    def generate_samples(count, struct):
        return sample_generator(count, struct)


    generate_samples(5, structure)
