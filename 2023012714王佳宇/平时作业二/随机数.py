import random
import string

def generate_data(data_type, **kwargs):
    """
    根据数据类型生成单个数据
    """
    if data_type == "int":
        data_range = kwargs.get("datarange")
        return random.randint(data_range[0], data_range[1])
    elif data_type == "float":
        data_range = kwargs.get("datarange")
        return random.uniform(data_range[0], data_range[1])
    elif data_type == "str":
        data_range = kwargs.get("datarange")
        length = kwargs.get("len")
        return ''.join(random.choices(data_range, k=length))
    elif data_type == "dict":
        key = ''.join(random.choices(string.ascii_letters, k=3))
        value = random.randint(0, 100)
        return {key: value}
    elif data_type == "list" or data_type == "tuple":
        # 递归生成嵌套结构
        return [generate_data(**item) for item in kwargs.get("struct", [])]
    else:
        raise ValueError(f"Unsupported data type: {data_type}")

def data_generator(struct):
    """
    生成器函数，根据结构生成数据
    """
    num = struct.get("num", 1)
    for _ in range(num):
        result = []
        for data_type, config in struct.items():
            if data_type == "num":
                continue
            result.append(generate_data(data_type, **config))
        yield tuple(result)

def main():
    struct = {
        'num': 100000000,  # 数据样本数量
        "tuple": {
            "struct": [
                {"type": "str", "datarange": string.ascii_uppercase, "len": 50},
                {"type": "list", "struct": [
                    {"type": "int", "datarange": (0, 10)},
                    {"type": "float", "datarange": (0, 1.0)}
                ]},
                {"type": "dict"}
            ]
        }
    }

    # 创建生成器
    sample_generator = data_generator(struct["tuple"])

    # 迭代生成样本
    for sample in sample_generator:
        print(sample)
        # break  # 如果只想测试一个样本，取消注释

if __name__ == "__main__":
    main()