import random
import string
from typing import Any, Dict, Generator, List, Tuple, Union, Callable, TypeVar
from functools import wraps

T = TypeVar('T')

# 定义类型别名
DataType = Union[str, int, float, List[Any], Dict[Any, Any], Tuple[Any, ...]]
StructureConfig = Dict[str, Union[int, Dict[str, Any]]]


def gen_str(data: Dict[str, Any]) -> str:
    """生成随机字符串"""
    return ''.join(random.choices(data['datarange'], k=data['len']))


def gen_int(data: Dict[str, Any]) -> int:
    """生成随机整数"""
    return random.randint(data['datarange'][0], data['datarange'][1])


def gen_float(data: Dict[str, Any]) -> float:
    """生成随机浮点数"""
    return random.uniform(data['datarange'][0], data['datarange'][1])


def gen_list(data: Dict[str, Any]) -> List[Any]:
    """生成随机列表"""
    return [generate_sample({k: v}) for k, v in data.items()]


def gen_dict(data: Dict[str, Any]) -> Dict[Any, Any]:
    """生成随机字典"""
    return {k: generate_sample({k: v}) for k, v in data.items()}


def gen_tuple(data: Dict[str, Any]) -> Tuple[Any, ...]:
    """生成随机元组"""
    return tuple(generate_sample({k: v}) for k, v in data.items())


# 类型到生成函数的映射
TYPE_TO_FUNC = {
    'str': gen_str,
    'int': gen_int,
    'float': gen_float,
    'list': gen_list,
    'dict': gen_dict,
    'tuple': gen_tuple,
}


def generate_sample(struct: StructureConfig) -> DataType:
    """根据结构配置生成单个随机样本"""
    if len(struct) != 1:
        raise ValueError("结构配置必须包含且仅包含一个类型键")
    type_name, data = next(iter(struct.items()))
    if type_name not in TYPE_TO_FUNC:
        raise ValueError(f"不支持的类型：'{type_name}'")
    return TYPE_TO_FUNC[type_name](data)


def random_sampler(struct: StructureConfig, num_samples: int) -> Generator[DataType, None, None]:
    """随机样本生成器"""
    for _ in range(num_samples):
        yield generate_sample(struct)


def extract_numeric_values(samples: List[DataType]) -> List[Union[int, float]]:
    """递归提取嵌套结构中的所有数值"""

    def flatten(obj: Any) -> List[Union[int, float]]:
        if isinstance(obj, (int, float)):
            return [obj]
        elif isinstance(obj, list):
            return [n for item in obj for n in flatten(item)]
        elif isinstance(obj, dict):
            return [n for value in obj.values() for n in flatten(value)]
        elif isinstance(obj, tuple):
            return [n for item in obj for n in flatten(item)]
        return []

    return [n for sample in samples for n in flatten(sample)]


def statistics_decorator(*operations: str) -> Callable:
    """
    统计操作装饰器，支持SUM、AVG、MAX、MIN四种统计操作的任意组合

    Args:
        operations: 统计操作名称，如"SUM", "AVG", "MAX", "MIN"
    """
    # 定义统计函数映射
    STATISTICS = {
        'SUM': lambda data: sum(data),
        'AVG': lambda data: sum(data) / len(data) if data else 0,
        'MAX': lambda data: max(data) if data else None,
        'MIN': lambda data: min(data) if data else None,
    }

    # 验证操作参数
    for op in operations:
        if op not in STATISTICS:
            raise ValueError(f"不支持的统计操作: {op}。支持的操作: {', '.join(STATISTICS.keys())}")

    def decorator(func: Callable[..., Generator]) -> Callable[..., Dict[str, Any]]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Dict[str, Any]:
            # 生成所有样本
            samples = list(func(*args, **kwargs))

            # 提取所有数值
            numeric_values = extract_numeric_values(samples)

            if not numeric_values:
                print("警告: 没有找到可统计的数值")
                return {
                    'samples': samples,
                    'statistics': {}
                }

            # 计算统计结果
            results = {}
            for op in operations:
                try:
                    results[op] = STATISTICS[op](numeric_values)
                except Exception as e:
                    results[op] = f"Error: {str(e)}"

            # 打印统计结果
            print("\n==== 统计结果 ====")
            for op, value in results.items():
                print(f"{op}: {value}")

            return {
                'samples': samples,
                'statistics': results
            }

        return wrapper

    return decorator


# 示例用法
@statistics_decorator('SUM', 'AVG', 'MAX', 'MIN')
def sample_generator(struct: StructureConfig, num_samples: int) -> Generator[DataType, None, None]:
    """装饰后的样本生成器"""
    return random_sampler(struct, num_samples)


if __name__ == '__main__':
    # 示例1：生成整数
    int_config = {
        'int': {
            'datarange': [1, 100]
        }
    }

    print("=== 整数样本统计 ===")
    result = sample_generator(int_config, 10)
    print(f"生成了 {len(result['samples'])} 个样本")

    # 示例2：生成嵌套结构
    nested_config = {
        'list': {
            'int': {'datarange': [1, 10]},
            'dict': {
                'float': {'datarange': [0.1, 1.0]}
            }
        }
    }

    print("\n=== 嵌套结构样本统计 ===")
    result = sample_generator(nested_config, 5)
    print("样本示例:")
    for s in result['samples'][:2]:
        print(s)
