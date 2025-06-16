import numpy as np


def bankers_algorithm(Max, Allocation, Available, Request, process_id):
    """
    银行家算法实现

    参数:
        Max (numpy.ndarray)      : 最大需求矩阵 (n进程 × m资源类型)
        Allocation (numpy.ndarray) : 已分配矩阵 (n进程 × m资源类型)
        Available (numpy.ndarray)  : 可用资源向量 (1 × m资源类型)
        Request (numpy.ndarray)    : 当前进程的资源请求 (1 × m资源类型)
        process_id (int)          : 发起请求的进程ID

    返回:
        tuple: (是否安全, 新分配矩阵, 新需求矩阵, 新可用资源, 安全序列)
    """

    # 1. 计算需求矩阵
    Need = Max - Allocation

    # 2. 检查请求合法性
    if not np.all(Request <= Need[process_id]):
        print(f"错误：进程 {process_id} 请求超过其最大需求")
        return False, Allocation, Need, Available, None

    if not np.all(Request <= Available):
        print(f"错误：进程 {process_id} 请求超过系统可用资源")
        return False, Allocation, Need, Available, None

    # 3. 试分配资源（临时状态）
    temp_Available = Available - Request
    temp_Allocation = Allocation.copy()
    temp_Allocation[process_id] += Request
    temp_Need = Need.copy()
    temp_Need[process_id] -= Request

    # 4. 安全检查算法
    def is_safe(available, allocation, need):
        n_processes, n_resources = allocation.shape
        work = available.copy()
        finish = np.zeros(n_processes, dtype=bool)
        safe_seq = []

        while True:
            found = False
            for i in range(n_processes):
                if not finish[i] and np.all(need[i] <= work):
                    work += allocation[i]
                    finish[i] = True
                    safe_seq.append(i)
                    found = True

            if not found:
                break

        if np.all(finish):
            return True, safe_seq
        return False, None

    # 5. 执行安全检查
    safe, safe_sequence = is_safe(temp_Available, temp_Allocation, temp_Need)
    if safe:
        print(f"可以安全分配资源给进程 {process_id}，安全序列: {safe_sequence}")
        return True, temp_Allocation, temp_Need, temp_Available, safe_sequence
    else:
        print(f"警告：分配会导致系统进入不安全状态")
        return False, Allocation, Need, Available, None


# 示例用法
if __name__ == "__main__":
    # 系统状态初始化 (5个进程，3类资源)
    Max = np.array([
        [7, 5, 3],  # 进程0的最大需求
        [3, 2, 2],  # 进程1
        [9, 0, 2],  # 进程2
        [2, 2, 2],  # 进程3
        [4, 3, 3]  # 进程4
    ])

    Allocation = np.array([
        [0, 1, 0],  # 进程0已分配
        [2, 0, 0],  # 进程1
        [3, 0, 2],  # 进程2
        [2, 1, 1],  # 进程3
        [0, 0, 2]  # 进程4
    ])

    Available = np.array([3, 3, 2])  # 当前可用资源

    # 进程1请求资源 [1, 0, 2]
    Request = np.array([1, 0, 2])
    process_id = 1

    print("初始状态:")
    print("Max:\n", Max)
    print("Allocation:\n", Allocation)
    print("Available:", Available)
    print("Request:", Request, "from Process", process_id)
    print("\n执行银行家算法...")

    # 执行银行家算法
    can_allocate, new_Allocation, new_Need, new_Available, safe_seq = bankers_algorithm(
        Max, Allocation, Available, Request, process_id
    )

    # 打印结果
    print("\n结果:")
    print("可以分配:", can_allocate)
    if can_allocate:
        print("安全序列:", safe_seq)
        print("\n分配后状态:")
        print("New Allocation:\n", new_Allocation)
        print("New Need:\n", new_Need)
        print("New Available:", new_Available)