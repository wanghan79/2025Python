"""
    content:BankersAlgorithm
    author:Zhang Lizhi
    date:2025/4/1
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

        self.max_claim = []
        # 已分配矩阵
        self.allocation = []
        # 需求矩阵
        self.need = []
        # 可用资源向量
        self.available = []

    def initialize(self):
        print("\n输入最大需求矩阵 (Max):")
        self.max_claim = self._input_matrix(self.processes, self.resources)
        print("\n输入已分配矩阵 (Allocation):")
        self.allocation = self._input_matrix(self.processes, self.resources)

        # need = Max - Allocation
        self.need = [
            [self.max_claim[i][j] - self.allocation[i][j]
            for j in range(self.resources)]
            for i in range(self.processes)
        ]

        print("\n输入可用资源向量 (Available):")
        self.available = [int(x) for x in input().split()]

    def _input_matrix(self, rows, cols):
        """辅助方法：输入矩阵"""
        matrix = []
        for i in range(rows):
            row = [int(x) for x in input(f"进程 P{i}: ").split()]
            if len(row) != cols:
                raise ValueError("输入资源数量不匹配!")
            matrix.append(row)
        return matrix

    def is_safe(self):
        """检查系统是否处于安全状态"""
        # 初始化工作向量
        work = self.available.copy()
        finish = [False] * self.processes
        safe_sequence = []

        while True:
            found = False
            for i in range(self.processes):
                if not finish[i] and all(self.need[i][j] <= work[j] for j in range(self.resources)):
                    # 执行该进程并释放资源
                    for j in range(self.resources):
                        work[j] += self.allocation[i][j]
                    finish[i] = True
                    safe_sequence.append(f"P{i}")
                    found = True
                    print(f"执行 P{i}，释放资源后可用: {work}")

            if not found:
                break

        if all(finish):
            print(f"\n安全序列: {' -> '.join(safe_sequence)}")
            return True
        else:
            print("\n系统处于不安全状态！可能导致死锁")
            return False

    def request_resources(self, process_id, request):
        """处理资源请求"""
        # 请求<=需求
        if any(request[j] > self.need[process_id][j] for j in range(self.resources)):
            print("错误：请求超过声明的最大需求")
            return False

        # 请求<=可用资源
        if any(request[j] > self.available[j] for j in range(self.resources)):
            print("错误：请求超过可用资源")
            return False

        # 尝试分配
        print("\n尝试分配资源...")
        for j in range(self.resources):
            self.available[j] -= request[j]
            self.allocation[process_id][j] += request[j]
            self.need[process_id][j] -= request[j]

        # 检查安全性
        if self.is_safe():
            print("资源分配成功，系统仍处于安全状态")
            return True
        else:
            # 撤销分配
            print("资源分配会导致系统不安全，撤销分配...")
            for j in range(self.resources):
                self.available[j] += request[j]
                self.allocation[process_id][j] -= request[j]
                self.need[process_id][j] += request[j]
            return False


def main():
    print("===== 银行家算法演示 =====")
    processes = int(input("输入进程数量: "))
    resources = int(input("输入资源种类数量: "))

    banker = BankersAlgorithm(processes, resources)
    banker.initialize()

    # 初始安全检查
    print("\n正在进行初始安全检查...")
    banker.is_safe()

    while True:
        print("\n1. 请求资源分配")
        print("2. 显示当前状态")
        print("3. 退出")
        choice = input("请选择操作: ")

        if choice == '1':
            pid = int(input("输入进程ID (0开始): "))
            req = [int(x) for x in input("输入请求资源向量: ").split()]
            banker.request_resources(pid, req)
        elif choice == '2':
            print("\n当前系统状态:")
            print("Max Claim:")
            for row in banker.max_claim:
                print(row)
            print("\nAllocation:")
            for row in banker.allocation:
                print(row)
            print("\nNeed:")
            for row in banker.need:
                print(row)
            print("\nAvailable:", banker.available)
        elif choice == '3':
            break
        else:
            print("无效输入")


if __name__ == "__main__":
    main()