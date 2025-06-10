import random
import string

def generate(kwargs):
    num = kwargs.get('num', 1)
    result = []
    for _ in range(num):
        res = []
        for key, value in kwargs.items():
            if key == 'num':
                continue
            elif key == int:
                low, high = value['datarange']
                res.append(random.randint(low, high))
            elif key == float:
                low, high = value['datarange']
                res.append(random.uniform(low, high))
            elif key == str:
                chars, length = value['datarange'], value['len']
                res.append(''.join(random.choice(chars) for _ in range(length)))
            elif key == dict:
                # 改进：允许自定义 dict 生成方式
                key_low, key_high = value.get('key_range', (0, 10))
                val_low, val_high = value.get('val_range', (0, 10))
                res.append({
                    random.randint(key_low, key_high):
                    random.randint(val_low, val_high)
                })
            elif key == list:
                # 修正：直接生成列表，而不是嵌套列表
                sub_items = []
                for sub_key, sub_value in value.items():
                    if sub_key == int:
                        low, high = sub_value['datarange']
                        sub_items.append(random.randint(low, high))
                    elif sub_key == float:
                        low, high = sub_value['datarange']
                        sub_items.append(random.uniform(low, high))
                res.append(sub_items)
            elif key == tuple:
                # 修正：直接生成元组，而不是嵌套列表
                sub_items = []
                for sub_key, sub_value in value.items():
                    if sub_key == str:
                        chars, length = sub_value['datarange'], sub_value['len']
                        sub_items.append(''.join(random.choice(chars) for _ in range(length)))
                res.append(tuple(sub_items))
        result.append(res)
    return result

def main():
    struct = {
        'num': 3,  # 生成 3 组数据a
        int: {'datarange': (1, 100)},  # 随机整数 1-100
        float: {'datarange': (0.0, 10.0)},  # 随机浮点数 0.0-10.0
        str: {'datarange': string.ascii_uppercase, 'len': 5},  # 5位大写字母
        dict: {'key_range': (1, 5), 'val_range': (10, 20)},  # 字典 {1-5: 10-20}
        list: {
            int: {'datarange': (0, 10)},  # 列表包含一个 0-10 的整数
            float: {'datarange': (0, 100)}  # 和一个 0-100 的浮点数
        },
        tuple: {
            str: {'datarange': string.ascii_lowercase, 'len': 3}  # 元组包含一个 3 位小写字母
        }
    }
    print(generate(struct))

if __name__ == "__main__":
    main()