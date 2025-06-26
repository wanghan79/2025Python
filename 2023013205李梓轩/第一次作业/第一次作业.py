"""
    content:BankersAlgorithm
    author:Li Zixuan
    date:2025/5/8
"""
class BankersAlgorithm:
    def __init__(self, processes, resources):
        """
        初始化银行家算法
        :param processes: 进程数量
        :param resources: 资源种类数量
        """
        self.processes = processes
        self.resources = resources

        # 最大需求矩阵
        self.max_claim = []
        # 已分配矩阵
        self.allocation = []
        # 需求矩阵
        self.need = []
        # 可用资源向量
        self.available = []
        # 安全序列存储
        self.safe_sequence = []

    def initialize_from_external(self, Max, Need, Available, Allocated):
        """
        从外部传入Max、Need、Available、Allocated初始化算法状态
        """
        self.max_claim = [list(row) for row in Max]
        self.need = [list(row) for row in Need]
        self.available = list(Available)
        self.allocation = [list(row) for row in Allocated]
        self.safe_sequence = []

    def is_safe(self):
        """检查系统是否处于安全状态"""
        work = self.available.copy()
        finish = [False] * self.processes
        self.safe_sequence = []

        # 查找安全序列
        while True:
            found = False
            for i in range(self.processes):
                if not finish[i]:
                    # 检查进程i的资源需求是否满足
                    need_met = True
                    for j in range(self.resources):
                        if self.need[i][j] > work[j]:
                            need_met = False
                            break

                    if need_met:
                        # 分配资源给进程i
                        for j in range(self.resources):
                            work[j] += self.allocation[i][j]
                        finish[i] = True
                        self.safe_sequence.append(f"P{i}")
                        found = True
                        # print(f"执行 P{i}，释放资源后可用: {work}")

            if not found:
                break

        # 检查所有进程是否完成
        return all(finish)

    def request_resources(self, process_id, request):
        """
        处理资源请求
        返回 (结果状态, Available, Allocation, Need)
        """
        # 0. 检查进程ID是否有效
        if process_id < 0 or process_id >= self.processes:
            return ("失败：无效的进程ID", self.available, self.allocation, self.need)

        # 1. 检查请求是否超过需求
        for j in range(self.resources):
            if request[j] > self.need[process_id][j]:
                return ("失败：请求超过需求", self.available, self.allocation, self.need)

        # 2. 检查请求是否超过可用资源
        for j in range(self.resources):
            if request[j] > self.available[j]:
                return ("失败：请求超过可用资源", self.available, self.allocation, self.need)

        # 3. 尝试分配资源
        old_available = self.available.copy()
        old_allocation = [row.copy() for row in self.allocation]
        old_need = [row.copy() for row in self.need]

        # 执行分配
        for j in range(self.resources):
            self.available[j] -= request[j]
            self.allocation[process_id][j] += request[j]
            self.need[process_id][j] -= request[j]

        # 4. 检查安全性
        is_safe = self.is_safe()

        if is_safe:
            result_message = f"成功：分配安全（安全序列: {' → '.join(self.safe_sequence)}）"
            return (result_message, self.available, self.allocation, self.need)
        else:
            # 5. 如果不安全则回滚
            self.available = old_available
            self.allocation = old_allocation
            self.need = old_need
            return ("失败：分配后系统进入不安全状态", self.available, self.allocation, self.need)

    def get_current_state(self):
        """获取当前系统状态"""
        return {
            "Max": self.max_claim,
            "Need": self.need,
            "Allocation": self.allocation,
            "Available": self.available
        }

    def print_state(self):
        """打印当前系统状态"""
        state = self.get_current_state()
        print("\n当前系统状态:")
        print("最大需求矩阵 (Max Claim):")
        for i, row in enumerate(state["Max"]):
            print(f"进程{i}:\t{row}")

        print("\n已分配矩阵 (Allocation):")
        for i, row in enumerate(state["Allocation"]):
            print(f"进程{i}:\t{row}")

        print("\n需求矩阵 (Need):")
        for i, row in enumerate(state["Need"]):
            print(f"进程{i}:\t{row}")

        print("\n可用资源 (Available):", state["Available"])


def bank_algorithm(Max, Need, Available, Allocated, request, process_id):
    """
    银行家算法封装函数

    参数:
        Max: 最大需求矩阵 (n x m)
        Need: 需求矩阵 (n x m)
        Available: 可用资源向量 (1 x m)
        Allocated: 已分配矩阵 (n x m)
        request: 资源请求向量 (1 x m)
        process_id: 请求资源的进程索引

    返回:
        (result, Available, Allocation, Need)
        result: 字符串，表示分配结果
        Available, Allocation, Need: 分配后的状态矩阵
    """
    # 获取进程数和资源种类数
    n = len(Max)  # 进程数
    m = len(Max[0]) if n > 0 else 0  # 资源种类数

    # 检查矩阵维度一致性
    if (len(Need) != n or len(Allocated) != n or
            any(len(Max[i]) != m for i in range(n)) or
            any(len(Need[i]) != m for i in range(n)) or
            any(len(Allocated[i]) != m for i in range(n)) or
            len(Available) != m or len(request) != m):
        return ("失败：输入的矩阵维度不一致", Available, Allocated, Need)

    # 创建银行家算法实例
    banker = BankersAlgorithm(n, m)

    # 使用外部提供的数据初始化
    banker.initialize_from_external(Max, Need, Available, Allocated)

    # 处理资源请求
    result, new_available, new_allocation, new_need = banker.request_resources(process_id, request)

    # 返回结果
    return (result, new_available, new_allocation, new_need)


# 测试示例
if __name__ == "__main__":
    # 示例数据（5个进程，3种资源）
    Max = [
        [7, 5, 3],  # P0
        [3, 2, 2],  # P1
        [9, 0, 2],  # P2
        [2, 2, 2],  # P3
        [4, 3, 3]  # P4
    ]
    Allocation = [
        [0, 1, 0],  # P0
        [2, 0, 0],  # P1
        [3, 0, 2],  # P2
        [2, 1, 1],  # P3
        [0, 0, 2]  # P4
    ]
    Need = [
        [7, 4, 3],  # P0
        [1, 2, 2],  # P1
        [6, 0, 0],  # P2
        [0, 1, 1],  # P3
        [4, 3, 1]  # P4
    ]
    Available = [3, 3, 2]

    print("===== 银行家算法测试 =====")
    print("测试1：安全请求（进程1请求[1, 0, 2]）")
    result, new_available, new_allocation, new_need = bank_algorithm(
        Max, Need, Available, Allocation, [1, 0, 2], 1
    )
    print("\n分配结果:", result)
    print("分配后的Available:", new_available)
    print("分配后的Allocation:")
    for i, row in enumerate(new_allocation):
        print(f"进程{i}:\t{row}")
    print("分配后的Need:")
    for i, row in enumerate(new_need):
        print(f"进程{i}:\t{row}")

    print("\n测试2：不安全请求（进程0请求[0, 2, 0]）")
    result, new_available, new_allocation, new_need = bank_algorithm(
        Max, Need, Available, Allocation, [0, 2, 0], 0
    )
    print("\n分配结果:", result)

    print("\n测试3：无效请求（进程1请求[1, 0, 3]超过Available）")
    result, new_available, new_allocation, new_need = bank_algorithm(
        Max, Need, Available, Allocation, [1, 0, 3], 1
    )
    print("\n分配结果:", result)