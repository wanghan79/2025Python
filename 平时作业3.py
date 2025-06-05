def stats_decorator(*stats_ops):

    def decorator(func):
        def wrapper(*args, **kwargs):
            data = list(func(*args, **kwargs))

            results = {}

            numeric_fields = [k for k, v in data[0].items() if isinstance(v, (int, float))]

            for field in numeric_fields:
                field_values = [sample[field] for sample in data]
                field_results = {}

                if 'SUM' in stats_ops:
                    field_results['SUM'] = sum(field_values)
                if 'AVG' in stats_ops:
                    field_results['AVG'] = sum(field_values) / len(field_values)
                if 'MAX' in stats_ops:
                    field_results['MAX'] = max(field_values)
                if 'MIN' in stats_ops:
                    field_results['MIN'] = min(field_values)
                results[field] = field_results

            # 打印统计结果
            print("\n统计结果:")
            for field, stats in results.items():
                print(f"字段 {field}:")
                for op, value in stats.items():
                    print(f"  {op}: {value:.2f}" if isinstance(value, float) else f"  {op}: {value}")

            return data

        return wrapper

    return decorator

if __name__ == "__main__":
    @stats_decorator('SUM', 'AVG', 'MAX', 'MIN')
    def generate_samples():
        structure = {"id": int, "score": float, "age": int}
        generator = random_sample_generator(10, structure)
        return generator

    samples = generate_samples()

    print("\n原始数据:")
    for sample in samples:
        print(sample)
"""
    参数:
        stats_ops: 统计操作列表
"""