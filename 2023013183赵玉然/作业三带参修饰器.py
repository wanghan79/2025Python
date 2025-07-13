import random
from functools import wraps

def statistics_decorator(*stats):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            results = {}
            if 'SUM' in stats:
                results['SUM'] = sum(data)
            if 'AVG' in stats:
                results['AVG'] = sum(data) / len(data)
            if 'MAX' in stats:
                results['MAX'] = max(data)
            if 'MIN' in stats:
                results['MIN'] = min(data)
            
            # Print the results
            for stat, value in results.items():
                print(f"{stat}: {value}")
            
            # Return the original data
            return data
        return wrapper
    return decorator

# Example usage
@statistics_decorator('SUM', 'AVG', 'MAX', 'MIN')
def generate_random_samples(n, lower_bound, upper_bound):
    return [random.uniform(lower_bound, upper_bound) for _ in range(n)]

# Generate 10 random samples between 0 and 100
generate_random_samples(10, 0, 100)