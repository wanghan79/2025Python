import random
from typing import Any, Dict, Generator, List, Tuple, Union, Callable, Optional
from collections import defaultdict

DataType = Dict[str, Any]
SampleGenerator = Callable[[DataType], Any]


def gen_str(data: DataType) -> str:
    """
    从指定字符串中随机生成指定长度的字符串
    """
    return ''.join(random.choices(data['datarange'], k=data['len']))


def gen_int(data: DataType) -> int:
    """
    从随机数范围中生成随机int数
    """
    return random.randint(data['datarange'][0], data['datarange'][1])


def gen_float(data: DataType) -> float:
    """
    从随机数范围中生成随机浮点数
    """
    return random.uniform(data['datarange'][0], data['datarange'][1])


def gen_list(data: DataType) -> list:
    """
    生成列表
    """
    return [generate_sample({k: v}) for k, v in data.items()]


def gen_dict(data: DataType) -> dict:
    """
    生成字典
    """
    return {k: generate_sample({k: v}) for k, v in data.items()}


def gen_tuple(data: DataType) -> tuple:
    """
    生成元组
    """
    return tuple(generate_sample({k: v}) for k, v in data.items())


TYPE_TO_FUNC: Dict[str, SampleGenerator] = {
    'str': gen_str,
    'int': gen_int,
    'float': gen_float,
    'list': gen_list,
    'dict': gen_dict,
    'tuple': gen_tuple,
}


def extract_numbers(data: Any) -> List[Union[int, float]]:
    """
    提取出生成数据中的数值型数据
    """
    numbers = []

    if isinstance(data, (list, tuple, set)):
        for item in data:
            numbers.extend(extract_numbers(item))
    elif isinstance(data, dict):
        for value in data.values():
            numbers.extend(extract_numbers(value))
    elif isinstance(data, (int, float)):
        numbers.append(data)

    return numbers


def calculate_stats(numbers: List[Union[int, float]], methods: List[str]) -> List[Tuple[str, float]]:
    """
    计算统计数据
    """
    if not numbers:
        return []

    stats = []
    n = len(numbers)
    sum_val = sum(numbers)
    avg_val = sum_val / n

    for method in methods:
        method = method.upper()
        if method == 'SUM':
            stats.append(('SUM', sum_val))
        elif method == 'AVG':
            stats.append(('AVG', avg_val))
        elif method == 'VAR':
            variance = sum((x - avg_val) ** 2 for x in numbers) / n
            stats.append(('VAR', variance))
        elif method == 'RMSE':
            variance = sum((x - avg_val) ** 2 for x in numbers) / n
            stats.append(('RMSE', variance ** 0.5))
        else:
            raise ValueError(f"Unsupported statistics method: {method}")

    return stats


def StaticsResInt(**kwargs) -> Callable:
    """
    装饰器函数，用于统计数值型数据
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **inner_kwargs) -> Optional[List[Tuple[str, float]]]:
            method_list = kwargs.get('name', [])
            if not method_list:
                return None

            # 生成随机样本
            results = list(func(*args, **inner_kwargs))
            if not results:
                return None

            # 提取数值型数据
            numbers = []
            for item in results:
                numbers.extend(extract_numbers(item))

            if not numbers:
                return None

            return calculate_stats(numbers, method_list)

        return wrapper

    return decorator


def generate_sample(struct: Dict[str, Any]) -> Any:
    """
    生成指定结构配置的随机样本
    """
    if len(struct) != 1:
        raise ValueError(f"结构配置必须包含且仅包含一个类型键：{struct}")

    type_name, data = next(iter(struct.items()))
    if type_name not in TYPE_TO_FUNC:
        raise ValueError(f"不支持的类型：'{type_name}'")

    return TYPE_TO_FUNC[type_name](data)


@StaticsResInt(name=['SUM', 'AVG', 'VAR', 'RMSE'])
def random_sampler(**kwargs) -> Generator[Any, None, None]:
    """
    随机数生成器
    """
    number = kwargs.pop('number', 1)
    for _ in range(number):
        yield generate_sample(kwargs)


if __name__ == '__main__':
    example = {
        'number': 10,
        'tuple': {
            'str': {
                'datarange': 'abcdefghijklmnopqrstuvwxyz',
                'len': 8
            },
            'list': {
                'int': {
                    'datarange': [1, 10]
                },
                'float': {
                    'datarange': [1, 10]
                }
            },
            'dict': {
                'int': {
                    'datarange': [1, 10]
                }
            }
        }
    }

    result = random_sampler(**example)
    if result:
        for static_method, data in result:
            print(f"The {static_method} of the numbers: {data:.4f}")