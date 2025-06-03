import random

def stats(*operations):
    def decorator(func):
        def wrapper(*args, **kwargs):
            samples = func(*args, **kwargs)
            print(f"样本: {samples}")
            results = {}
            if 'SUM' in operations:
                results['SUM'] = sum(samples)
            if 'AVG' in operations:
                results['AVG'] = sum(samples) / len(samples)
            if 'MAX' in operations:
                results['MAX'] = max(samples)
            if 'MIN' in operations:
                results['MIN'] = min(samples)
            print("统计结果:")
            for op, value in results.items():
                print(f"{op}: {value}")
            return samples
        return wrapper
    return decorator

@stats('SUM', 'AVG', 'MAX', 'MIN')
def generate_samples(n):
    return [random.randint(1, 100) for _ in range(n)]

generate_samples(5)
