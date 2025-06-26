import random
import string

class RandomGenerator:
    def __init__(self):
        pass

    def gen_str(self, data):
        length = data.get('len', 8)
        datarange = data.get('datarange', string.ascii_letters + string.digits)
        return ''.join(random.choice(datarange) for _ in range(length))

    def gen_int(self, data):
        datarange = data.get('datarange', [0, 100])
        return random.randint(datarange[0], datarange[1])

    def gen_float(self, data):
        datarange = data.get('datarange', [0.0, 1.0])
        return round(random.uniform(datarange[0], datarange[1]), 2)

    def gen_list(self, data):
        size = data.get('size', 1)
        elements = data.get('elements', [{'type': 'int', 'datarange': [0, 10]}])
        result = []
        for _ in range(size):
            elem_template = random.choice(elements)
            result.append(self._generate_element(elem_template))
        return result

    def gen_dict(self, data):
        keys = data.get('keys', {})
        return {k: self._generate_element(v) for k, v in keys.items()}

    def gen_tuple(self, data):
        datarange = data.get('datarange', ())
        return tuple(self._generate_element(item) for item in datarange)

    def _generate_element(self, template):
        if isinstance(template, dict):
            if 'type' not in template:
                # 假设是字典模板
                return {k: self._generate_element(v) for k, v in template.items()}
            type_name = template['type']
            if type_name not in ['str', 'int', 'float', 'list', 'dict', 'tuple']:
                raise ValueError(f"Unsupported type: {type_name}")
            func = getattr(self, f"gen_{type_name}")
            return func(template)
        elif isinstance(template, list):
            return [self._generate_element(item) for item in template]
        elif isinstance(template, tuple):
            return tuple(self._generate_element(item) for item in template)
        else:
            return None

    def generate(self, struct):
        result = []
        num = struct.get('num', 1)
        for _ in range(num):
            sample = []
            for key, value in struct.items():
                if key == 'num':
                    continue
                sample.append(self._generate_element(value))
            result.append(sample)
        return result

    def main(self):
        struct = {
            'num': 100,
            'tuple': {
                'type': 'tuple',
                'datarange': (
                    {'type': 'str', 'datarange': string.ascii_uppercase, 'len': 5},
                    {'type': 'int', 'datarange': [0, 10]},
                    {'type': 'float', 'datarange': [0.0, 1.0]}
                )
            },
            'list': {
                'type': 'list',
                'size': 3,
                'elements': [
                    {'type': 'int', 'datarange': [1, 10]},
                    {'type': 'float', 'datarange': [1.0, 10.0]}
                ]
            },
            'dict': {
                'type': 'dict',
                'keys': {
                    'key1': {'type': 'int', 'datarange': [1, 10]},
                    'key2': {'type': 'float', 'datarange': [1.0, 10.0]}
                }
            }
        }

        samples = self.generate(struct)
        for i, sample in enumerate(samples, 1):
            line = ' | '.join(str(element) for element in sample)
            print(f"Sample {i}: {line}")


if __name__ == "__main__":
    generator = RandomGenerator()
    generator.main()
