import random
import string


def generateRandomData(datatype, config):
    if datatype == "int":
        return random.randint(config["datarange"][0], config["datarange"][1])
    elif datatype == "float":
        return random.uniform(config["datarange"][0], config["datarange"][1])
    elif datatype == "str":
        datarange = config["datarange"]
        return ''.join(random.SystemRandom().choice(datarange) for _ in range(config["len"]))
    else:
        return None

def structDataSampling(num, **kwargs):
    for i in range(num):
        element = {}
        element['num'] = i + 1
        for key, value in kwargs.items():
            if isinstance(value, list):
                list_result = []
                for item in value:
                    for sub_key, sub_value in item.items():
                        list_result.append(generateRandomData(sub_key, sub_value))
                element[key] = list_result
            elif isinstance(value, tuple):
                tuple_result = tuple(
                    generateRandomData(sub_key, sub_value)
                    for sub_key, sub_value in value[0].items()
                )
                element[key] = tuple_result
            elif isinstance(value, dict):
            #同最基础版本，加入字典的空判断，防止出现递归造成输出错误
                if value:
                    element[key] = list(structDataSampling(num, **value))
                else:
                    element[key] = []
        else:
                element[key] = generateRandomData(key, value)
        yield element

result_generator = structDataSampling(
    100,
    tuple=[{'str': {'datarange': string.ascii_uppercase, 'len': 50}}],
    list=[{'int': {'datarange': (0, 10)}}, {'float': {'datarange': (0, 10)}}],
    dict={}
)

# 输出生成的数据
for item in result_generator:
    print(item)
