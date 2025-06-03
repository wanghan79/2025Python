def banker_algorithm(Max, Need, Available, Allocated, Request, process):
    """
    银行家算法实现
    参数:
        Max: 最大需求矩阵
        Need: 需求矩阵
        Available: 可用资源向量
        Allocated: 已分配矩阵
        Request: 请求向量
        process: 请求资源的进程号
    返回:
        (能否分配, 分配后的Max, Need, Available, Allocated)
    """
    # 1. 检查请求是否小于等于Need
    for i in range(len(Request)):
        if Request[i] > Need[process][i]:
            return (False, Max, Need, Available, Allocated)
    
    # 2. 检查请求是否小于等于Available
    for i in range(len(Request)):
        if Request[i] > Available[i]:
            return (False, Max, Need, Available, Allocated)
    
    # 3. 尝试分配资源
    temp_available = Available.copy()
    temp_allocated = [row.copy() for row in Allocated]
    temp_need = [row.copy() for row in Need]
    
    for i in range(len(Request)):
        temp_available[i] -= Request[i]
        temp_allocated[process][i] += Request[i]
        temp_need[process][i] -= Request[i]
    
    # 4. 安全检查算法
    work = temp_available.copy()
    finish = [False] * len(Max)
    safe_sequence = []
    
    while True:
        found = False
        for p in range(len(Max)):
            if not finish[p]:
                can_execute = True
                for i in range(len(work)):
                    if temp_need[p][i] > work[i]:
                        can_execute = False
                        break
                
                if can_execute:
                    for i in range(len(work)):
                        work[i] += temp_allocated[p][i]
                    finish[p] = True
                    safe_sequence.append(p)
                    found = True
        
        if not found:
            break
    
    # 5. 判断是否安全
    if all(finish):
        return (True, Max, temp_need, temp_available, temp_allocated)
    else:
        return (False, Max, Need, Available, Allocated)

# 示例使用
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
    
    Available = [3, 3, 2]
    
    # 进程1请求资源 (1, 0, 2)
    Request = [1, 0, 2]
    process = 1
    
    result, new_Max, new_Need, new_Available, new_Allocated = banker_algorithm(
        Max, Need, Available, Allocated, Request, process
    )
    
    print(f"能否分配: {result}")
    print("分配后的Max矩阵:")
    for row in new_Max:
        print(row)
    print("分配后的Need矩阵:")
    for row in new_Need:
        print(row)
    print("分配后的Available向量:", new_Available)
    print("分配后的Allocated矩阵:")
    for row in new_Allocated:
        print(row)
