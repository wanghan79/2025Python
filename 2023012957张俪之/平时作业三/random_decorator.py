"""
    content:Decorator
    time: 2025/5
    author:Zhang Lizhi
    function:SUM AVG MAX MIN
"""
import random
import string

# 写一个带参装饰器
def StaticRes(*statistics):
    def decorator(func):
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            
            # 提取数值数据
            def extract_numbers(obj):
                if isinstance(obj, (int, float)):
                    return [obj]
                elif isinstance(obj, (list, tuple)):
                    numbers = []
                    for item in obj:
                        numbers.extend(extract_numbers(item))
                    return numbers
                elif isinstance(obj, dict):
                    numbers = []
                    for value in obj.values():
                        numbers.extend(extract_numbers(value))
                    return numbers
                else:
                    return []
            
            numeric_data = []
            for item in data:
                numeric_data.extend(extract_numbers(item))
            
            results = {}
            for statistic in statistics:
                if statistic == 'SUM':
                    results['SUM'] = sum(numeric_data)
                elif statistic == 'AVG':
                    results['AVG'] = sum(numeric_data) / len(numeric_data) if numeric_data else 0
                elif statistic == 'MAX':
                    results['MAX'] = max(numeric_data) if numeric_data else None
                elif statistic == 'MIN':
                    results['MIN'] = min(numeric_data) if numeric_data else None
            return {"stats": results, "data": data}  
        return wrapper
    return decorator

@StaticRes('SUM', 'AVG', 'MAX', 'MIN')
def dataSampling(**kwargs):
    num = kwargs.get('num', 1)  
    struct = kwargs.get('struct', {}) 

    data_list = []
    for _ in range(num):
        root = []
        for key, value in struct.items():
            if isinstance(value, dict):
                if key in ['tuple', 'list', 'dict']:
                    container = []
                    for k, v in value.items():
                        if k == 'str':
                            datarange = v.get('datarange', string.ascii_uppercase)
                            length = v.get('len', 10)
                            tmp = ''.join(random.choice(datarange) for _ in range(length))
                            container.append(tmp)
                        elif k == 'int':
                            datarange = v.get('datarange', (0, 100))
                            it = iter(datarange)
                            container.append(random.randint(next(it), next(it)))
                        elif k == 'float':
                            datarange = v.get('datarange', (0.0, 100.0))
                            it = iter(datarange)
                            container.append(random.uniform(next(it), next(it)))
                    if key == 'tuple':
                        root.append(tuple(container))
                    elif key == 'list':
                        root.append(container)
                    elif key == 'dict':
                        dict_data = {}
                        for idx, item in enumerate(container):
                            if isinstance(item, str):
                                dict_data['str'] = item
                            elif isinstance(item, int):
                                dict_data['int'] = item
                            elif isinstance(item, float):
                                dict_data['float'] = item
                        root.append(dict_data)
                else:
                    if key == 'str':
                        datarange = value.get('datarange', string.ascii_uppercase)
                        length = value.get('len', 10)
                        tmp = ''.join(random.choice(datarange) for _ in range(length))
                        root.append(tmp)
                    elif key == 'int':
                        datarange = value.get('datarange', (0, 100))
                        it = iter(datarange)
                        root.append(random.randint(next(it), next(it)))
                    elif key == 'float':
                        datarange = value.get('datarange', (0.0, 100.0))
                        it = iter(datarange)
                        root.append(random.uniform(next(it), next(it)))
            elif isinstance(value, list):
                container = []
                for item in value:
                    if isinstance(item, dict):
                        for k, v in item.items():
                            if k == 'int':
                                datarange = v.get('datarange', (0, 100))
                                it = iter(datarange)
                                container.append(random.randint(next(it), next(it)))
                            elif k == 'float':
                                datarange = v.get('datarange', (0.0, 100.0))
                                it = iter(datarange)
                                container.append(random.uniform(next(it), next(it)))
                            elif k == 'str':
                                datarange = v.get('datarange', string.ascii_uppercase)
                                length = v.get('len', 10)
                                tmp = ''.join(random.choice(datarange) for _ in range(length))
                                container.append(tmp)
                root.append(container)
            else:
                root.append(value)
        data_list.append(root)
    return data_list

def apply():
    struct = {
        'tuple': {
            'str': {'datarange': string.ascii_uppercase, 'len': 50}
        },
        "list": {
            "int": {"datarange": (0, 10)},
        },
        'dict': {
            "float": {"datarange": (0, 1.0)},
            'str': {'datarange': string.ascii_lowercase, 'len': 10},
        },
        'int': {'datarange': (0, 10)}
    }

    return dataSampling(num=10, struct=struct)

result = apply()
print("统计结果:", result["stats"])
print("生成的随机数据:", result["data"])