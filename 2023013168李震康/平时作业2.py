import random
import string
from typing import List, Dict, Any, Iterator, Optional


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

    # 生成5个随机样本
    print("生成5个人员样本:")
    for i, sample in enumerate(random_sample_generator(5, person_structure, seed=42), 1):
        print(f"样本 {i}: {sample}")

    print("\n生成3个不同的样本:")
    for i, sample in enumerate(random_sample_generator(3, person_structure), 1):
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

    print("\n生成2个复杂的订单样本:")
    for i, sample in enumerate(random_sample_generator(2, complex_structure), 1):
        print(f"样本 {i}: {sample}")


if __name__ == "__main__":
    example_usage()
