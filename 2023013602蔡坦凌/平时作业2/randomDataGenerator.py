import string
import random

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
                    print(f"Unsupported key '{key}' encountered.")
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
                    print(f"Unsupported key '{k}' encountered.")
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
            print(f"Unsupported key '{key}' encountered.")

def flatten(nested_list):
    for item in nested_list:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield str(item)

def apply():
    struct = {
        "num": 100,
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
    count = 0
    for item in result:
        flattened = ', '.join(flatten(item))
        print(flattened)
        count += 1
        if count >= 100:
            break

apply()