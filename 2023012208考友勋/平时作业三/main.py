import random
from functools import wraps

def stats(operations):
    """
    带参装饰器，用于对数据生成函数的结果进行统计操作
    
    参数:
    operations (list): 包含统计操作名称的列表，支持 'SUM', 'AVG', 'MAX', 'MIN', 
                       'COUNT', 'VAR', 'STD', 'MEDIAN', 'RANGE'
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 调用被装饰的函数获取数据
            data = func(*args, **kwargs)
            
            # 提取数值类型数据
            numeric_data = [x for x in data if isinstance(x, (int, float))]
            
            # 验证数据有效性
            if not numeric_data:
                return {
                    'raw_data': data,
                    'numeric_data': numeric_data,
                    'statistics': {op: None for op in operations},
                    'error': 'No numeric data available for statistics'
                }
            
            # 存储统计结果的字典
            results = {
                'raw_data': data,
                'numeric_data': numeric_data,
                'statistics': {}
            }
            
            # 根据指定的操作进行统计
            if 'SUM' in operations:
                results['statistics']['SUM'] = sum(numeric_data)
            if 'AVG' in operations:
                results['statistics']['AVG'] = sum(numeric_data) / len(numeric_data)
            if 'MAX' in operations:
                results['statistics']['MAX'] = max(numeric_data)
            if 'MIN' in operations:
                results['statistics']['MIN'] = min(numeric_data)
            if 'COUNT' in operations:
                results['statistics']['COUNT'] = len(numeric_data)
            if 'VAR' in operations:
                mean = sum(numeric_data) / len(numeric_data)
                results['statistics']['VAR'] = sum((x - mean) ** 2 for x in numeric_data) / len(numeric_data)
            if 'STD' in operations:
                mean = sum(numeric_data) / len(numeric_data)
                variance = sum((x - mean) ** 2 for x in numeric_data) / len(numeric_data)
                results['statistics']['STD'] = variance ** 0.5
            if 'MEDIAN' in operations:
                sorted_data = sorted(numeric_data)
                n = len(sorted_data)
                if n % 2 == 0:
                    results['statistics']['MEDIAN'] = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
                else:
                    results['statistics']['MEDIAN'] = sorted_data[n//2]
            if 'RANGE' in operations:
                results['statistics']['RANGE'] = max(numeric_data) - min(numeric_data)
            
            return results
        return wrapper
    return decorator

@stats(['SUM', 'AVG', 'MAX', 'MIN', 'COUNT', 'VAR', 'STD', 'MEDIAN', 'RANGE'])
def generate_random_sample(n, low=1, high=100, include_strings=False, include_bools=False):
    """
    生成混合类型的随机样本
    
    参数:
    n (int): 样本大小
    low (int): 随机数下限
    high (int): 随机数上限
    include_strings (bool): 是否包含随机字符串
    include_bools (bool): 是否包含布尔值
    """
    sample = []
    for _ in range(n):
        choices = ['int', 'float']
        if include_strings:
            choices.append('string')
        if include_bools:
            choices.append('bool')
        
        data_type = random.choice(choices)
        if data_type == 'int':
            sample.append(random.randint(low, high))
        elif data_type == 'float':
            sample.append(round(random.uniform(low, high), 2))
        elif data_type == 'string':
            sample.append(''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5)))
        elif data_type == 'bool':
            sample.append(random.choice([True, False]))
    
    return sample

# 测试代码
if __name__ == "__main__":
    # 生成15个1-100之间的随机数，包含字符串和布尔值
    result = generate_random_sample(15, 1, 100, include_strings=True, include_bools=True)
    
    print("原始数据:", result['raw_data'])
    print("数值数据:", result['numeric_data'])
    
    print("\n统计结果:")
    for stat, value in result['statistics'].items():
        print(f"{stat}: {value}")
