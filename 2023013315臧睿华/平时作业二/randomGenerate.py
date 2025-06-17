# coding:utf-8
"""
  Author:  臧睿华
  Purpose: 使用生成器生成随机样本
  Created: 27/5/2025
"""
import random
import string

def structDataSampling(**kwargs):
    result = list()
    num = kwargs['num'] if 'num' in kwargs else 1
    for index in range(num):
        res = list()
        for k, v in kwargs.items():
            if k == 'num':
                continue
            elif k == 'dict':
                elem = dict()
                elem[random.randint(0, 10)] = random.randint(10, 50)
                res.append(elem)
            elif k == 'list':
                # 对于列表类型，调用自身并收集结果
                sublist = structDataSampling(**v)
                for item in sublist:
                    res.append(item)
            elif k == 'tuple':
                # 对于元组类型，同样调用自身并将结果转换为元组
                subtuples = structDataSampling(**v)
                res.append(tuple(subtuples))
            elif k == 'int':
                it = iter(v['datarange'])
                res.append(random.randint(next(it), next(it)))
            elif k == 'float':
                it = iter(v['datarange'])
                res.append(random.uniform(next(it), next(it)))
            elif k == 'str':
                datarange, length = v['datarange'], v['len']
                s = ''.join(random.choice(datarange) for _ in range(length))
                res.append(s)
            else:
                continue
            
        yield res


struct = {'num': 3, 'tuple': {'str': {"datarange": string.ascii_uppercase, "len": 10}}, 
          'list': {'num': 2, 'int': {"datarange": (0, 10)}, 'float': {"datarange": (0, 1.0)}}, 'dict': {}}

# 调用函数
for sample in structDataSampling(**struct):
    print(sample)