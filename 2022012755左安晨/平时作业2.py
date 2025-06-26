
"""
  Author:  Zuoanchen
  Created: 10/6/2025
"""

import random
import string


def datasampling(**kwargs):
    type, nested_data = list(kwargs.items())[0]

    if type == "tuple":
        yield tuple(next(datasampling(**item)) for item in nested_data)
    elif type == "list":
        yield [next(datasampling(**item)) for item in nested_data]
    elif type == "dict":
        yield {key: next(datasampling(**value)) for key, value in nested_data.items()}
    elif type == "int":
        yield random.randint(nested_data["datarange"][0], nested_data["datarange"][1])
    elif type == "float":
        yield random.uniform(nested_data["datarange"][0], nested_data["datarange"][1])
    elif type == "str":
        yield ''.join(random.SystemRandom().choice(nested_data["datarange"]) for _ in range(nested_data["len"]))

if __name__ == "__main__":
    data = {
        "dict": {
            "tuple": {
                "tuple": [
                    {"str": {"datarange": string.ascii_uppercase, "len": 5}},
                    {"int": {"datarange": (0, 10)}},
                    {
                        "tuple": [
                            {"int": {"datarange": (0, 10)}},
                            {"float": {"datarange": (0, 1.0)}},
                            {"str": {"datarange": string.ascii_uppercase, "len": 5}}
                        ]
                    }
                ]
            },
            "list": {
                "list": [
                    {"int": {"datarange": (0, 10)}},
                    {"float": {"datarange": (0, 1.0)}},
                    {"str": {"datarange": string.ascii_uppercase, "len": 5}}
                ]
            },
            "dict": {
                "dict": {
                    "list": {
                        "list": [
                            {"int": {"datarange": (0, 10)}},
                            {"str": {"datarange": string.ascii_uppercase, "len": 5}},
                            {
                                "tuple": [
                                    {"float": {"datarange": (0, 1.0)}},
                                    {"int": {"datarange": (0, 10)}}
                                ]
                            }
                        ]
                    }
                }
            }
        }
    }

    samples = (next(datasampling(**data)) for _ in range(10))
    for sample in samples:
        print(sample)
