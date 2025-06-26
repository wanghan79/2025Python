import random
import string


def generate_random_data(struct, **kwargs):
    """
    根据 struct 字典生成随机数据，使用生成器实现。
    struct 字典的格式如下：
    {
        数据类型: {
            数据类型: {"datarange": 范围, "len": 长度},
            ...
        },
        ...
    }
    kwargs 可以包含额外的参数，如 'num' 表示生成的组数。
    """
    num = kwargs.get('num', 1)  # 获取生成的组数，默认为1

    for _ in range(num):
        group = {}
        for data_type, config in struct.items():
            if data_type == 'num':
                continue
            group[data_type] = generate_item(data_type, config)
        # 将生成的数据转换为元组（如果需要）
        yield tuple(group.values()) if isinstance(group, dict) else group


def generate_item(data_type, config):
    """
    根据数据类型和配置生成单个随机数据项。
    """
    if data_type == int:
        return random.randint(*config["datarange"])
    elif data_type == float:
        return random.uniform(*config["datarange"])
    elif data_type == str:
        return ''.join(random.choices(config["datarange"], k=config["len"]))
    elif data_type == list or data_type == tuple:
        # 递归生成子节点
        return generate_sequence(data_type, config)
    elif data_type == dict:
        # 递归生成字典
        return dict(next(generate_random_data(config)))
    else:
        raise ValueError(f"Unsupported data type: {data_type}")


def generate_sequence(sequence_type, config):
    """
    生成列表或元组。
    """
    result = []
    for item_type, item_config in config.items():
        if isinstance(item_config, dict) and "num" in item_config:
            # 递归生成嵌套结构
            result.append(list(generate_random_data(item_config)))
        else:
            result.append(generate_item(item_type, item_config))
    return sequence_type(result)


# 定义 struct 字典
struct = {
    'num': 2,  # 生成 2 组数据
    tuple: {
        str: {"datarange": string.ascii_uppercase, "len": 3},  # 生成长度为 3 的随机大写字母字符串
        bool: {},  # 随机布尔值
        list: {
            int: {"datarange": (0, 10)},  # 生成 0-10 的随机整数
            float: {"datarange": (0, 1.0)},  # 生成 0-1.0 的随机浮点数
            set: {  # 生成包含随机字符串的集合
                str: {"datarange": string.ascii_lowercase, "len": 2},
                'num': 3  # 集合中有 3 个元素
            },
            dict: {
                'num': 2,  # 嵌套结构生成 2 组数据
                tuple: {
                    str: {"datarange": string.ascii_uppercase, "len": 3},
                    bool: {}  # 随机布尔值
                },
                list: {
                    int: {"datarange": (0, 10)},
                    float: {"datarange": (0, 1.0)}
                }
            }
        }
    }
}

# 调用函数生成随机数据
generated_data = list(generate_random_data(struct, num=struct['num']))
# 逐行打印每条数据
for data in generated_data:
    print(data)


