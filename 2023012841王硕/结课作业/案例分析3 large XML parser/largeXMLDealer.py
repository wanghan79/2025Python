import random
import string

def calc_decorator(*operations):
    """
    统计操作装饰器，根据指定的操作计算数值统计结果
    支持的操作：
    1: 最大值 (MAX)
    2: 最小值 (MIN)
    3: 总和 (SUM)
    4: 平均值 (AVG)
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            numeric_data = func(*args, **kwargs)
            results = {}
            if 1 in operations:
                results['max'] = max(numeric_data) if numeric_data else None
            if 2 in operations:
                results['min'] = min(numeric_data) if numeric_data else None
            if 3 in operations:
                results['sum'] = sum(numeric_data) if numeric_data else 0
            if 4 in operations:
                results['avg'] = (sum(numeric_data) / len(numeric_data)) if numeric_data else None
            return results
        return wrapper
    return decorator


def random_data_generator(**config):
    """
    数据生成器函数，根据配置生成不同类型的数据
    支持的数据类型：整数、浮点数、字符串、字典、列表和元组
    """
    count = config.get('num', 1)
    results = []

    for _ in range(count):
        current_sample = []
        for data_type, settings in config.items():
            if data_type == 'num':
                continue
            if data_type == "integer":
                start, end = settings['range']
                current_sample.append(random.randint(start, end))
            elif data_type == "float":
                start, end = settings['range']
                current_sample.append(random.uniform(start, end))
            elif data_type == "string":
                chars = settings['characters']
                length = settings['length']
                current_sample.append(''.join(random.choices(chars, k=length)))
            elif data_type == "dictionary":
                key = ''.join(random.choices(string.ascii_letters, k=3))
                value = random.randint(0, 100)
                current_sample.append({key: value})
            elif data_type in ("list", "tuple"):
                nested_data = random_data_generator(**settings)
                current_sample.append(nested_data if data_type == "list" else tuple(nested_data))
        results.append(current_sample if len(current_sample) > 1 else current_sample[0])
    return results[0] if count == 1 else results


# 示例数据结构配置
demo_config = {
    'num': 5,
    "integer": {"range": (0, 100)},
    "float": {"range": (0, 100.0)},
    "string": {
        "characters": string.ascii_uppercase,
        "length": 5
    },
    "dictionary": {},
    "list": {
        "integer": {"range": (0, 10)},
        "float": {"range": (0, 1.0)}
    }
}
requested_ops = {2, 4}  # 请求最小值和平均值

@calc_decorator(*requested_ops)
def create_and_analyze(**settings):
    generated_data = random_data_generator(**settings)
    def extract_values(items):
        for item in items:
            if isinstance(item, (list, tuple)):
                yield from extract_values(item)
            elif isinstance(item, dict):
                yield from extract_values(item.values())
            elif isinstance(item, (int, float)):
                yield item
    return list(extract_values([generated_data]))

if __name__ == '__main__':
    # 生成示例数据
    sample_data = random_data_generator(**demo_config)
    print("生成的数据示例:", sample_data)

    # 执行数据生成及统计分析
    analysis_results = create_and_analyze(**demo_config)
    print("统计结果:", analysis_results)