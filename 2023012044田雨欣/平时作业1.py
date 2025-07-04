def banker_algorithm(Max, Need, Available, Allocated, Request, process_id):

    if any(Request[i] > Need[process_id][i] for i in range(len(Request))):
        return False, Max, Need, Available, Allocated
    if any(Request[i] > Available[i] for i in range(len(Request))):
        return False, Max, Need, Available, Allocated

    new_Available = Available.copy()
    new_Allocated = [row.copy() for row in Allocated]
    new_Need = [row.copy() for row in Need]

    for i in range(len(Request)):
        new_Available[i] -= Request[i]
        new_Allocated[process_id][i] += Request[i]
        new_Need[process_id][i] -= Request[i]

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

        if not found:
            break

    if all(finish):
        return True, Max, new_Need, new_Available, new_Allocated
    else:
        return False, Max, Need, Available, Allocated

if __name__ == "__main__":
    Max = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
    Allocated = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
    Need = [[7, 4, 3], [1, 2, 2], [6, 0, 0], [0, 1, 1], [4, 3, 1]]
    Available = [3, 3, 2]
    Request = [1, 0, 2]
    process_id = 1

    can_allocate, new_Max, new_Need, new_Available, new_Allocated = banker_algorithm(
        Max, Need, Available, Allocated, Request, process_id
    )
    print(f"能否分配: {can_allocate}")
    print("分配后状态:")
    print("Max:", new_Max)
    print("Need:", new_Need)
    print("Available:", new_Available)
    print("Allocated:", new_Allocated)
    """
        Max: 最大需求矩阵
        Need: 需求矩阵
        Available: 可使用的资源向量
        Allocated: 已分配矩阵
        Request: 请求资源向量
        process_id: 发起请求的进程ID
    返回:(能否分配, 新的Max, 新的Need, 新的Available, 新的Allocated)
    """