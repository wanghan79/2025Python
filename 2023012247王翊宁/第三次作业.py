import numpy as np
from functools import wraps
from typing import Callable, List, Tuple, Dict


def stats_operations(*operations: str) -> Callable:
    """
    带参修饰器工厂函数，接收统计操作列表
    支持的统计操作: 'SUM', 'AVG', 'MAX', 'MIN'
    """
    valid_ops = {'SUM', 'AVG', 'MAX', 'MIN'}

    # 验证操作是否有效
    for op in operations:
        if op not in valid_ops:
            raise ValueError(f"无效的统计操作: {op}. 有效的操作是: {valid_ops}")

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Tuple[Dict, Tuple]:
            # 调用原始函数获取生成器
            samples_generator = func(*args, **kwargs)

            # 初始化统计数据结构
            stats = {
                'Max': {'SUM': [], 'AVG': [], 'MAX': [], 'MIN': []},
                'Allocated': {'SUM': [], 'AVG': [], 'MAX': [], 'MIN': []},
                'Available': {'SUM': [], 'AVG': [], 'MAX': [], 'MIN': []},
                'Need': {'SUM': [], 'AVG': [], 'MAX': [], 'MIN': []}
            }

            sample_count = 0
            all_samples = []

            # 处理每个样本
            for sample in samples_generator:
                Max, Allocated, Available, Need = sample
                all_samples.append(sample)
                sample_count += 1

                # 对每个矩阵进行统计
                for matrix, data in zip(['Max', 'Allocated', 'Available', 'Need'], sample):
                    matrix_sum = np.sum(data, axis=0)
                    stats[matrix]['SUM'].append(matrix_sum)
                    stats[matrix]['AVG'].append(np.mean(data, axis=0))
                    stats[matrix]['MAX'].append(np.max(data, axis=0))
                    stats[matrix]['MIN'].append(np.min(data, axis=0))

            # 计算最终统计结果
            result_stats = {}
            for matrix in stats:
                result_stats[matrix] = {}
                for op in operations:
                    if op == 'SUM':
                        result_stats[matrix][op] = np.sum(stats[matrix][op], axis=0)
                    elif op == 'AVG':
                        result_stats[matrix][op] = np.mean(stats[matrix][op], axis=0)
                    elif op == 'MAX':
                        result_stats[matrix][op] = np.max(stats[matrix][op], axis=0)
                    elif op == 'MIN':
                        result_stats[matrix][op] = np.min(stats[matrix][op], axis=0)

            return result_stats, tuple(all_samples)

        return wrapper

    return decorator


# 应用修饰器到样本生成函数
@stats_operations('SUM', 'AVG', 'MAX', 'MIN')
def generate_banker_samples(num_samples: int, num_processes: int, num_resources: int):
    """生成随机银行家算法样本"""

    def generate_sample():
        Max = np.random.randint(1, 10, size=(num_processes, num_resources))
        Allocated = np.array([
            [np.random.randint(0, Max[i][j] + 1) for j in range(num_resources)]
            for i in range(num_processes)
        ])
        Need = Max - Allocated
        Available = np.array([
            max(1, np.random.randint(0, np.sum(Allocated[:, j]) + 1)
            for j in range(num_resources)
        ])
        return Max, Allocated, Available, Need

    for _ in range(num_samples):
        yield generate_sample()


def print_stats_results(stats: Dict, samples: Tuple):
    """打印统计结果和样本"""
    print("\n生成的样本统计结果:")
    for matrix, ops in stats.items():
        print(f"\n{matrix}矩阵统计:")
        for op, values in ops.items():
            print(f"{op}: {values}")

    print("\n\n原始样本数据:")
    for i, sample in enumerate(samples, 1):
        print(f"\n样本 {i}:")
        print("Max:\n", sample[0])
        print("Allocated:\n", sample[1])
        print("Available:", sample[2])
        print("Need:\n", sample[3])


if __name__ == "__main__":
    # 使用示例
    print("银行家算法随机样本生成器(带统计功能)")
    print("=" * 50)

    # 生成3个样本，每个样本4个进程3类资源，并进行统计
    stats, samples = generate_banker_samples(
        num_samples=3,
        num_processes=4,
        num_resources=3
    )

    print_stats_results(stats, samples)