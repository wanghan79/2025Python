import random
import string
from functools import wraps
from typing import Any, Callable, Dict, List, Tuple, Union

# 定义数据生成器的类型
DataGenerator = Callable[..., List[Any]]

# 定义统计函数的类型
StatsFunction = Callable[[List[Union[int, float]]], Dict[str, Union[int, float]]]

# 装饰器：用于统计生成数据中的数值信息
def static_res(*stats: str) -> Callable[[DataGenerator], DataGenerator]:
    def decorator(func: DataGenerator) -> DataGenerator:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Dict[str, Union[int, float]]:
            data = func(*args, **kwargs)  # 调用原始生成器函数
            numbers = extract_numbers(data)  # 提取所有数值
            if not numbers:
                return {}  # 如果没有数值，返回空字典
            return calculate_stats(numbers, stats)  # 计算统计结果
        return wrapper
    return decorator

# 提取数据中的所有数值（递归）
def extract_numbers(data: Any) -> List[Union[int, float]]:
    numbers = []
    if isinstance(data, (int, float)):
        numbers.append(data)
    elif isinstance(data, dict):
        for value in data.values():
            numbers.extend(extract_numbers(value))
    elif isinstance(data, (list, tuple)):
        for item in data:
            numbers.extend(extract_numbers(item))
    return numbers

# 计算统计结果
def calculate_stats(numbers: List[Union[int, float]], stats: Tuple[str]) -> Dict[str, Union[int, float]]:
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

# 数据生成器
def generator(**kwargs: Any) -> List[Any]:
    num = kwargs.get("num", 1)
    result = []
    for _ in range(num):
        res = []
        for key, config in kwargs.items():
            if key == "num":
                continue
            res.append(create_data(key, config))
        result.append(res)
    return result

# 根据数据类型生成单个数据
def create_data(data_type: str, config: Dict[str, Any]) -> Any:
    if data_type == "int":
        return random.randint(*config['datarange'])
    elif data_type == "float":
        return random.uniform(*config['datarange'])
    elif data_type == "str":
        return ''.join(random.choices(config['datarange'], k=config['len']))
    elif data_type == "dict":
        key = ''.join(random.choices(string.ascii_letters, k=3))
        value = random.randint(0, 100)
        return {key: value}
    elif data_type == "list" or data_type == "tuple":
        data = generator(**config)
        return data if data_type == "list" else tuple(data)
    else:
        raise ValueError(f"Unsupported data type: {data_type}")

if __name__ == "__main__":
    # 定义装饰后的生成器函数
    @static_res('SUM', 'AVG', 'MAX', 'MIN')
    def decorated_generator(**kwargs):
        return generator(**kwargs)
    
    # 调用装饰后的函数
    result = decorated_generator(
        num=5,
        int={'datarange': (1, 100)},
        float={'datarange': (1.0, 10.0)},
        dict={},
        list={'num': 3, 'int': {'datarange': (10, 20)}}
    )
    
    # 打印原始数据
    print("原始数据:")
    raw_data = generator(
        num=5,
        int={'datarange': (1, 100)},
        float={'datarange': (1.0, 10.0)},
        dict={},
        list={'num': 3, 'int': {'datarange': (10, 20)}}
    )
    for i, sample in enumerate(raw_data, 1):
        print(f"样本{i}: {sample}")
    
    # 打印统计结果
    print("\n统计结果:")
    print(result)