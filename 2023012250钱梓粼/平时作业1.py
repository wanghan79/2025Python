def bankers_algorithm(max_matrix, need_matrix, available_matrix, allocated_matrix, request, process_id):
    """
    :param max_matrix: 最大需求矩阵 - 二维列表
    :param need_matrix: 需求矩阵 - 二维列表
    :param available_matrix: 可用资源向量 - 一维列表
    :param allocated_matrix: 已分配矩阵 - 二维列表
    :param request: 请求向量 - 一维列表
    :param process_id: 请求进程ID - 整数
    :return: (是否可以分配, 更新后的矩阵字典)
    """
    # 获取进程数和资源类型数
    num_processes = len(max_matrix)
    num_resources = len(available_matrix)
    
    # 检查请求是否合法
    for i in range(num_resources):
        if request[i] > need_matrix[process_id][i]:
            return False, {
                "Max": max_matrix,
                "Need": need_matrix,
                "Available": available_matrix,
                "Allocated": allocated_matrix
            }
        if request[i] > available_matrix[i]:
            return False, {
                "Max": max_matrix,
                "Need": need_matrix,
                "Available": available_matrix,
                "Allocated": allocated_matrix
            }
    
    # 尝试分配资源
    temp_available = available_matrix.copy()
    temp_allocated = [row[:] for row in allocated_matrix]
    temp_need = [row[:] for row in need_matrix]
    
    # 更新临时矩阵
    for i in range(num_resources):
        temp_available[i] -= request[i]
        temp_allocated[process_id][i] += request[i]
        temp_need[process_id][i] -= request[i]
    
    # 安全性检查
    def is_safe(available, allocated, need):
        work = available.copy()
        finish = [False] * num_processes
        
        while True:
            found = False
            for i in range(num_processes):
                if not finish[i] and all(need[i][j] <= work[j] for j in range(num_resources)):
                    found = True
                    finish[i] = True
                    for j in range(num_resources):
                        work[j] += allocated[i][j]
                    break
            
            if not found:
                break
        
        return all(finish)
    
    # 检查是否处于安全状态
    if is_safe(temp_available, temp_allocated, temp_need):
        return True, {
            "Max": max_matrix,
            "Need": temp_need,
            "Available": temp_available,
            "Allocated": temp_allocated
        }
    else:
        return False, {
            "Max": max_matrix,
            "Need": need_matrix,
            "Available": available_matrix,
            "Allocated": allocated_matrix
        }

# 测试代码
if __name__ == "__main__":
    # 示例数据
    max_matrix = [
        [3, 2, 2],  # P0
        [4, 3, 3],  # P1
        [3, 3, 2],  # P2
        [2, 2, 2]   # P3
    ]
    
    allocated_matrix = [
        [1, 0, 0],  # P0
        [2, 1, 1],  # P1
        [2, 1, 1],  # P2
        [1, 0, 1]   # P3
    ]
    
    available_matrix = [2, 3, 1]
    
    # 计算Need矩阵
    need_matrix = []
    for i in range(len(max_matrix)):
        need_row = []
        for j in range(len(max_matrix[0])):
            need_row.append(max_matrix[i][j] - allocated_matrix[i][j])
        need_matrix.append(need_row)
    
    # 测试资源请求
    request = [1, 1, 0]  # P0请求资源
    process_id = 0
    
    success, result = bankers_algorithm(
        max_matrix, 
        need_matrix, 
        available_matrix, 
        allocated_matrix, 
        request, 
        process_id
    )
    
    print(f"资源分配{'成功' if success else '失败'}")
    print("\n更新后的矩阵:")
    for matrix_name, matrix in result.items():
        print(f"\n{matrix_name}矩阵:")
        if isinstance(matrix[0], list):
            for row in matrix:
                print(row)
        else:
            print(matrix) 
