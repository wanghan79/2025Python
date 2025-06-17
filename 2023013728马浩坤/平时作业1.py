def safety_check(**kwargs):
    available = kwargs['available']
    allocation = kwargs['allocation']
    need = kwargs['need']

    # 2. 初始化变量
    n = len(allocation)  # 进程数
    m = len(available)  # 资源数
    work = available.copy()
    finish = [False] * n
    safe_sequence = []

    # 3. 循环检查
    for _ in range(n):
        found = False
        for i in range(n):

            # 4. 检查是否是为完成且需求小于等于可用资源向量
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                for j in range(m):
                    work[j] += allocation[i][j]
                finish[i] = True
                safe_sequence.append(i)
                found = True
                break
        if not found:
            break

    # 5. 返回结果
    if all(finish):
        return True, safe_sequence
    else:
        return False, []

def banker_algorithm(**kwargs):
    pid = kwargs['process_id']
    request = kwargs['request']
    available = kwargs['available']
    allocation = kwargs['allocation']
    need = kwargs['need']

    # 2. 保存原始数据，以便回滚
    original_avail = available.copy()
    original_alloc = [row.copy() for row in allocation]
    original_need = [row.copy() for row in need]

    # 3. 如果请求超过最大需求，则返回失败
    if any(request[j] > need[pid][j] for j in range(len(request))):
        return False, "失败：请求超过最大需求", original_avail, original_alloc, original_need, []

    # 4. 如果请求超过可用资源，则返回失败
    if any(request[j] > available[j] for j in range(len(request))):
        return False, "失败：请求超过可用资源", original_avail, original_alloc, original_need, []

    # 5. 从可用资源向量中减去请求向量
    new_avail = [available[j] - request[j] for j in range(len(available))]

    # 6. 从分配矩阵中增加请求向量
    new_alloc = [row.copy() for row in allocation]
    new_alloc[pid] = [new_alloc[pid][j] + request[j] for j in range(len(request))]

    # 7. 从需求矩阵中减去请求向量
    new_need = [row.copy() for row in need]
    new_need[pid] = [new_need[pid][j] - request[j] for j in range(len(request))]

    # 8. 执行安全检测
    to_safe_data = {
        'available': new_avail,
        'allocation': new_alloc,
        'need': new_need
    }
    is_safe, safe_seq = safety_check(**to_safe_data)
    if is_safe:
        return True, "成功：请求被允许", new_avail, new_alloc, new_need, safe_seq
    else:
        return False, "失败：导致不安全状态", original_avail, original_alloc, original_need, []


def print_matrix(**kwargs):
    title = kwargs['title']
    matrix = kwargs['matrix']
    resource_names = kwargs['resource_names']
    process_names = kwargs['process_names']

    # 2. 打印矩阵
    print(f"\n{title}:")
    header = "     " + "   ".join(resource_names)
    print(header)
    for idx, row in enumerate(matrix):
        process = process_names[idx]
        formatted_row = "  ".join(f"{val:2}" for val in row)
        print(f"{process}: {formatted_row}")

def main():
    print("="*100)
    print("初始系统状态：")
    print(f"\n可利用资源向量: {available}")
    print_matrix(**{'title' : "最大需求矩阵", 'matrix': max_matrix,
                    'resource_names': resource_names, 'process_names': process_names})
    print_matrix(**{'title' : "分配矩阵", 'matrix': allocation_matrix,
                    'resource_names': resource_names, 'process_names': process_names})
    print_matrix(**{'title' : "需求矩阵", 'matrix': need_matrix,
                    'resource_names': resource_names, 'process_names': process_names})

    is_safe, safe_seq = safety_check(**{'available': available,
                                        'allocation': allocation_matrix, 'need': need_matrix})
    print("\n" + "="*100)
    if is_safe:
        print(f'安全检测结果：系统安全，安全序列为：{" → ".join([f"P{i}" for i in safe_seq])}')
    else:
        print("安全检测结果：系统不安全")
    print("\n" + "="*100)

    copy_available = available.copy()
    to_banker_data = {'process_id': 1, 'request': [1, 0, 2], 'available': copy_available,
                      'allocation': [row.copy() for row in allocation_matrix], 'need': [row.copy() for row in need_matrix]}
    result, msg, new_avail, new_alloc, new_need, safe_seq = banker_algorithm(**to_banker_data)

    print(f"处理请求: 进程 P{to_banker_data['process_id']} 请求资源 {to_banker_data['request']}")
    print(f"结果：{msg}")
    if result:
        print(f"\n新的可利用资源向量: {new_avail}")
        print_matrix(**{'title' : "新的最大需求矩阵", 'matrix': max_matrix,
                        'resource_names': resource_names, 'process_names': process_names})
        print_matrix(**{'title' : "新的分配矩阵", 'matrix': new_alloc,
                        'resource_names': resource_names, 'process_names': process_names})
        print_matrix(**{'title' : "新的需求矩阵", 'matrix': new_need,
                        'resource_names': resource_names, 'process_names': process_names})
        print(f"新的安全序列：{' → '.join([f'P{i}' for i in safe_seq])}")


if __name__ == "__main__":
    available = [3, 3, 2]
    max_matrix = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]
    allocation_matrix = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]
    # need_matrix = max_matrix - allocation_matrix
    need_matrix = [
        [7-0, 5-1, 3-0],
        [3-2, 2-0, 2-0],
        [9-3, 0-0, 2-2],
        [2-2, 2-1, 2-1],
        [4-0, 3-0, 3-2]
    ]
    resource_names = ['A', 'B', 'C']
    process_names = [f'P{i}' for i in range(5)]

    main()