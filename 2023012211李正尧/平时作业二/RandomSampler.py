import random
import datetime
import string
from typing import Any, Dict, Generator, Union


def gen_str(data: Dict[str, Any]) -> str:
    """
    从指定字符集生成随机字符串

    Args:
        data: 包含配置信息的字典，需包含：
            - datarange: 字符集范围（字符串）
            - len: 生成字符串长度（整数）

    Returns:
        随机生成的指定长度字符串
    """
    char_range = data.get('datarange', string.ascii_letters)
    length = data.get('len', 8)
    return ''.join(random.choices(char_range, k=length))

def gen_int(data: Dict[str, Any]) -> int:
    """
    生成指定范围内的随机整数

    Args:
        data: 包含配置信息的字典，需包含：
            - datarange: 范围列表 [最小值, 最大值]
            - step: 步长（可选，默认1）

    Returns:
        范围内的随机整数
    """
    range_min, range_max = data.get('datarange', [0, 100])
    step = data.get('step', 1)
    return random.randint(range_min, range_max)

def gen_float(data: Dict[str, Any]) -> float:
    """
    生成指定范围内的随机浮点数

    Args:
        data: 包含配置信息的字典，需包含：
            - datarange: 范围列表 [最小值, 最大值]
            - precision: 小数精度（可选，默认2）

    Returns:
        范围内的随机浮点数
    """
    range_min, range_max = data.get('datarange', [0.0, 100.0])
    precision = data.get('precision', 2)
    return round(random.uniform(range_min, range_max), precision)

def gen_bool(data: Dict[str, Any]) -> bool:
    """生成随机布尔值"""
    return random.choice([True, False])

def gen_date(data: Dict[str, Any]) -> str:
    """
    生成指定范围内的随机日期

    Args:
        data: 包含配置信息的字典，需包含：
            - start_year: 起始年份（默认2000）
            - end_year: 结束年份（默认当前年份）
            - format: 日期格式（默认'%Y-%m-%d'）

    Returns:
        格式化后的随机日期字符串
    """
    start_year = data.get('start_year', 2000)
    end_year = data.get('end_year', datetime.datetime.now().year)
    date_format = data.get('format', '%Y-%m-%d')

    start_date = datetime.date(start_year, 1, 1)
    days = (datetime.date(end_year, 12, 31) - start_date).days
    random_days = random.randint(0, days)
    random_date = start_date + datetime.timedelta(days=random_days)

    return random_date.strftime(date_format)

def gen_list(data: Dict[str, Any]) -> list:
    """
    生成随机列表（支持嵌套结构）

    Args:
        data: 包含配置信息的字典，需包含：
            - element: 元素生成配置
            - length: 列表长度（默认10）
            - is_nested: 是否嵌套结构（默认False）

    Returns:
        随机生成的列表
    """
    element_config = data.get('element', {'str': {'len': 5}})
    length = data.get('length', 5)
    is_nested = data.get('is_nested', False)

    if is_nested:
        return [generate_sample({k: v}) for k, v in element_config.items() for _ in range(length)]
    return [generate_sample(element_config) for _ in range(length)]

def gen_dict(data: Dict[str, Any]) -> dict:
    """
    生成随机字典（支持嵌套结构）

    Args:
        data: 包含配置信息的字典，需包含：
            - keys: 键生成配置
            - values: 值生成配置
            - count: 键值对数量（默认5）

    Returns:
        随机生成的字典
    """
    key_config = data.get('keys', {'str': {'len': 5, 'datarange': string.ascii_lowercase}})
    value_config = data.get('values', {'int': {'datarange': [1, 100]}})
    count = data.get('count', 3)

    keys = [generate_sample(key_config) for _ in range(count)]
    values = [generate_sample(value_config) for _ in range(count)]

    return dict(zip(keys, values))

def gen_tuple(data: Dict[str, Any]) -> tuple:
    """
    生成随机元组（支持嵌套结构）

    Args:
        data: 包含配置信息的字典，需包含：
            - element: 元素生成配置
            - length: 元组长度（默认5）

    Returns:
        随机生成的元组
    """
    element_config = data.get('element', {'int': {'datarange': [1, 100]}})
    length = data.get('length', 5)
    return tuple(generate_sample(element_config) for _ in range(length))

def gen_union(data: Dict[str, Any]) -> Any:
    """
    从多种类型配置中随机选择一种生成样本

    Args:
        data: 包含多种类型配置的列表

    Returns:
        随机选择的类型生成的样本
    """
    options = data.get('options', [])
    if not options:
        raise ValueError("'union'类型配置中必须包含至少一种类型选项")

    # 随机选择一种类型配置
    selected_config = random.choice(options)
    return generate_sample(selected_config)



# 类型到生成函数的映射（可扩展）
TYPE_TO_FUNC = {
    'str': gen_str,
    'int': gen_int,
    'float': gen_float,
    'bool': gen_bool,
    'date': gen_date,
    'list': gen_list,
    'dict': gen_dict,
    'tuple': gen_tuple,
    'union': gen_union,  # 添加union类型支持
}

def generate_sample(struct: Dict[str, Any]) -> Any:
    """
    根据结构配置生成单个随机样本

    Args:
        struct: 样本结构配置字典，格式为 {类型: 配置参数}

    Returns:
        生成的随机样本

    Raises:
        ValueError: 当结构配置不合法时抛出
    """
    if len(struct) != 1:
        raise ValueError(f"结构配置必须包含且仅包含一个类型键，当前结构: {struct}")

    type_name, data = next(iter(struct.items()))
    if type_name not in TYPE_TO_FUNC:
        supported_types = ', '.join(TYPE_TO_FUNC.keys())
        raise ValueError(f"不支持的类型 '{type_name}'，支持的类型: {supported_types}")

    return TYPE_TO_FUNC[type_name](data)

def random_sampler(**kwargs) -> Generator[Any, None, None]:
    """
    随机样本生成器函数

    Args:
        **kwargs: 包含以下关键字参数:
            - number: 生成样本数量（必须为正整数）
            - 其他参数: 样本结构配置

    Yields:
        生成的随机样本

    Raises:
        ValueError: 当参数不合法时抛出
    """
    # 验证样本数量参数
    number = kwargs.get('number')
    if not isinstance(number, int) or number <= 0:
        raise ValueError("'number'参数必须为正整数")

    # 提取结构配置
    struct = {k: v for k, v in kwargs.items() if k != 'number'}
    if not struct:
        raise ValueError("必须提供样本结构配置")

    # 生成样本
    for _ in range(number):
        yield generate_sample(struct)



if __name__ == '__main__':
    print("=== 基础数据类型生成示例 ===")
    # 生成5个随机整数
    for num in random_sampler(number=5, int={'datarange': [1, 100]}):
        print(f"随机整数: {num}")

    print("\n=== 复杂嵌套结构示例 ===")
    # 修正union类型的配置格式
    complex_config = {
        'number': 2,
        'dict': {
            'keys': {'str': {'len': 4, 'datarange': string.ascii_uppercase}},
            'values': {
                'list': {
                    'element': {
                        'tuple': {
                            'element': {
                                'union': {  # 修正为字典格式，包含options列表
                                    'options': [
                                        {'str': {'len': 6, 'datarange': string.ascii_lowercase}},
                                        {'int': {'datarange': [100, 999]}},
                                        {'float': {'datarange': [0, 10], 'precision': 2}}
                                    ]
                                }
                            },
                            'length': 3
                        }
                    },
                    'length': 4,
                    'is_nested': True
                }
            },
            'count': 3
        }
    }

    for i, sample in enumerate(random_sampler(**complex_config), 1):
        print(f"样本 {i}:")
        print(sample)
        print("-" * 50)

    print("\n=== 日期类型生成示例 ===")
    # 生成3个2010-2025年间的随机日期
    for date in random_sampler(number=3, date={'start_year': 2010, 'end_year': 2025}):
        print(f"随机日期: {date}")

    print("\n=== 布尔值生成示例 ===")
    # 生成5个随机布尔值
    for boolean in random_sampler(number=5, bool={}):
        print(f"随机布尔值: {boolean}")

    print("\n=== 自定义联合类型示例 ===")
    # 生成3个随机类型样本（字符串、整数或布尔值）
    union_config = {
        'number': 3,
        'union': {
            'options': [
                {'str': {'len': 8}},
                {'int': {'datarange': [1000, 9999]}},
                {'bool': {}}
            ]
        }
    }

    for sample in random_sampler(**union_config):
        print(f"联合类型样本: {sample} (类型: {type(sample).__name__})")
