from typing import Callable, Iterable, Dict, Any


def stats(*operations: str):
    legal = {"SUM", "AVG", "MAX", "MIN"}
    ops = {op.upper() for op in operations}
    if not ops.issubset(legal):
        raise ValueError(f"operations 只能取 {legal}")

    def decorator(func: Callable[..., Iterable[Dict[str, Any]]]):
        def wrapper(*args, **kwargs):
            samples = list(func(*args, **kwargs))
            if not samples:
                print("[统计] 空样本")
                return samples

            # 只统计数字字段
            numeric_keys = [k for k, v in samples[0].items() if isinstance(v, (int, float))]
            result = {k: {} for k in numeric_keys}

            for k in numeric_keys:
                col = [s[k] for s in samples]
                if "SUM" in ops:
                    result[k]["SUM"] = sum(col)
                if "AVG" in ops:
                    result[k]["AVG"] = sum(col) / len(col)
                if "MAX" in ops:
                    result[k]["MAX"] = max(col)
                if "MIN" in ops:
                    result[k]["MIN"] = min(col)

            # 打印
            print("=== 统计结果 ===")
            for k, metrics in result.items():
                parts = [f"{name}={val:.3f}" if isinstance(val, float) else f"{name}={val}"
                         for name, val in metrics.items()]
                print(f"{k}: " + ", ".join(parts))
            return samples

        return wrapper

    return decorator


if __name__ == "__main__":
    import random


    @stats("SUM", "AVG")
    def fake_samples(n):
        return ({"x": random.randint(0, 10), "y": random.uniform(0, 1)} for _ in range(n))


    data = list(fake_samples(5))
    print("Data preview:", data)
