import random
import string

def dataSampling(**kwargs):
    num = kwargs.get('num', 1)
    for _ in range(num):
        res = []
        for key, value in kwargs.items():
            if key == 'num':
                continue
            elif key == 'int':
                res.append(random.randint(value['datarange'][0], value['datarange'][1]))
            elif key == 'float':
                res.append(random.uniform(value['datarange'][0], value['datarange'][1]))
            elif key == 'str':
                s = value['datarange']
                length = value['len']
                res.append(''.join(random.choices(s, k=length)))
            else:
                res.append(list(next(dataSampling(**value))))

        yield res

def output():
    struct = {
        'num': 2,
        'list': {
            'int': {"datarange": (0, 100)},
            'float': {"datarange": (0, 10.0)},
            'str': {"datarange": string.ascii_lowercase, "len": 5}
        },
        'tuple': {
            'tuple': {
                'float': {"datarange": (0, 1.0)},
                'dict': {
                    'str': {"datarange": string.ascii_uppercase, "len": 4},
                    'int': {"datarange": (0, 100)}
                }
            }
        }
    }

    samples = dataSampling(**struct)
    print("样本输出：")
    for i, sample in enumerate(samples):
        print(f"Sample {i + 1}: {sample}")

if __name__ == '__main__':
    output()
