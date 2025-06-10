import random
import string

def structDataSampling(num, **kwargs):
    def generate_sample(config):
        if isinstance(config, dict):
            if 'datarange' in config:
                if 'len' in config and isinstance(config['datarange'], str):
                    return ''.join(random.choice(config['datarange']) for _ in range(config['len']))
                else:
                    it = iter(config['datarange'])
                    low, high = next(it), next(it)
                    if isinstance(low, int) and isinstance(high, int):
                        return random.randint(low, high)
                    else:
                        return random.uniform(low, high)
            else:
                return {key: generate_sample(value) for key, value in config.items()}
        elif isinstance(config, list):
            return [generate_sample(item) for item in config]
        elif isinstance(config, tuple):
            return tuple(generate_sample(item) for item in config)
        else:
            return config

    for _ in range(num):
        yield generate_sample(kwargs)

def StaticRes(*metrics):
    def decorator(func):
        def wrapper(*args, **kwargs):
            samples = list(func(*args, **kwargs))
            numeric_values = []

            def collect(data):
                if isinstance(data, (int, float)):
                    numeric_values.append(data)
                elif isinstance(data, dict):
                    for value in data.values():
                        collect(value)
                elif isinstance(data, (list, tuple)):
                    for item in data:
                        collect(item)

            for sample in samples:
                collect(sample)

            result = {}
            if not numeric_values:
                return {metric: None for metric in metrics}

            if 'SUM' in metrics:
                result['SUM'] = sum(numeric_values)
            if 'AVG' in metrics:
                result['AVG'] = sum(numeric_values) / len(numeric_values)
            if 'MAX' in metrics:
                result['MAX'] = max(numeric_values)
            if 'MIN' in metrics:
                result['MIN'] = min(numeric_values)
            return result
        return wrapper
    return decorator

@StaticRes('SUM', 'AVG', 'MAX', 'MIN')
def dataSampling():
    structure = {
        "int": {"datarange": (0, 100)},
        "float": {"datarange": (0, 10000)},
        "str": {"datarange": string.ascii_uppercase, "len": 10},
        "tuple": (
            {"datarange": string.ascii_lowercase, "len": 5},
            {"datarange": (10, 20)}
        ),
        "list": [
            {"datarange": (0, 10)},
            {"datarange": "ABCDEFG", "len": 3}
        ],
        "dict": {
            "name": {"datarange": string.ascii_letters, "len": 8},
            "age": {"datarange": (18, 60)},
            "scores": {
                "math": {"datarange": (60, 100)},
                "english": {"datarange": (60, 100)}
            }
        }
    }

    return structDataSampling(1000, **structure)

if __name__ == "__main__":
    print("=== 样本统计结果 ===")
    result = dataSampling()
    for k, v in result.items():
        if isinstance(v, float):
            print(f"{k}: {v:.2f}")
        else:
            print(f"{k}: {v}")