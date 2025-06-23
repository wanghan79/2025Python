def banker_algorithm(Max, Need, Available, Allocated, Request):
    n = len(Max)  
    m = len(Available)  
    
    for i in range(m):
        if Request[i] > Need[n-1][i]:  
            return False, None, None, None, None
    
    for i in range(m):
        if Request[i] > Available[i]:
            return False, None, None, None, None
  
    new_available = Available.copy()
    new_allocated = Allocated[n-1].copy()
    new_need = Need[n-1].copy()
    
    for i in range(m):
        new_available[i] -= Request[i]
        new_allocated[i] += Request[i]
        new_need[i] -= Request[i]
    
    work = new_available.copy()
    finish = [False] * n
    safe_sequence = []
    
    while True:
        found = False
        for i in range(n):
            if not finish[i] and all(Need[i][j] <= work[j] for j in range(m)):
                work = [work[j] + Allocated[i][j] for j in range(m)]
                finish[i] = True
                safe_sequence.append(i)
                found = True
        if not found:
            break
    
    if all(finish):
      
        Need[n-1] = new_need
        Allocated[n-1] = new_allocated
        return True, Need, Allocated, new_available, safe_sequence
    else:
        return False, None, None, None, None

Max = [[7, 5], [3, 2], [9, 0]]
Need = [[7, 5], [3, 2], [9, 0]]
Available = [2, 3]
Allocated = [[0, 1], [2, 0], [3, 0]]
Request = [1, 0]  

result, new_need, new_allocated, new_available, seq = banker_algorithm(Max, Need, Available, Allocated, Request)
print("是否可分配:", result)
if result:
    print("分配后Need矩阵:", new_need)
    print("分配后Allocated矩阵:", new_allocated)
    print("分配后Available矩阵:", new_available)
    print("安全序列:", seq)
