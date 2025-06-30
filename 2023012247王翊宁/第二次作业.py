import numpy as np
from typing import Tuple


def generate_banker_samples(num_samples: int, num_processes: int, num_resources: int) -> Tuple:
    """
    生成随机银行家算法样本
    参数:
        num_samples: 需要生成的样本数量
        num_processes: 每个样本的进程数量
        num_resources: 资源种类数量
    返回:
        生成器，每次迭代返回一个样本的(Max, Allocated, Available, Need)
    """

    def generate_sample():
        # 生成Max矩阵 (每个进程对每类资源的最大需求)
        Max = np.random.randint(1, 10, size=(num_processes, num_resources))

        # 生成Allocated矩阵 (确保不超过Max)
        Allocated = np.array([
            [np.random.randint(0, Max[i][j] + 1) for j in range(num_resources)]
            for i in range(num_processes)
        ])

        # 计算Need矩阵
        Need = Max - Allocated

        # 生成Available资源 (确保至少能满足一个进程的需求)
        Available = np.array([
            max(1, np.random.randint(0, np.sum(Allocated[:, j]) + 1))
            for j in range(num_resources)
        ])

        return Max, Allocated, Available, Need

    for _ in range(num_samples):
        yield generate_sample()


def sample_generator_usage_example():
    # 使用示例
    num_samples = 3  # 生成3个样本
    num_processes = 4  # 每个样本4个进程
    num_resources = 3  # 3类资源

    print(f"生成{num_samples}个随机银行家算法样本(进程:{num_processes}, 资源:{num_resources}):\n")

    for i, (Max, Allocated, Available, Need) in enumerate(
            generate_banker_samples(num_samples, num_processes, num_resources), 1
    ):
        print(f"样本 {i}:")
        print("Max矩阵:\n", Max)
        print("Allocated矩阵:\n", Allocated)
        print("Available矩阵:\n", Available)
        print("Need矩阵:\n", Need)
        print("-" * 50)


if __name__ == "__main__":
    sample_generator_usage_example()