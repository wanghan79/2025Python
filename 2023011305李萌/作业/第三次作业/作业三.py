import random
import string
from functools import wraps

# 数据类型定义
SCALAR_TYPES = {'integer', 'decimal', 'text'}
CONTAINER_TYPES = {'array', 'record', 'mapping'}

class StatCollector:
    
    
    def __init__(self):
        self.values = []
    
    def add(self, value):
    
        if isinstance(value, (int, float)):
            self.values.append(value)
    
    def calculate(self, stats):
        
        result = {}
        if not self.values:
            return {stat: None for stat in stats}
            
        if 'SUM' in stats:
            result['SUM'] = sum(self.values)
        if 'AVG' in stats:
            result['AVG'] = sum(self.values) / len(self.values)
        if 'MAX' in stats:
            result['MAX'] = max(self.values)
        if 'MIN' in stats:
            result['MIN'] = min(self.values)
            
        return result

def DataStats(*requested_stats):
    """
    带参装饰器：对数据生成函数进行统计
    
    参数:
        requested_stats: 需要计算的统计指标列表
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            collector = StatCollector()
            for item in func(*args, **kwargs):
                collector.add(item)
            return collector.calculate(requested_stats)
        return wrapper
    return decorator

def generate_scalar(data_spec):
    """生成标量数据（数值或字符串）"""
    data_type = data_spec['type']
    config = data_spec.get('config', {})
    
    if data_type == 'integer':
        min_val, max_val = config.get('range', (0, 100))
        return random.randint(min_val, max_val)
        
    elif data_type == 'decimal':
        min_val, max_val = config.get('range', (0.0, 1.0))
        return random.uniform(min_val, max_val)
        
    elif data_type == 'text':
        char_set = config.get('charset', string.ascii_letters)
        length = config.get('length', 10)
        return ''.join(random.choice(char_set) for _ in range(length))
        
    raise ValueError(f"不支持的标量类型: {data_type}")

def generate_container(data_spec):
    """生成容器数据（数组、记录、映射）"""
    container_type = data_spec['type']
    config = data_spec.get('config', {})
    elements = config.get('elements', [])
    count = config.get('count', 1)
    
    if container_type == 'array':
        return [generate_data(elem) for elem in elements for _ in range(count)]
        
    elif container_type == 'record':
        return tuple(generate_data(elem) for elem in elements for _ in range(count))
        
    elif container_type == 'mapping':
        return {f"key{i}": generate_data(elem) 
                for i, elem in enumerate(elements) 
                for _ in range(count)}
                
    raise ValueError(f"不支持的容器类型: {container_type}")

def generate_data(data_spec):
    """根据数据规范生成数据"""
    data_type = data_spec['type']
    
    if data_type in SCALAR_TYPES:
        return generate_scalar(data_spec)
        
    if data_type in CONTAINER_TYPES:
        return generate_container(data_spec)
        
    raise ValueError(f"不支持的数据类型: {data_type}")

def flatten(data):
    """递归展开容器中的所有标量值"""
    if isinstance(data, (int, float)):
        yield data
    elif isinstance(data, (list, tuple)):
        for item in data:
            yield from flatten(item)
    elif isinstance(data, dict):
        for value in data.values():
            yield from flatten(value)

@DataStats('SUM', 'AVG', 'MAX', 'MIN')
def create_samples(specification):
    """
    根据规范创建样本数据并应用统计
    
    参数:
        specification: 数据生成规范
    """
    for data_spec in specification:
        data = generate_data(data_spec)
        yield from flatten(data)

if __name__ == "__main__":
    # 示例1：统计数组中的数值
    print("示例1:")
    spec1 = [
        {
            "type": "array",
            "config": {
                "count": 3,
                "elements": [
                    {"type": "integer", "config": {"range": (0, 100)}},
                    {"type": "decimal", "config": {"range": (0.0, 10.0)}},
                ]
            }
        }
    ]
    result1 = create_samples(spec1)
    print(f"统计结果: {result1}")
    
    # 示例2：统计嵌套结构中的数值
    print("\n示例2:")
    spec2 = [
        {
            "type": "record",
            "config": {
                "count": 2,
                "elements": [
                    {
                        "type": "mapping",
                        "config": {
                            "count": 1,
                            "elements": [
                                {"type": "integer", "config": {"range": (1, 10)}},
                                {"type": "decimal", "config": {"range": (0.0, 1.0)}},
                            ]
                        }
                    }
                ]
            }
        }
    ]
    result2 = create_samples(spec2)
    print(f"统计结果: {result2}")
    

    # 示例3：自定义统计指标
    print("\n示例3:")
    @DataStats('MAX', 'MIN')
    def custom_samples(data_specs):
        yield from create_samples(data_specs)
    
    spec3 = [
        {"type": "integer", "config": {"range": (0, 100), "count": 10}},
        {"type": "decimal", "config": {"range": (0.0, 1.0), "count": 10}},
    ]
    result3 = custom_samples(spec3)
    print(f"自定义统计结果: {result3}")