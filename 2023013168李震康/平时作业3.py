import random
import string
from typing import List, Dict, Any, Iterator, Optional, Callable, Union, Tuple, Set


def statistics_decorator(operations: List[str], fields: List[str] = None) -> Callable:

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Iterator[Dict[str, Any]]:
            # 存储所有生成的样本
            all_samples = []

            # 生成样本并存储
            for sample in func(*args, **kwargs):
                all_samples.append(sample)
                yield sample

            # 如果没有样本，直接返回
            if not all_samples:
                return

            # 确定要统计的字段
            if fields is None:
                # 找出所有数值类型的字段
                numeric_fields = set()
                for sample in all_samples:
                    for field, value in sample.items():
                        if isinstance(value, (int, float)):
                            numeric_fields.add(field)
                fields_to_stat = list(numeric_fields)
            else:
                fields_to_stat = fields

            # 执行统计操作
            stats = {}
            for field in fields_to_stat:
                # 收集该字段的所有值
                values = [sample.get(field) for sample in all_samples
                          if isinstance(sample.get(field), (int, float))]

                if not values:
                    continue

                field_stats = {}
                for op in operations:
                    if op.upper() == 'SUM':
                        field_stats['SUM'] = sum(values)
                    elif op.upper() == 'AVG':
                        field_stats['AVG'] = sum(values) / len(values)
                    elif op.upper() == 'MAX':
                        field_stats['MAX'] = max(values)
                    elif op.upper() == 'MIN':
                        field_stats['MIN'] = min(values)

                if field_stats:
                    stats[field] = field_stats

            # 打印统计结果
            print("\n--- 统计结果 ---")
            for field, field_stats in stats.items():
                print(f"字段 '{field}':")
                for op, value in field_stats.items():
                    print(f"  {op}: {value}")
            print("---------------")

        return wrapper

    return decorator


def random_sample_generator(
        num_samples: int,
        sample_structure: Dict[str, Dict[str, Any]],
        seed: Optional[int] = None
) -> Iterator[Dict[str, Any]]:
    """
    生成随机样本的生成器函数

    参数:
    num_samples: 要生成的样本数量
    sample_structure: 样本结构定义，格式为:
        {字段名: {类型: 类型名, 参数: 参数值}}
        支持的类型: 'int', 'float', 'str', 'bool', 'choice', 'list'
    seed: 随机数生成器的种子，用于复现结果

    返回:
    生成器，每次生成一个随机样本
    """
    if seed is not None:
        random.seed(seed)

    # 支持的类型及其生成函数
    type_generators = {
        'int': lambda params: random.randint(params.get('min', 0), params.get('max', 100)),
        'float': lambda params: random.uniform(params.get('min', 0.0), params.get('max', 1.0)),
        'str': lambda params: ''.join(random.choices(
            string.ascii_letters + string.digits,
            k=params.get('length', 10)
        )),
        'bool': lambda params: random.choice([True, False]),
        'choice': lambda params: random.choice(params.get('options', [])),
        'list': lambda params: [
            random_sample_generator(1, {params.get('item_key', 'item'): params.get('item_structure', {})},
                                    seed=None).__next__()[params.get('item_key', 'item')]
            for _ in range(random.randint(params.get('min_length', 0), params.get('max_length', 5)))
        ]
    }

    # 生成指定数量的样本
    for _ in range(num_samples):
        sample = {}
        for field, config in sample_structure.items():
            field_type = config.get('type', 'int')
            field_params = config.get('params', {})

            if field_type in type_generators:
                sample[field] = type_generators[field_type](field_params)
            else:
                # 不支持的类型，默认为None
                sample[field] = None

        yield sample


# 使用范例
def example_usage():
    # 定义样本结构
    person_structure = {
        'id': {'type': 'int', 'params': {'min': 1000, 'max': 9999}},
        'name': {'type': 'str', 'params': {'length': 8}},
        'age': {'type': 'int', 'params': {'min': 18, 'max': 65}},
        'height': {'type': 'float', 'params': {'min': 150.0, 'max': 190.0}},
        'is_active': {'type': 'bool'},
        'role': {'type': 'choice', 'params': {'options': ['admin', 'user', 'guest']}},
        'hobbies': {'type': 'list', 'params': {
            'min_length': 1,
            'max_length': 4,
            'item_key': 'hobby',
            'item_structure': {'hobby': {'type': 'choice', 'params': {
                'options': ['reading', 'swimming', 'running', 'painting', 'coding']}}}
        }}
    }

    # 定义一个统计装饰器版本的生成器
    @statistics_decorator(operations=['SUM', 'AVG', 'MAX', 'MIN'])
    def generate_person_samples(num_samples, seed=None):
        return random_sample_generator(num_samples, person_structure, seed)

    # 生成5个随机样本并统计
    print("生成5个人员样本并进行统计:")
    for i, sample in enumerate(generate_person_samples(5, seed=42), 1):
        print(f"样本 {i}: {sample}")

    # 定义一个更复杂的结构
    complex_structure = {
        'order_id': {'type': 'str', 'params': {'length': 10}},
        'timestamp': {'type': 'float', 'params': {'min': 1600000000.0, 'max': 1700000000.0}},
        'items': {'type': 'list', 'params': {
            'min_length': 1,
            'max_length': 5,
            'item_key': 'item',
            'item_structure': {
                'product_id': {'type': 'int', 'params': {'min': 100, 'max': 999}},
                'name': {'type': 'choice', 'params': {'options': ['laptop', 'phone', 'tablet', 'headphones', 'mouse']}},
                'price': {'type': 'float', 'params': {'min': 10.0, 'max': 2000.0}},
                'quantity': {'type': 'int', 'params': {'min': 1, 'max': 10}},
                'attributes': {'type': 'list', 'params': {
                    'min_length': 0,
                    'max_length': 3,
                    'item_key': 'attribute',
                    'item_structure': {
                        'attribute': {'type': 'choice', 'params': {'options': ['color', 'size', 'weight', 'material']}},
                        'value': {'type': 'choice', 'params': {
                            'options': ['red', 'blue', 'green', 'small', 'medium', 'large', 'light', 'heavy', 'metal',
                                        'plastic']}}
                    }
                }}
            }
        }}
    }

    # 定义一个只统计特定字段的装饰器版本的生成器
    @statistics_decorator(operations=['SUM', 'AVG'], fields=['timestamp'])
    def generate_order_samples(num_samples, seed=None):
        return random_sample_generator(num_samples, complex_structure, seed)

    # 生成3个订单样本并统计
    print("\n生成3个订单样本并只统计timestamp字段:")
    for i, sample in enumerate(generate_order_samples(3, seed=42), 1):
        print(f"样本 {i}: {sample}")

    # 定义一个统计嵌套结构中字段的装饰器版本的生成器
    def extract_nested_values(samples, path):
        """提取嵌套结构中的值"""
        values = []
        for sample in samples:
            current = sample
            for key in path.split('.'):
                if isinstance(current, list):
                    # 处理列表情况
                    for item in current:
                        if isinstance(item, dict) and key in item:
                            values.append(item[key])
                    break
                elif isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    break
            else:
                # 如果路径完整匹配
                if not isinstance(current, (dict, list)):
                    values.append(current)
        return values

    @statistics_decorator(operations=['SUM', 'AVG', 'MAX', 'MIN'], fields=['items.price'])
    def generate_order_with_nested_stats(num_samples, seed=None):
        return random_sample_generator(num_samples, complex_structure, seed)

    # 生成2个订单样本并统计嵌套字段
    print("\n生成2个订单样本并统计嵌套字段:")
    for i, sample in enumerate(generate_order_with_nested_stats(2, seed=42), 1):
        print(f"样本 {i}: {sample}")


if __name__ == "__main__":
    example_usage()
