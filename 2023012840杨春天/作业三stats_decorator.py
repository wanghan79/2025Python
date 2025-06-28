import functools
from typing import Callable, Dict, List, Union, Any

def stats_analyzer(operations: List[str]):
    """
    统计分析装饰器，用于对生成的随机样本进行统计操作
    
    参数:
    operations (List[str]): 要执行的统计操作列表，支持 'SUM', 'AVG', 'MAX', 'MIN'
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 调用原始函数生成样本
            samples = list(func(*args, **kwargs))
            
            if not samples:
                print("没有生成任何样本数据")
                return samples
            
            # 确定样本维度
            first_sample = samples[0]
            if not isinstance(first_sample, (list, tuple)):
                # 如果样本不是序列类型，将其转换为单元素元组
                samples = [(s,) for s in samples]
            
            # 初始化统计结果
            num_dimensions = len(samples[0])
            stats = {op: [0] * num_dimensions for op in operations}
            
            # 计算统计值
            for op in operations:
                for dim in range(num_dimensions):
                    values = [sample[dim] for sample in samples]
                    
                    if op == 'SUM':
                        stats[op][dim] = sum(values)
                    elif op == 'AVG':
                        stats[op][dim] = sum(values) / len(values)
                    elif op == 'MAX':
                        stats[op][dim] = max(values)
                    elif op == 'MIN':
                        stats[op][dim] = min(values)
                    else:
                        raise ValueError(f"不支持的统计操作: {op}")
            
            # 输出统计结果
            print("\n=== 统计结果 ===")
            for op, results in stats.items():
                print(f"{op}: {results}")
            print("===============\n")
            
            return samples
        
        return wrapper
    return decorator

# 示例：对随机样本生成函数应用统计装饰器
if __name__ == "__main__":
    import random
    
    # 使用统计装饰器修饰随机样本生成函数
    @stats_analyzer(operations=['SUM', 'AVG', 'MAX', 'MIN'])
    def generate_random_samples(n: int):
        """生成n个随机样本，每个样本包含3个维度的数据"""
        for _ in range(n):
            yield (
                random.randint(1, 100),  # 整数维度
                random.uniform(0, 1),    # 浮点数维度
                random.randint(50, 200)  # 另一个整数维度
            )
    
    # 生成10个随机样本并自动进行统计分析
    samples = generate_random_samples(10)
    
    # 打印生成的样本
    print("生成的样本数据:")
    for i, sample in enumerate(samples):
        print(f"样本 {i+1}: {sample}")    