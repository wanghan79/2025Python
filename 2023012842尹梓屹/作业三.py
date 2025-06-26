import random
import string
from typing import Dict, List, Union, Generator, Callable
from functools import wraps

# 1. 随机样本生成器基础实现
def random_sample_generator(
    sample_count: int,
    structure: Dict[str, Union[str, List[str], Dict[str, str]]]
) -> Generator[Dict[str, Union[str, int, float, bool]], None, None]:
    """
    随机样本生成器基础函数
    
    参数:
        sample_count: 要生成的样本数量
        structure: 定义样本结构的字典
        
    返回:
        生成器，每次迭代返回一个随机样本字典
    """
    def generate_value(field_type: Union[str, List[str], Dict[str, str]]):
        if isinstance(field_type, dict):
            return {k: generate_value(v) for k, v in field_type.items()}
        elif isinstance(field_type, list):
            return random.choice(field_type)
        elif field_type == "str":
            length = random.randint(5, 15)
            return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        elif field_type == "int":
            return random.randint(0, 100)
        elif field_type == "float":
            return round(random.uniform(0, 100), 2)
        elif field_type == "bool":
            return random.choice([True, False])
        else:
            raise ValueError(f"Unsupported field type: {field_type}")

    for _ in range(sample_count):
        yield {field: generate_value(field_type) for field, field_type in structure.items()}

# 2. 统计修饰器实现
def stats_operations(*operations: str, fields: List[str]):
    """
    带参修饰器工厂函数，为生成器添加统计功能
    
    参数:
        operations: 统计操作列表 (SUM, AVG, MAX, MIN)
        fields: 要统计的字段列表
        
    返回:
        装饰器函数
    """
    valid_ops = {'SUM', 'AVG', 'MAX', 'MIN'}
    
    # 验证操作是否有效
    for op in operations:
        if op not in valid_ops:
            raise ValueError(f"Invalid operation: {op}. Valid operations are: {valid_ops}")
    
    def decorator(generator_func: Callable):
        @wraps(generator_func)
        def wrapper(*args, **kwargs):
            # 初始化统计数据结构
            stats_data = {field: [] for field in fields}
            
            # 创建生成器
            gen = generator_func(*args, **kwargs)
            
            # 定义内部生成器函数
            def wrapped_generator():
                nonlocal stats_data
                
                # 遍历原始生成器
                for sample in gen:
                    # 收集需要统计的字段值
                    for field in fields:
                        if field in sample:
                            value = sample[field]
                            if isinstance(value, (int, float)):
                                stats_data[field].append(value)
                    
                    yield sample
                
                # 所有样本生成完成后，计算统计结果
                print("\n统计结果:")
                for field in fields:
                    if field in stats_data and stats_data[field]:
                        values = stats_data[field]
                        print(f"\n字段 '{field}':")
                        
                        if 'SUM' in operations:
                            print(f"  SUM: {sum(values)}")
                        if 'AVG' in operations:
                            print(f"  AVG: {sum(values)/len(values):.2f}")
                        if 'MAX' in operations:
                            print(f"  MAX: {max(values)}")
                        if 'MIN' in operations:
                            print(f"  MIN: {min(values)}")
                    else:
                        print(f"\n字段 '{field}': 无有效数据")
            
            return wrapped_generator()
        return wrapper
    return decorator

# 3. 应用修饰器的示例
if __name__ == "__main__":
    # 定义样本结构
    sample_structure = {
        "id": "int",
        "name": "str",
        "age": "int",
        "salary": "float",
        "bonus": "float",
        "department": ["HR", "Engineering", "Marketing", "Finance"],
        "is_manager": "bool"
    }
    
    # 创建带统计功能的生成器
    @stats_operations('SUM', 'AVG', 'MAX', 'MIN', fields=['age', 'salary', 'bonus'])
    def stat_sample_generator(count, structure):
        return random_sample_generator(count, structure)
    
    # 生成并打印10个样本
    print("生成10个带统计的随机样本:")
    generator = stat_sample_generator(10, sample_structure)
    
    # 遍历生成器会触发统计计算
    for i, sample in enumerate(generator, 1):
        print(f"\n样本 {i}:")
        for key, value in sample.items():
            print(f"  {key}: {value}")