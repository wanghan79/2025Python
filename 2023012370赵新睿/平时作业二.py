import random
import string
from typing import Dict, Any, Union, List, Tuple


class RandomSampleGenerator:
    """
    随机样本生成器，根据用户定义的结构和数量生成随机样本

    特性:
    - 支持多种数据类型: int, float, str, list, tuple, dict
    - 支持嵌套数据结构
    - 支持自定义范围和约束条件
    - 支持控制生成样本数量
    - 完善的错误处理
    """

    def __init__(self):
        self.supported_types = {int, float, str, list, tuple, dict}

    def _generate_value(self, type_def: Dict[type, Dict]) -> Any:
        """
        根据类型定义生成单个值

        参数:
            type_def: 类型定义字典，键为类型，值为生成规则

        返回:
            生成的随机值
        """
        if not isinstance(type_def, dict) or len(type_def) != 1:
            raise ValueError("类型定义必须是一个包含单个键值对的字典")

        data_type, rules = next(iter(type_def.items()))

        if data_type not in self.supported_types:
            raise ValueError(f"不支持的数据类型: {data_type}")

        # 生成整数
        if data_type is int:
            if 'datarange' not in rules or len(rules['datarange']) != 2:
                raise ValueError("整数类型需要'datarange'参数，且必须是长度为2的元组")

            min_val, max_val = rules['datarange']
            value = random.randint(min_val, max_val)

            if 'constraint' in rules:
                while not rules['constraint'](value):
                    value = random.randint(min_val, max_val)
            return value

        # 生成浮点数
        elif data_type is float:
            if 'datarange' not in rules or len(rules['datarange']) != 2:
                raise ValueError("浮点数类型需要'datarange'参数，且必须是长度为2的元组")

            min_val, max_val = rules['datarange']
            value = random.uniform(min_val, max_val)

            if 'constraint' in rules:
                while not rules['constraint'](value):
                    value = random.uniform(min_val, max_val)
            return value

        # 生成字符串
        elif data_type is str:
            if 'datarange' not in rules:
                raise ValueError("字符串类型需要'datarange'参数")
            if 'len' not in rules:
                raise ValueError("字符串类型需要'len'参数")

            chars = rules['datarange']
            length = rules['len']
            value = ''.join(random.choice(chars) for _ in range(length))

            if 'constraint' in rules:
                while not rules['constraint'](value):
                    value = ''.join(random.choice(chars) for _ in range(length))
            return value

        # 生成字典
        elif data_type is dict:
            if not rules:
                raise ValueError("字典类型需要定义键值对生成规则")

            key_type_def = rules.get('key', {str: {'datarange': string.ascii_letters, 'len': 5}})
            value_type_def = rules.get('value', {int: {'datarange': (0, 100)}})

            key = self._generate_value(key_type_def)
            value = self._generate_value(value_type_def)
            return {key: value}

        # 生成列表
        elif data_type is list:
            if not rules:
                raise ValueError("列表类型需要定义元素生成规则")

            length = rules.get('length', 3)  # 默认长度3
            element_def = {k: v for k, v in rules.items() if k != 'length'}

            if not element_def:
                raise ValueError("列表类型需要定义元素类型")

            return [self._generate_value(element_def) for _ in range(length)]

        # 生成元组
        elif data_type is tuple:
            if not rules:
                raise ValueError("元组类型需要定义元素生成规则")

            element_defs = []
            for elem_type, elem_rules in rules.items():
                if elem_type == 'length':
                    continue
                element_defs.append({elem_type: elem_rules})

            if not element_defs:
                raise ValueError("元组类型需要定义元素类型")

            return tuple(self._generate_value(def_) for def_ in element_defs)

    def generate_samples(self, structure: Dict, num_samples: int = 1) -> List[Any]:
        """
        生成指定数量的随机样本

        参数:
            structure: 数据结构定义
            num_samples: 要生成的样本数量

        返回:
            生成的样本列表
        """
        if not isinstance(structure, dict):
            raise ValueError("结构定义必须是一个字典")

        if num_samples < 1:
            raise ValueError("样本数量必须大于0")

        return [self._generate_value(structure) for _ in range(num_samples)]


# 使用示例
if __name__ == "__main__":
    generator = RandomSampleGenerator()

    # 定义数据结构
    sample_structure = {
        tuple: {
            int: {
                'datarange': (1, 100),
                'constraint': lambda x: x % 2 == 0  # 只生成偶数
            },
            float: {
                'datarange': (0.0, 1.0),
                'constraint': lambda x: x > 0.5  # 只生成大于0.5的数
            },
            str: {
                'datarange': string.ascii_letters + string.digits,
                'len': 8,
                'constraint': lambda s: any(c.isdigit() for c in s)  # 必须包含数字
            },
            list: {
                dict: {
                    'key': {str: {'datarange': string.ascii_lowercase, 'len': 3}},
                    'value': {int: {'datarange': (1, 10)}}
                },
                'length': 2  # 列表长度为2
            }
        }
    }

    # 生成5个样本
    samples = generator.generate_samples(sample_structure, 5)

    # 打印结果
    for i, sample in enumerate(samples, 1):
        print(f"样本 {i}: {sample}")