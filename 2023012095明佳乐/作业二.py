import random
import string

def generate(**kwargs):
    num = kwargs.get('num', 1)
    for _ in range(num):
        res = list()
        for k, v in kwargs.items():
            if k == 'num':
                continue
            elif k =="int":
                it = iter(v['datarange'])
                res.append(random.randint(next(it), next(it)))
            elif k =="float":
                it = iter(v['datarange'])
                res.append(random.uniform(next(it), next(it)))
            elif k =="str" :
                res.append(''.join(random.SystemRandom().choice(v['datarange']) for _ in range(v['len'])))
            elif k == "dict":
                key = ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(3))
                value = random.randint(0, 100)
                res.append({key: value})
            elif k == "list":
                res.append(list(generate(**v)))
            elif k == "tuple":
                res.append(tuple(
                    generate(**v)
                ))
            else:
                continue
        yield res


def main():
    struct = {
        'num': 1,  # 设置生成一个样本进行测试
        "tuple": {
            "str": {
                "datarange": string.ascii_uppercase, 
                "len": 50
            },
            "list": {
                "int": {
                    "datarange": (0, 10)
                }, 
                "float": {
                    "datarange": (0, 1.0)
                }
            }, 
            "dict": {}
        }
    }
    
    i=0
    count=10
    while i<count:
        sample_generator=generate(**struct)
        for sample in sample_generator:
            print(sample)
        i+=1
    

main()