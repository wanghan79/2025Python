import random
import string
from typing import Dict, Any, Tuple, Generator, List, Callable, Optional

GENERATOR_FUNCTIONS = {
    int: lambda args: random.randint(args[0], args[1]),
    float: lambda args: round(random.uniform(args[0], args[1]), 2),
    str: lambda args: ''.join(random.choices(string.ascii_lowercase, k=args[0])),
    bool: lambda _: random.choice([True, False]),
}


def statistical_analysis(operations: List[str], fields: Optional[List[str]] = None):
    '''
    装饰器：对生成的样本进行统计分析
       operations: 操作，支持 SUM AVG MAX MIN
       fields: 需要统计的字段列表
    '''

    def decorator(func):
        def wrapper(*args, **kwargs):
            samples = list(func(*args, **kwargs))

            if not fields:
                sample_fields = samples[0].keys() if samples else []
                fields_to_analyze = [
                    field for field in sample_fields
                    if isinstance(samples[0][field], (int, float))
                ]
            else:
                fields_to_analyze = fields

            results = {}
            for field in fields_to_analyze:
                field_values = [sample[field] for sample in samples]
                field_results = {}

                for op in operations:
                    if op == 'SUM':
                        field_results['SUM'] = sum(field_values)
                    elif op == 'AVG':
                        field_results['AVG'] = sum(field_values) / len(field_values)
                    elif op == 'MAX':
                        field_results['MAX'] = max(field_values)
                    elif op == 'MIN':
                        field_results['MIN'] = min(field_values)

                results[field] = field_results

            '''
            输出统计结果
            '''
            print("\n统计结果:")
            for field, field_results in results.items():
                print(f"字段 '{field}':")
                for op, value in field_results.items():
                    print(f"  {op}: {value}")

            return samples

        return wrapper

    return decorator


def generate_random_sample(structure: Dict[str, Tuple[type, tuple]]) -> Dict[str, Any]:
    return {
        field: GENERATOR_FUNCTIONS[datatype](args)
        for field, (datatype, args) in structure.items()
    }


@statistical_analysis(operations=['SUM', 'AVG', 'MAX', 'MIN'])
def sample_generator(sample_count: int, structure: Dict[str, Tuple[type, tuple]]) -> Generator[
    Dict[str, Any], None, None]:
    for _ in range(sample_count):
        yield generate_random_sample(structure)


if __name__ == "__main__":
    '''
    定义样本结构
    '''
    SAMPLE_STRUCTURE = {
        "structure1": (int, (10, 100)),
        "structure2": (float, (1.5, 2.0)),
        "structure3": (str, (15,)),
        "structure4": (bool, ()),
    }

    '''
    定义样本数量
    '''
    SAMPLE_COUNT = 5

    samples = sample_generator(SAMPLE_COUNT, SAMPLE_STRUCTURE)
