import random
import string
from typing import List, Dict, Union, Optional, Callable


def random_sample_generator(
        sample_count: int,
        structure: Dict[str, Union[str, List, Dict, Callable]],
        seed: Optional[int] = None
) -> List[Dict]:
    """
    生成随机样本数据

    Args:
        sample_count (int): 生成的样本数量
        structure (Dict): 定义样本结构的字典，键是字段名，值是数据类型或生成函数
        seed (int, optional): 随机种子，用于可复现性

    Returns:
        List[Dict]: 生成的样本列表，每个样本是一个字典

    Example:
        structure = {
            "id": "int",
            "name": "str",
            "age": ("int", 18, 65),
            "is_active": "bool",
            "score": lambda: round(random.uniform(0, 100), 2)
        }
        samples = random_sample_generator(5, structure)
    """
    if seed is not None:
        random.seed(seed)

    samples = []
    for _ in range(sample_count):
        sample = {}
        for field, field_type in structure.items():
            if isinstance(field_type, str):
                if field_type == "int":
                    sample[field] = random.randint(0, 1000)
                elif field_type == "float":
                    sample[field] = round(random.uniform(0, 100), 2)
                elif field_type == "str":
                    sample[field] = ''.join(random.choices(string.ascii_letters, k=10))
                elif field_type == "bool":
                    sample[field] = random.choice([True, False])
                else:
                    raise ValueError(f"Unsupported type: {field_type}")
            elif isinstance(field_type, (tuple, list)):
                if field_type[0] == "int":
                    sample[field] = random.randint(field_type[1], field_type[2])
                elif field_type[0] == "float":
                    sample[field] = round(random.uniform(field_type[1], field_type[2]), 2)
                elif field_type[0] == "choice":
                    sample[field] = random.choice(field_type[1])
                else:
                    raise ValueError(f"Unsupported type in tuple: {field_type[0]}")
            elif callable(field_type):
                sample[field] = field_type()
            else:
                raise ValueError(f"Invalid field type: {field_type}")
        samples.append(sample)

    return samples


def print_samples(samples: List[Dict], max_rows: int = 10) -> None:
    """打印样本数据（限制最大行数）"""
    print("\nGenerated Samples:")
    for i, sample in enumerate(samples[:max_rows]):
        print(f"Sample {i + 1}: {sample}")
    if len(samples) > max_rows:
        print(f"... and {len(samples) - max_rows} more samples")


def main():
    # 示例1：生成用户数据
    user_structure = {
        "user_id": "int",
        "username": "str",
        "age": ("int", 18, 65),
        "email": lambda: f"{''.join(random.choices(string.ascii_lowercase, k=8))}@example.com",
        "is_premium": "bool",
        "credit_score": ("float", 300, 850),
    }
    users = random_sample_generator(15, user_structure, seed=42)
    print_samples(users)

    # 示例2：生成商品数据
    product_structure = {
        "product_id": "int",
        "name": ("choice", ["Laptop", "Phone", "Tablet", "Headphones"]),
        "price": ("float", 50, 2000),
        "in_stock": "bool",
        "tags": lambda: random.sample(["electronics", "gadget", "new", "sale"], k=2),
    }
    products = random_sample_generator(8, product_structure)
    print_samples(products)


if __name__ == "__main__":
    main()