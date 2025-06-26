import random
import string

def generate(kwargs):
    result = list()
    res = list()
    for k, v in kwargs.items():
        if k == int:
            it = iter(v['datarange'])
            res.append(random.randint(next(it), next(it)))
        elif k == float:
            it = iter(v['datarange'])
            res.append(random.uniform(next(it), next(it)))
        elif k == str:
            datarange, length = v['datarange'], v['len']
            tmp = ''.join(random.SystemRandom().choice(datarange) for _ in range(length))
            res.append(tmp)
        elif k == dict:
            elem = dict()
            for sub_k, sub_v in v.items():
                it = iter(sub_v['datarange'])
                if sub_k == int:
                    elem[random.randint(0, 10)] = random.randint(next(it), next(it))
                elif sub_k == float:
                    elem[random.randint(0, 10)] = random.uniform(next(it), next(it))
            res.append(elem)
        elif k == list:
            res.append(list(generate(v)))
        elif k == tuple:
            res.append(tuple(generate(v)))
        else:
            continue
    result.append(res)
    yield result

def extract_numbers(data):
    nums = []
    if isinstance(data, (int, float)):
        nums.append(data)
    elif isinstance(data, (list, tuple)):
        for item in data:
            nums.extend(extract_numbers(item))
    elif isinstance(data, dict):
        for key, value in data.items():
            nums.extend(extract_numbers(key))
            nums.extend(extract_numbers(value))
    return nums

def statistics(*ops):
    def decorator(func):
        def wrapper(*args, **kwargs):
            data_list = []
            for i in range(10):  # 控制样本数量
                gen = func(*args, **kwargs)
                sample = next(gen)
                print(f"样本 {i + 1}:", sample)  #  打印样本数据
                data_list.extend(extract_numbers(sample))

            results = {}
            if 'SUM' in ops:
                results['SUM'] = sum(data_list)
            if 'AVG' in ops:
                results['AVG'] = sum(data_list) / len(data_list) if data_list else 0
            if 'MAX' in ops:
                results['MAX'] = max(data_list)
            if 'MIN' in ops:
                results['MIN'] = min(data_list)

            print("统计结果:", results)
            return results
        return wrapper
    return decorator


@statistics('SUM', 'AVG', 'MAX', 'MIN')  # 任意组合
def main():
    struct = {
        tuple: {
            str: {"datarange": string.ascii_uppercase, "len": 50},
            list: {
                int: {"datarange": [0, 10]},
                float: {"datarange": [0, 10]}
            },
            dict: {
                int: {"datarange": [0, 10]}
            }
        }
    }
    return generate(struct)

if __name__ == '__main__':
    main()
