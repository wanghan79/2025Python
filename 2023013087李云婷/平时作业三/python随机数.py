import random
import string
import functools


# 带参装饰器
def StaticRes(*stats):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)  # 调用被装饰的函数
            # 提取所有可统计的数值
            values = []
            for item in result:
                if isinstance(item, (int, float)):
                    values.append(item)
                elif isinstance(item, list):
                    values.extend([x for x in item if isinstance(x, (int, float))])
                elif isinstance(item, tuple):
                    values.extend([x for x in item if isinstance(x, (int, float))])
                elif isinstance(item, dict):
                    values.extend([x for x in item.values() if isinstance(x, (int, float))])

            stats_result = {}
            if 'SUM' in stats:
                stats_result['SUM'] = sum(values) if values else 0
            if 'AVG' in stats:
                stats_result['AVG'] = sum(values) / len(values) if values else 0
            if 'MAX' in stats:
                stats_result['MAX'] = max(values) if values else None
            if 'MIN' in stats:
                stats_result['MIN'] = min(values) if values else None
            return stats_result

        return wrapper

    return decorator


# 生成随机数据的函数
def generate(**kwargs):
    num = kwargs.get('num', 1)  # 使用 get 方法获取 num，默认值为 1
    for _ in range(num):
        res = list()
        for k, v in kwargs.items():
            if k == 'num':
                continue
            elif k == 'int':
                it = iter(v['datarange'])
                value = random.randint(next(it), next(it))
                res.append(value)
            elif k == 'float':
                it = iter(v['datarange'])
                value = random.uniform(next(it), next(it))
                res.append(value)
            elif k == 'str':
                datarange, length = v['datarange'], v['len']
                value = ''.join(random.SystemRandom().choice(datarange) for _ in range(length))
                res.append(value)
            elif k == 'dict':
                elem = dict()
                elem[random.randint(0, 10)] = random.randint(0, 10)
                res.append(elem)
            elif k == 'list':
                value = list(generate(**v))  # 递归调用，注意传递字典
                res.append(value)
            elif k == 'tuple':
                value = tuple(generate(**v))  # 递归调用，注意传递字典
                res.append(value)
            else:
                continue
        yield res  # 使用 yield 逐个生成结果


# 被装饰的函数
@StaticRes('SUM', 'AVG', 'MAX', 'MIN')  # 指定需要统计的指标
def data_sampling(**kwargs):
    generator = generate(**kwargs)
    results = []
    for sample in generator:
        print("Generated Sample:", sample)  # 打印生成的样本
        results.append(sample)
    return results


# 主函数
def main():
    struct = {
        'num': 10,  # 生成10个样本（减少数量以便快速测试）
        'int': {'datarange': (1, 100)},  # 生成1到100之间的随机整数
        'float': {'datarange': (0.0, 1.0)},  # 生成0.0到1.0之间的随机浮点数
        'str': {'datarange': string.ascii_uppercase, 'len': 3},  # 生成3个随机大写字母
        'list': {
            'int': {'datarange': (1, 10)}
        },
        'tuple': {
            'float': {'datarange': (0.0, 1.0)}
        },
        'dict': {
            'int': {'datarange': (1, 10)}
        }
    }
    result = data_sampling(**struct)
    print("\nStatistics Result:", result)  # 打印统计结果


if __name__ == "__main__":
    main()