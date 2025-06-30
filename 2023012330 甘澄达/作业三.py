import functools
from typing import List, Dict, Any, Callable, Optional, Union


def stats_operations(*stat_ops: str, fields: Optional[List[str]] = None):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 调用原始函数生成样本
            samples = func(*args, **kwargs)

            if not samples or not isinstance(samples, list):
                return samples

            # 如果没有指定字段，则自动检测所有数值字段
            target_fields = fields if fields else _detect_numeric_fields(samples[0])

            # 执行统计操作
            statistics = {}
            for field in target_fields:
                field_stats = {}
                values = [sample[field] for sample in samples if
                          field in sample and isinstance(sample[field], (int, float))]

                if not values:
                    continue

                if 'SUM' in stat_ops:
                    field_stats['SUM'] = sum(values)
                if 'AVG' in stat_ops:
                    field_stats['AVG'] = sum(values) / len(values)
                if 'MAX' in stat_ops:
                    field_stats['MAX'] = max(values)
                if 'MIN' in stat_ops:
                    field_stats['MIN'] = min(values)

                statistics[field] = field_stats

            # 打印统计结果
            print("\n=== 统计结果 ===")
            for field, stats in statistics.items():
                print(f"\n字段: {field}")
                for op, value in stats.items():
                    print(f"{op}: {value:.2f}" if isinstance(value, float) else f"{op}: {value}")

            return samples

        return wrapper

    return decorator


def _detect_numeric_fields(sample: Dict[str, Any]) -> List[str]:
    return [k for k, v in sample.items() if isinstance(v, (int, float))]


# 修改后的RandomSampleGenerator类，添加统计功能
class RandomSampleGenerator:
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)

    # ... (保留原有的所有方法)

    @stats_operations('SUM', 'AVG', 'MAX', 'MIN')
    def generate_samples_with_stats(self, schema: Dict[str, Any], count: int = 1) -> List[Dict[str, Any]]:
        return self.generate_samples(schema, count)

    @stats_operations('AVG', 'MAX', fields=['price', 'score'])
    def generate_samples_with_selected_stats(self, schema: Dict[str, Any], count: int = 1) -> List[Dict[str, Any]]:
        return self.generate_samples(schema, count)
