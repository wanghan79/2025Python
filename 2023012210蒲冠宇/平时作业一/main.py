"""
    模块功能: 银行家算法实现
    作者信息: Li Zixuan
    创建日期: 2025/5/8
"""

class ResourceManager:
    """银行家算法的资源管理器，用于实现死锁避免策略"""
    
    def __init__(self, num_processes, num_resources):
        """
        初始化资源管理器
        :param num_processes: 系统中的进程总数
        :param num_resources: 系统中的资源类型数
        """
        self.num_processes = num_processes
        self.num_resources = num_resources
        
        # 系统资源状态矩阵
        self.max_demand = []      # 最大需求矩阵
        self.allocated = []       # 已分配资源矩阵
        self.remaining_need = []  # 仍需资源矩阵
        self.available_res = []   # 可用资源向量
        self.safety_sequence = [] # 安全序列记录

    def load_system_state(self, max_matrix, need_matrix, available, allocation_matrix):
        """
        从外部加载系统状态数据
        :param max_matrix: 最大需求矩阵
        :param need_matrix: 需求矩阵
        :param available: 可用资源向量
        :param allocation_matrix: 已分配资源矩阵
        """
        self.max_demand = [list(row) for row in max_matrix]
        self.remaining_need = [list(row) for row in need_matrix]
        self.available_res = list(available)
        self.allocated = [list(row) for row in allocation_matrix]
        self.safety_sequence = []

    def is_system_safe(self):
        """
        执行安全性检查算法
        :return: 如果系统处于安全状态返回True，否则返回False
        """
        # 复制当前可用资源和初始化完成标志
        work = self.available_res.copy()
        finish = [False] * self.num_processes
        self.safety_sequence = []
        
        # 模拟资源分配过程
        while True:
            found = False
            for i in range(self.num_processes):
                if not finish[i] and self._can_allocate(i, work):
                    # 分配资源并回收
                    for j in range(self.num_resources):
                        work[j] += self.allocated[i][j]
                    finish[i] = True
                    self.safety_sequence.append(f"P{i}")
                    found = True
                    break  # 每次找到一个可执行进程后重新扫描
            
            if not found:
                break
        
        # 检查是否所有进程都能完成
        return all(finish)

    def _can_allocate(self, process_id, work_resources):
        """
        判断是否可以将资源分配给指定进程
        :param process_id: 进程ID
        :param work_resources: 当前可用资源向量
        :return: 如果可以分配返回True，否则返回False
        """
        for j in range(self.num_resources):
            if self.remaining_need[process_id][j] > work_resources[j]:
                return False
        return True

    def process_request(self, process_id, request):
        """
        处理资源请求
        :param process_id: 请求资源的进程ID
        :param request: 请求的资源向量
        :return: (结果消息, 可用资源, 已分配矩阵, 需求矩阵)
        """
        # 验证请求合法性
        if not self._is_valid_request(process_id, request):
            return ("非法请求：无效的进程ID或请求超过需求", 
                    self.available_res, self.allocated, self.remaining_need)
        
        # 检查资源是否足够
        if any(request[j] > self.available_res[j] for j in range(self.num_resources)):
            return ("请求被拒绝：可用资源不足", 
                    self.available_res, self.allocated, self.remaining_need)
        
        # 尝试资源分配
        old_state = self._save_state()
        self._allocate_resources(process_id, request)
        
        # 检查安全性
        if self.is_system_safe():
            result_msg = f"请求被批准（安全序列: {' → '.join(self.safety_sequence)}）"
            return (result_msg, self.available_res, self.allocated, self.remaining_need)
        else:
            # 回滚到原始状态
            self._restore_state(old_state)
            return ("请求被拒绝：分配将导致系统进入不安全状态", 
                    self.available_res, self.allocated, self.remaining_need)

    def _is_valid_request(self, process_id, request):
        """验证请求的合法性"""
        if process_id < 0 or process_id >= self.num_processes:
            return False
        return all(request[j] <= self.remaining_need[process_id][j] for j in range(self.num_resources))

    def _save_state(self):
        """保存当前系统状态用于回滚"""
        return {
            'available': self.available_res.copy(),
            'allocated': [row.copy() for row in self.allocated],
            'need': [row.copy() for row in self.remaining_need]
        }

    def _restore_state(self, state):
        """从保存的状态中恢复系统"""
        self.available_res = state['available']
        self.allocated = state['allocated']
        self.remaining_need = state['need']

    def _allocate_resources(self, process_id, request):
        """执行资源分配操作"""
        for j in range(self.num_resources):
            self.available_res[j] -= request[j]
            self.allocated[process_id][j] += request[j]
            self.remaining_need[process_id][j] -= request[j]

    def get_system_status(self):
        """获取当前系统状态"""
        return {
            "MaxDemand": self.max_demand,
            "Need": self.remaining_need,
            "Allocation": self.allocated,
            "Available": self.available_res
        }

    def display_status(self):
        """打印当前系统状态"""
        status = self.get_system_status()
        print("\n系统当前状态:")
        
        print("最大需求矩阵 (Max Demand):")
        for i, row in enumerate(status["MaxDemand"]):
            print(f"进程 {i}:\t{row}")

        print("\n已分配资源矩阵 (Allocation):")
        for i, row in enumerate(status["Allocation"]):
            print(f"进程 {i}:\t{row}")

        print("\n需求矩阵 (Remaining Need):")
        for i, row in enumerate(status["Need"]):
            print(f"进程 {i}:\t{row}")

        print("\n可用资源 (Available):", status["Available"])


def execute_banker_algorithm(max_matrix, need_matrix, available, allocation_matrix, request, process_id):
    """
    执行银行家算法处理资源请求
    :param max_matrix: 最大需求矩阵
    :param need_matrix: 需求矩阵
    :param available: 可用资源向量
    :param allocation_matrix: 已分配资源矩阵
    :param request: 请求的资源向量
    :param process_id: 请求资源的进程ID
    :return: (结果消息, 新的可用资源, 新的已分配矩阵, 新的需求矩阵)
    """
    # 验证输入矩阵维度
    n_processes = len(max_matrix)
    if n_processes == 0:
        return ("错误：进程数量不能为0", available, allocation_matrix, need_matrix)
    
    m_resources = len(max_matrix[0])
    
    # 检查所有矩阵维度是否一致
    if (len(need_matrix) != n_processes or 
        len(allocation_matrix) != n_processes or
        any(len(row) != m_resources for row in max_matrix) or
        any(len(row) != m_resources for row in need_matrix) or
        any(len(row) != m_resources for row in allocation_matrix) or
        len(available) != m_resources or
        len(request) != m_resources):
        return ("错误：输入矩阵维度不一致", available, allocation_matrix, need_matrix)
    
    # 创建资源管理器实例
    banker = ResourceManager(n_processes, m_resources)
    
    # 加载系统状态
    banker.load_system_state(max_matrix, need_matrix, available, allocation_matrix)
    
    # 处理资源请求
    result, new_available, new_allocation, new_need = banker.process_request(process_id, request)
    
    return (result, new_available, new_allocation, new_need)


# 测试用例
if __name__ == "__main__":
    # 示例数据（5个进程，3种资源）
    max_demand = [
        [7, 5, 3],  # P0
        [3, 2, 2],  # P1
        [9, 0, 2],  # P2
        [2, 2, 2],  # P3
        [4, 3, 3]   # P4
    ]
    
    allocated_resources = [
        [0, 1, 0],  # P0
        [2, 0, 0],  # P1
        [3, 0, 2],  # P2
        [2, 1, 1],  # P3
        [0, 0, 2]   # P4
    ]
    
    remaining_need = [
        [7, 4, 3],  # P0
        [1, 2, 2],  # P1
        [6, 0, 0],  # P2
        [0, 1, 1],  # P3
        [4, 3, 1]   # P4
    ]
    
    available_resources = [3, 3, 2]

    print("===== 银行家算法测试 =====")
    
    print("测试场景1：安全请求（进程1请求 [1, 0, 2]）")
    result, new_available, new_allocation, new_need = execute_banker_algorithm(
        max_demand, remaining_need, available_resources, allocated_resources, [1, 0, 2], 1
    )
    print("\n分配结果:", result)
    print("分配后的可用资源:", new_available)
    print("分配后的已分配矩阵:")
    for i, row in enumerate(new_allocation):
        print(f"进程 {i}:\t{row}")
    print("分配后的需求矩阵:")
    for i, row in enumerate(new_need):
        print(f"进程 {i}:\t{row}")

    print("\n测试场景2：不安全请求（进程0请求 [0, 2, 0]）")
    result, new_available, new_allocation, new_need = execute_banker_algorithm(
        max_demand, remaining_need, available_resources, allocated_resources, [0, 2, 0], 0
    )
    print("\n分配结果:", result)

    print("\n测试场景3：无效请求（进程1请求 [1, 0, 3] 超过可用资源）")
    result, new_available, new_allocation, new_need = execute_banker_algorithm(
        max_demand, remaining_need, available_resources, allocated_resources, [1, 0, 3], 1
    )
    print("\n分配结果:", result)
