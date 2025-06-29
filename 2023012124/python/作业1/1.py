import numpy as np

def bankers_algorithm(Max, Need, Available, Allocated, Request):
    num_processes = len(Max)
    num_resources = len(Available)
    
    if any(Request[i] > Need[i] for i in range(num_resources)):
        return "请求超过进程所需资源"
    
    if any(Request[i] > Available[i] for i in range(num_resources)):
        return "请求超过系统可用资源"
    
    Temp_Available = Available.copy()
    Temp_Allocated = Allocated.copy()
    Temp_Need = Need.copy()
    
    for i in range(num_resources):
        Temp_Available[i] -= Request[i]
        Temp_Allocated[num_processes - 1][i] += Request[i]
        Temp_Need[num_processes - 1][i] -= Request[i]
    
    work = Temp_Available.copy()
    finish = [False] * num_processes
    
    while True:
        progress = False
        for i in range(num_processes):
            if not finish[i] and all(Temp_Need[i][j] <= work[j] for j in range(num_resources)):
                for j in range(num_resources):
                    work[j] += Temp_Allocated[i][j]
                finish[i] = True
                progress = True
                break
        
        if not progress:
            break
    
    if all(finish):
        return "请求可以分配", Temp_Allocated, Temp_Need, Temp_Available
    else:
        return "请求不能分配", Allocated, Need, Available

Max = np.array([[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]])
Need = np.array([[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]])
Available = np.array([3, 3, 2])
Allocated = np.array([[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]])
Request = np.array([1, 0, 2])

result = bankers_algorithm(Max, Need, Available, Allocated, Request)
print(result)
