import random
import string

def generate(**kwargs):
    num = kwargs.pop('num', 1)

    for _ in range(num):
        res = []
        for key, value in kwargs.items():
            if key == "int":
                res.append(random.randint(value['datarange'][0], value['datarange'][1]))
            elif key == "float":
                res.append(random.uniform(value['datarange'][0], value['datarange'][1]))
            elif key == "str":
                datarange, length = value['datarange'], value['len']
                res.append(''.join(random.choices(datarange, k=length)))
            else:
                res.append(list(next(generate(**value))))
        yield res


def main():
    struct = {
        'num': 3,
        "list": {
            "int": {"datarange": (0, 100)},
            "float": {"datarange": (0, 10.0)},
            "str": {"datarange": string.ascii_lowercase, "len": 5},
            "dict": {
                "pair1": {
                    "key": {
                        "tuple": {
                            "int": {"datarange": (1, 10)},
                            "str": {"datarange": string.ascii_letters, "len": 2}
                        }
                    },
                    "value": {
                        "str": {"datarange": string.ascii_uppercase, "len": 4}
                    }
                },
                "pair2": {
                    "key": {
                        "int": {"datarange": (0, 5)}
                    },
                    "value": {
                        "float": {"datarange": (0, 1.0)}
                    }
                }
            },
            "list": {
                "tuple": {
                    "float": {"datarange": (0, 1.0)},
                    "dict": {
                        "pair1": {
                            "key": {
                                "str": {"datarange": "abc", "len": 1}
                            },
                            "value": {
                                "int": {"datarange": (100, 200)}
                            }
                        }
                    }
                }
            }
        }
    }

    sample_generator = generate(**struct)

    for i, sample in enumerate(sample_generator):
        print(f"样本 {i + 1}: {sample}")


if __name__ == "__main__":
    main()