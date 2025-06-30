作业三：使用带参修饰器实现对随机样本生成函数的统计操作修饰，能够实现SUM、AVG、MAX、MIN四种统计操作的任意组合进行统计结果输出。
import random
import string
from functools import wraps
from typing import List, Dict, Any, Union, Tuple, Generator

# 带参数的修饰器：用于统计指定字段的 SUM、AVG、MAX、MIN
def stat_decorator(field_name: str, stats: List[str]):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = list(func(*args, **kwargs))  # 先获取所有生成的数据
            values = [item[field_name] for item in data if isinstance(item[field_name], (int, float))]

            print(f"\n针对字段 '{field_name}' 的统计结果：")
            if 'SUM' in stats:
                print(f"SUM = {sum(values)}")
            if 'AVG' in stats:
                print(f"AVG = {round(sum(values) / len(values), 2)}")
            if 'MAX' in stats:
                print(f"MAX = {max(values)}")
            if 'MIN' in stats:
                print(f"MIN = {min(values)}")

            return iter(data)  # 返回生成器形式
        return wrapper
    return decorator

# 随机样本生成器：结构和数量由调用者输入
@stat_decorator('score', stats=['SUM', 'AVG', 'MAX', 'MIN'])  # 自由组合统计操作
def random_sample_generator(
    field_spec: Dict[str, Union[Tuple[str, int], Tuple[str, int, int], Tuple[str, float, float], Tuple[str, List[Any]]]],
    num_samples: int
) -> Generator[Dict[str, Any], None, None]:
    for _ in range(num_samples):
        sample = {}
        for field, spec in field_spec.items():
            if spec[0] == 'int':
                sample[field] = random.randint(spec[1], spec[2])
            elif spec[0] == 'float':
                sample[field] = round(random.uniform(spec[1], spec[2]), 2)
            elif spec[0] == 'str':
                sample[field] = ''.join(random.choices(string.ascii_letters, k=spec[1]))
            elif spec[0] == 'choice':
                sample[field] = random.choice(spec[1])
            else:
                raise ValueError(f"Unsupported field type: {spec[0]}")
        yield sample

# 示例调用
if __name__ == "__main__":
    structure = {
        'id': ('int', 1000, 9999),
        'name': ('str', 6),
        'age': ('int', 18, 35),
        'score': ('float', 0.0, 100.0),
        'gender': ('choice', ['Male', 'Female'])
    }

    # 生成 5 条样本
    gen = random_sample_generator(structure, 5)

    # 输出每条样本
    for sample in gen:
        print(sample)
代码运行结果如下：
针对字段 'score' 的统计结果：
SUM = 252.48
AVG = 50.5
MAX = 99.81
MIN = 8.78
{'id': 8109, 'name': 'IoedOG', 'age': 32, 'score': 8.78, 'gender': 'Male'}
{'id': 7744, 'name': 'cwFEOk', 'age': 19, 'score': 71.25, 'gender': 'Female'}
{'id': 7597, 'name': 'NTtIVW', 'age': 27, 'score': 62.19, 'gender': 'Male'}
{'id': 2823, 'name': 'ZJFuIz', 'age': 22, 'score': 10.45, 'gender': 'Female'}
{'id': 7492, 'name': 'FAJznu', 'age': 24, 'score': 99.81, 'gender': 'Female'}
这段程序的运行结果展示了通过生成器自动生成的5条用户数据，并对字段 score（成绩）进行了统计分析。程序基于用户自定义结构，生成了包含编号、姓名、年龄、成绩和性别的随机样本数据；利用带参修饰器自动对字段 score 执行了 SUM（总和）、AVG（平均）、MAX（最大）、MIN（最小） 四种统计操作；结果显示了成绩字段的整体分布特征，同时也输出了每个样本的具体数据。
