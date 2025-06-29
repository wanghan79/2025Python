import string
import random
from typing import Generator, Any, Dict, Union, List, Tuple, Callable
from functools import wraps


def stats_operations(*operations):
    """
    统计操作装饰器工厂函数
    支持SUM、AVG、MAX、MIN四种统计操作
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 执行原函数获取结果
            result = list(func(*args, **kwargs))

            # 如果结果为空，直接返回
            if not result:
                print("无数据可统计")
                return result

            # 统计计算
            stats = {}
            numeric_data = []

            # 提取数值型数据
            for item in result:
                if isinstance(item, (int, float)):
                    numeric_data.append(item)
                elif isinstance(item, (list, tuple)):
                    numeric_data.extend([x for x in item if isinstance(x, (int, float))])
                elif isinstance(item, dict):
                    numeric_data.extend([v for v in item.values() if isinstance(v, (int, float))])

            # 如果没有数值数据，直接返回
            if not numeric_data:
                print("数据中不包含可统计的数值")
                return result

            # 执行请求的统计操作
            for op in operations:
                op = op.upper()
                if op == 'SUM':
                    stats['总和'] = sum(numeric_data)
                elif op == 'AVG':
                    stats['平均值'] = sum(numeric_data) / len(numeric_data)
                elif op == 'MAX':
                    stats['最大值'] = max(numeric_data)
                elif op == 'MIN':
                    stats['最小值'] = min(numeric_data)
                else:
                    print(f"未知操作: {op}")

            # 打印统计结果
            print("\n统计结果:")
            for k, v in stats.items():
                print(f"{k}: {v:.2f}" if isinstance(v, float) else f"{k}: {v}")

            return result

        return wrapper

    return decorator


class RandomDataMaker:
    """随机数据生成器"""

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

                for k, v in zip(keys, values):
                    output[k] = v
        return output

    @classmethod
    def generate(cls, data_type: str, options: Dict[str, Any]) -> Generator[Any, None, None]:
        """数据生成核心方法"""
        quantity = options.get('count', 1)

        for _ in range(quantity):
            if data_type == 'int':
                yield cls.make_number(*options['range'])
            elif data_type == 'float':
                yield cls.make_decimal(
                    *options['range'],
                    options.get('decimal')
                )
            elif data_type == 'str':
                yield cls.make_text(
                    options.get('length', 1),
                    options.get('chars', string.ascii_letters)
                )
            elif data_type == 'bool':
                yield cls.make_boolean()
            elif data_type == 'choice':
                yield cls.pick_random(options.get('items', []))
            elif data_type in ('list', 'tuple'):
                yield cls.make_collection(
                    list if data_type == 'list' else tuple,
                    {k: v for k, v in options.items() if k != 'count'}
                )
            elif data_type == 'dict':
                yield cls.make_dictionary(
                    {k: v for k, v in options.items() if k != 'count'}
                )
            elif data_type in ('key', 'value'):
                for nested_type, nested_conf in options.items():
                    yield from cls.generate(nested_type, nested_conf)


@stats_operations('SUM', 'AVG', 'MAX', 'MIN')
def create_samples(**kwargs) -> Generator[Any, None, None]:
    """创建数据样本"""
    for sample_type, config in kwargs.items():
        yield from RandomDataMaker.generate(sample_type, config)


def create_batch(size: int, **kwargs) -> List[Any]:
    """批量生成数据"""
    generator = create_samples(**kwargs)
    return [next(generator) for _ in range(size)]


if __name__ == '__main__':
    print("示例1：生成随机数据并统计")
    samples = create_samples(
        int={'count': 5, 'range': (1, 100)},
        float={'count': 3, 'range': (10.5, 20.5), 'decimal': 2}
    )
    print("\n生成的样本:")
    for sample in samples:
        print(sample)

    print("\n示例2：生成复杂结构数据并统计")
    samples = create_samples(
        list={
            'count': 2,
            'int': {'count': 3, 'range': (50, 150)},
            'float': {'count': 2, 'range': (5.5, 15.5), 'decimal': 1}
        }
    )
    print("\n生成的样本:")
    for sample in samples:
        print(sample)

    print("\n示例3：自定义统计操作")


    @stats_operations('SUM', 'AVG')
    def custom_samples(**kwargs):
        for sample_type, config in kwargs.items():
            yield from RandomDataMaker.generate(sample_type, config)


    samples = custom_samples(
        int={'count': 10, 'range': (1, 20)},
        float={'count': 5, 'range': (1.0, 5.0)}
    )
    print("\n生成的样本:")
    for sample in samples:
        print(sample)