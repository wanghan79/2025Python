def banker_algorithm(Max, Need, Available, Allocated, Request):
    """
    银行家算法实现

    :param Max: 最大需求矩阵，表示每个进程对每种资源的最大需求
    :param Need: 需求矩阵，表示每个进程还需要的资源数量
    :param Available: 可用资源向量，表示系统当前可用的资源数量
    :param Allocated: 已分配矩阵，表示每个进程已分配的资源数量
    :param Request: 资源申请向量，表示某个进程请求的资源数量
    :return: 是否可以分配资源，以及分配后的 Max, Need, Available, Allocated 矩阵
    """
    # 获取进程数量和资源种类数量
    num_processes = len(Max)
    num_resources = len(Available)

    # 检查请求是否超过进程的最大需求
    process_index = Request[0]  # 请求的进程编号
    request_resources = Request[1:]  # 请求的资源向量

    for i in range(num_resources):
        if request_resources[i] > Need[process_index][i]:
            return False, Max, Need, Available, Allocated

    # 检查请求是否超过可用资源
    for i in range(num_resources):
        if request_resources[i] > Available[i]:
            return False, Max, Need, Available, Allocated

    # 假设分配资源
    Available_temp = Available[:]
    Allocated_temp = [row[:] for row in Allocated]
    Need_temp = [row[:] for row in Need]

    for i in range(num_resources):
        Available_temp[i] -= request_resources[i]
        Allocated_temp[process_index][i] += request_resources[i]
        Need_temp[process_index][i] -= request_resources[i]

    # 安全性检查
    Work = Available_temp[:]
    Finish = [False] * num_processes

    while True:
        found = False
        for i in range(num_processes):
            if not Finish[i]:
                can_allocate = True
                for j in range(num_resources):
                    if Need_temp[i][j] > Work[j]:
                        can_allocate = False
                        break
                if can_allocate:
                    for j in range(num_resources):
                        Work[j] += Allocated_temp[i][j]
                    Finish[i] = True
                    found = True
        if not found:
            break

    # 检查是否所有进程都完成
    if all(Finish):
        # 如果安全，则更新实际的 Available 和 Allocated 矩阵
        Available = Available_temp
        Allocated = Allocated_temp
        Need = Need_temp
        return True, Max, Need, Available, Allocated
    else:
        # 如果不安全，则不分配资源
        return False, Max, Need, Available, Allocated

# 示例调用
if __name__ == "__main__":
    # 示例数据
    Max = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]
    Allocated = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]
    Need = [
        [7, 4, 3],
        [1, 2, 2],
        [6, 0, 0],
        [0, 1, 1],
        [4, 3, 1]
    ]
    Available = [10, 5, 7]
    Request = [1, 1, 0, 2]  # 进程编号为 1，请求资源向量为 [1, 0, 2]

    # 调用银行家算法
    can_allocate, Max, Need, Available, Allocated = banker_algorithm(Max, Need, Available, Allocated, Request)

    # 输出结果
    print("Can Allocate:", can_allocate)
    print("Max Matrix:")
    for row in Max:
        print(row)
    print("Need Matrix:")
    for row in Need:
        print(row)
    print("Available Vector:", Available)
    print("Allocated Matrix:")
    for row in Allocated:
        print(row)