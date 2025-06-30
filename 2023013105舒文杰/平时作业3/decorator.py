
import random

# 类型映射到生成函数的字典
GEN_FUNCS = {}

def make_string(cfg):
    chars = cfg.get("chars", "abcde")
    length = cfg.get("length", 6)
    return ''.join(random.choices(chars, k=length))

def make_int(cfg):
    low, high = cfg.get("range", [0, 10])
    return random.randint(low, high)

def make_float(cfg):
    low, high = cfg.get("range", [0.0, 1.0])
    return random.uniform(low, high)

def make_list(cfg):
    return [build_data({k: v}) for k, v in cfg.items()]

def make_dict(cfg):
    return {str(i): build_data({k: v}) for i, (k, v) in enumerate(cfg.items())}

def make_tuple(cfg):
    return tuple(build_data({k: v}) for k, v in cfg.items())

GEN_FUNCS["str"] = make_string
GEN_FUNCS["int"] = make_int
GEN_FUNCS["float"] = make_float
GEN_FUNCS["list"] = make_list
GEN_FUNCS["dict"] = make_dict
GEN_FUNCS["tuple"] = make_tuple

def build_data(definition):
    """
    按照定义生成对应结构的数据
    """
    if len(definition) != 1:
        raise ValueError("每次只能定义一个类型")
    key, val = next(iter(definition.items()))
    if key not in GEN_FUNCS:
        raise ValueError(f"未知类型：{key}")
    return GEN_FUNCS[key](val)

def collect_numbers(data):
    """
    递归提取结构中的所有数值（int/float）
    """
    nums = []
    if isinstance(data, (int, float)):
        nums.append(data)
    elif isinstance(data, (list, tuple, set)):
        for elem in data:
            nums.extend(collect_numbers(elem))
    elif isinstance(data, dict):
        for val in data.values():
            nums.extend(collect_numbers(val))
    return nums

def with_stats(*methods):
    """
    带参数的修饰器，用于统计数据（如 AVG、SUM 等）
    """
    def outer(func):
        def inner(*args, **kwargs):
            all_results = []
            for sample in func(*args, **kwargs):
                print(sample)
                all_results.append(sample)

            print(f"\n总共生成了 {len(all_results)} 个样本。\n")

            numbers = []
            for r in all_results:
                numbers.extend(collect_numbers(r))

            if not numbers:
                print("未提取到任何数值。")
                return []

            output = []
            mean = sum(numbers) / len(numbers)

            for method in methods:
                if method == "SUM":
                    output.append(("SUM", sum(numbers)))
                elif method == "AVG":
                    output.append(("AVG", mean))
                elif method == "VAR":
                    variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
                    output.append(("VAR", variance))
                elif method == "RMSE":
                    rmse = (sum((x - mean) ** 2 for x in numbers) / len(numbers)) ** 0.5
                    output.append(("RMSE", rmse))
                else:
                    raise ValueError(f"不支持的统计方法：{method}")

            return output
        return inner
    return outer

@with_stats("SUM", "AVG", "VAR", "RMSE")
def sample_data_gen(**kwargs):
    """
    样本生成器函数
    """
    count = kwargs.pop("count", 1)
    for _ in range(count):
        yield build_data(kwargs)


if __name__ == "__main__":
    # 简单结构样例
    config = {
        "count": 5,
        "tuple": {
            "str": {"chars": "xyzopq", "length": 6},
            "list": {
                "int": {"range": [10, 100]},
                "float": {"range": [1.5, 5.5]}
            },
            "dict": {
                "int": {"range": [0, 50]}
            }
        }
    }

    results = sample_data_gen(**config)
    print("统计结果：")
    for name, value in results:
        print(f"{name} = {value:.3f}")
