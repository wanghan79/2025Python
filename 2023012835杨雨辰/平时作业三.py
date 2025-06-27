import random
import string
from typing import Dict, List, Any, Optional, Generator, Callable, Union


def generate_random_sample(structure: Dict[str, str]) -> Dict[str, Any]:
    """根据指定结构生成单个随机样本"""
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
            sample[field] = None
    return sample


def stats_analysis(operations: List[str], fields: List[str]):
    """
    带参装饰器，用于对生成的随机样本进行统计分析

    Args:
        operations: 统计操作列表，支持 SUM、AVG、MAX、MIN
        fields: 需要统计的字段列表
    """

    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            # 获取生成器
            gen = func(*args, **kwargs)

            # 初始化统计数据结构
            stats = {field: {'SUM': 0, 'COUNT': 0, 'MAX': float('-inf'), 'MIN': float('inf')}
                     for field in fields}

            # 遍历生成器，收集统计数据
            samples = []
            for item in gen:
                if isinstance(item, list):  # 批量模式
                    samples.extend(item)
                else:  # 单个模式
                    samples.append(item)

            # 计算统计信息
            for sample in samples:
                for field in fields:
                    if field in sample and isinstance(sample[field], (int, float)):
                        value = sample[field]
                        stats[field]['SUM'] += value
                        stats[field]['COUNT'] += 1
                        if value > stats[field]['MAX']:
                            stats[field]['MAX'] = value
                        if value < stats[field]['MIN']:
                            stats[field]['MIN'] = value

            # 计算平均值
            for field in fields:
                if stats[field]['COUNT'] > 0:
                    stats[field]['AVG'] = round(stats[field]['SUM'] / stats[field]['COUNT'], 2)

            # 输出指定的统计结果
            result = {}
            for field in fields:
                field_stats = {}
                for op in operations:
                    if op in ['SUM', 'AVG', 'MAX', 'MIN'] and stats[field]['COUNT'] > 0:
                        field_stats[op] = stats[field][op]
                if field_stats:
                    result[field] = field_stats

            # 返回原始生成器和统计结果
            return samples, result

        return wrapper

    return decorator


@stats_analysis(operations=['SUM', 'AVG', 'MAX', 'MIN'], fields=['age', 'height'])
def random_sample_generator(
        structure: Dict[str, str],
        count: int,
        batch_size: Optional[int] = None
) -> Generator[Union[Dict[str, Any], List[Dict[str, Any]]], None, None]:
    """生成指定数量和结构的随机样本生成器"""
    if batch_size is None:
        for _ in range(count):
            yield generate_random_sample(structure)
    else:
        batches = (count + batch_size - 1) // batch_size
        for _ in range(batches):
            current_batch = []
            for _ in range(batch_size):
                if len(current_batch) < count:
                    current_batch.append(generate_random_sample(structure))
            yield current_batch


# 使用范例
if __name__ == "__main__":
    sample_structure = {
        'id': 'int',
        'name': 'str',
        'age': 'int',
        'height': 'float',
        'is_student': 'boolean'
    }

    # 生成10个样本，每批5个
    samples, statistics = random_sample_generator(sample_structure, count=10, batch_size=5)

    print("生成的样本:")
    for i, sample in enumerate(samples):
        print(f"样本 {i + 1}: {sample}")

    print("\n统计结果:")
    for field, stats in statistics.items():
        print(f"{field}: {stats}")