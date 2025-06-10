def banker(Max, Need, Available, Allocated, Request):
    n = len(Max)
    m = len(Available)
    i = 0
    while i < m:
        if Request[i] > Need[0][i]:
            print("请求超出需求")
            return
        if Request[i] > Available[i]:
            print("资源不足，不能分配")
            return
        i += 1
    i = 0
    while i < m:
        Available[i] = Available[i] - Request[i]
        Allocated[0][i] = Allocated[0][i] + Request[i]
        Need[0][i] = Need[0][i] - Request[i]
        i += 1
    Work = []
    Finish = []
    i = 0
    while i < m:
        Work.append(Available[i])
        i += 1
    i = 0
    while i < n:
        Finish.append(False)
        i += 1
    safe = []
    count = 0
    while count < n:
        found = False
        i = 0
        while i < n:
            if Finish[i] == False:
                j = 0
                ok = True
                while j < m:
                    if Need[i][j] > Work[j]:
                        ok = False
                    j += 1
                if ok:
                    j = 0
                    while j < m:
                        Work[j] = Work[j] + Allocated[i][j]
                        j += 1
                    safe.append(i)
                    Finish[i] = True
                    found = True
                    count += 1
            i += 1
        if found == False:
            break
    if count == n:
        print("可以分配，系统安全")
        print("Max =", Max)
        print("Need =", Need)
        print("Available =", Available)
        print("Allocated =", Allocated)
    else:
        print("不能分配，系统不安全")

Max = [[7,5,3],[3,2,2],[9,0,2],[2,2,2],[4,3,3]]
Allocated = [[0,1,0],[2,0,0],[3,0,2],[2,1,1],[0,0,2]]
Need = []
i = 0
while i < len(Max):
    row = []
    j = 0
    while j < len(Max[0]):
        row.append(Max[i][j] - Allocated[i][j])
        j += 1
    Need.append(row)
    i += 1
Available = [3,3,2]
Request = [1,0,2]

banker(Max, Need, Available, Allocated, Request)
