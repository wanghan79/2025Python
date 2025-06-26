import random
from functools import wraps
from typing import List, Callable, Any

def statistics(*operations):
    """
    带参数的装饰器，用于对函数返回的数据进行统计
    
    参数:
        *operations: 可变参数，指定需要进行的统计操作
                    可选值: 'SUM', 'AVG', 'MAX', 'MIN'
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> dict:
            # 调用原函数获取数据
            data = func(*args, **kwargs)
            
            # 确保数据是列表格式
            if not isinstance(data, list):
                raise ValueError("被装饰的函数必须返回一个列表")
            
            if not data:
                raise ValueError("数据列表不能为空")
            
            # 打印原始数据
            print(f"原始数据: {data}")
            print("-" * 50)
            
            # 存储统计结果
            results = {}
            
            # 根据指定的操作进行统计
            for operation in operations:
                operation = operation.upper()
                
                if operation == 'SUM':
                    results['SUM'] = sum(data)
                elif operation == 'AVG':
                    results['AVG'] = sum(data) / len(data)
                elif operation == 'MAX':
                    results['MAX'] = max(data)
                elif operation == 'MIN':
                    results['MIN'] = min(data)
                else:
                    print(f"警告: 未知的统计操作 '{operation}'，已忽略")
            
            # 打印统计结果
            print("统计结果:")
            for op, value in results.items():
                print(f"{op}: {value:.2f}")
            
            return results
        
        return wrapper
    return decorator


# 示例1: 使用所有统计操作
@statistics('SUM', 'AVG', 'MAX', 'MIN')
def generate_random_samples(n: int, min_val: int = 1, max_val: int = 100) -> List[int]:
    """生成n个随机整数样本"""
    return [random.randint(min_val, max_val) for _ in range(n)]


# 示例2: 只使用部分统计操作
@statistics('AVG', 'MAX')
def generate_uniform_samples(n: int, low: float = 0.0, high: float = 1.0) -> List[float]:
    """生成n个均匀分布的随机浮点数样本"""
    return [random.uniform(low, high) for _ in range(n)]


# 示例3: 使用单个统计操作
@statistics('SUM')
def generate_normal_samples(n: int, mean: float = 0.0, std: float = 1.0) -> List[float]:
    """生成n个正态分布的随机样本"""
    return [random.normalvariate(mean, std) for _ in range(n)]


# 示例4: 自定义随机样本生成函数
@statistics('MIN', 'MAX', 'AVG')
def generate_custom_samples(n: int) -> List[float]:
    """生成自定义的随机样本（指数分布）"""
    return [random.expovariate(1.0) for _ in range(n)]


# 使用示例
if __name__ == "__main__":
    print("=" * 60)
    print("示例1: 生成10个1-100的随机整数，进行所有统计操作")
    print("=" * 60)
    result1 = generate_random_samples(10)
    
    print("\n" + "=" * 60)
    print("示例2: 生成15个0-10的均匀分布随机数，计算平均值和最大值")
    print("=" * 60)
    result2 = generate_uniform_samples(15, 0, 10)
    
    print("\n" + "=" * 60)
    print("示例3: 生成20个标准正态分布随机数，计算总和")
    print("=" * 60)
    result3 = generate_normal_samples(20)
    
    print("\n" + "=" * 60)
    print("示例4: 生成12个指数分布随机数，计算最小值、最大值和平均值")
    print("=" * 60)
    result4 = generate_custom_samples(12)
    
    # 动态组合统计操作的示例
    print("\n" + "=" * 60)
    print("动态组合统计操作示例")
    print("=" * 60)
    
    # 可以根据需要动态创建装饰器
    operations_list = ['SUM', 'MIN']
    
    @statistics(*operations_list)
    def dynamic_samples(n: int) -> List[int]:
        return [random.randint(1, 50) for _ in range(n)]
    
    result5 = dynamic_samples(8)