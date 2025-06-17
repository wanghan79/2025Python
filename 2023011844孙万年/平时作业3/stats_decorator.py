def stats_decorator(*operations):
    """
    带参数统计修饰器
    参数:
        operations: 统计操作列表 (支持 'SUM','AVG','MAX','MIN')
    返回:
        装饰器函数
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            for data in func(*args, **kwargs):
                results = {}
                if 'SUM' in operations:
                    results['SUM'] = sum(data)
                if 'AVG' in operations:
                    results['AVG'] = sum(data) / len(data)
                if 'MAX' in operations:
                    results['MAX'] = max(data)
                if 'MIN' in operations:
                    results['MIN'] = min(data)
                yield data, results
        return wrapper
    return decorator

# 使用示例
if __name__ == "__main__":
    # 应用装饰器
    @stats_decorator('SUM', 'AVG', 'MAX', 'MIN')
    def decorated_generator(count, structure):
        return data_generator(count, structure)
    
    print("带统计的生成器:")
    gen = decorated_generator(3, (4, 'int', (1, 10)))
    for data, stats in gen:
        print(f"数据: {data}")
        print(f"统计: {stats}\n")