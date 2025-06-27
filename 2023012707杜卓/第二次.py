import random
import string

def generateRandomData(sample_count, **kwargs):

    def getData(**kwargs):
        result = list()
        for key, value in kwargs['subs'].items():
            if value['datatype'] is int:
                it = iter(value['datarange'])
                item = random.randint(next(it), next(it))
            elif value['datatype'] is float:
                it = iter(value['datarange'])
                item = random.uniform(next(it), next(it))
            elif value['datatype'] is str:
                item = ''.join(random.SystemRandom().choice(value['datarange']) for _ in range(0,10))
            elif value['datatype'] is tuple:
                list_tuple = getData(**value)
                item = tuple(list_tuple)
            elif value['datatype'] is list:
                item = getData(**value)
            elif value['datatype'] is set:
                list_set = getData(**value)
                item = set(list_set)
            elif value['datatype'] is dict:
                dict_data = {}
                for _ in range(random.randint(1, 5)):
                    key = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
                    value = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                    dict_data[key] = value
                item = dict_data
            else:
                getData(**value)
            result.append(item)
        return kwargs['datatype'](result)
    

    for _ in range(sample_count):
        yield getData(**kwargs)


def myInput():

    while True:
        try:
            count = int(input("请输入需要获取的样本组数: "))
            if count <= 0:
                print("样本数量必须是正整数，请重新输入。")
            else:
                return count
        except ValueError:
            print("输入无效，请输入一个整数。")

def printResult(samples):

    for i, sample in enumerate(samples, 1):
        print(f"样本 {i}: {sample}")


dataStructure = {
    "datatype": tuple,
    "subs": {
        "sub1": {
            "datatype": list,
            "subs": {
                "sub1": {
                    "datatype": int,
                    "datarange": (0, 100)
                },
                "sub2": {
                    "datatype": float,
                    "datarange": (0, 5000)
                }
            },
        },
        "sub2": {
            "datatype": str,
            "datarange": string.ascii_uppercase
        },
        "sub3": {
            "datatype": dict
        }
    }
}


if __name__ == "__main__":
    count = myInput()
    samples = generateRandomData(count, **dataStructure)
    printResult(samples)