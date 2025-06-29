import random
import string
from typing import Dict, Any, List, Tuple, Callable
from functools import wraps

# 统计操作类型
STATS_OPS = {
    'SUM': sum,
    'AVG': lambda x: sum(x) / len(x) if x else 0,
    'MAX': max,
    'MIN': min
}


def stats_decorator(*operations: str):
    """
    带参修饰器，用于对生成器函数进行统计操作

    参数:
        operations: 统计操作列表，可选'SUM', 'AVG', 'MAX', 'MIN'

    返回:
        装饰后的函数，会输出指定统计结果
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 调用原函数获取结果
            results = func(*args, **kwargs)

            # 如果不是列表，转换为列表处理
            if not isinstance(results, list):
                results = [results]

            # 分别收集整数和浮点数
            int_values = []
            float_values = []

            for sample in results:
                # 递归收集数值
                def collect_numbers(data):
                    if isinstance(data, int):
                        int_values.append(data)
                    elif isinstance(data, float):
                        float_values.append(data)
                    elif isinstance(data, (list, tuple)):
                        for item in data:
                            collect_numbers(item)
                    elif isinstance(data, dict):
                        for value in data.values():
                            collect_numbers(value)

                collect_numbers(sample)

            # 执行统计操作
            print("\n统计结果:")

            # 整数统计
            if int_values:
                print("=== 整数统计 ===")
                for op in operations:
                    if op in STATS_OPS:
                        try:
                            value = STATS_OPS[op](int_values)
                            print(f"{op}: {value}")
                        except Exception as e:
                            print(f"无法计算整数 {op}: {str(e)}")
                    else:
                        print(f"未知统计操作: {op}")
            else:
                print("没有找到可统计的整数数据")

            # 浮点数统计
            if float_values:
                print("\n=== 浮点数统计 ===")
                for op in operations:
                    if op in STATS_OPS:
                        try:
                            value = STATS_OPS[op](float_values)
                            print(f"{op}: {value:.4f}")
                        except Exception as e:
                            print(f"无法计算浮点数 {op}: {str(e)}")
                    else:
                        print(f"未知统计操作: {op}")
            else:
                print("没有找到可统计的浮点数数据")

            print()

            return results

        return wrapper

    return decorator


class RandomSampleGenerator:
    """
    随机样本生成器，根据用户定义的结构和数量生成随机样本

    添加了分类型统计功能
    """

    def __init__(self):
        self.supported_types = {int, float, str, list, tuple, dict}

    def _generate_value(self, type_def: Dict[type, Dict]) -> Any:
        """根据类型定义生成单个值"""
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

    @stats_decorator('SUM', 'AVG', 'MAX', 'MIN')  # 默认应用所有统计操作
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

    # 生成5个样本(会自动应用统计)
    print("生成样本并自动统计:")
    samples = generator.generate_samples(sample_structure, 5)

    # 打印结果
    for i, sample in enumerate(samples, 1):
        print(f"样本 {i}: {sample}")

    # 自定义统计操作的例子
    print("\n自定义统计操作示例:")


    @stats_decorator('AVG', 'MAX')
    def custom_generate_samples(generator, structure, num_samples):
        return generator.generate_samples(structure, num_samples)


    # 生成3个样本，只计算平均值和最大值
    samples = custom_generate_samples(generator, sample_structure, 3)
    for i, sample in enumerate(samples, 1):
        print(f"样本 {i}: {sample}")