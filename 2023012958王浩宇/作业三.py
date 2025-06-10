import random
import string

def compute_statistics(*metrics):
    def decorator(func):
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            stats = {}
            
            if 'highest' in metrics:
                stats['highest'] = max(data)
            if 'lowest' in metrics:
                stats['lowest'] = min(data)
            if 'total' in metrics:
                stats['total'] = sum(data)
            if 'mean' in metrics:
                stats['mean'] = sum(data) / len(data)
            
            return stats
        return wrapper
    return decorator

def generate_data(**kwargs):
    count = kwargs.get('count', 1)
    results = []
    
    for _ in range(count):
        sample = []
        for data_type, config in kwargs.items():
            if data_type == 'count':
                continue
            
            if data_type == "integer":
                start, end = config['range']
                sample.append(random.randint(start, end))
            
            elif data_type == "floating":
                start, end = config['range']
                sample.append(random.uniform(start, end))
            
            elif data_type == "string":
                chars = config['range']
                length = config['length']
                sample.append(''.join(random.choices(chars, k=length)))
            
            elif data_type == "dictionary":
                key = ''.join(random.choices(string.ascii_letters, k=3))
                value = random.randint(0, 100)
                sample.append({key: value})
            
            elif data_type in ("array", "sequence"):
                nested_data = generate_data(**config)
                sample.append(nested_data if data_type == "array" else tuple(nested_data))
        
        results.append(sample if len(sample) > 1 else sample[0])
    
    return results[0] if count == 1 else results

def extract_numerical_data(data):
    def flatten(items):
        for item in items:
            if isinstance(item, (list, tuple)):
                yield from flatten(item)
            elif isinstance(item, dict):
                yield from flatten(item.values())
            elif isinstance(item, (int, float)):
                yield item
    return list(flatten([data]))

# Example data structure
data_structure = {
    'count': 5,
    "integer": {"range": (0, 100)},
    "floating": {"range": (0, 100.0)},
    "string": {
        "range": string.ascii_uppercase,
        "length": 5
    },
    "dictionary": {},
    "array": {
        "integer": {"range": (0, 10)},
        "floating": {"range": (0, 1.0)}
    }
}

if __name__ == '__main__':
    metrics = ['lowest', 'mean']
    decorated_function = compute_statistics(*metrics)(extract_numerical_data)
    generated_data = generate_data(**data_structure)
    print("Generated data:", generated_data)
    print("Statistics:", decorated_function(generated_data))