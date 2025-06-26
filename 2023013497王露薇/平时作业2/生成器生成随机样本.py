import random
import string

from randomGenerator import generate


def structDataSampling(**kwargs):
     result = list()
     num=kwargs.get("num",1)
     for index in range(0,num):
        element = list()
        for key,value in kwargs.items():
            if key == "num":
               continue
            if  key == "int":
                it = iter(value['datarange']) #iter()迭代器
                tmp = random.randint(next(it),next(it))#next()每次调用都会消耗一个值
                element.append(tmp)
            elif key == "float":
                it = iter(value['datarange'])
                tmp = random.uniform(next(it),next(it))
                element.append(tmp)
            elif key == "str":
                tmp = ''.join(random.SystemRandom().choice(value["datarange"]) for _ in range(value["len"]))
                element.append(tmp)
            else:
                # element.append(structDataSampling(**value))
                generated = structDataSampling(**value)
                element.extend(generated[0] if len(generated) == 1 else generated)
        result.append(element)
     return result

def apply():
    struct = {
        "num":10,
        "list":{
            "list": {
                "int": {"datarange": (0, 10)},
                "float": {"datarange": (0, 10000)}
            },
            "str": {"datarange": string.ascii_letters, "len": 10},
            "int": {"datarange": (0, 10)},
            "float": {"datarange": (0, 10000)}
        },
        "tuple":{
            "str":{"datarange":string.ascii_letters,"len":10},
            "list":{
                "int":{"datarange":(0,10)},
                "float":{"datarange":(0,10000)}
            },
            "dict":{
                "str":{"datarange":string.ascii_letters,"len":10},
                "int":{"datarange":(0,10)}
            }
        }
    }
    result = structDataSampling(**struct)
    for item in result:
        print(item)
apply()