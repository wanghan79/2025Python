import random
import string
from typing import Dict, List, Any, Optional, Generator


def generate_random_sample(structure: Dict[str, str]) -> Dict[str, Any]:
    """根据指定结构生成单个随机样本

    Args:
        structure: 样本结构字典，键为字段名，值为字段类型（int/float/str/boolean）

    Returns:
        符合指定结构的随机样本字典
    """
    sample = {}
    for field, field_type in structure.items():
        if field_type == 'int':
            sample[field] = random.randint(1, 100)
        elif field_type == 'float':
            sample[field] = round(random.uniform(1.0, 100.0), 2)
        elif field_type == 'str':
            length = random.randint(5, 15)
            sample[field] = ''.join(random.choices(string.ascii_letters, k=length))
        elif field_type == 'boolean':
            sample[field] = random.choice([True, False])
        else:
            sample[field] = None  # 未知类型默认为None
    return sample


def random_sample_generator(
        structure: Dict[str, str],
        count: int,
        batch_size: Optional[int] = None
) -> Generator[Dict[str, Any], None, None]:
    """生成指定数量和结构的随机样本生成器

    Args:
        structure: 样本结构字典，键为字段名，值为字段类型（int/float/str/boolean）
        count: 需要生成的样本总数
        batch_size: 每批生成的样本数量，默认为None（单个生成）

    Yields:
        随机样本字典（单个或批量列表）
    """
    if batch_size is None:
        # 单个生成模式
        for _ in range(count):
            yield generate_random_sample(structure)
    else:
        # 批量生成模式
        batches = (count + batch_size - 1) // batch_size  # 向上取整计算批次数
        for _ in range(batches):
            current_batch = []
            for _ in range(batch_size):
                if len(current_batch) < count:  # 确保不超过总数
                    current_batch.append(generate_random_sample(structure))
            yield current_batch


# 使用范例
if __name__ == "__main__":
    # 定义样本结构
    sample_structure = {
        'id': 'int',
        'name': 'str',
        'age': 'int',
        'height': 'float',
        'is_student': 'boolean'
    }

    print("=== 单个生成模式 ===")
    # 创建生成器，生成5个样本
    single_generator = random_sample_generator(sample_structure, count=5)
    # 逐个获取样本
    for sample in single_generator:
        print(sample)

    print("\n=== 批量生成模式 ===")
    # 创建生成器，每批生成2个样本，总共生成7个样本
    batch_generator = random_sample_generator(sample_structure, count=7, batch_size=2)
    # 逐批获取样本
    for i, batch in enumerate(batch_generator):
        print(f"Batch {i + 1}:")
        for sample in batch:
            print(f"  {sample}")