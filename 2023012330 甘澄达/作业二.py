import random
import string
from typing import Dict, Any, List, Union
import json
from datetime import datetime, timedelta


class RandomSampleGenerator:
    def __init__(self, seed=None):

        if seed is not None:
            random.seed(seed)

    def generate_random_value(self, field_type: str, **kwargs) -> Any:

        if field_type == 'int':
            min_val = kwargs.get('min', 0)
            max_val = kwargs.get('max', 100)
            return random.randint(min_val, max_val)

        elif field_type == 'float':
            min_val = kwargs.get('min', 0)
            max_val = kwargs.get('max', 100)
            decimal_places = kwargs.get('decimal_places', 2)
            return round(random.uniform(min_val, max_val), decimal_places)

        elif field_type == 'str':
            length = kwargs.get('length', 10)
            prefix = kwargs.get('prefix', '')
            chars = kwargs.get('chars', string.ascii_letters + string.digits)
            return prefix + ''.join(random.choice(chars) for _ in range(length))

        elif field_type == 'bool':
            return random.choice([True, False])

        elif field_type == 'date':
            start_date = kwargs.get('start_date', datetime(2000, 1, 1))
            end_date = kwargs.get('end_date', datetime(2023, 12, 31))
            delta = end_date - start_date
            random_days = random.randint(0, delta.days)
            return (start_date + timedelta(days=random_days)).date()

        elif field_type == 'datetime':
            start_date = kwargs.get('start_date', datetime(2000, 1, 1))
            end_date = kwargs.get('end_date', datetime(2023, 12, 31))
            delta = end_date - start_date
            random_seconds = random.randint(0, int(delta.total_seconds()))
            return start_date + timedelta(seconds=random_seconds)

        elif field_type == 'choice':
            choices = kwargs.get('choices', [])
            if not choices:
                raise ValueError("'choices' must be provided for 'choice' type")
            return random.choice(choices)

        elif field_type == 'array':
            item_schema = kwargs.get('item_schema', {'type': 'str'})
            min_items = kwargs.get('min_items', 1)
            max_items = kwargs.get('max_items', 5)
            num_items = random.randint(min_items, max_items)
            return [self.generate_sample(item_schema) for _ in range(num_items)]

        elif field_type == 'object':
            properties = kwargs.get('properties', {})
            return {k: self.generate_sample(v) for k, v in properties.items()}

        else:
            raise ValueError(f"Unsupported field type: {field_type}")

    def generate_sample(self, schema: Dict[str, Any]) -> Dict[str, Any]:

        if schema.get('type') != 'object':

    raise ValueError("Top level schema must be of type 'object'")

    return self.generate_random_value(**schema)


def generate_samples(self, schema: Dict[str, Any], count: int = 1) -> List[Dict[str, Any]]:
    return [self.generate_sample(schema) for _ in range(count)]


@staticmethod
def print_samples(samples: List[Dict[str, Any]], pretty: bool = True):
    indent = 2 if pretty else None
    print(json.dumps(samples, indent=indent, default=str))
