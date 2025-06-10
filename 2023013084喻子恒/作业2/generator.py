import random
from typing import Dict, Any, Iterator, Union


def data_generator(kwargs: Dict[ str, Any ]) -> Iterator[ Union[ list, tuple, dict, int, float, str ] ]:
# 使用生成器生成随机数据
    num = kwargs.get('num', 1)

    for _ in range(num):
        resp = []
        for key, value in kwargs.items():
            if key == 'num':
                continue

            if key is int:
                start, end = iter(value[ 'datarange' ])
                resp.append(random.randint(start, end))
            elif key is float:
                start, end = iter(value[ 'datarange' ])
                resp.append(random.uniform(start, end))
            elif key is str:
                chars = value[ 'datarange' ]
                length = value[ 'len' ]
                tmp = ''.join(random.SystemRandom().choice(chars) for _ in range(length))
                resp.append(tmp)
            elif key is dict:
                dictionary = {random.SystemRandom(): random.choice(value[ 'datarange' ])}
                resp.append(dictionary)
            elif key is list:
                resp.append(list(data_generator(value)))
            elif key is tuple:
                resp.append(tuple(data_generator(value)))

        yield resp


def create(kwargs: Dict[ str, Any ], limit: int = None) -> Iterator[ Union[ list, tuple, dict, int, float, str ] ]:
# 创建生成器，可控制生成数量
    num = kwargs.get('num', 1)
    if limit is not None:
        num = min(num, limit)

    kwargs[ 'num' ] = num
    return data_generator(kwargs)

    # 定义数据生成规则
sample_kwargs = {
    'num': 10000,
    int: {
        'datarange': (1, 100)
        },
    float: {
        'datarange': (1.0, 100.0)
    },
    str: {
        'datarange': 'abcdefghijklmnopqrstuvwxyz',
        'len': 5
    },
    list: {
        'num': 3,
        int: {
            'datarange': (10, 20)
        }
    }
}

# 使用生成器创建数据
data_gen = create(sample_kwargs)

count = 0
for item in data_gen:
    print(item)
    # 处理每条数据
    count += 1
    if count % 10000 == 0:
        print(f"已生成 {count:,} 条数据")

print(f"总共生成 {count:,} 条数据")
