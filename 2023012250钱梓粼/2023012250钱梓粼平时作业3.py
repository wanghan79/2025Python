from functools import wraps
from typing import List, Callable, Union, Dict
from abc import ABC, abstractmethod
import random
from dataclasses import dataclass

# 统计操作的抽象基类
class StatOperation(ABC):
    @abstractmethod
    def calculate(self, data: List[Union[int, float]]) -> float:
        pass
    
    @abstractmethod
    def name(self) -> str:
        pass

# 具体的统计操作实现
class SumOperation(StatOperation):
    def calculate(self, data: List[Union[int, float]]) -> float:
        return sum(data)
    
    def name(self) -> str:
        return 'SUM'

class AverageOperation(StatOperation):
    def calculate(self, data: List[Union[int, float]]) -> float:
        return sum(data) / len(data)
    
    def name(self) -> str:
        return 'AVG'

class MaxOperation(StatOperation):
    def calculate(self, data: List[Union[int, float]]) -> float:
        return max(data)
    
    def name(self) -> str:
        return 'MAX'

class MinOperation(StatOperation):
    def calculate(self, data: List[Union[int, float]]) -> float:
        return min(data)
    
    def name(self) -> str:
        return 'MIN'

# 统计操作管理器
@dataclass
class StatsManager:
    operations: Dict[str, StatOperation] = None
    
    def __post_init__(self):
        if self.operations is None:
            self.operations = {
                'SUM': SumOperation(),
                'AVG': AverageOperation(),
                'MAX': MaxOperation(),
                'MIN': MinOperation()
            }
    
    def calculate_stats(self, data: List[Union[int, float]], requested_ops: tuple) -> Dict[str, float]:
        results = {}
        for op_name in requested_ops:
            op_name = op_name.upper()
            if op_name in self.operations:
                operation = self.operations[op_name]
                results[operation.name()] = operation.calculate(data)
        return results

def stats_decorator(*operations: str):
    """
    带参修饰器，用于对函数返回的数据进行统计操作
    支持的操作：'SUM', 'AVG', 'MAX', 'MIN'
    可以组合使用多个操作
    """
    stats_manager = StatsManager()
    
    def decorator(func: Callable[..., List[Union[int, float]]]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            stats = stats_manager.calculate_stats(result, operations)
            
            print(f"\n原始数据: {result}")
            if stats:
                print("\n统计结果:")
                for op, value in stats.items():
                    print(f"{op}: {value}")
            
            return result
        return wrapper
    return decorator

# 示例生成器函数
class SampleGenerator:
    @staticmethod
    @stats_decorator('SUM', 'AVG', 'MAX', 'MIN')
    def generate_random_samples(n: int, start: int = 1, end: int = 100) -> List[int]:
        """生成n个随机整数样本"""
        return [random.randint(start, end) for _ in range(n)]

    @staticmethod
    @stats_decorator('MAX', 'MIN')
    def generate_random_floats(n: int, start: float = 0.0, end: float = 1.0) -> List[float]:
        """生成n个随机浮点数样本"""
        return [random.uniform(start, end) for _ in range(n)]

if __name__ == "__main__":
    # 测试整数样本生成并统计所有指标
    print("\n=== 测试1：生成10个随机整数并计算所有统计量 ===")
    SampleGenerator.generate_random_samples(10)
    
    # 测试浮点数样本生成并只统计最大最小值
    print("\n=== 测试2：生成5个随机浮点数并只计算最大最小值 ===")
    SampleGenerator.generate_random_floats(5) 
