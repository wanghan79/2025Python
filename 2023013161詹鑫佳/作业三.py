import random
import string


def Statistics(*ops):
    def decorator(func):
        def wrapper(**kwargs):
            data = list(func(**kwargs))

            # 提取嵌套结构中的数值数据
            def extract_numbers(item):
                numbers = []
                if isinstance(item, (int, float)):
                    numbers.append(item)
                elif isinstance(item, (list, tuple)):
                    for sub_item in item:
                        numbers.extend(extract_numbers(sub_item))
                elif isinstance(item, dict):
                    for key, value in item.items():
                        numbers.extend(extract_numbers(key))
                        numbers.extend(extract_numbers(value))
                return numbers

            numeric_values = []
            for sample in data:
                for item in sample:
                    numeric_values.extend(extract_numbers(item))

            result = {}

            if not numeric_values:
                result['error'] = "没有可用于统计的数值类型数据"
            else:
                supported_ops = {'sum', 'avg', 'max', 'min'}
                invalid_ops = set(ops) - supported_ops
                if invalid_ops:
                    result['error'] = f"不支持的操作: {invalid_ops}"

                if 'sum' in ops:
                    result['sum'] = sum(numeric_values)
                if 'avg' in ops:
                    result['avg'] = round(sum(numeric_values) / len(numeric_values), 2)
                if 'max' in ops:
                    result['max'] = max(numeric_values)
                if 'min' in ops:
                    result['min'] = min(numeric_values)

            return data, result  # 返回原始数据和统计结果（分开）

        return wrapper
    return decorator


@Statistics('sum', 'avg', 'max', 'min')  # 可自由组合：如 ('max', 'avg')
def SampleData(**kwargs):
    num = kwargs.get('num', 1)  # 使用 get 方法获取 num，默认值为 1
    for _ in range(num):
        answer = list()
        for k, v in kwargs.items():
            if k == 'num':
                continue
            elif k == 'int':
                it = iter(v['datarange'])
                answer.append(random.randint(next(it), next(it)))
            elif k == 'float':
                it = iter(v['datarange'])
                answer.append(random.uniform(next(it), next(it)))
            elif k == 'str':
                datarange, length = v['datarange'], v['len']
                tmp = ''.join(random.SystemRandom().choice(datarange) for _ in range(length))
                answer.append(tmp)
            elif k == 'dict':
                elem = dict()
                elem[random.randint(0, 10)] = random.randint(0, 10)
                answer.append(elem)
            elif k == 'list':
                answer.append(list(SampleData(**v)[0]))  # 递归调用，注意传递字典
            elif k == 'tuple':
                answer.append(tuple(SampleData(**v)[0]))  # 递归调用，注意传递字典
            else:
                continue
        yield answer


def main():
    struct = {
        'num': 5,  # 控制生成样本数量
        'tuple': {
            'str': {"datarange": string.ascii_uppercase, "len": 3},
            'list': {
                'int': {"datarange": (0, 10)},
                'float': {"datarange": (0, 1.0)}
            },
            'dict': {}
        }
    }

    data, stats = SampleData(**struct)

    print("生成的数据：")
    for d in data:
        print(d)  # 只打印原始数据，不含任何统计字段

    print("\n统计结果：")
    if 'error' in stats:
        print(stats['error'])
    else:
        if 'sum' in stats:
            print(f"总和: {stats['sum']}")
        if 'avg' in stats:
            print(f"平均值: {stats['avg']}")
        if 'max' in stats:
            print(f"最大值: {stats['max']}")
        if 'min' in stats:
            print(f"最小值: {stats['min']}")


if __name__ == "__main__":
    main()
