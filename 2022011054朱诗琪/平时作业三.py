import random
import math
import string
'''
通过装饰器实现了一个数据统计分析工具，
它能够从复杂结构数据中提取数值型数据，
并提供交互式界面让用户选择数据类型（整数、浮点数或两者）和统计方法（求和、均值、方差、均方根误差、最大值、最小值）进行计算。
'''
def StaticRes(*stats):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 1. 调用原函数，生成结构数据
            samples = func(*args, **kwargs)

            # 2. 打印每条生成的数据结构
            for i, sample in enumerate(samples):
                print(f"生成数据为: {sample}")

            # 3. 遍历提取所有数值型数据
            numbers = []

            def collect(d):
                if isinstance(d, (int, float)):
                    numbers.append(d)
                elif isinstance(d, (list, tuple, set)):
                    for item in d:
                        collect(item)
                elif isinstance(d, dict):
                    for v in d.values():
                        collect(v)

            for sample in samples:
                collect(sample)

            print(f"\n可参与运算的数据为: {numbers}\n")

            # 4. 交互部分
            while True:
                type_choice = input("请选择要处理的数据类型: 整数类型（int）, 浮点数类型（float）, 或两者一起处理（both)。\n请输入 'int', 'float', 'both', 或输入 'e' 直接退出: ").strip().lower()
                if type_choice == 'e':
                    break
                if type_choice not in ('int', 'float', 'both'):
                    print("输入无效，请重新输入。\n")
                    continue

                # 5. 根据类型过滤数据
                if type_choice == 'int':
                    selected = [x for x in numbers if isinstance(x, int)]
                elif type_choice == 'float':
                    selected = [x for x in numbers if isinstance(x, float)]
                else:
                    selected = numbers

                if not selected:
                    print("选中的数据类型中无数据可处理。\n")
                    continue

                method = input("请选择要进行的运算: 求和（sum), 求均值（ave）, 求方差（var）, 均方根误差（rmse）, 最大值（max）, 最小值（min）。\n请输入 'sum', 'ave', 'var', 'rmse', 'max', 'min'，或输入 'e' 直接退出: ").strip().lower()
                if method == 'e':
                    break
                if method not in ('sum', 'ave', 'var', 'rmse', 'max', 'min'):
                    print("输入无效，请重新输入。\n")
                    continue

                result = None
                if method == 'sum':
                    result = sum(selected)
                elif method == 'ave':
                    result = sum(selected) / len(selected)
                elif method == 'var':
                    avg = sum(selected) / len(selected)
                    result = sum((x - avg) ** 2 for x in selected) / len(selected)
                elif method == 'rmse':
                    avg = sum(selected) / len(selected)
                    mse = sum((x - avg) ** 2 for x in selected) / len(selected)
                    result = math.sqrt(mse)
                elif method == 'max':
                    result = max(selected)
                elif method == 'min':
                    result = min(selected)

                print(f"所选数据的 {method} 为: {round(result, 4)}\n")
        return wrapper
    return decorator

@StaticRes('SUM', 'AVG', 'VAR', 'RMSE', 'MAX', 'MIN')
def dataSampling(count=2, **kwargs):
    result = []
    for _ in range(count):
        item = [
            random.randint(1, 20),
            random.uniform(1.0, 10.0),
            ([random.randint(1, 20)], [""]),
            [[random.randint(10, 30), ''.join(random.choices(string.ascii_lowercase, k=8)), random.uniform(1.0, 10.0)]]
        ]
        result.append(item)
    return result

if __name__ == "__main__":
    dataSampling()
