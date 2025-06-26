import random
import string

def extract_values(data):
    """
    递归提取嵌套结构中的 int 和 float 类型数据。
    """
    values = []
    if isinstance(data, (list, tuple, set)):
        for item in data:
            values.extend(extract_values(item))
    elif isinstance(data, dict):
        for value in data.values():
            values.extend(extract_values(value))
    elif isinstance(data, (int, float)):
        values.append(data)
    return values


def Statistics(*operations):
    def decorator(func):
        def wrapper(*args, **kwargs):
            samples = []
            all_values = []

            # 只收集样本和提取数值，不修改样本结构
            for sample in func(*args, **kwargs):
                samples.append(sample)
                all_values.extend(extract_values(sample))

            stats = {}
            if not all_values:
                stats = {op: None for op in operations}
            else:
                for op in operations:
                    if op == 'SUM':
                        stats['SUM'] = sum(all_values)
                    elif op == 'AVG':
                        stats['AVG'] = sum(all_values) / len(all_values)
                    elif op == 'MAX':
                        stats['MAX'] = max(all_values)
                    elif op == 'MIN':
                        stats['MIN'] = min(all_values)

            return samples, stats  # 最终才返回统计结果
        return wrapper
    return decorator



@Statistics('SUM', 'AVG', 'MAX', 'MIN')
def dataSampling(config):
    """
    根据配置 config 生成一个随机样本。
    支持 int, float, str, list, tuple, dict 类型。
    """

    def generate_item(k, v):
        if k == 'int':
            it = iter(v['datarange'])
            return random.randint(next(it), next(it))
        elif k == 'float':
            it = iter(v['datarange'])
            return random.uniform(next(it), next(it))
        elif k == 'str':
            datarange = v.get('datarange', string.ascii_letters)
            length = v.get('len', 8)
            return ''.join(random.choices(datarange, k=length))
        elif k == 'list':
            return [generate_item(key, val) for key, val in v.items()]
        elif k == 'tuple':
            return tuple(generate_item(key, val) for key, val in v.items())
        elif k == 'dict':
            return {key: generate_item(key, val) for key, val in v.items()}
        return None

    num = config.get('num', 1)

    for _ in range(num):
        sample = {}
        for key, value in config.items():
            if key == 'num':
                continue
            sample[key] = generate_item(key, value)
        yield sample


# 示例配置
struct = {
    'num': 100,
    'tuple': {
        'str': {"datarange": string.ascii_uppercase, "len": 10}
    },
    'dict': {
        'list': {
            'int': {"datarange": (0, 10)}
        }
    },
    'int': {"datarange": (0, 10)},
    'float': {"datarange": (0, 10)}
}

if __name__ == "__main__":
    samples, stats = dataSampling(struct)

    print("Generated Samples:")
    for idx, sample in enumerate(samples, start=1):
        print(f"Sample {idx}: {sample}")

    print("\nOverall Statistics:")
    for stat, value in stats.items():
        print(f"{stat}: {value}")

