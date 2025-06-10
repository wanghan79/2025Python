import random
import string
from typing import Any, Dict, List, Union, Iterable


class RandomGenerator:


    @staticmethod
    def generate(config: Dict[str, Any]) -> List[Any]:

        num = config.get('num', 1)
        result = []

        for _ in range(num):
            item = RandomGenerator._generate_item(config)
            result.append(item)

        return result

    @staticmethod
    def _generate_item(config: Dict[str, Any]) -> Any:

        if isinstance(config, dict) and 'type' in config:
            # 处理显式类型声明
            return RandomGenerator._generate_by_type(config)
        elif isinstance(config, dict):
            # 处理字典结构
            return {k: RandomGenerator._generate_item(v) for k, v in config.items() if k != 'num'}
        elif isinstance(config, (list, tuple)):
            # 处理列表或元组结构
            return type(config)(RandomGenerator._generate_item(item) for item in config)
        else:
            return config

    @staticmethod
    def _generate_by_type(type_config: Dict[str, Any]) -> Any:
        
        data_type = type_config['type']
        params = type_config.get('params', {})

        if data_type == 'int':
            return random.randint(params.get('min', 0), params.get('max', 100))
        elif data_type == 'float':
            return round(random.uniform(params.get('min', 0), params.get('max', 1.0)), params.get('precision', 2))
        elif data_type == 'str':
            length = params.get('length', 10)
            charset = params.get('charset', string.ascii_letters + string.digits)
            return ''.join(random.choices(charset, k=length))
        elif data_type == 'bool':
            return random.choice([True, False])
        elif data_type == 'choice':
            return random.choice(params['options'])
        elif data_type == 'list':
            length = params.get('length', 5)
            return [RandomGenerator._generate_by_type(params['item_type']) for _ in range(length)]
        elif data_type == 'dict':
            return {k: RandomGenerator._generate_by_type(v) for k, v in params['structure'].items()}
        else:
            raise ValueError(f"Unsupported data type: {data_type}")


# 使用示例
if __name__ == "__main__":
    # 示例1: 生成基本数据类型
    print("基本数据类型示例:")
    config1 = {
        'num': 3,
        'id': {'type': 'int', 'params': {'min': 1, 'max': 1000}},
        'name': {'type': 'str', 'params': {'length': 8}},
        'score': {'type': 'float', 'params': {'min': 0, 'max': 100, 'precision': 1}},
        'active': {'type': 'bool'}
    }
    print(RandomGenerator.generate(config1))

    # 示例2: 生成嵌套结构数据
    print("\n嵌套结构示例:")
    config2 = {
        'num': 2,
        'user': {
            'id': {'type': 'int'},
            'username': {'type': 'str', 'params': {'length': 6}},
            'preferences': {
                'theme': {'type': 'choice', 'params': {'options': ['light', 'dark', 'system']}},
                'notifications': {'type': 'bool'}
            },
            'scores': {'type': 'list', 'params': {
                'item_type': {'type': 'int', 'params': {'min': 1, 'max': 10}},
                'length': 3
            }}
        }
    }
    print(RandomGenerator.generate(config2))

    # 示例3: 生成复杂数据结构
    print("\n复杂数据结构示例:")
    config3 = {
        'num': 2,
        'data': [
            {'type': 'int', 'params': {'min': 100, 'max': 200}},
            {'type': 'str', 'params': {'charset': string.ascii_uppercase, 'length': 4}},
            {
                'type': 'dict',
                'params': {
                    'structure': {
                        'key1': {'type': 'float'},
                        'key2': {'type': 'choice', 'params': {'options': ['A', 'B', 'C']}}
                    }
                }
            }
        ]
    }
    print(RandomGenerator.generate(config3))