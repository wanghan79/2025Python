"""
    author:Zhang Lizhi
    time: 2025/4
    content:使用生成器生成随机样本
    
"""
import random
import string

def generate(kwargs):
    num = kwargs.get('num', 1)  
    struct = kwargs.get('struct', {})  

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
        yield root


def apply():
    struct = {
        'num':  100,  
        'struct': {
            'tuple': {
                'str': {'datarange': string.ascii_uppercase, 'len': 50},
                'int': {'datarange': (0, 10)},
                'float': {'datarange': (0.0, 1.0)}
            },
            'list': {
                'float': {'datarange': (0.0, 1.0)},
                'str': {'datarange': string.ascii_lowercase, 'len': 10}
            },
            'dict': {
                'str': {'datarange': string.ascii_lowercase, 'len': 10},
                
                'float': {'datarange': (0.0, 1.0)}
            },
            'int': {'datarange': (0, 10)},
            'float': {'datarange': (0.0, 1.0)},
            'str': {'datarange': string.ascii_letters, 'len': 20}
        }
    }

    count = 0
    for data in generate(struct):
        print(data)
        count += 1
        if count > 100:
            break


if __name__ == "__main__":
    apply()