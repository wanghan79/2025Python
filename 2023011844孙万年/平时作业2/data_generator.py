def data_generator(count, data_structure):
    """
    随机样本生成器
    参数:
        count: 生成样本数量
        data_structure: 描述样本结构的元组 (元素数量, 数据类型, (可选)范围)
    返回:
        生成器对象
    """
    import random
    num_elements, data_type, *range_info = data_structure
    
    for _ in range(count):
        sample = []
        for _ in range(num_elements):
            if data_type == 'int':
                low, high = range_info[0] if range_info else (0, 100)
                sample.append(random.randint(low, high))
            elif data_type == 'float':
                low, high = range_info[0] if range_info else (0.0, 1.0)
                sample.append(random.uniform(low, high))
            elif data_type == 'str':
                length = range_info[0] if range_info else 5
                sample.append(''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=length)))
        yield sample

# 使用示例
if __name__ == "__main__":
    # 生成5个样本，每个样本包含3个0-100之间的整数
    gen = data_generator(5, (3, 'int', (0, 100)))
    print("随机整数样本:")
    for sample in gen:
        print(sample)
    
    # 生成3个样本，每个样本包含2个字符串（长度4）
    gen = data_generator(3, (2, 'str', 4))
    print("\n随机字符串样本:")
    for sample in gen:
        print(sample)