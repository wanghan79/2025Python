def banker_algorithm(processes, resources, Max, Allocated, Available, Request, process_id):
    """
    银行家算法实现

    参数:
        processes: 进程数量
        resources: 资源种类数量
        Max: 最大需求矩阵 (processes x resources)
        Allocated: 已分配矩阵 (processes x resources)
        Available: 可用资源向量 (resources)
        Request: 请求资源向量 (resources)
        process_id: 请求资源的进程ID

    返回:
        bool: 是否可以安全分配
        dict: 分配后的矩阵和向量
    """

    # 1. 检查请求是否小于等于Need
    Need = [[Max[i][j] - Allocated[i][j] for j in range(resources)] for i in range(processes)]
    for j in range(resources):
        if Request[j] > Need[process_id][j]:
            print(f"错误：进程 {process_id} 请求的资源超过其最大需求")
            return False, None

    # 2. 检查请求是否小于等于Available
    for j in range(resources):
        if Request[j] > Available[j]:
            print(f"错误：进程 {process_id} 请求的资源超过系统可用资源")
            return False, None

    # 3. 尝试分配资源
    temp_Available = Available.copy()
    temp_Allocated = [row.copy() for row in Allocated]
    temp_Need = [row.copy() for row in Need]

    for j in range(resources):
        temp_Available[j] -= Request[j]
        temp_Allocated[process_id][j] += Request[j]
        temp_Need[process_id][j] -= Request[j]

    # 4. 安全检查算法
    work = temp_Available.copy()
    finish = [False] * processes
    safe_sequence = []

    while True:
        # 找到一个满足条件的进程
        found = False
        for i in range(processes):
            if not finish[i]:
                # 检查Need[i] <= Work
                can_allocate = True
                for j in range(resources):
                    if temp_Need[i][j] > work[j]:
                        can_allocate = False
                        break

                if can_allocate:
                    # 模拟执行完成，释放资源
                    for j in range(resources):
                        work[j] += temp_Allocated[i][j]
                    finish[i] = True
                    safe_sequence.append(i)
                    found = True

        if not found:
            break

    # 检查是否所有进程都完成
    if all(finish):
        print("安全序列:", safe_sequence)
        print("可以安全分配")

        # 更新实际分配
        for j in range(resources):
            Available[j] -= Request[j]
            Allocated[process_id][j] += Request[j]
            Need[process_id][j] -= Request[j]

        return True, {
            'Max': Max,
            'Allocated': Allocated,
            'Need': Need,
            'Available': Available
        }
    else:
        print("不安全状态，不能分配")
        return False, None


# 示例使用
if __name__ == "__main__":
    # 示例数据
    processes = 5
    resources = 3

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

    Available = [3, 3, 2]

    # 进程1请求资源 [1, 0, 2]
    Request = [1, 0, 2]
    process_id = 1

    # 调用银行家算法
    success, matrices = banker_algorithm(processes, resources, Max, Allocated, Available, Request, process_id)

    if success:
        print("\n分配后的矩阵:")
        print("Max矩阵:")
        for row in matrices['Max']:
            print(row)

        print("\nAllocated矩阵:")
        for row in matrices['Allocated']:
            print(row)

        print("\nNeed矩阵:")
        for row in matrices['Need']:
            print(row)

        print("\nAvailable向量:")
        print(matrices['Available'])
