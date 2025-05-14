def banker_algorithm(Max, Allocated, Available, Request, process_num=None):
    Need = [[Max[i][j] - Allocated[i][j] for j in range(len(Max[0]))] for i in range(len(Max))]
    
    if process_num is None:
        is_safe, safe_sequence = safety_algorithm(Need, Allocated, Available.copy())
        return (is_safe, safe_sequence, Allocated, Need, Available)
    
    for j in range(len(Request)):
        if Request[j] > Need[process_num][j]:
            return (False, [], Allocated, Need, Available)
    
    for j in range(len(Request)):
        if Request[j] > Available[j]:
            return (False, [], Allocated, Need, Available)
    
    new_Allocated = [row[:] for row in Allocated]
    new_Need = [row[:] for row in Need]
    new_Available = Available.copy()
    
    for j in range(len(Request)):
        new_Allocated[process_num][j] += Request[j]
        new_Need[process_num][j] -= Request[j]
        new_Available[j] -= Request[j]
    
    is_safe, safe_sequence = safety_algorithm(new_Need, new_Allocated, new_Available.copy())
    
    if is_safe:
        return (True, safe_sequence, new_Allocated, new_Need, new_Available)
    else:
        return (False, [], Allocated, Need, Available)

def safety_algorithm(Need, Allocated, Work):
    n = len(Need)
    m = len(Work)
    Finish = [False] * n
    safe_sequence = []
    
    while True:
        found = False
        for i in range(n):
            if not Finish[i]:
                can_allocate = True
                for j in range(m):
                    if Need[i][j] > Work[j]:
                        can_allocate = False
                        break
                
                if can_allocate:
                    for j in range(m):
                        Work[j] += Allocated[i][j]
                    Finish[i] = True
                    safe_sequence.append(i)
                    found = True
        
        if not found:
            break
    
    is_safe = all(Finish)
    return (is_safe, safe_sequence if is_safe else [])

def print_matrices(name, matrix):
    print(f"{name}:")
    for row in matrix:
        print(" ".join(f"{val:3}" for val in row))
    print()

def test_case():
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
    
    Available = [3, 3, 2]
    Request = [1, 0, 2]
    process_num = 1
    
    print("初始状态:")
    print_matrices("Max", Max)
    print_matrices("Allocated", Allocated)
    Need = [[Max[i][j] - Allocated[i][j] for j in range(len(Max[0]))] for i in range(len(Max))]
    print_matrices("Need", Need)
    print("Available:", Available)
    print("\n进程 P{} 请求资源: {}".format(process_num, Request))
    
    is_safe, safe_sequence, new_Allocated, new_Need, new_Available = banker_algorithm(
        Max, Allocated, Available, Request, process_num
    )
    
    if is_safe:
        print("\n请求可以安全分配")
        print("安全序列:", " -> ".join(f"P{p}" for p in safe_sequence))
        print("\n分配后状态:")
        print_matrices("Allocated", new_Allocated)
        print_matrices("Need", new_Need)
        print("Available:", new_Available)
    else:
        print("\n请求不能分配，会导致系统不安全")

if __name__ == "__main__":
    test_case()
