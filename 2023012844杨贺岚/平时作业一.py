def banker_algorithm(Max, Allocated, Need, Available, Request):
    import copy
    # 深拷贝原始数据，避免修改原始矩阵
    Max_c = copy.deepcopy(Max)
    Allocated_c = copy.deepcopy(Allocated)
    Need_c = copy.deepcopy(Need)
    Available_c = copy.deepcopy(Available)
    
    # 解析请求
    pid, req_vector = Request
    n = len(Max_c)     
    m = len(Available_c)
    
    # 检查请求是否小于等于需求
    if any(req_vector[j] > Need_c[pid][j] for j in range(m)):
        return False, Max, Allocated, Need, Available, "错误：请求超过声明的最大需求"
    
    # 检查请求是否小于等于可用资源
    if any(req_vector[j] > Available_c[j] for j in range(m)):
        return False, Max, Allocated, Need, Available, "错误：请求超过可用资源，进程需等待"
    
    # 尝试分配资源
    for j in range(m):
        Available_c[j] -= req_vector[j]
        Allocated_c[pid][j] += req_vector[j]
        Need_c[pid][j] -= req_vector[j]
    
    # 安全性检查
    Work = Available_c[:]
    Finish = [False] * n
    
    found = True
    while found:
        found = False
        for i in range(n):
            if not Finish[i] and all(Need_c[i][j] <= Work[j] for j in range(m)):
                for j in range(m):
                    Work[j] += Allocated_c[i][j]
                Finish[i] = True
                found = True
    
    # 检查所有进程是否完成
    if all(Finish):
        return True, Max_c, Allocated_c, Need_c, Available_c, "分配成功！系统处于安全状态"
    else:
        # 回滚分配
        for j in range(m):
            Available_c[j] += req_vector[j]
            Allocated_c[pid][j] -= req_vector[j]
            Need_c[pid][j] += req_vector[j]
        return False, Max, Allocated, Need, Available, "拒绝分配：分配后系统将进入不安全状态"


# 示例数据
Max = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
Allocated = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
Need = [[7, 4, 3], [1, 2, 2], [6, 0, 0], [0, 1, 1], [4, 3, 1]]
Available = [3, 3, 2]
Request = (1, [1, 0, 2])  # 进程1请求资源[1,0,2]

# 调用银行家算法
success, Max_new, Allocated_new, Need_new, Available_new, message = banker_algorithm(
    Max, Allocated, Need, Available, Request
)

print(message)
if success:
    print("\n分配后状态:")
    print("Max矩阵:")
    for row in Max_new:
        print(row)
    
    print("\nAllocated矩阵:")
    for row in Allocated_new:
        print(row)
    
    print("\nNeed矩阵:")
    for row in Need_new:
        print(row)
    
    print("\nAvailable向量:", Available_new)
