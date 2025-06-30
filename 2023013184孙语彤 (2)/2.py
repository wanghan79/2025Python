import random
from typing import Dict, Tuple, Any, Iterable, Generator


def sample_generator(
        n: int,
        schema: Dict[str, Tuple[str, Tuple[Any, Any]]]
) -> Generator[Dict[str, Any], None, None]:

    for _ in range(n):
        record = {}
        for field, (ftype, param) in schema.items():
            if ftype == "int":
                low, high = param
                record[field] = random.randint(low, high)
            elif ftype == "float":
                low, high = param
                record[field] = random.uniform(low, high)
            elif ftype == "choice":
                record[field] = random.choice(param)
            else:
                raise ValueError(f"不支持的字段类型：{ftype}")
        yield record


# ----------------------------- DEMO -----------------------------
if __name__ == "__main__":
    demo_schema = {
        "age": ("int", (18, 60)),
        "score": ("float", (0.0, 100.0)),
        "gender": ("choice", ("M", "F")),
    }
    for rec in sample_generator(5, demo_schema):
        print(rec)
