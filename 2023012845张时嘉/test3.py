import functools
import random

def generate_random_samples(num_samples, struct):
    """生成指定结构的随机样本列表"""
    samples = []
    for _ in range(num_samples):
        sample = {}
        for field, (data_type, *params) in struct.items():
            if data_type == "int":
                sample[field] = random.randint(params[0], params[1])
            elif data_type == "float":
                sample[field] = round(random.uniform(params[0], params[1]), 2)
        samples.append(sample)
    return samples

def stats_decorator(*operations):
    """
    operations: 统计操作列表，可选"SUM", "AVG", "MAX", "MIN"
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            samples = func(*args, **kwargs)
            numeric_values = []
            for sample in samples:
                for val in sample.values():
                    if isinstance(val, (int, float)):
                        numeric_values.append(val)
           
            stats_result = {}
            for op in operations:
                if op == "SUM":
                    stats_result[op] = sum(numeric_values)
                elif op == "AVG":
                    stats_result[op] = sum(numeric_values)/len(numeric_values) if numeric_values else 0
                elif op == "MAX":
                    stats_result[op] = max(numeric_values) if numeric_values else None
                elif op == "MIN":
                    stats_result[op] = min(numeric_values) if numeric_values else None
                else:
                    raise ValueError("不支持的统计操作")
            
            print(f"执行统计操作：{', '.join(operations)}")
            print(f"统计结果：{stats_result}\n")
            return samples
        return wrapper
    return stats_decorator

if __name__ == "__main__":
    @stats_decorator("SUM", "MAX")
    def generate_scores(num):
        struct = {
            "math": ("int", 0, 100),
            "english": ("float", 0.0, 100.0)
        }
        return generate_random_samples(num, struct)
    samples = generate_scores(5)
    print("生成的样本：")
    for idx, sample in enumerate(samples, 1):
        print(f"样本{idx}: {sample}")
    
    print("\n------------------------\n")

    @stats_decorator("MIN", "AVG")
    def generate_heights(num):
        struct = {
            "height": ("float", 150.0, 200.0)
        }
        return generate_random_samples(num, 3)  
