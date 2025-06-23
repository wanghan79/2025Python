import random
from functools import wraps
from typing import Dict, List, Tuple, Generator, Callable, Any

# 带参数的装饰器工厂
def stats_operations(*operations: str) -> Callable:
    valid_ops = {'SUM', 'AVG', 'MAX', 'MIN'}
    for op in operations:
        if op not in valid_ops:
            raise ValueError(f"无效的统计操作: {op}. 有效的操作包括: {valid_ops}")
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Generator:
            generator = func(*args, **kwargs)

            stats = {
                'fields': {},
                'count': 0
            }

            for sample in generator:
                stats['count'] += 1

                for field, value in sample.items():

                    if not isinstance(value, (int, float)):
                        continue
                    
                    if field not in stats['fields']:
                        stats['fields'][field] = {
                            'values': [],
                            'sum': 0,
                            'max': float('-inf'),
                            'min': float('inf')
                        }

                    field_stats = stats['fields'][field]
                    field_stats['values'].append(value)
                    field_stats['sum'] += value
                    if value > field_stats['max']:
                        field_stats['max'] = value
                    if value < field_stats['min']:
                        field_stats['min'] = value
                yield sample
            
            print("\n===== 统计结果 =====")
            print(f"总样本数: {stats['count']}")
            
            if not stats['fields']:
                print("没有数值字段可供统计")
                return

            for field, field_stats in stats['fields'].items():
                print(f"\n字段: {field}")
                
                if 'SUM' in operations:
                    print(f"  SUM: {field_stats['sum']}")
                
                if 'AVG' in operations:
                    avg = field_stats['sum'] / stats['count'] if stats['count'] > 0 else 0
                    print(f"  AVG: {avg:.2f}")
                
                if 'MAX' in operations:
                    print(f"  MAX: {field_stats['max']}")
                
                if 'MIN' in operations:
                    print(f"  MIN: {field_stats['min']}")
        
        return wrapper
    return decorator

# 随机样本生成函数（带统计装饰器）
@stats_operations('SUM', 'AVG', 'MAX', 'MIN')  # 可以修改这里的统计操作组合
def random_sample_generator(
    num_samples: int = 100,
    sample_structure: Dict[str, Tuple] = None
) -> Generator[Dict[str, Any], None, None]:

  
    if sample_structure is None:
        sample_structure = {
            "id": ("int", 1, 1000),
            "name": ("choice", ["Alice", "Bob", "Charlie", "David", "Eve"]),
            "age": ("int", 18, 65),
            "income": ("float", 20000.0, 150000.0),
            "score": ("float", 0.0, 10.0),
            "is_active": ("bool",),
            "interests": ("list", 3, ["sports", "music", "reading", "travel", "cooking"])
        }
    
    for i in range(num_samples):
        sample = {}
        for field, spec in sample_structure.items():
            data_type = spec[0]
            
            if data_type == "int":
                sample[field] = random.randint(spec[1], spec[2])
            
            elif data_type == "float":
                sample[field] = random.uniform(spec[1], spec[2])
            
            elif data_type == "bool":
                sample[field] = random.choice([True, False])
            
            elif data_type == "choice":
                sample[field] = random.choice(spec[1])
            
            elif data_type == "list":
                length = spec[1]
                options = spec[2]
                sample[field] = random.choices(options, k=length)
            
            elif data_type == "norm":
                sample[field] = random.gauss(spec[1], spec[2])
            
            else:
                raise ValueError(f"不支持的数据类型: {data_type}")
        
        yield sample

# 使用示例
if __name__ == "__main__":
    sample_gen = random_sample_generator(
        num_samples=10,
        sample_structure={
            "user_id": ("int", 1000, 9999),
            "username": ("choice", ["john_doe", "jane_smith", "admin", "guest"]),
            "age": ("int", 18, 65),
            "income": ("float", 20000.0, 150000.0),
            "score": ("float", 0.0, 10.0),
            "premium": ("bool",),
            "tags": ("list", 2, ["tech", "science", "art", "business"])
        }
    )
    
    # 使用生成器并自动进行统计
    print("生成的随机样本:")
    for i, sample in enumerate(sample_gen):
        print(f"\n样本 {i+1}:")
        for key, value in sample.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.2f}") 
            else:
                print(f"  {key}: {value}")
