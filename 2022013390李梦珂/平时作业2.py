import random
import string


def random_sample_generator(num_samples, template):
    """
    随机样本生成器

    参数:
        num_samples: 需要生成的样本数量
        template: 样本的结构模板，是一个字典，键为字段名，值为字段类型
                  支持的字段类型有：
                  - 'int': 随机整数
                  - 'float': 随机浮点数
                  - 'str': 随机字符串（长度为随机 5-10 个字符）
                  - 'bool': 随机布尔值
                  - 'list': 随机列表（长度为随机 3-5 个随机整数）
                  - 'custom': 自定义函数，用于生成特定类型的值

    返回:
        生成器，逐个生成符合模板的随机样本
    """
    for _ in range(num_samples):
        sample = {}
        for field, field_type in template.items():
            if field_type == 'int':
                sample[field] = random.randint(0, 100)  # 随机整数
            elif field_type == 'float':
                sample[field] = random.uniform(0, 100)  # 随机浮点数
            elif field_type == 'str':
                sample[field] = ''.join(random.choices(string.ascii_letters, k=random.randint(5, 10)))  # 随机字符串
            elif field_type == 'bool':
                sample[field] = random.choice([True, False])  # 随机布尔值
            elif field_type == 'list':
                sample[field] = [random.randint(0, 100) for _ in range(random.randint(3, 5))]  # 随机列表
            elif callable(field_type):
                sample[field] = field_type()  # 自定义函数生成值
            else:
                raise ValueError(f"不支持的字段类型: {field_type}")
        yield sample


def custom_field_generator():
    """自定义字段生成器示例"""
    return random.choice(['apple', 'banana', 'cherry'])


def main():
    # 由调用者输入样本数量和结构
    num_samples = int(input("请输入随机样本的数量: "))
    print("请输入样本的结构模板（格式为字段名:字段类型，多个字段用逗号分隔）：")
    print("支持的字段类型: int, float, str, bool, list, custom")
    template_input = input("例如：id:int,name:str,age:int\n请输入模板: ")

    # 解析模板输入
    template = {}
    for item in template_input.split(","):
        field, field_type = item.split(":")
        if field_type == "custom":
            template[field] = custom_field_generator  # 将自定义字段生成器绑定到字段
        else:
            template[field] = field_type

    # 使用生成器生成随机样本
    generator = random_sample_generator(num_samples, template)

    # 打印生成的样本
    print(f"\n生成 {num_samples} 个随机样本：")
    for sample in generator:
        print(sample)


if __name__ == "__main__":
    main()