import random
import string
from functools import wraps


class DataStatistic:
    def __init__(self, stat_type='sum'):
        """
        统计装饰器类
        :param stat_type: 统计类型，可选'sum'/'avg'/'max'/'min'
        """
        self.stat_type = stat_type

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 调用原始函数获取结果
            results = func(*args, **kwargs)

            # 对结果进行统计
            stats = []
            for result in results:
                group_stats = {}
                for item in result:
                    if isinstance(item, (int, float)):
                        key = 'numbers'
                        if key not in group_stats:
                            group_stats[key] = []
                        group_stats[key].append(item)
                    elif isinstance(item, dict):
                        key = 'dict_values'
                        if key not in group_stats:
                            group_stats[key] = []
                        group_stats[key].extend(item.values())
                    elif isinstance(item, (list, tuple)):
                        key = f'{type(item).__name__}_items'
                        if key not in group_stats:
                            group_stats[key] = []
                        for sub_item in item:
                            if isinstance(sub_item, (int, float)):
                                group_stats[key].append(sub_item)

                # 计算统计值
                calculated_stats = {}
                for key, values in group_stats.items():
                    if not values:
                        continue
                    if self.stat_type == 'sum':
                        calculated_stats[f'{key}_sum'] = sum(values)
                    elif self.stat_type == 'avg':
                        calculated_stats[f'{key}_avg'] = sum(values) / len(values)
                    elif self.stat_type == 'max':
                        calculated_stats[f'{key}_max'] = max(values)
                    elif self.stat_type == 'min':
                        calculated_stats[f'{key}_min'] = min(values)

                stats.append(calculated_stats)

            return {'data': results, 'stats': stats}

        return wrapper


class DataGenerator:
    @DataStatistic(stat_type='sum')  # 这里可以修改为 'avg', 'max', 'min'
    def generate(self, kwargs):
        num = kwargs.get('num', 1)
        result = []
        for _ in range(num):
            res = []
            for key, value in kwargs.items():
                if key == 'num':
                    continue
                elif key == int:
                    low, high = value['datarange']
                    res.append(random.randint(low, high))
                elif key == float:
                    low, high = value['datarange']
                    res.append(random.uniform(low, high))
                elif key == str:
                    chars, length = value['datarange'], value['len']
                    res.append(''.join(random.choice(chars) for _ in range(length)))
                elif key == dict:
                    key_low, key_high = value.get('key_range', (0, 10))
                    val_low, val_high = value.get('val_range', (0, 10))
                    res.append({
                        random.randint(key_low, key_high):
                            random.randint(val_low, val_high)
                    })
                elif key == list:
                    sub_items = []
                    for sub_key, sub_value in value.items():
                        if sub_key == int:
                            low, high = sub_value['datarange']
                            sub_items.append(random.randint(low, high))
                        elif sub_key == float:
                            low, high = sub_value['datarange']
                            sub_items.append(random.uniform(low, high))
                    res.append(sub_items)
                elif key == tuple:
                    sub_items = []
                    for sub_key, sub_value in value.items():
                        if sub_key == str:
                            chars, length = sub_value['datarange'], sub_value['len']
                            sub_items.append(''.join(random.choice(chars) for _ in range(length)))
                    res.append(tuple(sub_items))
            result.append(res)
        return result


def main():
    generator = DataGenerator()

    struct = {
        'num': 3,  # 生成3组数据
        int: {'datarange': (1, 100)},  # 随机整数1-100
        float: {'datarange': (0.0, 10.0)},  # 随机浮点数0.0-10.0
        str: {'datarange': string.ascii_uppercase, 'len': 5},  # 5位大写字母
        dict: {'key_range': (1, 5), 'val_range': (10, 20)},  # 字典{1-5: 10-20}
        list: {
            int: {'datarange': (0, 10)},  # 列表包含一个0-10的整数
            float: {'datarange': (0, 100)}  # 和一个0-100的浮点数
        },
        tuple: {
            str: {'datarange': string.ascii_lowercase, 'len': 3}  # 元组包含一个3位小写字母
        }
    }

    result = generator.generate(struct)
    print("Generated Data:")
    for i, data in enumerate(result['data']):
        print(f"Group {i + 1}: {data}")

    print("\nStatistics:")
    for i, stat in enumerate(result['stats']):
        print(f"Group {i + 1} Stats: {stat}")


if __name__ == "__main__":
    main()