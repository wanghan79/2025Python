import random
import string
from typing import Dict, List, Union, Generator

def random_sample_generator(
    sample_count: int,
    structure: Dict[str, Union[str, List[str], Dict[str, str]]]
) -> Generator[Dict[str, Union[str, int, float, bool]], None, None]:
    """
    随机样本生成器
    
    参数:
        sample_count: 要生成的样本数量
        structure: 定义样本结构的字典，键为字段名，值为字段类型或选项
        
    返回:
        生成器，每次迭代返回一个随机样本字典
    
    结构定义示例:
        {
            "name": "str",  # 随机字符串
            "age": "int",  # 随机整数(18-80)
            "score": "float",  # 随机浮点数(0-100)
            "is_active": "bool",  # 随机布尔值
            "gender": ["male", "female", "other"],  # 从列表中随机选择
            "address": {  # 嵌套字典
                "city": ["Beijing", "Shanghai", "Guangzhou"],
                "zipcode": "str"  # 随机6位数字字符串
            }
        }
    """
    def generate_value(field_type: Union[str, List[str], Dict[str, str]]) -> Union[str, int, float, bool, Dict[str, Union[str, int, float, bool]]]:
        if isinstance(field_type, dict):
            # 处理嵌套字典
            return {k: generate_value(v) for k, v in field_type.items()}
        elif isinstance(field_type, list):
            # 从列表中随机选择
            return random.choice(field_type)
        elif field_type == "str":
            # 生成随机字符串
            length = random.randint(5, 15)
            return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        elif field_type == "int":
            # 生成随机整数
            return random.randint(0, 100)
        elif field_type == "float":
            # 生成随机浮点数
            return round(random.uniform(0, 100), 2)
        elif field_type == "bool":
            # 生成随机布尔值
            return random.choice([True, False])
        else:
            raise ValueError(f"不支持的字段类型: {field_type}")

    for _ in range(sample_count):
        yield {field: generate_value(field_type) for field, field_type in structure.items()}


# 示例用法
if __name__ == "__main__":
    # 定义样本结构
    sample_structure = {
        "id": "int",
        "name": "str",
        "age": "int",
        "salary": "float",
        "department": ["HR", "Engineering", "Marketing", "Finance"],
        "is_manager": "bool",
        "address": {
            "city": ["New York", "London", "Tokyo", "Beijing"],
            "street": "str",
            "zipcode": "str"
        },
        "skills": ["Python", "Java", "C++", "JavaScript", "SQL"]
    }
    
    # 生成10个随机样本
    print("生成10个随机样本:")
    generator = random_sample_generator(10, sample_structure)
    
    # 打印生成的样本
    for i, sample in enumerate(generator, 1):
        print(f"\n样本 {i}:")
        for key, value in sample.items():
            if isinstance(value, dict):
                print(f"  {key}:")
                for sub_key, sub_value in value.items():
                    print(f"    {sub_key}: {sub_value}")
            else:
                print(f"  {key}: {value}")