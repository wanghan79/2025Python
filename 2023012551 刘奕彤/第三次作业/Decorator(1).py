import random
import math
from typing import Any, Callable, Dict, Generator, List, Tuple, Union

###################################################################################
##
##  数据生成函数
##
###################################################################################

def gen_str(data: Dict[str, Any]) -> str:
    """从指定字符串中随机生成指定长度的字符串"""
    return ''.join(random.choices(data['datarange'], k=data['len']))

def gen_int(data: Dict[str, Any]) -> int:
    """从随机数范围中生成随机int数"""
    return random.randint(data['datarange'][0], data['datarange'][1])

def gen_float(data: Dict[str, Any]) -> float:
    """从随机数范围中生成随机浮点数"""
    return random.uniform(data['datarange'][0], data['datarange'][1])

def gen_list(data: Dict[str, Any]) -> list:
    """生成列表"""
    return [generate_sample(item) for item in data['elements']]

def gen_dict(data: Dict[str, Any]) -> dict:
    """生成字典"""
    return {key: generate_sample(config) for key, config in data['fields'].items()}

def gen_tuple(data: Dict[str, Any]) -> tuple:
    """生成元组"""
    return tuple(generate_sample(item) for item in data['elements'])

# 类型映射字典
TYPE_TO_FUNC = {
    'str': gen_str,
    'int': gen_int,
    'float': gen_float,
    'list': gen_list,
    'dict': gen_dict,
    'tuple': gen_tuple,
}

###################################################################################
##
##  核心函数
##
###################################################################################

def generate_sample(config: Dict[str, Any]) -> Any:
    """
    生成指定结构配置的随机样本

    参数:
        config: 描述要生成数据结构的字典，格式为 {'type': ..., ...}

    返回:
        随机生成的样本数据
    """
    if 'type' not in config:
        raise ValueError(f"配置必须包含 'type' 键：{config}")

    type_name = config['type']

    if type_name not in TYPE_TO_FUNC:
        raise ValueError(f"不支持的类型：'{type_name}'")

    return TYPE_TO_FUNC[type_name](config)

def extract_numbers(data: Any) -> List[Union[int, float]]:
    """
    递归提取数据结构中的所有数值（整数和浮点数）

    参数:
        data: 任意数据结构

    返回:
        包含所有数值的列表
    """
    numbers = []

    # 处理列表、元组、集合
    if isinstance(data, (list, tuple, set)):
        for item in data:
            numbers.extend(extract_numbers(item))

    # 处理字典
    elif isinstance(data, dict):
        for value in data.values():
            numbers.extend(extract_numbers(value))

    # 处理数值型数据
    elif isinstance(data, (int, float)):
        numbers.append(data)

    return numbers

def statistics(*metrics: str) -> Callable:
    """
    带参数的统计装饰器，支持多种统计操作

    支持的统计操作:
        SUM: 求和
        AVG: 平均值
        MAX: 最大值
        MIN: 最小值
        VAR: 方差
        STD: 标准差
        COUNT: 数值个数
        RANGE: 范围(最大值-最小值)
        MEDIAN: 中位数
        RMSE: 均方根误差

    参数:
        metrics: 统计方法名称列表

    返回:
        装饰器函数
    """
    # 验证参数
    valid_metrics = {'SUM', 'AVG', 'MAX', 'MIN', 'VAR', 'STD', 'COUNT', 'RANGE', 'MEDIAN', 'RMSE'}
    invalid_metrics = set(metrics) - valid_metrics
    if invalid_metrics:
        raise ValueError(f"不支持的统计方法: {invalid_metrics}")

    # 装饰器工厂函数
    def decorator(func: Callable) -> Callable:
        # 装饰器包装函数
        def wrapper(*args, ​**kwargs) -> Dict[str, Union[float, int]]:
            # 1. 执行生成器函数，收集样本
            samples = list(func(*args, ​**kwargs))

            # 2. 提取数值数据
            all_numbers = []
            for sample in samples:
                all_numbers.extend(extract_numbers(sample))

            # 3. 计算结果
            results = {}

            if not all_numbers:
                print("警告: 未提取到数值型数据，无法进行统计计算")
                return results

            # 计算基础统计量
            total = sum(all_numbers)
            count = len(all_numbers)
            sorted_numbers = sorted(all_numbers)

            # 计算需要的统计量
            if 'SUM' in metrics:
                results['SUM'] = total

            if 'COUNT' in metrics:
                results['COUNT'] = count

            if 'AVG' in metrics:
                results['AVG'] = total / count if count > 0 else 0

            if 'MAX' in metrics:
                results['MAX'] = max(all_numbers) if all_numbers else 0

            if 'MIN' in metrics:
                results['MIN'] = min(all_numbers) if all_numbers else 0

            if 'RANGE' in metrics and 'MAX' in metrics and 'MIN' in metrics:
                results['RANGE'] = results['MAX'] - results['MIN']

            # 计算方差和标准差
            if any(m in metrics for m in ['VAR', 'STD', 'RMSE']) or 'AVG' in metrics:
                mean = results['AVG'] if 'AVG' in metrics else total / count
                squared_diffs = sum((x - mean) ​** 2 for x in all_numbers)

                if 'VAR' in metrics:
                    results['VAR'] = squared_diffs / count if count > 0 else 0

                if 'STD' in metrics:
                    results['STD'] = math.sqrt(results.get('VAR', squared_diffs / count)) if count > 0 else 0

                if 'RMSE' in metrics:
                    results['RMSE'] = math.sqrt(squared_diffs / count) if count > 0 else 0

            # 计算中位数
            if 'MEDIAN' in metrics:
                if count % 2 == 0:
                    mid = count // 2
                    results['MEDIAN'] = (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2
                else:
                    results['MEDIAN'] = sorted_numbers[count // 2]

            return results

        return wrapper

    return decorator

###################################################################################
##
##  带统计功能的生成器
##
###################################################################################

def random_sampler(sample_config: Dict[str, Any], sample_count: int) -> Generator[Any, None, None]:
    """
    随机样本生成器

    参数:
        sample_config: 样本结构配置
        sample_count: 生成的样本数量

    返回:
        生成器，每次迭代产生一个随机样本
    """
    for _ in range(sample_count):
        yield generate_sample(sample_config)

###################################################################################
##
##  使用示例
##
###################################################################################

def enhanced_data_generator_example():
    """增强型数据生成器示例"""
    print("=" * 50)
    print("增强型数据生成器示例")
    print("=" * 50)

    # 配置样本结构
    config = {
        'type': 'dict',
        'fields': {
            'id': {
                'type': 'int',
                'datarange': [1000, 9999]
            },
            'temperature': {
                'type': 'float',
                'datarange': [-20.0, 40.0]
            },
            'measurements': {
                'type': 'list',
                'elements': [
                    {
                        'type': 'float',
                        'datarange': [0.0, 100.0]
                    },
                    {
                        'type': 'int',
                        'datarange': [0, 100]
                    }
                ]
            }
        }
    }

    # 创建带装饰器的生成器函数
    @statistics('SUM', 'AVG', 'MAX', 'MIN', 'COUNT', 'RANGE', 'STD')
    def sensor_data_generator():
        """传感器数据生成器"""
        return random_sampler(config, 100)

    print("生成传感器数据并计算统计量:")
    stats = sensor_data_generator()

    print("\n统计结果:")
    for metric, value in stats.items():
        if isinstance(value, float):
            print(f"{metric}: {value:.4f}")
        else:
            print(f"{metric}: {value}")

def financial_data_example():
    """金融数据示例"""
    print("\n" + "=" * 50)
    print("金融数据分析")
    print("=" * 50)

    # 金融数据配置
    config = {
        'type': 'list',
        'elements': [
            {
                'type': 'dict',
                'fields': {
                    'symbol': {
                        'type': 'str',
                        'datarange': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                        'len': 3
                    },
                    'price': {
                        'type': 'float',
                        'datarange': [50.0, 200.0]
                    },
                    'volume': {
                        'type': 'int',
                        'datarange': [1000, 10000]
                    }
                }
            },
            {
                'type': 'int',
                'datarange': [1, 100]
            }
        ]
    }

    # 创建带装饰器的生成器函数
    @statistics('MIN', 'MAX', 'AVG', 'VAR', 'MEDIAN')
    def stock_data_generator():
        """股票数据生成器"""
        return random_sampler(config, 50)

    print("生成股票数据并计算统计量:")
    stats = stock_data_generator()

    print("\n统计结果:")
    for metric, value in stats.items():
        if isinstance(value, float):
            print(f"{metric}: {value:.4f}")
        else:
            print(f"{metric}: {value}")

def scientific_data_example():
    """科研数据示例"""
    print("\n" + "=" * 50)
    print("科研数据分析")
    print("=" * 50)

    # 科研数据配置
    config = {
        'type': 'tuple',
        'elements': [
            {
                'type': 'dict',
                'fields': {
                    'experiment_id': {
                        'type': 'int',
                        'datarange': [100, 199]
                    },
                    'measurements': {
                        'type': 'list',
                        'elements': [
                            {
                                'type': 'float',
                                'datarange': [0.0, 1.0]
                            }
                        ]
                    }
                }
            },
            {
                'type': 'float',
                'datarange': [10.0, 20.0]
            }
        ]
    }

    # 创建带装饰器的生成器函数 - 多种统计指标
    @statistics('AVG', 'STD', 'MEDIAN', 'RMSE')
    def experiment_data_generator():
        """实验数据生成器"""
        return random_sampler(config, 75)

    print("生成科学实验数据并计算统计量:")
    stats = experiment_data_generator()

    print("\n统计结果:")
    for metric, value in stats.items():
        print(f"{metric}: {value:.4f}")

def mixed_statistics_example():
    """混合统计操作示例"""
    print("\n" + "=" * 50)
    print("混合统计操作示例")
    print("=" * 50)

    # 混合数据配置
    config = {
        'type': 'list',
        'elements': [
            {
                'type': 'int',
                'datarange': [500, 1000]
            },
            {
                'type': 'float',
                'datarange': [1.5, 3.5]
            }
        ]
    }

    # 第一种统计组合
    @statistics('AVG', 'MAX', 'MIN')
    def mixed_generator_1():
        return random_sampler(config, 30)

    # 第二种统计组合
    @statistics('COUNT', 'SUM', 'RANGE')
    def mixed_generator_2():
        return random_sampler(config, 30)

    # 第三种统计组合
    @statistics('MEDIAN', 'VAR', 'STD')
    def mixed_generator_3():
        return random_sampler(config, 30)

    print("生成数据并计算不同统计组合:")
    stats1 = mixed_generator_1()
    stats2 = mixed_generator_2()
    stats3 = mixed_generator_3()

    print("\n统计组合1 (AVG, MAX, MIN):")
    for metric, value in stats1.items():
        print(f"{metric}: {value:.4f}")

    print("\n统计组合2 (COUNT, SUM, RANGE):")
    for metric, value in stats2.items():
        print(f"{metric}: {value:.4f}")

    print("\n统计组合3 (MEDIAN, VAR, STD):")
    for metric, value in stats3.items():
        print(f"{metric}: {value:.4f}")

def custom_data_generation():
    """自定义数据生成"""
    print("\n" + "=" * 50)
    print("自定义数据生成")
    print("=" * 50)

    # 用户自定义配置
    fields = {}
    print("创建自定义数据结构 (输入 'done' 结束)")

    while True:
        key = input("\n字段名称: ")
        if key.lower() == 'done':
            break

        data_type = input(f"{key} 类型 (int/float/str/list/dict/tuple): ")

        if data_type == 'int':
            min_val = int(input(f"{key} 最小值: "))
            max_val = int(input(f"{key} 最大值: "))
            fields[key] = {'type': 'int', 'datarange': [min_val, max_val]}

        elif data_type == 'float':
            min_val = float(input(f"{key} 最小值: "))
            max_val = float(input(f"{key} 最大值: "))
            fields[key] = {'type': 'float', 'datarange': [min_val, max_val]}

        elif data_type == 'str':
            length = int(input(f"{key} 长度: "))
            chars = input(f"{key} 字符集 (默认为a-z0-9): ") or string.ascii_letters + string.digits
            fields[key] = {'type': 'str', 'datarange': chars, 'len': length}

        # 简化其他类型的处理...
        else:
            print(f"暂时只支持 int, float 和 str 类型的自定义配置")
            continue

    # 创建配置
    config = {
        'type': 'dict',
        'fields': fields
    }

    # 选择统计方法
    print("\n可用的统计方法: SUM, AVG, MAX, MIN, COUNT, VAR, STD, RANGE, MEDIAN, RMSE")
    stats_input = input("输入统计方法，用逗号分隔 (如: AVG,MAX,MIN): ")
    stats_methods = [s.strip().upper() for s in stats_input.split(',')]

    # 创建带装饰器的生成器函数
    @statistics(*stats_methods)
    def custom_data_generator():
        sample_count = int(input("\n生成样本数量: "))
        return random_sampler(config, sample_count)

    print("\n生成数据并计算统计量:")
    stats = custom_data_generator()

    if stats:
        print("\n统计结果:")
        for metric, value in stats.items():
            if isinstance(value, float):
                print(f"{metric}: {value:.4f}")
            else:
                print(f"{metric}: {value}")
    else:
        print("未得到有效的统计结果")

if __name__ == '__main__':
    # 执行所有示例
    enhanced_data_generator_example()
    financial_data_example()
    scientific_data_example()
    mixed_statistics_example()

    # 可以选择性运行自定义生成器
    run_custom = input("\n运行自定义数据生成器? (y/n): ")
    if run_custom.lower() == 'y':
        import string
        custom_data_generation()

    print("\n程序结束")