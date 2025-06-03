def stat_decorator(*stats):
    def decorator(func):
        def wrapper(*args, **kwargs):
            data = list(func(*args, **kwargs))
            result = {}
            if 'SUM' in stats:
                result['SUM'] = sum(data)
            if 'AVG' in stats:
                result['AVG'] = sum(data) / len(data) if data else 0
            if 'MAX' in stats:
                result['MAX'] = max(data)
            if 'MIN' in stats:
                result['MIN'] = min(data)
            print("原始数据： ", data)
            print("统计结果：", result)
            return data
        return wrapper
    return decorator

@stat_decorator('SUM', 'AVG', 'MAX', 'MIN')
def generate_numbers(n):
    import random
    return (random.randint(1, 100) for _ in range(n))

if __name__ == "__main__":
    generate_numbers(10)
