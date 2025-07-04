import numpy as np

def banker_algorithm(max_matrix, need_matrix, available_vector, allocated_matrix, request_vector):
    """
    使用银行家算法计算是否能够分配资源，并输出分配后的四个矩阵。

    Args:
        max_matrix (numpy.ndarray): 最大资源需求矩阵 (Max)。
        need_matrix (numpy.ndarray): 需求矩阵 (Need)。
        available_vector (numpy.ndarray): 可用资源向量 (Available)。
        allocated_matrix (numpy.ndarray): 已分配资源矩阵 (Allocation)。
        request_vector (numpy.ndarray): 资源申请向量 (Request)。

    Returns:
        tuple: 包含是否能够分配资源的布尔值，以及分配后的四个矩阵（如果能够分配）。
    """
    num_processes = max_matrix.shape[0]
    num_resources = max_matrix.shape[1]

    # 检查 Request <= Need
    if not np.all(request_vector <= need_matrix[process_id]):
        print(f"进程 {process_id} 申请的资源超过了声明的需求。")
        return False, None, None, None, None

    # 检查 Request <= Available
    if not np.all(request_vector <= available_vector):
        print(f"资源不足，进程 {process_id} 申请的资源超过了当前可用资源。")
        return False, None, None, None, None

    # 尝试分配资源 (假设分配)
    temp_available = available_vector - request_vector
    temp_allocation = allocated_matrix.copy()
    temp_allocation[process_id] += request_vector
    temp_need = need_matrix.copy()
    temp_need[process_id] -= request_vector

    # 安全性检查
    finish = np.zeros(num_processes, dtype=bool)  # 所有进程都初始化为未完成
    work = temp_available.copy()  # 初始化工作向量
    safe_sequence = []  # 保存安全序列

    while True:
        found = False
        for i in range(num_processes):
            if not finish[i] and np.all(temp_need[i] <= work):
                work += temp_allocation[i]  # 释放进程 i 占用的资源
                finish[i] = True
                safe_sequence.append(i)
                found = True
                break

        if not found:
            break

    # 判断是否安全
    if np.all(finish):
        print("资源可以安全分配。")
        print("安全序列:", safe_sequence)
        return True, max_matrix, temp_need, temp_available, temp_allocation
    else:
        print("资源分配后，系统处于不安全状态。")
        return False, None, None, None, None


# 示例用法
if __name__ == "__main__":
    # 资源数量
    num_processes = 5
    num_resources = 3

    # 初始化矩阵 (使用 NumPy 数组)
    max_matrix = np.array([
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ])

    allocated_matrix = np.array([
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ])

    available_vector = np.array([3, 3, 2])

    # 计算 Need 矩阵
    need_matrix = max_matrix - allocated_matrix

    # 进程 1 (索引为 1) 申请资源 (1, 0, 2)
    request_vector = np.array([1, 0, 2])
    process_id = 1

    # 运行银行家算法
    is_safe, new_max, new_need, new_available, new_allocation = banker_algorithm(
        max_matrix, need_matrix, available_vector, allocated_matrix, request_vector
    )

    if is_safe:
        print("\n分配后的状态:")
        print("Max:\n", new_max)
        print("Need:\n", new_need)
        print("Available:\n", new_available)
        print("Allocation:\n", new_allocation)
    else:
        print("资源无法分配。")