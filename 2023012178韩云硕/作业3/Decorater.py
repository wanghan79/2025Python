import random
import string
from functools import wraps

def extract_numbers(data):
    return [x for x in data if isinstance(x, (int, float))]


def StaticRes(*stats):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            raw_data = func(**kwargs)

            numeric_data = extract_numbers(raw_data)

            result = {
                "raw_data": raw_data,
                "numeric_data": numeric_data,
                "statistics": {}
            }

            if not numeric_data:
                result["statistics"]["error"] = "No numeric data found"
                return result

            for stat in stats:
                stat = stat.upper()
                if stat == "SUM":
                    result["statistics"]["SUM"] = sum(numeric_data)
                elif stat == "AVG":
                    result["statistics"]["AVG"] = sum(numeric_data) / len(numeric_data)
                elif stat == "VAR":
                    avg = sum(numeric_data) / len(numeric_data)
                    var = sum((x - avg) ** 2 for x in numeric_data) / len(numeric_data)
                    result["statistics"]["VAR"] = var
                elif stat == "RMSE":
                    avg = sum(numeric_data) / len(numeric_data)
                    mse = sum((x - avg) ** 2 for x in numeric_data) / len(numeric_data)
                    result["statistics"]["RMSE"] = mse ** 0.5
                else:
                    raise ValueError(f"Unsupported statistic: {stat}")

            return result

        return wrapper
    return decorator


@StaticRes("sum", "avg", "var", "rmse")
def dataSampling(**kwargs):
    num_samples = kwargs.get('num_samples', 10)
    int_range = kwargs.get('int_range', (0, 100))
    float_range = kwargs.get('float_range', (0.0, 100.0))
    str_length = kwargs.get('str_length', 5)

    data = []
    for _ in range(num_samples):
        choice = random.choice(['int', 'float', 'str'])
        if choice == 'int':
            data.append(random.randint(*int_range))
        elif choice == 'float':
            data.append(round(random.uniform(*float_range), 2))
        elif choice == 'str':
            data.append(''.join(random.choices(string.ascii_letters + string.digits, k=str_length)))
    return data

result = dataSampling(
    num_samples=100,
    int_range=(1, 50),
    float_range=(0.0, 20.0),
    str_length=6
)

print("原始数据:", result["raw_data"])
print("有效数值:", result["numeric_data"])
print("统计结果:", result["statistics"])