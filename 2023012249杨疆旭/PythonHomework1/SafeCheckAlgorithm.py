import copy

def input_matrix(rows, cols, name):
    matrix = []
    print(f"\n请输入{name}矩阵（每行用空格分隔）:")
    for i in range(rows):
        while True:
            row = input(f"进程{i} > ").split()
            if len(row) != cols:
                print(f"错误：需要输入{cols}个数值")
                continue
            try:
                values = [int(x) for x in row]
                if any(v < 0 for v in values):
                    print("错误：不能包含负数")
                    continue
                matrix.append(values)
                break
            except ValueError:
                print("错误：请输入整数")

def input_vector(length, name):
    while True:
        values = input(f"\n请输入{name}向量（用空格分隔）> ").split()
        if len(values) != length:
            print(f"错误：需要输入{length}个数值")
            continue
        try:
            result = [int(x) for x in values]
            if any(v < 0 for v in result):
                print("错误：不能包含负数")
                continue
            return result
        except ValueError:
            print("错误：请输入整数")

def safety_check(max_res, allocated, available):
    processes = len(max_res)
    resource_types = len(available)

    need = [
        [max_res[i][j] - allocated[i][j]
         for j in range(resource_types)]
        for i in range(processes)
    ]

    work = copy.deepcopy(available)
    finish = [False] * processes
    safe_seq = []

    for _ in range(processes):
        progress = False
        for i in range(processes):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(resource_types)):
                # 释放资源
                for j in range(resource_types):
                    work[j] += allocated[i][j]
                finish[i] = True
                safe_seq.append(i)
                progress = True
        if not progress:
            break

    is_safe = all(finish)
    msg = "安全状态：系统安全" if is_safe else "安全状态：检测到死锁风险"
    return is_safe, safe_seq, msg

if __name__ == "__main__":
    try:
        processes = int(input("请输入进程数: "))
        resource_types = int(input("请输入资源类型数: "))
        if processes <= 0 or resource_types <= 0:
            raise ValueError("进程数和资源类型数必须大于0")

        max_res = input_matrix(processes, resource_types, "最大需求")
        allocated = input_matrix(processes, resource_types, "已分配")
        available = input_vector(resource_types, "可用资源")

        is_safe, sequence, msg = safety_check(max_res, allocated, available)

        print("\n===== 系统安全检测报告 =====")
        print(msg)
        print(f"安全序列: {sequence if is_safe else '无有效安全序列'}")
        print("=" * 30)

    except ValueError as e:
        print(f"\n错误：输入数据不合法 - {str(e)}")
    except Exception as e:
        print(f"\n运行时错误：{str(e)}")