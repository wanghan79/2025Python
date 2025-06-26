def banker_algorithm(Max, Need, Available, Allocated, Request, process_num):
    """
    银行家算法核心实现
    
    参数:
        Max: 最大需求矩阵
        Need: 需求矩阵
        Available: 可用资源向量
        Allocated: 分配矩阵
        Request: 请求向量
        process_num: 请求进程号
        
    返回:
        (是否安全, 新Available, 新Allocated, 新Need)
    """
    # 检查请求是否合法
    if any(Request[i] > Need[process_num][i] for i in range(len(Request))):
        return False, Available, Allocated, Need, "错误：请求超过声明的最大需求"
    
    if any(Request[i] > Available[i] for i in range(len(Request))):
        return False, Available, Allocated, Need, "错误：请求超过可用资源"
    
    # 尝试分配
    new_Available = [Available[i] - Request[i] for i in range(len(Available))]
    new_Allocated = [row.copy() for row in Allocated]
    new_Need = [row.copy() for row in Need]
    
    for i in range(len(Request)):
        new_Allocated[process_num][i] += Request[i]
        new_Need[process_num][i] -= Request[i]
    
    # 安全性检查
    work = new_Available.copy()
    finish = [False] * len(Max)
    safe_sequence = []
    
    while True:
        found = False
        for i in range(len(Max)):
            if not finish[i] and all(new_Need[i][j] <= work[j] for j in range(len(work))):
                work = [work[j] + new_Allocated[i][j] for j in range(len(work))]
                finish[i] = True
                safe_sequence.append(i)
                found = True
                break
        
        if not found:
            break
    
    if all(finish):
        return True, new_Available, new_Allocated, new_Need, f"安全序列: {safe_sequence}"
    else:
        return False, Available, Allocated, Need, "警告：分配将导致不安全状态"


def print_matrices(name, matrix):
    """打印矩阵"""
    print(f"\n{name}:")
    for row in matrix:
        print(" ".join(f"{elem:>3}" for elem in row))


# 使用示例
if __name__ == "__main__":
    # 输入数据
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
    
    # 进程1请求[1,0,2]
    Request = [1, 0, 2]
    process_num = 1
    
    # 执行银行家算法
    is_safe, Avail, Alloc, Nd, msg = banker_algorithm(Max, Need, Available, Allocated, Request, process_num)
    
    # 输出结果
    print("\n银行家算法计算结果:")
    print(f"请求能否分配: {'是' if is_safe else '否'}")
    print(f"消息: {msg}")
    
    if is_safe:
        print("\n分配后状态:")
        print("Available:", " ".join(map(str, Avail)))
        print_matrices("Max", Max)
        print_matrices("Allocated", Alloc)
        print_matrices("Need", Nd)