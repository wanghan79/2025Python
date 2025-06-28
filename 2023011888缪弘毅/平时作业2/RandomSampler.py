import random
import string

# 样本生成器函数
def sample_generator(count, schema):
    # 内部辅助函数，用于生成指定类型的数据
    def sampling(data_type, config):
        if data_type == 'int':
            # 生成一个指定范围内的整数
            return random.randint(config[0], config[1])
        elif data_type == 'float':
            # 生成一个指定范围内的浮点数，保留两位小数
            return round(random.uniform(config[0], config[1]), 2)
        elif data_type == 'str':
            # 生成一个指定长度的随机字符串（只含字母）
            return ''.join(random.choices(string.ascii_letters, k=config[0]))
        elif data_type in ['list', 'tuple']:
            # 生成列表或元组，支持嵌套子类型（例如多个字符串或多个浮点数）
            elements = []
            for sub_type, sub_config in config.items():
                if sub_type != 'num':  # 'num' 表示生成多少个元素，跳过它
                    # 重复生成 num 次指定类型的元素
                    sub_elements = [sampling(sub_type, sub_config) for _ in range(config.get('num', 1))]
                    elements.extend(sub_elements)  # 添加到结果中
            # 根据 data_type 类型返回 list 或 tuple
            return elements if data_type == 'list' else tuple(elements)
        else:
            # 不支持的类型，返回 None
            return None

    # 生成 count 个样本
    for _ in range(count):
        sample = {}  # 当前样本，字典形式
        for key, rule in schema.items():
            data_type = rule[0]  # 类型名，如 'int'、'str'、'list'
            if data_type in ['int', 'float', 'str']:
                # 简单类型直接调用 sampling
                sample[key] = sampling(data_type, rule[1:])
            elif data_type in ['list', 'tuple']:
                # 列表或元组类型，传递子结构
                sample[key] = sampling(data_type, rule[1])
            else:
                sample[key] = None  # 未知类型
        yield sample  # 使用生成器逐个返回样本

# 定义生成样本的数据结构（schema）
schema = {
    'id': ('int', 1000, 9999),                     # id 字段，随机整数，范围 1000~9999
    'name': ('str', 6),                            # name 字段，长度为 6 的随机字符串
    'score': ('float', 0, 100),                    # score 字段，随机浮点数，范围 0~100
    'tags': ('list', {                             # tags 字段，包含多个字符串的列表
        'str': (4,),                               # 每个字符串长度为 4
        'num': 3                                   # 列表包含 3 个元素
    }),
    'coordinates': ('tuple', {                     # coordinates 字段，包含多个浮点数的元组
        'float': (0.0, 1.0),                       # 每个浮点数范围 0.0 ~ 1.0
        'num': 2                                   # 元组包含 2 个元素
    })
}


# 生成 2 个样本并打印
gen = sample_generator(2, schema)
for sample in gen:
    print(sample)
