import string
import random

def structDataSampling_second(**kwargs):
    element = []
    for key, value in kwargs.items():
        if key == "list":
            element.append(structDataSampling_second(**value))
        elif key == "dict":
            elements = structDataSampling_second(**value)
            element.append(dict(enumerate(elements)))
        elif key == "tuple":
            tuple_elements = structDataSampling_second(**value)
            element.append(tuple(tuple_elements))
        elif key == "int":
            it = random.randint(value['datarange'][0], value['datarange'][1])
            element.append(it)
        elif key == "float":
            # 生成随机浮点数
            it = random.uniform(value['datarange'][0], value['datarange'][1])
            element.append(it)
        elif key == "str":
            # 生成随机字符串
            length = value.get('len', 5)  # 默认长度为5
            it = ''.join(random.choices(value['datarange'], k=length))
            element.append(it)
        else:
            print(f"Warning: Unsupported key '{key}' encountered.")
            continue
    return element

# 示例结构，包含新增的元组

struct = {
    "int": {"datarange": (0, 100)},
    "float": {"datarange": (0, 10000)},
    "str": {"datarange": string.ascii_uppercase, "len": 50},
    "list": {
        "int": {"datarange": (100, 200)},
        "float": {"datarange": (1000, 2000)},
        "str": {"datarange": string.ascii_lowercase, "len": 10}
    },
    "dict": {
        "int": {"datarange": (500, 600)},
        "float": {"datarange": (5000, 6000)},
        "str": {"datarange": string.digits, "len": 8}
    },
    "tuple": {
        "int": {"datarange": (700, 800)},
        "float": {"datarange": (7000, 8000)},
        "str": {"datarange": string.punctuation, "len": 5}
    }
}
# 生成数据并打印结果
result = structDataSampling_second(**struct)
print(result)
