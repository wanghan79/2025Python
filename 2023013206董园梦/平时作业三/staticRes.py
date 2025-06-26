from typing import Callable, Generator, Any, Dict, List, Tuple, Union
from functools import wraps
from random_num import generate_random_sample_generator, generate_batch_samples
import math
import sys

def stats_decorator(*stats_ops: str) -> Callable:
    """
    带参装饰器：对生成器数据进行分类统计
    
    Args:
        stats_ops: 统计操作（"SUM", "AVG", "MAX", "MIN", "COUNT"）
    
    Returns:
        装饰后的生成器函数
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Generator:
            # 初始化
            stats = {
                "id": {
                    "SUM": 0,
                    "COUNT": 0,
                    "MAX": -math.inf,
                    "MIN": math.inf,
                    "TYPE": "整数(1-100)"
                },
                "value": {
                    "SUM": 0,
                    "COUNT": 0,
                    "MAX": -math.inf,
                    "MIN": math.inf,
                    "TYPE": "浮点数(0.01-1.0)"
                },
                "price": {
                    "SUM": 0,
                    "COUNT": 0,
                    "MAX": -math.inf,
                    "MIN": math.inf,
                    "TYPE": "浮点数(0.01-1.0)"
                },
                "quantity": {
                    "SUM": 0,
                    "COUNT": 0,
                    "MAX": -math.inf,
                    "MIN": math.inf,
                    "TYPE": "整数(1-100)"
                }
            }
            
            # 获取生成器
            gen = func(*args, **kwargs)
            
            sample_count = 0  # 添加样本计数器
            for item in gen:
                sample_count += 1
                yield item 
                
                # 统计id
                if "id" in item:
                    data = item["id"]
                    stats["id"]["SUM"] += data
                    stats["id"]["COUNT"] += 1
                    stats["id"]["MAX"] = max(stats["id"]["MAX"], data)
                    stats["id"]["MIN"] = min(stats["id"]["MIN"], data)
                
                # 统计value
                if "value" in item:
                    data = item["value"]
                    stats["value"]["SUM"] += data
                    stats["value"]["COUNT"] += 1
                    stats["value"]["MAX"] = max(stats["value"]["MAX"], data)
                    stats["value"]["MIN"] = min(stats["value"]["MIN"], data)
                
                # 统计items中的price和quantity
                if "items" in item:
                    for item_data in item["items"]:
                        if "price" in item_data:
                            data = item_data["price"]
                            stats["price"]["SUM"] += data
                            stats["price"]["COUNT"] += 1
                            stats["price"]["MAX"] = max(stats["price"]["MAX"], data)
                            stats["price"]["MIN"] = min(stats["price"]["MIN"], data)
                        
                        if "quantity" in item_data:
                            data = item_data["quantity"]
                            stats["quantity"]["SUM"] += data
                            stats["quantity"]["COUNT"] += 1
                            stats["quantity"]["MAX"] = max(stats["quantity"]["MAX"], data)
                            stats["quantity"]["MIN"] = min(stats["quantity"]["MIN"], data)
            
            # 输出
            print("\n=== 分类统计结果 ===")
            for field, data in stats.items():
                if data["COUNT"] > 0:
                    print(f"\n【{field}】")
                    if "SUM" in stats_ops:
                        print(f"sum: {data['SUM']:.4f}" if field in ['value', 'price'] else f"sum: {data['SUM']}")
                    if "AVG" in stats_ops:
                        print(f"avg: {data['SUM']/data['COUNT']:.4f}" if field in ['value', 'price'] else f"avg: {data['SUM']/data['COUNT']:.2f}")
                    if "MAX" in stats_ops:
                        print(f"max: {data['MAX']:.4f}" if field in ['value', 'price'] else f"max: {data['MAX']}")
                    if "MIN" in stats_ops:
                        print(f"min: {data['MIN']:.4f}" if field in ['value', 'price'] else f"min: {data['MIN']}")
                    if "COUNT" in stats_ops:
                        print(f"count: {data['COUNT']}")
                
        return wrapper
    return decorator

# 测试用例
if __name__ == "__main__":
    # 使用random_num中的生成器
    @stats_decorator("SUM", "AVG", "MAX", "MIN", "COUNT")
    def generate_complex_samples(batch_size: int):
        structure = {
            "id": 0,  # 将会生成1-100的整数
            "value": 0.0,  # 将会生成0.01-1.0的浮点数
            "items": [{
                "price": 0.0,
                "quantity": 0
            }]
        }
        gen = generate_random_sample_generator(structure)
        return generate_batch_samples(gen, batch_size, print_samples=False)
    
    print("=== 测试：小批量数据统计 ===")
    sample_number = 1  # 初始化样本编号
    for sample in generate_complex_samples(100):
        print(f"生成样本{sample_number}: {sample}")
        sample_number += 1