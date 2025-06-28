import random
import string


def extract_numeric(data):
    nums = []
    if isinstance(data, (int, float)):
        nums.append(data)
    elif isinstance(data, dict):
        for item in data.values():
            nums.extend(extract_numeric(item))
    elif isinstance(data, (list, tuple)):
        for item in data:
            nums.extend(extract_numeric(item))
    else:
        try:
            for item in data:
                nums.extend(extract_numeric(item))
        except Exception:
            pass
    return nums


def StaticRes(func):
    def wrapper(*args, stats_funcs, **kwargs):
        gen = func(*args, **kwargs)
        if not stats_funcs:
            raise ValueError("必须通过 stats_funcs 参数至少提供一个统计函数。")
        for data in gen:
            nums = extract_numeric(data)
            merged = {}
            for fn in stats_funcs:
                res = fn(nums)
                if not isinstance(res, dict):
                    raise TypeError(f"统计函数 {fn.__name__} 必须返回 dict 类型结果。")
                merged.update(res)
            yield {'tree': data, 'stats': merged}
    return wrapper


def randomGenerator(data_type, boundary):
    if data_type == "int":
        lo, hi = boundary['datarange']
        return random.randint(lo, hi)
    elif data_type == "float":
        lo, hi = boundary['datarange']
        return random.uniform(lo, hi)
    elif data_type == "str":
        return ''.join(random.SystemRandom().choice(boundary['datarange']) for _ in range(boundary['len']))
    else:
        return None


def generatorTree(**item):
    result = {}
    try:
        for key, value in item.items():
            if key in ("int", "float", "str"):
                result[key] = randomGenerator(key, value)
            elif key == "list":
                result[key] = [generatorTree(**i) for i in value]
            elif key == "dict":
                d = {}
                for i in value:
                    d.update(generatorTree(**i))
                result[key] = d
            elif key == "tuple":
                result[key] = tuple(generatorTree(**i) for i in value)
            else:
                coll = eval(key)()
                for i in value:
                    coll.add(generatorTree(**i))
                result[key] = coll
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None


@StaticRes
def multiGenerator(values, **kwargs):
    for _ in range(values):
        yield generatorTree(**kwargs)


def apply():
    """
    自定义数据类型要求:
        - 提供 add(element) 方法，用于添加子节点
        - 实现可迭代协议 (__iter__) 以支持 extract_numeric
    自定义统计函数要求:
        - 至少提供一个统计函数
        - 接受一个参数 nums
        - 返回值需为dict类型
    """
    struct = {
        "dict": [{
            "tuple": [
                {"int": {"datarange": [1, 10]}},
                {"int": {"datarange": [1, 10]}}
            ],
            "list": [
                {"dict": [
                    {"float": {"datarange": [1, 10]}},
                    {"str": {"datarange": string.ascii_uppercase, "len": 10}}
                ]}
            ] * 3
        }]
    }
    def MIN(nums):
        return {'MIN': min(nums) if nums else None}
    def MAX(nums):
        return {'MAX': max(nums) if nums else None}
    def AVG(nums):
        return {'AVG': sum(nums) / len(nums) if nums else 0}
    def SUM(nums):
        return {'SUM': sum(nums) if nums else 0}
    for item in multiGenerator(10000000000, **struct, stats_funcs=[MIN, MAX, AVG, SUM]):
        print(item)


if __name__ == "__main__":
    apply()
