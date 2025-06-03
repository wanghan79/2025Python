
import random

def sample_generator(sample_num, sample_structure):
    for _ in range(sample_num):
        sample = {}
        for key, (datatype, args) in sample_structure.items():
            if datatype == int:
                sample[key] = random.randint(*args)
            elif datatype == float:
                sample[key] = round(random.uniform(*args), 2)
            elif datatype == str:
                sample[key] = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=args[0]))
        yield sample

def str_to_type(type_str):
    if type_str == "int":
        return int
    elif type_str == "float":
        return float
    elif type_str == "str":
        return str
    else:
        raise ValueError("不支持的类型: " + type_str)

if __name__ == "__main__":
    sample_num = int(input("请输入样本数量: "))
    field_count = int(input("请输入字段个数: "))

    structure = {}
    for i in range(field_count):
        name = input(f"字段{i+1}名称: ")
        type_str = input(f"字段{i+1}类型（int/float/str）: ")
        data_type = str_to_type(type_str)
        param_input = input(f"字段{i+1}参数（例如：int/float是1,100；str是5）: ")

        if data_type in [int, float]:
            args = tuple(map(eval, param_input.strip().split(',')))
        elif data_type == str:
            args = (int(param_input.strip()),)
        else:
            raise ValueError("未识别的数据类型")

        structure[name] = (data_type, args)

    for sample in sample_generator(sample_num, structure):
        print(sample)
