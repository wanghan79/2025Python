import random
import string
import statistics
from functools import wraps

# 定义带参装饰器，用于对数据进行统计操作
def statistic_decorator(*stats):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)  # 调用原函数生成数据
            stats_results = {}  # 用于存储统计结果
            flattened_data = []

            # 将结果展平并过滤出数值类型数据
            def flatten_and_filter(data):
                for item in data:
                    if isinstance(item, (int, float)):
                        flattened_data.append(item)
                    elif isinstance(item, (list, tuple)):
                        flatten_and_filter(item)

            flatten_and_filter(result)

            # 根据统计操作计算结果
            if 'SUM' in stats and flattened_data:
                stats_results['SUM'] = sum(flattened_data)
            if 'AVG' in stats and flattened_data:
                stats_results['AVG'] = statistics.mean(flattened_data)
            if 'MAX' in stats and flattened_data:
                stats_results['MAX'] = max(flattened_data)
            if 'MIN' in stats and flattened_data:
                stats_results['MIN'] = min(flattened_data)

            # 输出统计结果
            if stats_results:
                print("统计结果：", stats_results)
            return result  # 返回原函数的结果
        return wrapper
    return decorator


class DataProcessor:
    def __init__(self):
        pass

    def dataSampling(self, **kwargs):
        result = []
        for key, specs in kwargs.items():
            if key == 'int':
                result.append(random.randint(*specs['datarange']))
            elif key == 'float':
                result.append(random.uniform(*specs['datarange']))
            elif key == 'str':
                chars = specs['datarange']
                length = specs.get('len', 0)
                result.append(''.join(random.choice(chars) for _ in range(length)))
            elif key == 'tuple':
                tuple_elements = [self.dataSampling(**{k: v}) for k, v in specs.items() if isinstance(v, dict)]
                result.append(tuple(tuple_elements))
            elif key == 'list':
                list_elements = [self.dataSampling(**specs) for _ in range(specs.get('count', 1))]
                result.append(list_elements)
        return result


# 动态应用装饰器
def apply_decorator(func, stats):
    return statistic_decorator(*stats)(func)


# 使用示例
if __name__ == "__main__":
    processor = DataProcessor()
    struct = {
        'int': {'datarange': [1, 10]},
        'float': {'datarange': [1.0, 10.0]},
        'tuple': {
            'int': {'datarange': [1, 50]},
            'str': {'datarange': string.ascii_uppercase, 'len': 3}
        },
        'list': {
            'int': {'datarange': [1, 30]},
            'str': {'datarange': string.ascii_lowercase, 'len': 8},
            'float': {'datarange': [1.0, 10.0]}
        }
    }

    # 用户输入指定统计操作
    print("可用的统计操作：SUM、AVG、MAX、MIN")
    user_input = input("请输入需要的统计操作（用逗号分隔，例如：SUM,AVG）：").strip().upper()
    stats_to_apply = [stat.strip() for stat in user_input.split(",")]

    # 动态应用装饰器
    decorated_dataSampling = apply_decorator(processor.dataSampling, stats_to_apply)

    # 调用装饰后的 dataSampling 方法
    data = decorated_dataSampling(**struct)
    print("生成的数据：", data)