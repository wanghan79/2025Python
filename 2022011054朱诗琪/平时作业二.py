import random
import string
import json  # 用于解析外部传入的 JSON 数据 (假设外部数据是 JSON 格式)

def dataSampling_generator(specs):
    """
    使用生成器生成单个符合指定数据类型规范的样本。
    specs 是一个包含数据类型和参数的字典。
    """
    data_type = specs.get('type')
    if data_type == 'int':
        range_l, range_r = specs['datarange']
        yield random.randint(range_l, range_r)
    elif data_type == 'float':
        range_l, range_r = specs['datarange']
        yield random.uniform(range_l, range_r)
    elif data_type == 'str':
        chars = specs['datarange']
        length = specs['len']
        yield ''.join(random.choice(chars) for _ in range(length))
    elif data_type == 'tuple':
        elements_specs = specs.get('elements', [])
        yield tuple(next(dataSampling_generator(elem_spec)) for elem_spec in elements_specs)
    elif data_type == 'list':
        count = specs.get('count', 1)
        item_spec = specs.get('item_spec')
        if item_spec:
            yield [next(dataSampling_generator(item_spec)) for _ in range(count)]
        else:
            yield []
    else:
        yield None  # 处理未知数据类型

def dataScreening_external(num_samples, external_data_specs):
    """
    使用生成器解析外部传入的数据结构规范，并生成指定数量的样本。
    external_data_specs 应该是描述所需数据结构的字典。
    """
    for _ in range(num_samples):
        yield next(dataSampling_generator(external_data_specs))

def process_and_output(data_generator, num_to_output=10):
    """
    处理数据生成器并输出指定数量的样本。
    """
    print(f"输出前 {num_to_output} 个样本:")
    for i, sample in enumerate(data_generator):
        print(f"Sample {i+1}: {sample}")
        if i >= num_to_output - 1:
            break

if __name__ == "__main__":
    # 模拟外部传入的数据结构规范 (可以是 JSON 字符串或 Python 字典)
    external_data_format_str = """
    {
        "type": "list",
        "count": 5,
        "item_spec": {
            "type": "tuple",
            "elements": [
                {"type": "int", "datarange": [1, 100]},
                {"type": "str", "datarange": "abc", "len": 3},
                {"type": "float", "datarange": [0.0, 1.0]}
            ]
        }
    }
    """

    # 将 JSON 字符串解析为 Python 字典
    try:
        external_data_specs = json.loads(external_data_format_str)
    except json.JSONDecodeError as e:
        print(f"解析外部数据格式失败: {e}")
        external_data_specs = {}

    if external_data_specs:
        num_samples_to_generate = 100000000
        data_generator = dataScreening_external(num_samples_to_generate, external_data_specs)

        # 输出前 20 个样本 (可以根据需要调整输出数量)
        process_and_output(data_generator, num_to_output=20)

        print(f"\n已创建可以生成 {num_samples_to_generate} 个样本的生成器。")
        print("可以迭代 data_generator 来逐个获取样本，避免一次性加载到内存。")

        # 示例：迭代生成器获取后续的几个样本
        # print("\n获取接下来的 5 个样本:")
        # for i in range(5):
        #     try:
        #         print(f"Next Sample {i+1}: {next(data_generator)}")
        #     except StopIteration:
        #         print("生成器已耗尽。")
        #         break