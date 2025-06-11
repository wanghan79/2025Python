import copy
from typing import List, Tuple, Union

def bankers_algorithm(
    Max: List[List[int]],
    Need: List[List[int]],
    Available: List[int],
    Allocated: List[List[int]],
    Request: List[int],
    process_index: int
) -> Tuple[bool, List[List[int]], List[List[int]], List[int], List[List[int]]]:
    """
    银行家算法实现，判断资源请求是否安全
    
    参数:
        Max: 最大需求矩阵
        Need: 需求矩阵
        Available: 可用资源向量
        Allocated: 已分配矩阵
        Request: 请求向量
        process_index: 请求进程索引
        
    返回:
        (是否安全, Max, Need, Available, Allocated)
    """
    # 验证输入维度一致性
    n = len(Max)  # 进程数
    m = len(Available)  # 资源种类数
    
    if n != len(Need) or n != len(Allocated):
        raise ValueError("所有矩阵的行数（进程数）必须一致")
    
    if any(len(row) != m for row in Max) or any(len(row) != m for row in Need) or any(len(row) != m for row in Allocated):
        raise ValueError("所有矩阵的列数（资源种类）必须与Available的长度一致")
    
    if len(Request) != m:
        raise ValueError("请求向量长度必须与资源种类数一致")
    
    if process_index < 0 or process_index >= n:
        raise ValueError("进程索引无效")

    # 1. 检查请求是否合法
    # 请求不能超过声明的需求
    for j in range(m):
        if Request[j] > Need[process_index][j]:
            return False, Max, Need, Available, Allocated
    
    # 请求不能超过可用资源
    for j in range(m):
        if Request[j] > Available[j]:
            return False, Max, Need, Available, Allocated

    # 2. 模拟分配资源
    work_allocated = copy.deepcopy(Allocated)
    work_available = Available.copy()
    work_need = copy.deepcopy(Need)
    
    for j in range(m):
        work_available[j] -= Request[j]
        work_allocated[process_index][j] += Request[j]
        work_need[process_index][j] -= Request[j]

    # 3. 安全性检查
    work = work_available.copy()
    finish = [False] * n  # 标记进程是否完成
    progress_made = True  # 标记是否在本轮中有进程完成
    
    # 当还有未完成的进程且在本轮中有进展时继续
    while progress_made and not all(finish):
        progress_made = False
        for i in range(n):
            # 只考虑未完成的进程
            if not finish[i]:
                # 检查当前进程的需求是否小于等于可用资源
                can_execute = True
                for j in range(m):
                    if work_need[i][j] > work[j]:
                        can_execute = False
                        break
                
                # 如果资源足够，则"执行"该进程并释放其资源
                if can_execute:
                    for j in range(m):
                        work[j] += work_allocated[i][j]
                    finish[i] = True
                    progress_made = True

    # 4. 判断是否所有进程都能完成
    if all(finish):
        # 系统安全，返回新状态
        return True, Max, work_need, work_available, work_allocated
    else:
        # 系统不安全，返回原始状态
        return False, Max, Need, Available, Allocated


# 示例数据
Max = [[7, 5, 3],
       [3, 2, 2],
       [9, 0, 2],
       [2, 2, 2],
       [4, 3, 3]]

Allocated = [[0, 1, 0],
             [2, 0, 0],
             [3, 0, 2],
             [2, 1, 1],
             [0, 0, 2]]

Available = [3, 3, 2]

Need = [[7, 4, 3],
        [1, 2, 2],
        [6, 0, 0],
        [0, 1, 1],
        [4, 3, 1]]

Request = [1, 0, 2]
process_index = 1

# 调用函数
can_allocate, newMax, newNeed, newAvailable, newAllocated = bankers_algorithm(
    Max, Need, Available, Allocated, Request, process_index
)

print("是否可以分配:", can_allocate)
print("分配后 Available:", newAvailable)
print("分配后 Allocated[1]:", newAllocated[1])
print("分配后 Need[1]:", newNeed[1])