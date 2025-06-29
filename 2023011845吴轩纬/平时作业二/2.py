import random
import string
from csv_helper import CsvHelper
def create(kwargs):
    num = kwargs['num'] if 'num' in kwargs else 1
    for i in range(num):
        resp = list()
        for key, value in kwargs.items():
            if key == 'num':
                continue
            elif key is int:
                index = iter(value['datarange'])
                resp.append(random.randint(next(index), next(index)))
            elif key is float:
                index = iter(value['datarange'])
                resp.append(random.uniform(next(index), next(index)))
            elif key is str:
                tmp = ''.join(random.SystemRandom().choice(value['datarange']) for _ in range(value['len']))
                resp.append(tmp)
            elif key is dict:
                dictionary = dict()
                dictionary[random.SystemRandom] = random.choice(value['datarange'])
                resp.append(dictionary)
            elif key is list:
                resp.append(create(value))
            elif key is tuple:
                resp.append(tuple(create(value)))
            else:
                continue
        yield resp

def main():
    struct = {"num":10000,int: {"datarange": (0, 100)}, float: {"datarange": (0, 10000)}, str: {"datarange": string.ascii_uppercase, "len": 50}}

    generator=create(struct)
    for data in generator:
        CsvHelper.write(data,'1.csv')
if __name__ == '__main__':
    main()
