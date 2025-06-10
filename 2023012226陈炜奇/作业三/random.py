import random
import string
from functools import wraps

# 统计操作类型
SUM = "SUM"
AVG = "AVG"
MAX = "MAX"
MIN = "MIN"


def statistic_operation(*stat_ops):
    """
    带参修饰器，用于对随机样本生成函数进行统计操作修饰
    支持SUM、AVG、MAX、MIN四种统计操作的任意组合

    Args:
        *stat_ops: 统计操作类型列表

    Returns:
        修饰器函数
    """
    # 检查统计操作是否合法
    valid_ops = {SUM, AVG, MAX, MIN}
    if not all(op in valid_ops for op in stat_ops):
        raise ValueError("Invalid statistic operation")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 调用原始函数生成样本数据
            samples = func(*args, **kwargs)

            # 对所有样本数据进行统计操作
            results = {}
            for key in samples[0]:
                if isinstance(samples[0][key], (int, float)):
                    values = [sample[key] for sample in samples]

                    # 执行所有指定的统计操作
                    if SUM in stat_ops:
                        results[f"{key}_{SUM}"] = sum(values)
                    if AVG in stat_ops:
                        results[f"{key}_{AVG}"] = sum(values) / len(values)
                    if MAX in stat_ops:
                        results[f"{key}_{MAX}"] = max(values)
                    if MIN in stat_ops:
                        results[f"{key}_{MIN}"] = min(values)

            # 输出统计结果
            print("\n统计结果:")
            for key, value in results.items():
                print(f"{key}: {value}")

            return samples

        return wrapper

    return decorator


class RandomSampleGenerator:
    def __init__(self, num_samples, structure):
        """初始化随机样本生成器

        Args:
            num_samples: 需要生成的样本数量
            structure: 定义样本结构的字典
        """
        self.num_samples = num_samples
        self.structure = structure

    def generate_data(self, structure):
        """根据定义的结构生成数据

        Args:
            structure: 定义数据结构的字典

        Returns:
            生成的数据
        """
        if 'type' not in structure:
            return None

        data_type = structure['type']

        if data_type == 'int':
            dr = structure.get('datarange', [0, 100])
            return random.randint(dr[0], dr[1])

        elif data_type == 'float':
            dr = structure.get('datarange', [0.0, 100.0])
            return round(random.uniform(dr[0], dr[1]), 2)

        elif data_type == 'str':
            dr = structure.get('datarange', string.ascii_letters)
            length = structure.get('len', 8)
            return ''.join(random.choices(dr, k=length))

        elif data_type == 'list':
            elements = structure.get('elements', [])
            size = structure.get('size', random.randint(1, 10))
            if elements:
                return [self.generate_data(elements[0]) for _ in range(size)]
            else:
                return []

        elif data_type == 'dict':
            keys = structure.get('keys', {})
            return {k: self.generate_data(v) for k, v in keys.items()}

        elif data_type == 'tuple':
            elements = structure.get('elements', [])
            return tuple(self.generate_data(e) for e in elements)

        else:
            return None

    def generate_samples(self):
        """生成指定数量的随机样本

        Returns:
            包含所有随机样本的列表
        """
        samples = []
        for _ in range(self.num_samples):
            sample = {}
            for key, value in self.structure.items():
                sample[key] = self.generate_data(value)
            samples.append(sample)
        return samples

    @classmethod
    def from_manual_config(cls, num_samples, structure):
        """从手动配置创建生成器实例

        Args:
            num_samples: 样本数量
            structure: 样本结构定义

        Returns:
            RandomSampleGenerator 实例
        """
        return cls(num_samples, structure)


@statistic_operation(SUM, AVG, MAX, MIN)
def generate_samples_with_statistics(num_samples, structure):
    generator = RandomSampleGenerator(num_samples, structure)
    return generator.generate_samples()


if __name__ == "__main__":
    # 定义结构
    structure = {
        "int_field": {"type": "int", "datarange": [1, 100]},
        "float_field": {"type": "float", "datarange": [0.0, 100.0]},
        "str_field": {"type": "str", "datarange": string.ascii_uppercase, "len": 8},
        "list_field": {
            "type": "list",
            "elements": [{"num": {"type": "int", "datarange": [1, 10]}}],
            "size": 5
        },
        "dict_field": {
            "type": "dict",
            "keys": {
                "key1": {"type": "int", "datarange": [1, 10]},
                "key2": {"type": "str", "datarange": string.ascii_lowercase, "len": 5}
            }
        },
        "tuple_field": {
            "type": "tuple",
            "elements": [
                {"type": "int", "datarange": [1, 10]},
                {"type": "str", "datarange": string.digits, "len": 4}
            ]
        }
    }

    # 生成样本并进行统计
    samples = generate_samples_with_statistics(10, structure)

    # 打印生成的样本
    print("\n生成的随机样本:")
    for i, sample in enumerate(samples):
        print(f"样本 {i + 1}: {sample}")
