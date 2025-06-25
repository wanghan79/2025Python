import random
def stats_decorator(*operations):
    def decorator(func):
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            results = {}
            for op in operations:
                if op == 'SUM':
                    results['SUM'] = sum(data)
                elif op == 'AVG':
                    results['AVG'] = sum(data) / len(data)
                elif op == 'MAX':
                    results['MAX'] = max(data)
                elif op == 'MIN':
                    results['MIN'] = min(data)
            return results
        return wrapper
    return decorator

# 范例
@stats_decorator('SUM', 'AVG', 'MAX')
def generate_scores(n):
    return [random.randint(0, 100) for _ in range(n)]

print(generate_scores(10))
