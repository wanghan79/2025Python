"""
此为Python 程序设计课平时作业三
"""
import random
import string
import math
from collections import defaultdict
from typing import Any, Dict, Generator, Iterable, List, Union

###############################################################################
# 常量与辅助函数
###############################################################################

# 用于判断数值类型
NUMERIC_TYPES = (int, float)

# 支持的基本及容器类型关键字
BASE_KEYS = {"int", "float", "double", "str", "bool", "choice"}
CONTAINER_KEYS = {"list", "tuple", "set", "dict"}

def calc_mean(seq: List[Union[int, float]]) -> float:
    """计算平均值"""
    return sum(seq) / len(seq) if seq else 0.0

def calc_std(seq: List[Union[int, float]]) -> float:
    """计算样本标准差"""
    if len(seq) < 2:
        return 0.0
    m = calc_mean(seq)
    return math.sqrt(sum((x - m) ** 2 for x in seq) / len(seq))


###############################################################################
# 统计装饰器
###############################################################################

def with_statistics(*ops):
    """
    装饰器：包装生成器函数，返回采样结果与统计信息。
    ops 传入内置统计函数（sum, max, min 等）或自定义函数。
    """
    op_map = {fn.__name__: fn for fn in ops}

    def decorator(gen_fn):
        def wrapper(*args, **kwargs):
            numeric_pool: List[Union[int, float]] = []
            type_buckets: Dict[str, List[Any]] = defaultdict(list)

            # 逐项收集
            for elem in gen_fn(*args, **kwargs):
                type_buckets[type(elem).__name__].append(elem)
                if isinstance(elem, NUMERIC_TYPES):
                    numeric_pool.append(elem)

            # 全局统计
            global_stats = {}
            for name, func in op_map.items():
                if name == "mean":
                    global_stats["mean"] = calc_mean(numeric_pool)
                elif name == "std":
                    global_stats["std"] = calc_std(numeric_pool)
                elif numeric_pool:  # 适用于 sum/max/min/count
                    global_stats[name] = func(numeric_pool)

            # 各类型统计
            per_type = {}
            for tname, items in type_buckets.items():
                entry = {"count": len(items)}
                if items and isinstance(items[0], NUMERIC_TYPES):
                    entry.update(
                        sum=sum(items),
                        min=min(items),
                        max=max(items),
                        mean=calc_mean(items),
                        std=calc_std(items),
                    )
                per_type[tname] = entry

            # 返回结构
            return {
                "statistics": global_stats,
                "by_type": per_type,
                "samples": numeric_pool[:10],   # 最多展示前 10 个数值样本
            }
        return wrapper
    return decorator


###############################################################################
# 随机数据生成核心
###############################################################################

def _gen_primitive(key: str, rule: Dict[str, Any]) -> Iterable[Any]:
    """根据 key 生成基本类型数据"""
    n = rule.get("num", 1)

    if key == "int":
        lo, hi = rule["datarange"]
        for _ in range(n):
            yield random.randint(lo, hi)

    elif key == "float":
        lo, hi = rule["datarange"]
        prec = rule.get("precision")
        for _ in range(n):
            val = random.uniform(lo, hi)
            yield round(val, prec) if prec is not None else val

    elif key == "str":
        alphabet = rule.get("datarange", string.ascii_letters)
        length = rule.get("len", 5)
        for _ in range(n):
            yield "".join(random.choice(alphabet) for _ in range(length))

    elif key == "bool":
        for _ in range(n):
            yield random.choice([True, False])

    elif key == "choice":
        options = rule["options"]
        for _ in range(n):
            yield random.choice(options)

    else:
        raise ValueError(f"Unsupported primitive type: {key}")

def _gen_container(key: str, rule: Dict[str, Any]) -> Iterable[Any]:
    """根据 key 生成容器类型数据；输出扁平的叶子元素"""
    n = rule.get("num", 1)

    if key in {"list", "tuple", "set"}:
        for _ in range(n):
            # 逐个子配置递归生成并展开
            for sub_key, sub_rule in rule.items():
                if sub_key == "num":
                    continue
                for item in generate({sub_key: sub_rule}):
                    yield item

    elif key == "dict":
        for _ in range(n):
            for sub_key, mapping in rule.items():
                if sub_key == "num":
                    continue
                # mapping 需包含 'key' 与 'value'
                keys = list(generate(mapping["key"]))
                vals = list(generate(mapping["value"]))
                for k, v in zip(keys, vals):
                    if isinstance(v, NUMERIC_TYPES):  # 只保留数值 value
                        yield v
    else:
        raise ValueError(f"Unsupported container type: {key}")

def generate(schema: Dict[str, Any]) -> Generator[Any, None, None]:
    """主递归生成器：接受单键 schema，产出叶子数据"""
    if len(schema) != 1:
        raise ValueError("schema must contain exactly one root key")
    key, rule = next(iter(schema.items()))

    if key in BASE_KEYS:
        yield from _gen_primitive(key, rule)
    elif key in CONTAINER_KEYS:
        yield from _gen_container(key, rule)
    else:
        raise ValueError(f"Unknown schema key: {key}")


###############################################################################
# 对外采样接口
###############################################################################

@with_statistics(sum, max, min, calc_mean, calc_std, len)
def sampling(**schemas):
    """按用户传入的多项 schema 依次采样"""
    for k, v in schemas.items():
        yield from generate({k: v})


###############################################################################
# 示例运行
###############################################################################
if __name__ == "__main__":
    # 示例 1：扁平元组
    print("示例 1：扁平元组")
    res1 = sampling(
        tuple={
            "num": 100,
            "int":   {"num": 2, "datarange": (0, 1000)},
            "float": {"num": 2, "datarange": (0.0, 1000.0)},
            "str":   {"num": 3, "datarange": string.ascii_letters, "len": 5},
        }
    )
    print(res1)

    # 示例 2：嵌套元组
    print("\n示例 2：嵌套元组")
    res2 = sampling(
        tuple={
            "num": 50,
            "tuple": {
                "num": 3,
                "int":   {"num": 2, "datarange": (1, 100)},
                "float": {"num": 2, "datarange": (1.0, 100.0), "precision": 2},
            },
        }
    )
    print(res2)

    # 示例 3：列表混合
    print("\n示例 3：列表混合")
    res3 = sampling(
        list={
            "num": 1,
            "int":   {"num": 10, "datarange": (1, 10)},
            "bool":  {"num": 5},
            "choice": {"num": 3, "options": [10, 20, 30, 40, 50]},
        }
    )
    print(res3)
