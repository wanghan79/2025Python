import random
from math import sqrt
import string

def StaticRes(*stats):
    def decorator(func):
        def wrapper(*args, **kwargs):
            data_generator = func(*args, **kwargs)

            result = {
                'SUM': 0,
                'AVG': 0,
                'VAR': 0,
                'RMSE': 0,
                'count': 0
            }

            for item in data_generator:
                numbers = extract_numbers(item)
                if numbers:
                    result['count'] += len(numbers)
                    result['SUM'] += sum(numbers)
                    avg = result['SUM'] / result['count']
                    squared_diffs = [(x - avg) ** 2 for x in numbers]
                    result['VAR'] += sum(squared_diffs)
                    result['RMSE'] += sum(squared_diffs)

            if result['count'] > 0:
                result['AVG'] = result['SUM'] / result['count']
                if result['count'] > 1:
                    result['VAR'] /= result['count']
                    result['RMSE'] = sqrt(result['RMSE'] / result['count'])
                else:
                    result['VAR'] = 0
                    result['RMSE'] = 0
            else:
                result['SUM'] = 0
                result['AVG'] = 0
                result['VAR'] = 0
                result['RMSE'] = 0

            final_result = {}
            if 'SUM' in stats:
                final_result['SUM'] = result['SUM']
            if 'AVG' in stats:
                final_result['AVG'] = result['AVG']
            if 'VAR' in stats:
                final_result['VAR'] = result['VAR']
            if 'RMSE' in stats:
                final_result['RMSE'] = result['RMSE']

            return final_result
        return wrapper
    return decorator

def extract_numbers(element):
    numbers = []
    if isinstance(element, (int, float)):
        numbers.append(element)
    elif isinstance(element, (list, tuple, set)):
        for item in element:
            numbers.extend(extract_numbers(item))
    elif isinstance(element, dict):
        for key, value in element.items():
            numbers.extend(extract_numbers(value))
    elif isinstance(element, str):
        pass
    return numbers


def structDataSampling(**kwargs):
    num = kwargs.get('num', 1)

    kwargs.pop('num', None)

    def generator():
        count = 0
        while count < num:
            element = []

            for key, value in kwargs.items():
                if key == "list":
                    element.append(list(generator_inner(**value)))
                elif key == "dict":
                    element.append(dict(generator_inner(**value)))
                elif key == "int":
                    it = random.randint(value['datarange'][0], value['datarange'][1])
                    element.append(it)
                elif key == "float":
                    it = random.uniform(value['datarange'][0], value['datarange'][1])
                    element.append(it)
                elif key == "str":
                    length = value.get('len', 5)
                    it = ''.join(random.choices(list(value['datarange']), k=length))
                    element.append(it)
                elif key == "tuple":
                    tuple_content = list(generator_inner(**value))
                    element.append(tuple(tuple_content))
                else:
                    print(f"Warning: Unsupported key '{key}' encountered.")
                    continue

            yield element
            count += 1

    return generator()


def generator_inner(**kwargs):
    for key, value in kwargs.items():
        if key == "list" or key == "dict":
            for k, v in value.items():
                if k == "list":
                    yield from generator_inner(**v)
                elif k == "dict":
                    yield from generator_inner(**v)
                elif k == "int":
                    yield random.randint(v['datarange'][0], v['datarange'][1])
                elif k == "float":
                    yield random.uniform(v['datarange'][0], v['datarange'][1])
                elif k == "str":
                    length = v.get('len', 5)
                    yield ''.join(random.choices(list(v['datarange']), k=length))
                elif k == "tuple":
                    yield tuple(generator_inner(**v))
                else:
                    print(f"Warning: Unsupported key '{k}' encountered.")

        elif key == "int":
            yield random.randint(value['datarange'][0], value['datarange'][1])
        elif key == "float":
            yield random.uniform(value['datarange'][0], value['datarange'][1])
        elif key == "str":
            length = value.get('len', 5)
            yield ''.join(random.choices(list(value['datarange']), k=length))
        elif key == "tuple":
            yield tuple(generator_inner(**value))
        else:
            print(f"Warning: Unsupported key '{key}' encountered.")


@StaticRes('SUM', 'AVG', 'VAR', 'RMSE')
def structDataSampling(**kwargs):
    num = kwargs.get('num', 1)

    kwargs.pop('num', None)

    def generator():
        count = 0
        while count < num:
            element = []

            for key, value in kwargs.items():
                if key == "list":
                    element.append(list(generator_inner(**value)))
                elif key == "dict":
                    element.append(dict(generator_inner(**value)))
                elif key == "int":
                    it = random.randint(value['datarange'][0], value['datarange'][1])
                    element.append(it)
                elif key == "float":
                    it = random.uniform(value['datarange'][0], value['datarange'][1])
                    element.append(it)
                elif key == "str":
                    length = value.get('len', 5)
                    it = ''.join(random.choices(list(value['datarange']), k=length))
                    element.append(it)
                elif key == "tuple":
                    tuple_content = list(generator_inner(**value))
                    element.append(tuple(tuple_content))
                else:
                    print(f"Warning: Unsupported key '{key}' encountered.")
                    continue

            yield element
            count += 1

    return generator()


def apply():
    struct = {
        "num": 10,
        "list": {
            "str": {"datarange": string.ascii_letters, "len": 10},
        },
        "tuple": {
            "str": {"datarange": string.ascii_letters, "len": 10},
            "list": {
                "int": {"datarange": (0, 10)},
                "float": {"datarange": (0, 10000)}
            },
            "dict": {
                "str": {"datarange": string.ascii_letters, "len": 10},
                "int": {"datarange": (0, 10)}
            }
        }
    }
    result = structDataSampling(**struct)
    print(result)

apply()