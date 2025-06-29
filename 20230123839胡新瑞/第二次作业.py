"""
随机数据生成工具
支持生成各种类型的随机数据，包括数字、字符串、布尔值、列表、字典等
"""

import string
import random
from typing import Generator, Any, Dict, Union, List, Tuple


class RandomDataMaker:
    """我的随机数据生成器"""

    @classmethod
    def make_number(cls, min_val: int, max_val: int) -> int:
        """生成指定范围内的随机整数"""
        return random.randint(min_val, max_val)

    @classmethod
    def make_decimal(cls, min_val: float, max_val: float, decimal_places: int = None) -> float:
        """生成随机浮点数，可指定小数位数"""
        num = random.uniform(min_val, max_val)
        return round(num, decimal_places) if decimal_places is not None else num

    @classmethod
    def make_text(cls, length: int, chars: str = string.ascii_letters) -> str:
        """生成随机字符串"""
        return ''.join(random.choice(chars) for _ in range(length))

    @classmethod
    def make_boolean(cls) -> bool:
        """随机生成True或False"""
        return random.choice([True, False])

    @classmethod
    def pick_random(cls, items: List[Any]) -> Any:
        """从列表中随机选取一个元素"""
        return random.choice(items)

    @classmethod
    def make_collection(cls, col_type: type, elements: Dict[str, Dict]) -> Union[List, Tuple]:
        """生成列表或元组集合"""
        result = []
        for elem_type, elem_conf in elements.items():
            if elem_type != 'count':
                generated = list(cls.generate(elem_type, elem_conf))
                result.extend(generated)
        return col_type(result)

    @classmethod
    def make_dictionary(cls, items: Dict[str, Dict]) -> Dict[Any, Any]:
        """生成字典数据"""
        output = {}
        for item_name, item_conf in items.items():
            if item_name != 'count':
                key_conf = item_conf.get('key', {})
                val_conf = item_conf.get('value', {})

                keys = list(cls.generate('key', key_conf)) if key_conf else []
                values = list(cls.generate('value', val_conf)) if val_conf else []
