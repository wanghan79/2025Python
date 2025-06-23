import random
from typing import Generator, Union, List, Dict, Any

def random_sample_generator(
    num_samples: int = 100,
    sample_structure: Union[Dict[str, Any], List[Dict[str, Any]]] = None
) -> Generator[Dict[str, Any], None, None]:
  
    if sample_structure is None:
        sample_structure = {
            "id": ("int", 1, 1000),
            "name": ("choice", ["Alice", "Bob", "Charlie", "David", "Eve"]),
            "age": ("int", 18, 65),
            "income": ("float", 20000.0, 150000.0),
            "is_active": ("bool",),
            "interests": ("list", 3, ["sports", "music", "reading", "travel", "cooking"])
        }
    
    if isinstance(sample_structure, dict):
        sample_structure = [sample_structure] * num_samples
    
    if len(sample_structure) < num_samples:
        sample_structure = sample_structure * (num_samples // len(sample_structure) + 1
    sample_structure ) = sample_structure[:num_samples]
    
    # 生成样本
    for i, structure in enumerate(sample_structure):
        sample = {}
        for field, spec in structure.items():
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
    custom_structure = [
        {
            "user_id": ("int", 1000, 9999),
            "username": ("choice", ["john_doe", "jane_smith", "admin", "guest"]),
            "score": ("float", 0.0, 10.0),
            "premium": ("bool",),
            "tags": ("list", 2, ["tech", "science", "art", "business"])
        },
        {
            "product_id": ("int", 1, 100),
            "product_name": ("choice", ["Laptop", "Phone", "Tablet", "Monitor"]),
            "price": ("float", 99.99, 1999.99),
            "in_stock": ("bool",),
            "rating": ("norm", 4.5, 0.5)
        }
    ]
    
    # 创建生成器
    sample_gen = random_sample_generator(
        num_samples=5,
        sample_structure=custom_structure
    )
    
    # 使用生成器
    print("生成的随机样本:")
    for i, sample in enumerate(sample_gen):
        print(f"\n样本 {i+1}:")
        for key, value in sample.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.2f}")  # 格式化浮点数
            else:
                print(f"  {key}: {value}")
