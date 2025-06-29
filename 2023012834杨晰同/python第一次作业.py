def banker_algorithm(Max, Need, Available, Allocated, Request, process_num):
    for i in range(len(Request)):
        if Request[i] > Need[process_num][i]:
            return False, Max, Need, Available, Allocated

    for i in range(len(Request)):
        if Request[i] > Available[i]:
            return False, Max, Need, Available, Allocated

    old_Available = Available.copy()
    old_Allocated = [row.copy() for row in Allocated]
    old_Need = [row.copy() for row in Need]

    for i in range(len(Request)):
        Available[i] -= Request[i]
        Allocated[process_num][i] += Request[i]
        Need[process_num][i] -= Request[i]

    if is_safe(Need, Available, Allocated):
        return True, Max, Need, Available, Allocated
    else:
        return False, Max, old_Need, old_Available, old_Allocated


def is_safe(Need, Available, Allocated):
    n = len(Need)
    m = len(Available)

    Work = Available.copy()
    Finish = [False] * n
    safe_sequence = []

    while True:
        found = False
        for i in range(n):
            if not Finish[i]:
                can_execute = True
                for j in range(m):
                    if Need[i][j] > Work[j]:
                        can_execute = False
                        break

                if can_execute:
                    for j in range(m):
                        Work[j] += Allocated[i][j]
                    Finish[i] = True
                    safe_sequence.append(i)
                    found = True

        if not found:
            break

    if all(Finish):
        return True
    else:
        return False


def print_state(Max, Need, Available, Allocated):
    print("Max:")
    for row in Max:
        print(row)

    print("Allocated:")
    for row in Allocated:
        print(row)

    print("Need:")
    for row in Need:
        print(row)

    print("Available:")
    print(Available)


if __name__ == "__main__":
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

    Need = []
    for i in range(len(Max)):
        Need.append([Max[i][j] - Allocated[i][j] for j in range(len(Max[i]))])

    Available = [3, 3, 2]

    print("Initial state:")
    print_state(Max, Need, Available, Allocated)

    print("\nRequest 1: Process 1 requests (1,0,2)")
    Request = [1, 0, 2]
    process_num = 1

    can_allocate, Max, Need, Available, Allocated = banker_algorithm(
        Max, Need, Available, Allocated, Request, process_num
    )

    if can_allocate:
        print_state(Max, Need, Available, Allocated)

    print("\nRequest 2: Process 4 requests (3,3,0)")
    Request = [3, 3, 0]
    process_num = 4

    can_allocate, Max, Need, Available, Allocated = banker_algorithm(
        Max, Need, Available, Allocated, Request, process_num
    )

    if can_allocate:
        print_state(Max, Need, Available, Allocated)

    print("\nRequest 3: Process 0 requests (0,2,0)")
    Request = [0, 2, 0]
    process_num = 0

    can_allocate, Max, Need, Available, Allocated = banker_algorithm(
        Max, Need, Available, Allocated, Request, process_num
    )

    if can_allocate:
        print_state(Max, Need, Available, Allocated)