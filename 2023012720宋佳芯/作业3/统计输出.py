import random
import string
from functools import wraps
from typing import Callable, Dict, List, Union, Any


def stats_decorator(*operations: str):

    valid_ops = {'SUM', 'AVG', 'MAX', 'MIN'}

    # 验证操作是否有效
    for op in operations:
        if op not in valid_ops:
            raise ValueError(f"无效的统计操作: {op}. 有效操作: {valid_ops}")

    def decorator(func: Callable):

        @wraps(func)
        def wrapper(*args, **kwargs):
            # 调用原始函数获取结果
            results = func(*args, **kwargs)

            # 如果结果不是数字列表，尝试提取数值字段
            if not all(isinstance(x, (int, float)) for x in results):
                # 假设结果是字典列表，尝试提取第一个数值字段
                if results and isinstance(results[0], dict):
                    numeric_fields = [
                        k for k, v in results[0].items()
                        if isinstance(v, (int, float))
                    ]
                    if numeric_fields:
                        field = numeric_fields[0]
                        values = [item[field] for item in results]
                    else:
                        raise ValueError("结果中没有找到数值字段进行统计")
                else:
                    raise ValueError("不支持的结果类型进行统计")
            else:
                values = results

            # 执行统计操作
            stats = {}
            if 'SUM' in operations:
                stats['SUM'] = sum(values)
            if 'AVG' in operations:
                stats['AVG'] = sum(values) / len(values)
            if 'MAX' in operations:
                stats['MAX'] = max(values)
            if 'MIN' in operations:
                stats['MIN'] = min(values)

            # 返回原始结果和统计信息
            return {
                'data': results,
                'stats': stats
            }

        return wrapper

    return decorator


# 示例随机样本生成函数
@stats_decorator('SUM', 'AVG', 'MAX', 'MIN')
def generate_random_samples(
        sample_count: int,
        structure: Dict[str, Union[str, List[str]]]
) -> List[Dict[str, Any]]:
    
    samples = []
    for _ in range(sample_count):
        sample = {}
        for field, field_type in structure.items():
            if isinstance(field_type, list):
                sample[field] = random.choice(field_type)
            else:
                if field_type == 'int':
                    sample[field] = random.randint(0, 100)
                elif field_type == 'float':
                    sample[field] = round(random.uniform(0, 100), 2)
                elif field_type == 'str':
                    length = random.randint(5, 15)
                    sample[field] = ''.join(random.choices(string.ascii_letters, k=length))
                elif field_type == 'bool':
                    sample[field] = random.choice([True, False])
                else:
                    raise ValueError(f"不支持的字段类型: {field_type}")
        samples.append(sample)
    return samples


# 使用示例
if __name__ == "__main__":
    # 定义样本结构
    user_structure = {
        "id": "int",
        "username": "str",
        "score": "float",  # 我们将对这个字段进行统计
        "is_active": "bool",
        "level": ["bronze", "silver", "gold"]
    }

    print("生成10个用户样本并计算统计信息:")
    result = generate_random_samples(10, user_structure)

    # 打印样本数据
    print("\n样本数据:")
    for i, user in enumerate(result['data'], 1):
        print(f"用户{i}: {user}")

    # 打印统计信息
    print("\n统计信息:")
    for stat, value in result['stats'].items():
        print(f"{stat}: {value:.2f}" if isinstance(value, float) else f"{stat}: {value}")


    # 另一个示例，只计算部分统计量
    @stats_decorator('AVG', 'MAX')
    def generate_scores(count: int) -> List[float]:
        return [round(random.uniform(60, 100), 1) for _ in range(count)]


    print("\n生成5个分数并计算平均和最高分:")
    scores_result = generate_scores(5)
    print(f"分数: {scores_result['data']}")
    print(f"平均分: {scores_result['stats']['AVG']:.1f}")
    print(f"最高分: {scores_result['stats']['MAX']:.1f}")