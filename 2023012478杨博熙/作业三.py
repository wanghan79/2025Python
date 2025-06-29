import functools
import random
from typing import List, Callable, Union


def stats_decorator(*operations: str):
    """
    带参修饰器，用于对随机样本生成函数进行统计操作

    参数:
        operations: 要执行的统计操作，可以是 'SUM', 'AVG', 'MAX', 'MIN' 中的任意组合
    """

    def decorator(func: Callable[..., List[Union[int, float]]]):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 调用原函数获取随机样本
            samples = func(*args, **kwargs)

            # 进行统计操作
            results = {}
            for op in operations:
                op = op.upper()
                if op == 'SUM':
                    results['SUM'] = sum(samples)
                elif op == 'AVG':
                    results['AVG'] = sum(samples) / len(samples) if samples else 0
                elif op == 'MAX':
                    results['MAX'] = max(samples) if samples else None
                elif op == 'MIN':
                    results['MIN'] = min(samples) if samples else None

            # 打印原始样本和统计结果
            print(f"原始样本: {samples}")
            print(f"统计结果: {results}")

            # 返回原始样本和统计结果
            return samples, results

        return wrapper

    return decorator


# 示例：生成随机整数样本
@stats_decorator('SUM', 'AVG', 'MAX', 'MIN')
def generate_random_integers(n: int, min_val: int = 1, max_val: int = 100) -> List[int]:
    """生成n个范围在[min_val, max_val]之间的随机整数"""
    return [random.randint(min_val, max_val) for _ in range(n)]


# 示例：生成随机浮点数样本
@stats_decorator('AVG', 'MAX')  # 只计算平均值和最大值
def generate_random_floats(n: int, min_val: float = 0.0, max_val: float = 1.0) -> List[float]:
    """生成n个范围在[min_val, max_val]之间的随机浮点数"""
    return [random.uniform(min_val, max_val) for _ in range(n)]


# 测试
if __name__ == "__main__":
    print("生成10个随机整数并计算所有统计量:")
    generate_random_integers(10)

    print("\n生成5个随机浮点数并只计算平均值和最大值:")
    generate_random_floats(5)

    # 自定义组合
    print("\n自定义统计组合:")


    @stats_decorator('SUM', 'MIN')  # 只计算总和和最小值
    def custom_random_sample(n: int) -> List[int]:
        return [random.randint(1, 50) for _ in range(n)]


    custom_random_sample(8)
