import random
import string
from typing import List, Dict, Union, Callable, Optional
from functools import wraps


def stats_decorator(*stats_ops: str):
    """
    带参数的修饰器，用于对随机样本生成函数进行统计操作

    Args:
        stats_ops (str): 统计操作类型，支持 "SUM", "AVG", "MAX", "MIN"

    Returns:
        Callable: 修饰后的函数

    Example:
        @stats_decorator("SUM", "AVG", "MAX")
        def generate_samples(...):
            ...
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            samples = func(*args, **kwargs)

            if not samples:
                print("No samples generated.")
                return samples

            # 提取数值型字段
            numeric_fields = [
                field for field in samples[0].keys()
                if isinstance(samples[0][field], (int, float))
            ]

            print("\n=== Statistics ===")
            for field in numeric_fields:
                values = [sample[field] for sample in samples]
                print(f"\nField: {field}")

                if "SUM" in stats_ops:
                    print(f"SUM: {sum(values)}")
                if "AVG" in stats_ops:
                    print(f"AVG: {sum(values) / len(values):.2f}")
                if "MAX" in stats_ops:
                    print(f"MAX: {max(values)}")
                if "MIN" in stats_ops:
                    print(f"MIN: {min(values)}")

            return samples

        return wrapper

    return decorator


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


def print_samples(samples: List[Dict], max_rows: int = 5) -> None:
    """打印样本数据（限制最大行数）"""
    print("\nGenerated Samples:")
    for i, sample in enumerate(samples[:max_rows]):
        print(f"Sample {i + 1}: {sample}")
    if len(samples) > max_rows:
        print(f"... and {len(samples) - max_rows} more samples")


@stats_decorator("SUM", "AVG", "MAX", "MIN")
def generate_user_data(sample_count: int) -> List[Dict]:
    """生成用户数据（带统计修饰器）"""
    structure = {
        "user_id": "int",
        "age": ("int", 18, 65),
        "score": lambda: round(random.uniform(0, 100), 2),
        "is_active": "bool",
    }
    return random_sample_generator(sample_count, structure, seed=42)


@stats_decorator("AVG", "MAX")
def generate_product_data(sample_count: int) -> List[Dict]:
    """生成商品数据（带统计修饰器）"""
    structure = {
        "product_id": "int",
        "price": ("float", 50, 2000),
        "in_stock": "bool",
    }
    return random_sample_generator(sample_count, structure)


def main():
    # 示例1：生成用户数据（带完整统计）
    print("\n=== Generating User Data (Full Stats) ===")
    users = generate_user_data(10)
    print_samples(users)

    # 示例2：生成商品数据（仅 AVG 和 MAX）
    print("\n=== Generating Product Data (AVG & MAX) ===")
    products = generate_product_data(8)
    print_samples(products)


if __name__ == "__main__":
    main()