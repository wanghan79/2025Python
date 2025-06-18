import random
import string
import datetime
from typing import Any, Dict, Generator, List, Union, Optional

def generate_int(min_val: int = 0, max_val: int = 100) -> int:
    """生成指定范围内的随机整数"""
    return random.randint(min_val, max_val)

def generate_float(min_val: float = 0.0, max_val: float = 1.0, precision: int = 2) -> float:
    """生成指定范围内的随机浮点数"""
    return round(random.uniform(min_val, max_val), precision)

def generate_string(length: int = 10, charset: str = string.ascii_letters + string.digits) -> str:
    """生成指定长度的随机字符串"""
    return ''.join(random.choices(charset, k=length))

def generate_boolean() -> bool:
    """生成随机布尔值"""
    return random.choice([True, False])

def generate_date(start_year: int = 2000, end_year: int = 2025) -> str:
    """生成指定年份范围内的随机日期"""
    start_date = datetime.date(start_year, 1, 1)
    end_date = datetime.date(end_year, 12, 31)
    days_diff = (end_date - start_date).days
    random_days = random.randint(0, days_diff)
    return (start_date + datetime.timedelta(days=random_days)).isoformat()

def generate_list(element_type: str, length: int = 5, **kwargs) -> List[Any]:
    """生成指定类型的随机列表"""
    # 基础数据类型的生成器
    generators = {
        'int': lambda: generate_int(**kwargs),
        'float': lambda: generate_float(**kwargs),
        'str': lambda: generate_string(**kwargs),
        'bool': lambda: generate_boolean(),
        'date': lambda: generate_date(**kwargs),
    }
    
    # 处理基础数据类型
    if element_type in generators:
        return [generators[element_type]() for _ in range(length)]
    
    # 处理复合数据类型
    elif element_type == 'dict':
        # 确保提供了字典结构定义
        if 'structure' not in kwargs:
            raise ValueError("生成字典类型的列表元素时需要提供 'structure' 参数")
        
        # 从kwargs中提取结构定义并生成字典列表
        dict_structure = kwargs['structure']
        return [generate_dict(dict_structure) for _ in range(length)]
    
    else:
        raise ValueError(f"不支持的元素类型: {element_type}")

def generate_dict(structure: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """根据结构定义生成随机字典"""
    result = {}
    
    for key, config in structure.items():
        # 创建配置的副本，避免修改原始配置
        config_copy = config.copy()
        data_type = config_copy.pop('type')
        
        # 使用函数工厂模式避免闭包问题
        def create_generator(func, config):
            def generator():
                return func(**config)
            return generator
        
        # 为列表和字典类型创建生成器
        if data_type == 'list':
            generators = {
                'list': create_generator(generate_list, config_copy)
            }
        elif data_type == 'dict':
            generators = {
                'dict': create_generator(generate_dict, config_copy)
            }
        else:
            generators = {}
        
        # 添加基础类型生成器
        generators.update({
            'int': lambda: generate_int(**config_copy),
            'float': lambda: generate_float(**config_copy),
            'str': lambda: generate_string(**config_copy),
            'bool': lambda: generate_boolean(),
            'date': lambda: generate_date(**config_copy),
        })
        
        if data_type not in generators:
            raise ValueError(f"不支持的数据类型: {data_type}")
        
        result[key] = generators[data_type]()
    
    return result

def random_sample_generator(
    n_samples: int,
    structure: Dict[str, Dict[str, Any]]
) -> Generator[Dict[str, Any], None, None]:
    """
    生成随机样本的主生成器
    
    参数:
        n_samples: 生成的样本数量
        structure: 样本结构定义，格式为:
            {
                "字段名1": {"type": "int", "min_val": 0, "max_val": 100},
                "字段名2": {"type": "float", "min_val": 0.0, "max_val": 1.0},
                "字段名3": {"type": "str", "length": 5},
                "字段名4": {"type": "list", "element_type": "int", "length": 3},
                "字段名5": {"type": "dict", "structure": {"子字段": {"type": "bool"}}},
            }
    
    返回:
        生成器对象，逐个生成符合结构的随机样本
    """
    for _ in range(n_samples):
        yield generate_dict(structure)

# 使用范例
if __name__ == "__main__":
    # 定义用户资料结构（修正参数名：min -> min_val, max -> max_val）
    user_profile_structure = {
        "id": {"type": "int", "min_val": 1, "max_val": 1000},
        "name": {"type": "str", "length": 8},
        "age": {"type": "int", "min_val": 18, "max_val": 100},
        "is_active": {"type": "bool"},
        "registration_date": {"type": "date", "start_year": 2010, "end_year": 2023},
        "scores": {"type": "list", "element_type": "float", "length": 5, "min_val": 0.0, "max_val": 100.0},
        "preferences": {"type": "dict", "structure": {
            "theme": {"type": "str", "charset": "light,dark", "length": 5},
            "notifications": {"type": "bool"},
            "language": {"type": "str", "charset": "en,zh,es,fr", "length": 2}
        }}
    }
    
    # 生成5个用户样本
    samples = random_sample_generator(5, user_profile_structure)
    
    # 打印样本
    print("=== 用户资料样本 ===")
    for i, sample in enumerate(samples, 1):
        print(f"样本 {i}:")
        for key, value in sample.items():
            print(f"  {key}: {value}")
        print()
    
    # 更复杂的嵌套结构示例（修正参数名）
    complex_structure = {
        "id": {"type": "str", "length": 6},
        "nested_list": {"type": "list", "element_type": "dict", "length": 3, "structure": {
            "key": {"type": "str", "length": 4},
            "value": {"type": "int", "min_val": 0, "max_val": 100}
        }},
        "metrics": {"type": "dict", "structure": {
            "count": {"type": "int", "min_val": 0, "max_val": 1000},
            "average": {"type": "float", "min_val": 0.0, "max_val": 100.0},
            "timestamps": {"type": "list", "element_type": "date", "length": 5, "start_year": 2020, "end_year": 2023}
        }}
    }
    
    # 生成2个电商产品样本
    print("\n=== 复杂嵌套结构示例 ===")
    complex_samples = random_sample_generator(2, complex_structure)
    
    for i, sample in enumerate(complex_samples, 1):
        print(f"复杂样本 {i}:")
        print(sample)
        print()
