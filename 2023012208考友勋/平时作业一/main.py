def banker_algorithm(Max, Need, Available, Allocated, Request, pid):
    """
    银行家算法实现函数
    
    参数:
    Max (list): 最大需求矩阵，二维列表，形状为 (n_processes, n_resources)
    Need (list): 需求矩阵，二维列表，形状为 (n_processes, n_resources)
    Available (list): 可用资源向量，一维列表，长度为 n_resources
    Allocated (list): 已分配资源矩阵，二维列表，形状为 (n_processes, n_resources)
    Request (list): 进程请求的资源向量，一维列表，长度为 n_resources
    pid (int): 请求资源的进程编号（从0开始）
    
    返回:
    tuple: (是否可以分配, 分配后的 Max, 分配后的 Need, 分配后的 Available, 分配后的 Allocated)
    """
    n_processes = len(Max)
    n_resources = len(Available)
    
    # 验证输入矩阵维度是否匹配
    if (len(Need) != n_processes or len(Allocated) != n_processes or
        any(len(row) != n_resources for row in Max) or
        any(len(row) != n_resources for row in Need) or
        any(len(row) != n_resources for row in Allocated) or
        len(Request) != n_resources):
        raise ValueError("输入矩阵维度不匹配")
    
    # 步骤1: 检查请求是否超过需求
    if any(Request[j] > Need[pid][j] for j in range(n_resources)):
        return (False, Max, Need, Available, Allocated)
    
    # 步骤2: 检查请求是否超过可用资源
    if any(Request[j] > Available[j] for j in range(n_resources)):
        return (False, Max, Need, Available, Allocated)
    
    # 步骤3: 尝试分配资源（创建副本，避免修改原始数据）
    new_Available = Available.copy()
    new_Allocated = [row.copy() for row in Allocated]
    new_Need = [row.copy() for row in Need]
    
    # 更新矩阵
    for j in range(n_resources):
        new_Available[j] -= Request[j]
        new_Allocated[pid][j] += Request[j]
        new_Need[pid][j] -= Request[j]
    
    # 步骤4: 安全性检查
    def is_safe_state(work, allocated, need):
        """检查系统是否处于安全状态"""
        work_copy = work.copy()
        finish = [False] * n_processes
        safe_sequence = []
        
        while True:
            found = False
            for i in range(n_processes):
                if not finish[i] and all(need[i][j] <= work_copy[j] for j in range(n_resources)):
                    # 分配资源给进程i并回收资源
                    for j in range(n_resources):
                        work_copy[j] += allocated[i][j]
                    finish[i] = True
                    safe_sequence.append(i)
                    found = True
                    break  # 重新扫描所有进程
            if not found:
                break
        
        return all(finish), safe_sequence
    
    # 执行安全性检查
    safe, sequence = is_safe_state(new_Available, new_Allocated, new_Need)
    
    # 步骤5: 返回结果
    if safe:
        return (True, Max, new_Need, new_Available, new_Allocated)
    else:
        return (False, Max, Need, Available, Allocated)

# 示例使用
if __name__ == "__main__":
    # 初始化矩阵（经典银行家算法示例）
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
        [7, 4, 3],  # 7-0, 5-1, 3-0
        [1, 2, 2],  # 3-2, 2-0, 2-0
        [6, 0, 0],  # 9-3, 0-0, 2-2
        [0, 1, 1],  # 2-2, 2-1, 2-1
        [4, 3, 1]   # 4-0, 3-0, 3-2
    ]
    
    Available = [3, 3, 2]  # 可用资源
    
    # 模拟进程1请求资源 [1, 0, 2]
    Request = [1, 0, 2]
    pid = 1
    
    # 执行银行家算法
    result, max_after, need_after, avail_after, alloc_after = banker_algorithm(
        Max, Need, Available, Allocated, Request, pid
    )
    
    # 输出结果
    print(f"资源请求 {Request} 是否被批准: {result}")
    
    if result:
        print("\n分配后的矩阵状态:")
        print("Max:")
        for row in max_after:
            print(f"  {row}")
        
        print("\nNeed:")
        for row in need_after:
            print(f"  {row}")
        
        print(f"\nAvailable: {avail_after}")
        
        print("\nAllocated:")
        for row in alloc_after:
            print(f"  {row}")
