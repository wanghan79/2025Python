from copy import deepcopy


def banker_algorithm(Max, Need, Available, Allocated, Request, pid):
    """
    银行家算法分配函数

    参数：
      Max:    最大需求矩阵，二维列表，行数为进程数，列数为资源种类数
      Need:   需求矩阵，等于 Max - Allocated
      Available: 可用资源向量，一维列表，长度为资源种类数
      Allocated: 已分配矩阵，二维列表
      Request: 请求资源向量，一维列表，长度为资源种类数
      pid:    发起请求的进程编号（从0开始）

    返回：
      (can_allocate, new_Available, new_Allocated, new_Need, Max)
      can_allocate: 布尔，是否安全分配
      new_*: 分配后的各矩阵（若不可分配，则返回原始矩阵的深拷贝）
    """
    # 深拷贝输入，以免修改原始数据
    new_Available = deepcopy(Available)
    new_Allocated = deepcopy(Allocated)
    new_Need = deepcopy(Need)

    m = len(Max)       # 进程数
    n = len(Available) # 资源种类数

    # 检查 Request 是否小于等于 Need[pid]
    for j in range(n):
        if Request[j] > new_Need[pid][j]:
            return False, Available, Allocated, Need, Max

    # 检查 Request 是否小于等于 Available
    for j in range(n):
        if Request[j] > new_Available[j]:
            return False, Available, Allocated, Need, Max

    # 尝试分配：
    for j in range(n):
        new_Available[j] -= Request[j]
        new_Allocated[pid][j] += Request[j]
        new_Need[pid][j] -= Request[j]

    # 安全性检测
    work = deepcopy(new_Available)
    finish = [False] * m

    while True:
        allocated_in_loop = False
        for i in range(m):
            if not finish[i]:
                # 检查 Need[i] <= work
                if all(new_Need[i][j] <= work[j] for j in range(n)):
                    # 模拟该进程完成，释放资源
                    for j in range(n):
                        work[j] += new_Allocated[i][j]
                    finish[i] = True
                    allocated_in_loop = True
        if not allocated_in_loop:
            break

    # 如果所有进程都能完成，则安全
    if all(finish):
        return True, new_Available, new_Allocated, new_Need, Max
    else:
        # 若不安全，撤销分配，返回原始数据
        return False, Available, Allocated, Need, Max


if __name__ == "__main__":
    # 示例
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
    Need = [[Max[i][j] - Allocated[i][j] for j in range(3)] for i in range(5)]
    Available = [3, 3, 2]
    Request = [1, 0, 2]
    pid = 1
    can_allocate, A, Al, N, M = banker_algorithm(Max, Need, Available, Allocated, Request, pid)
    print("Can allocate?", can_allocate)
    print("Available:", A)
    print("Allocated:", Al)
    print("Need:", N)
    print("Max:", M)
