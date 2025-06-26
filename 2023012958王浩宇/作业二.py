import random
import string

def produce_data(**kwargs):
    quantity = kwargs.get('quantity', 1)
    for _ in range(quantity):
        result = []
        for key, value in kwargs.items():
            if key == 'quantity':
                continue
            elif key == "integer":
                bounds = iter(value['limits'])
                result.append(random.randint(next(bounds), next(bounds)))
            elif key == "floating":
                bounds = iter(value['limits'])
                result.append(random.uniform(next(bounds), next(bounds)))
            elif key == "string":
                result.append(''.join(random.choice(value['limits']) for _ in range(value['length'])))
            elif key == "dictionary":
                key_name = ''.join(random.choice(string.ascii_letters) for _ in range(3))
                key_value = random.randint(0, 100)
                result.append({key_name: key_value})
            elif key in ("array", "sequence"):
                nested_data = list(produce_data(**value))
                result.append(nested_data if key == "array" else tuple(nested_data))
        yield result


def run():
    structure = {
        'quantity': 1,
        "sequence": {
            "string": {
                "limits": string.ascii_uppercase,
                "length": 50
            },
            "array": {
                "integer": {
                    "limits": (0, 10)
                },
                "floating": {
                    "limits": (0, 1.0)
                }
            },
            "dictionary": {}
        }
    }
    
    iterations = 10
    for _ in range(iterations):
        data_generator = produce_data(**structure)
        for data in data_generator:
            print(data)


if __name__ == "__main__":
    run()