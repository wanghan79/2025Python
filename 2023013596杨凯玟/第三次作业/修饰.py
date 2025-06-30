from functools import wraps
from typing import Callable, Dict, List, Union
import time


def stats_operations(*operations: str):
    """
    带参装饰器工厂，支持动态指定统计操作
    可用操作: 'SUM', 'AVG', 'MAX', 'MIN'
    """

    def decorator(generator_func: Callable):
        @wraps(generator_func)
        def wrapper(*args, **kwargs):
            stats = {
                'SUM': {},
                'AVG': {'count': 0},
                'MAX': {},
                'MIN': {}
            }
            start_time = time.time()
            for sample in generator_func(*args, **kwargs):
                yield sample

                for field, value in sample.items():
                    if isinstance(value, (int, float)):
                        # SUM统计
                        if 'SUM' in operations:
                            stats['SUM'][field] = stats['SUM'].get(field, 0) + value

                        # AVG统计
                        if 'AVG' in operations:
                            stats['AVG'][field] = stats['AVG'].get(field, 0) + value
                            stats['AVG']['count'] += 1

                        # MAX统计
                        if 'MAX' in operations:
                            if field not in stats['MAX'] or value > stats['MAX'][field]:
                                stats['MAX'][field] = value

                        # MIN统计
                        if 'MIN' in operations:
                            if field not in stats['MIN'] or value < stats['MIN'][field]:
                                stats['MIN'][field] = value
            results = {}
            for op in operations:
                if op == 'AVG' and stats['AVG']['count'] > 0:
                    results['AVG'] = {
                        field: round(total / stats['AVG']['count'], 2)
                        for field, total in stats['AVG'].items()
                        if field != 'count'
                    }
                else:
                    results[op] = stats[op]

            print(f"\n=== 统计结果（耗时{time.time() - start_time:.2f}s）===")
            for op, values in results.items():
                print(f"{op}: {values}")

        return wrapper

    return decorator


# ==================== 使用示例 ====================
class EnhancedSampleGenerator(RandomSampleGenerator):
    @stats_operations('SUM', 'AVG', 'MAX', 'MIN')
    def generate_numeric_samples(self, fields: List[str], num_samples: int):
        """生成只包含数值字段的样本"""
        structure = {field: random.choice(['int', 'float']) for field in fields}
        yield from self.generate_samples(structure, num_samples)


if __name__ == "__main__":

    print("=== 全统计模式 ===")
    gen = EnhancedSampleGenerator()
    for sample in gen.generate_numeric_samples(['price', 'quantity', 'rating'], 1000):
        pass  # 只需迭代即可触发统计

    print("\n=== 自定义统计组合 ===")
    gen = EnhancedSampleGenerator()


    @stats_operations('SUM', 'AVG')
    def financial_data(num):
        structure = {'revenue': 'float', 'cost': 'float'}
        yield from gen.generate_samples(structure, num)


    for data in financial_data(500):
        pass  # 自动计算SUM和AVG