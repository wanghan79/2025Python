import random
import string


def random_string(length):
    """生成随机字符串"""
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


def random_list(element_type, length=5):
    """生成随机列表"""
    if element_type == 'int':
        return [random.randint(0, 100) for _ in range(length)]
    elif element_type == 'float':
        return [round(random.uniform(0.0, 100.0), 2) for _ in range(length)]
    elif element_type == 'str':
        return [random_string(10) for _ in range(length)]
    else:
        raise ValueError(f"Unsupported list element type: {element_type}")


def random_tuple(element_types):
    """生成随机元组"""
    elements = []
    for element_type in element_types:
        if element_type == 'int':
            elements.append(random.randint(0, 100))
        elif element_type == 'float':
            elements.append(round(random.uniform(0.0, 100.0), 2))
        elif element_type == 'str':
            elements.append(random_string(10))
        else:
            raise ValueError(f"Unsupported tuple element type: {element_type}")
    return tuple(elements)


def sample_generator(sample_num, sample_structure):
    for _ in range(sample_num):
        sample = {}
        for field_name, field_info in sample_structure.items():
            if isinstance(field_info, dict):
                sample[field_name] = next(sample_generator(1, field_info))['nested']
            elif isinstance(field_info, str):
                if field_info == 'int':
                    sample[field_name] = random.randint(0, 100)
                elif field_info == 'float':
                    sample[field_name] = round(random.uniform(0.0, 100.0), 2)
                elif field_info == 'str':
                    sample[field_name] = random_string(10)
                elif field_info == 'list':
                    sample[field_name] = random_list('int')  # Default to int list
                elif field_info == 'tuple':
                    sample[field_name] = random_tuple(['int', 'float'])  # Default to mixed tuple
                else:
                    raise ValueError(f"Unsupported field type: {field_info}")
            elif isinstance(field_info, list):
                sample[field_name] = random_tuple(field_info)
            else:
                raise ValueError(f"Unsupported field info format: {field_info}")
        yield {'nested': sample}


# 使用范例
if __name__ == "__main__":
    # 定义样本结构
    structure = {
        'id': 'int',
        'value': 'float',
        'description': 'str',
        'attributes': ['int', 'float'],
        'tags': 'list',
        'info': {
            'nested_id': 'int',
            'nested_value': 'float'
        }
    }

    generator = sample_generator(5, structure)
    for sample in generator:
        print(sample['nested'])
