"""
银行家算法实现

功能：
1. 提供了银行家算法的核心实现，包括资源分配请求的处理和安全性检查。
2. 提供了辅助函数，用于格式化打印矩阵和结果。

作者：多雅晗
"""
import numpy as np
from typing import Tuple, List, Optional

def bankers_algorithm(max_matrix: List[List[int]],
                      need_matrix: List[List[int]],
                      available_vector: List[int],
                      allocated_matrix: List[List[int]],
                      request: List[int],
                      process_id: int) -> Tuple[bool, dict]:
    """
    银行家算法实现

    参数:
    max_matrix: 最大需求矩阵，每个进程对每种资源的最大需求
    need_matrix: 需求矩阵，每个进程还需要的资源数量
    available_vector: 可用资源向量
    allocated_matrix: 已分配矩阵，每个进程已分配的资源
    request: 请求向量，某个进程请求的资源数量
    process_id: 发出请求的进程ID

    返回:
    tuple: (是否可以分配, 结果字典)
    """

    # 转换为numpy数组
    max_mat = np.array(max_matrix)
    need_mat = np.array(need_matrix)
    available_vec = np.array(available_vector)
    allocated_mat = np.array(allocated_matrix)
    request_vec = np.array(request)

    n_processes = len(max_mat)
    n_resources = len(available_vec)

    # 步骤1: 检查请求是否合法
    # 1.1 检查请求是否超过需求
    if np.any(request_vec > need_mat[process_id]):
        return False, {
            "error": f"进程 {process_id} 的请求超过了其声明的最大需求",
            "request": request_vec.tolist(),
            "need": need_mat[process_id].tolist()
        }

    # 1.2 检查请求是否超过可用资源
    if np.any(request_vec > available_vec):
        return False, {
            "error": f"进程 {process_id} 的请求超过了系统可用资源",
            "request": request_vec.tolist(),
            "available": available_vec.tolist()
        }

    # 步骤2: 试探性分配资源
    # 复制当前状态
    new_available = available_vec.copy()
    new_allocated = allocated_mat.copy()
    new_need = need_mat.copy()

    # 更新状态
    new_available -= request_vec
    new_allocated[process_id] += request_vec
    new_need[process_id] -= request_vec

    # 步骤3: 安全性检查
    safe, safe_sequence = safety_check(new_allocated, new_need, new_available)

    if safe:
        return True, {
            "can_allocate": True,
            "safe_sequence": safe_sequence,
            "new_state": {
                "Max": max_mat.tolist(),
                "Allocated": new_allocated.tolist(),
                "Need": new_need.tolist(),
                "Available": new_available.tolist()
            },
            "message": f"可以为进程 {process_id} 分配资源，系统仍处于安全状态"
        }
    else:
        return False, {
            "can_allocate": False,
            "error": "分配后系统将处于不安全状态，拒绝分配",
            "current_state": {
                "Max": max_mat.tolist(),
                "Allocated": allocated_mat.tolist(),
                "Need": need_mat.tolist(),
                "Available": available_vec.tolist()
            }
        }


def safety_check(allocated: np.ndarray, need: np.ndarray, available: np.ndarray) -> Tuple[bool, List[int]]:
    """
    安全性检查算法

    参数:
    allocated: 已分配矩阵
    need: 需求矩阵
    available: 可用资源向量

    返回:
    tuple: (是否安全, 安全序列)
    """
    n_processes = len(allocated)
    work = available.copy()
    finish = [False] * n_processes
    safe_sequence = []

    while len(safe_sequence) < n_processes:
        found = False

        # 寻找一个可以完成的进程
        for i in range(n_processes):
            if not finish[i] and np.all(need[i] <= work):
                work += allocated[i]
                finish[i] = True
                safe_sequence.append(i)
                found = True
                break

        if not found:
            return False, []

    return True, safe_sequence

def print_matrices(result_dict: dict):
    """
    格式化打印矩阵结果
    """
    if result_dict.get("can_allocate"):
        state = result_dict["new_state"]
        print("=== 分配后的系统状态 ===")
    else:
        state = result_dict.get("current_state", {})
        print("=== 当前系统状态 ===")

    if state:
        print(f"Max矩阵:\n{np.array(state['Max'])}")
        print(f"\nAllocated矩阵:\n{np.array(state['Allocated'])}")
        print(f"\nNeed矩阵:\n{np.array(state['Need'])}")
        print(f"\nAvailable向量: {state['Available']}")

    if result_dict.get("safe_sequence"):
        print(f"\n安全序列: {result_dict['safe_sequence']}")


# 示例使用
if __name__ == "__main__":
    max_matrix = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]

    allocated_matrix = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]

    # 计算需求矩阵
    need_matrix = []
    for i in range(len(max_matrix)):
        need_row = []
        for j in range(len(max_matrix[i])):
            need_row.append(max_matrix[i][j] - allocated_matrix[i][j])
        need_matrix.append(need_row)

    available_vector = [3, 3, 2]  # 可用资源

    # 测试案例1: 进程1请求资源[1, 0, 2]
    print("=== 测试案例1: 进程1请求[1, 0, 2] ===")
    request1 = [1, 0, 2]
    process_id1 = 1

    can_allocate, result = bankers_algorithm(
        max_matrix, need_matrix, available_vector,
        allocated_matrix, request1, process_id1
    )

    print(f"分配结果: {'可以分配' if can_allocate else '拒绝分配'}")
    if result.get("message"):
        print(f"消息: {result['message']}")
    if result.get("error"):
        print(f"错误: {result['error']}")

    print_matrices(result)

    print("\n" + "=" * 50 + "\n")

    # 测试案例2: 进程4请求资源[3, 3, 0]
    print("=== 测试案例2: 进程4请求[3, 3, 0] ===")
    request2 = [3, 3, 0]
    process_id2 = 4

    can_allocate2, result2 = bankers_algorithm(
        max_matrix, need_matrix, available_vector,
        allocated_matrix, request2, process_id2
    )

    print(f"分配结果: {'可以分配' if can_allocate2 else '拒绝分配'}")
    if result2.get("message"):
        print(f"消息: {result2['message']}")
    if result2.get("error"):
        print(f"错误: {result2['error']}")

    print_matrices(result2)