import random
from typing import Dict, List, Union, Any, Generator

class RandomSampleGenerator:
    def __init__(self):
        self._data_types = {
            'int': lambda: random.randint(0, 100),
            'float': lambda: round(random.uniform(0, 100), 2),
            'str': lambda: ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5)),
            'bool': lambda: random.choice([True, False]),
            'list': lambda: [self._generate_value('int') for _ in range(3)],
            'dict': lambda: {'key': self._generate_value('str'), 'value': self._generate_value('int')}
        }

    def _generate_value(self, data_type: str) -> Any:
        """生成单个随机值"""
        return self._data_types.get(data_type, lambda: None)()

    def generate_samples(
        self,
        sample_structure: Dict[str, str],
        num_samples: int = 1,
        seed: Union[int, None] = None
    ) -> Generator[Dict[str, Any], None, None]:
        """
        生成随机样本的生成器
        :param sample_structure: 样本结构定义，如 {'id': 'int', 'name': 'str', 'scores': 'list'}
        :param num_samples: 生成样本数量
        :param seed: 随机种子（可选）
        :return: 生成器，每次yield一个样本字典
        """
        if seed is not None:
            random.seed(seed)

        for _ in range(num_samples):
            yield {
                field: self._generate_value(data_type)
                for field, data_type in sample_structure.items()
            }

# ==================== 使用示例 ====================
if __name__ == "__main__":
    generator = RandomSampleGenerator()

    user_structure = {
        'user_id': 'int',
        'username': 'str',
        'is_active': 'bool',
        'credit_score': 'float'
    }
    print("=== 用户样本 ===")
    for i, sample in enumerate(generator.generate_samples(user_structure, num_samples=5, seed=42)):
        print(f"样本{i+1}: {sample}")

    product_structure = {
        'product_id': 'int',
        'name': 'str',
        'price': 'float',
        'tags': 'list',
        'metadata': 'dict',
        'in_stock': 'bool'
    }
    print("\n=== 产品样本 ===")
    for i, sample in enumerate(generator.generate_samples(product_structure, num_samples=3)):
        print(f"样本{i+1}: {sample}")

    print("\n=== 流式处理10万样本 ===")
    large_generator = generator.generate_samples(
        {'transaction_id': 'int', 'amount': 'float'},
        num_samples=100000
    )
    for _ in range(3):  # 只展示前3个
        print(next(large_generator))