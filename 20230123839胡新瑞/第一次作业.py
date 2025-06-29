def banker_algorithm(Max, Allocated, Available, Request, process_num=None):
    """
    银行家算法实现

    参数:
        Max: 最大需求矩阵 (n x m)，n个进程对m种资源的最大需求
        Allocated: 已分配矩阵 (n x m)
        Available: 可用资源向量 (1 x m)
        Request: 请求资源向量 (1 x m)
        process_num: 发起请求的进程编号 (0-based)

    返回:
        (is_safe, new_Allocated, new_Need, new_Available)
        is_safe: 是否安全
        new_*: 分配后的新矩阵
    """

    # 如果没有指定进程编号，则返回原始状态
    if process_num is None:
        Need = [[Max[i][j] - Allocated[i][j] for j in range(len(Max[0]))] for i in range(len(Max))]
        return (True, Allocated, Need, Available)

    # 1. 检查请求是否小于等于Need
    Need = [[Max[i][j] - Allocated[i][j] for j in range(len(Max[0]))] for i in range(len(Max))]
    for j in range(len(Request)):
        if Request[j] > Need[process_num][j]:
            print("错误：请求超过了声明的最大需求")
            return (False, Allocated, Need, Available)

    # 2. 检查请求是否小于等于Available
    for j in range(len(Request)):
        if Request[j] > Available[j]:
            print("错误：请求超过了可用资源")
            return (False, Allocated, Need, Available)

    # 3. 尝试分配资源
    new_Available = Available.copy()
    new_Allocated = [row.copy() for row in Allocated]
    new_Need = [row.copy() for row in Need]

    for j in range(len(Request)):
        new_Available[j] -= Request[j]
        new_Allocated[process_num][j] += Request[j]
        new_Need[process_num][j] -= Request[j]

    # 4. 检查安全性
    is_safe, safe_sequence = check_safety(new_Allocated, new_Need, new_Available, Max)

    if is_safe:
        print("请求可以安全分配")
        print("安全序列:", safe_sequence)
        return (True, new_Allocated, new_Need, new_Available)
    else:
        print("警告：分配后系统将处于不安全状态")
        # 恢复原始状态
        return (False, Allocated, Need, Available)


def check_safety(Allocated, Need, Available, Max):
    """
    检查系统是否处于安全状态

    返回:
        (is_safe, safe_sequence)
    """
    n = len(Allocated)  # 进程数
    m = len(Available)  # 资源种类数

    # 初始化工作向量
    Work = Available.copy()
    Finish = [False] * n
    safe_sequence = []

    # 安全算法核心逻辑
    while True:
        # 查找满足条件的进程
        found = False
        for i in range(n):
            if not Finish[i]:
                # 检查Need[i] <= Work
                can_allocate = True
                for j in range(m):
                    if Need[i][j] > Work[j]:
                        can_allocate = False
                        break

                if can_allocate:
                    # 模拟资源释放
                    for j in range(m):
                        Work[j] += Allocated[i][j]
                    Finish[i] = True
                    safe_sequence.append(i)
                    found = True

        # 如果没有找到可分配的进程则退出循环
        if not found:
            break

    # 检查所有进程是否完成
    is_safe = all(Finish)
    return (is_safe, safe_sequence if is_safe else [])