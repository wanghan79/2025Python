import os
import random
def StaticRes(*stats):
    def decarator(func):
        def wrapper(*args, **kwargs):
            #根据StaticRes参数，获取统计方式：SUM,AVG,MAX,MIN
            #调用被修饰的DataSampling -执行func
            #对DataSampling获得的结果进行统计 -修饰功能
            # 调用被修饰的函数 dataSampling
            data = func(*args, **kwargs)

            # 初始化统计结果字典
            result = {}

            # 根据统计方式计算统计结果
            for stat in stats:
                if stat == "SUM":
                    result["SUM"] = sum(data)
                elif stat == "AVG":
                    result["AVG"] = sum(data) / len(data) if data else 0
                elif stat == "MAX":
                    result["MAX"] = max(data) if data else None
                elif stat == "MIN":
                    result["MIN"] = min(data) if data else None
                else:
                    raise ValueError(f"Unsupported statistic: {stat}")

            return result

        return wrapper

    return decarator

def dataSampling(**kwargs):
    ...


#定义所的修饰函数
@StaticRes("SUM","AVG","MAX","MIN")
def dataSampling(num_samples=10, lower_bound=0, upper_bound=100):
    return [random.randint(lower_bound, upper_bound) for _ in range(num_samples)]


#调用修饰后的函数，实现所有随机样本中的数值内容统计
result = dataSampling()
print(result)

