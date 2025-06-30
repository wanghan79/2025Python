import random
import string
from typing import Dict, Any, Iterator, List, Union, Tuple, Callable


def create_random_data(**kwargs: Dict[str, Any]) -> Iterator[List[Any]]:
    """创建随机数据的生成器。

    Args:
        **kwargs: 包含数据结构信息的关键字参数。

    Yields:
        包含随机数据的列表。
    """
    quantity = kwargs.get('quantity', 1)
    for _ in range(quantity):
        data = []
        for key, value in kwargs.items():
            if key == 'quantity':
                continue
            elif key == 'integer':
                data_range = iter(value['data_range'])
                data.append(random.randint(next(data_range), next(data_range)))
            elif key == 'floating_point':
                data_range = iter(value['data_range'])
                data.append(random.uniform(next(data_range), next(data_range)))
            elif key == 'string':
                data.append(''.join(random.SystemRandom().choice(value['data_range']) for _ in range(value['length'])))
            elif key == 'dictionary':
                key_str = ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(3))
                value_int = random.randint(0, 100)
                data.append({key_str: value_int})
            elif key == 'list':
                data.append(list(create_random_data(**value)))
            elif key == 'tuple':
                data.append(tuple(create_random_data(**value)))
            else:
                continue
        yield data


def main_program() -> None:
    """主程序入口，获取用户输入并生成随机样本。"""
    # 获取用户输入的样本数量
    sample_quantity = int(input("请输入要生成的样本数量："))
    print("请输入样本结构（以字典形式表示）：")
    structure = eval(input())

    # 使用生成器生成随机样本
    sample_generator = create_random_data(**structure)
    for _ in range(sample_quantity):
        sample = next(sample_generator)
        print(sample)


if __name__ == "__main__":
    main_program()