import random
import string


def structDataSampling(num, **kwargs):
    """
    :param num: 生成器生成的数量
    :param kwargs: 生成器的参数
    :return: generator: 生成器
    """

    def generator():
        count = 0
        while count < num:
            element = []

            for key, value in kwargs.items():
                if key == "int":
                    element.append(random.randint(value['dataRange'][0], value['dataRange'][1]))
                elif key == "float":
                    element.append(random.randint(value['dataRange'][0], value['dataRange'][1]))
                elif key == "str":
                    length = value.get('length', 5)
                    element.append(''.join(random.choices(list(value['dataRange']), k=length)))
                elif key == "list":
                    element.append(list(generator_inner(**value)))
                elif key == "dict":
                    element.append(dict(generator_inner(**value)))
                elif key == "tuple":
                    element.append(tuple(generator_inner(**value)))
                else:
                    print(f"'{key}' 并非有效的数据结构")
                    continue
            yield element

            count += 1

    return generator()


def generator_inner(**kwargs):
    """
    :param kwargs: 生成器的参数
    :return: generator: 生成器
    """
    for key, value in kwargs.items():
        if key == "int":
            yield random.randint(value['dataRange'][0], value['dataRange'][1])
        elif key == "float":
            yield random.uniform(value['dataRange'][0], value['dataRange'][1])
        elif key == "str":
            length = value.get('length', 5)
            yield ''.join(random.choices(list(value['dataRange']), k=length))
        elif key == "list" or key == "dict":
            for list_key, list_value in value.items():
                if list_key == "int":
                    yield random.randint(list_value['dataRange'][0], list_value['dataRange'][1])
                elif list_key == "float":
                    yield random.uniform(list_value['dataRange'][0], list_value['dataRange'][1])
                elif list_key == "str":
                    length = list_value.get('length', 5)
                    yield ''.join(random.choices(list(list_value['dataRange']), k=length))
                elif list_key == "list":
                    yield list(generator_inner(**list_value))
                elif list_key == "dict":
                    yield dict(generator_inner(**list_value))
                elif list_key == "tuple":
                    yield tuple(generator_inner(**list_value))
        elif key == "tuple":
            yield tuple(generator_inner(**value))
        else:
            print(f"'{key}' 并非有效的数据结构")
            continue


def apply():
    struct = {
        "num": 10,
        "int": {"dataRange": (0, 100)},
        "float": {"dataRange": (0, 10000)},
        "str": {"dataRange": string.ascii_letters, "len": 10},
        "list": {
            "str": {"dataRange": string.ascii_letters, "len": 10},
        },
        "tuple": {
            "str": {"dataRange": string.ascii_letters, "len": 10},
            "list": {
                "int": {"dataRange": (0, 10)},
                "float": {"dataRange": (0, 10000)}
            },
            "dict": {
                "str": {"dataRange": string.ascii_letters, "len": 10},
                "int": {"dataRange": (0, 10)}
            }
        }
    }
    result = structDataSampling(**struct)
    count = 0
    for item in result:
        print(item)
        count += 1
        if count >= 100000000:
            break


if __name__ == '__main__':
    apply()
