def bankers_algorithm(Max, Allocation, Available, Request):

    Need = [[Max[i][j] - Allocation[i][j] for j in range(len(Max[0]))] for i in range(len(Max))]

    process_index, request_vector = Request

    num_resources = len(Available)
    num_processes = len(Max)

    print("初始状态：")
    print_matrix("Max", Max)
    print_matrix("Allocation", Allocation)
    print_matrix("Need", Need)
    print("Available:", Available)

    for j in range(num_resources):
        if request_vector[j] > Need[process_index][j]:
            print("\n错误：请求超出进程所需资源，无法分配。")
            return

    for j in range(num_resources):
        if request_vector[j] > Available[j]:
            print("\n错误：当前没有足够资源，无法分配。")
            return

    work = Available[:]
    finish = [False] * num_processes

    for j in range(num_resources):
        Available[j] -= request_vector[j]
        Allocation[process_index][j] += request_vector[j]
        Need[process_index][j] -= request_vector[j]

    print(f"\n尝试为进程 {process_index} 分配资源 {request_vector} 后的状态：")
    print_matrix("Allocation", Allocation)
    print_matrix("Need", Need)
    print("Available:", Available)

    safe_sequence = []
    while True:
        found = False
        for i in range(num_processes):
            if not finish[i]:
                if all(Need[i][j] <= work[j] for j in range(num_resources)):
                    for j in range(num_resources):
                        work[j] += Allocation[i][j]
                    finish[i] = True
                    safe_sequence.append(i)
                    found = True
        if not found:
            break

    if all(finish):
        print("\n系统处于安全状态，资源可以安全分配。")
        print("安全序列为:", safe_sequence)
        print("\n最终状态：")
        print_matrix("Allocation", Allocation)
        print_matrix("Need", Need)
        print("Available:", Available)
        return {
            "safe": True,
            "safe_sequence": safe_sequence,
            "Allocation": Allocation,
            "Need": Need,
            "Available": Available
        }
    else:
        print("\n分配后系统不安全，回滚操作，拒绝此次请求。")

        # 回滚
        for j in range(num_resources):
            Available[j] += request_vector[j]
            Allocation[process_index][j] -= request_vector[j]
            Need[process_index][j] += request_vector[j]

        print("已恢复到请求前的状态：")
        print_matrix("Allocation", Allocation)
        print_matrix("Need", Need)
        print("Available:", Available)

        return {
            "safe": False,
            "Allocation": Allocation,
            "Need": Need,
            "Available": Available
        }


def print_matrix(name, matrix):
    print(f"{name}:")
    for row in matrix:
        print(row)
    print()


if __name__ == "__main__":
    Max = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]

    Allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]

    Available = [3, 3, 2]

    Request = (1, [1, 0, 2])

    result = bankers_algorithm(Max, Allocation, Available, Request)