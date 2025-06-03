import os
import random
import string
from functools import wraps

# 带参修饰器
def StaticRes(*stats):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 调用原始函数获取数据
            data = func(*args, **kwargs)
            
            # 提取所有数值(包括int和float)
            numbers = []
            def extract_numbers(item):
                if isinstance(item, (int, float)):
                    numbers.append(item)
                elif isinstance(item, dict):
                    for v in item.values():
                        extract_numbers(v)
                elif isinstance(item, (list, tuple)):
                    for i in item:
                        extract_numbers(i)
            
            for item in data:
                for sub_item in item:
                    extract_numbers(sub_item)
            
            # 如果没有数值数据，返回空字典
            if not numbers:
                return {}
            
            # 计算统计结果
            result = {}
            for stat in stats:
                stat = stat.upper()
                if stat == 'SUM':
                    result['SUM'] = sum(numbers)
                elif stat == 'AVG':
                    result['AVG'] = sum(numbers) / len(numbers)
                elif stat == 'MAX':
                    result['MAX'] = max(numbers)
                elif stat == 'MIN':
                    result['MIN'] = min(numbers)
                elif stat == 'COUNT':
                    result['COUNT'] = len(numbers)
            
            return result
        return wrapper
    return decorator

def Generator(**kwargs):
    # 初始化
    result = list()
    # 提取num
    num = kwargs["num"] if "num" in kwargs else 1

    for _ in range(num):
        res = list()
        for k,v in kwargs.items():
            if k == "num":
                continue
            elif k == "int":
                it = iter(v['datarange'])
                res.append(random.randint(next(it), next(it)))
            elif k == "float":
                it = iter(v['datarange'])
                res.append(random.uniform(next(it), next(it)))
            elif k == "str":
                res.append(''.join([random.SystemRandom().choice(v['datarange']) for _ in range(v['len'])]))
            elif k == "dict":
                key = ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(3))
                value = random.randint(0, 100)
                res.append({key: value})
            elif k == "list":
                res.append(Generator(**v))
            elif k == "tuple":
                res.append(tuple(Generator(**v)))
            else:
                continue
        result.append(res)
    return result

if __name__ == "__main__":
    # 定义修饰函数
    @StaticRes('SUM', 'AVG', 'MAX', 'MIN')
    def decorated_generator(**kwargs):
        return Generator(**kwargs)
    
    # 调用修饰后的函数
    result = decorated_generator(
        num=5,
        int={'datarange': (1, 100)},
        float={'datarange': (1.0, 10.0)},
        dict={},
        list={'num': 3, 'int': {'datarange': (10, 20)}}
    )
    
    print("原始数据:")
    raw_data = Generator(
        num=5,
        int={'datarange': (1, 100)},
        float={'datarange': (1.0, 10.0)},
        dict={},
        list={'num': 3, 'int': {'datarange': (10, 20)}}
    )
    
    for i, sample in enumerate(raw_data, 1):
        print(f"样本{i}: {sample}")
    
    print("\n统计结果:")
    print(result)