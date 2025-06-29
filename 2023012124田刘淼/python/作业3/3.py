import random
from functools import wraps

def statistic_decorator(operations):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            samples = func(*args, **kwargs)
            
            results = {}
            if 'SUM' in operations:
                results['SUM'] = sum(samples)
            if 'AVG' in operations:
                results['AVG'] = sum(samples) / len(samples) if samples else 0
            if 'MAX' in operations:
                results['MAX'] = max(samples) if samples else None
            if 'MIN' in operations:
                results['MIN'] = min(samples) if samples else None
            
            return results
        return wrapper
    return decorator

@statistic_decorator(operations=['SUM', 'AVG', 'MAX'])
def generate_random_samples(n=10, lower_bound=1, upper_bound=100):
    return [random.randint(lower_bound, upper_bound) for _ in range(n)]

stats = generate_random_samples(n=15)
print(stats)
