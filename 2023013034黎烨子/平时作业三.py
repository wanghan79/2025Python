def stats_decorator(*stats_operations):
    """
    带参修饰器，实现对随机样本生成函数的统计操作
    支持的统计操作: SUM, AVG, MAX, MIN
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            # 调用原始函数获取生成器
            generator = func(*args, **kwargs)

            # 初始化统计数据结构
            stats_data = {
                'int': [],
                'float': [],
                'str_lengths': []
            }

            # 处理生成器的每个样本
            for sample in generator:
                yield sample  # 先yield样本，保持生成器特性

                # 收集统计数据
                if 'int' in sample:
                    stats_data['int'].append(sample['int'])
                if 'float' in sample:
                    stats_data['float'].append(sample['float'])
                if 'str' in sample:
                    stats_data['str_lengths'].append(len(sample['str']))

            # 所有样本处理完成后，输出统计结果
            print("\n统计结果:")

            if 'SUM' in stats_operations:
                print("SUM统计:")
                if stats_data['int']:
                    print(f"  int总和: {sum(stats_data['int'])}")
                if stats_data['float']:
                    print(f"  float总和: {sum(stats_data['float'])}")
                if stats_data['str_lengths']:
                    print(f"  str总长度: {sum(stats_data['str_lengths'])}")
                print()

            if 'AVG' in stats_operations:
                print("AVG统计:")
                if stats_data['int']:
                    print(f"  int平均值: {sum(stats_data['int']) / len(stats_data['int'])}")
                if stats_data['float']:
                    print(f"  float平均值: {sum(stats_data['float']) / len(stats_data['float'])}")
                if stats_data['str_lengths']:
                    print(f"  str平均长度: {sum(stats_data['str_lengths']) / len(stats_data['str_lengths'])}")
                print()

            if 'MAX' in stats_operations:
                print("MAX统计:")
                if stats_data['int']:
                    print(f"  int最大值: {max(stats_data['int'])}")
                if stats_data['float']:
                    print(f"  float最大值: {max(stats_data['float'])}")
                if stats_data['str_lengths']:
                    print(f"  str最大长度: {max(stats_data['str_lengths'])}")
                print()

            if 'MIN' in stats_operations:
                print("MIN统计:")
                if stats_data['int']:
                    print(f"  int最小值: {min(stats_data['int'])}")
                if stats_data['float']:
                    print(f"  float最小值: {min(stats_data['float'])}")
                if stats_data['str_lengths']:
                    print(f"  str最小长度: {min(stats_data['str_lengths'])}")
                print()

        return wrapper

    return decorator


# 示例使用
if __name__ == "__main__":
    # 应用修饰器，指定需要SUM和AVG统计
    @stats_decorator('SUM', 'AVG', 'MAX', 'MIN')
    def decorated_generator(sample_count, sample_structure):
        return random_sample_generator(sample_count, sample_structure)


    # 定义样本结构
    sample_structure = {
        'int': (1, 100),
        'float': (0.0, 1.0),
        'str': 5
    }

    # 使用修饰后的生成器
    print("使用修饰后的生成器:")
    gen = decorated_generator(5, sample_structure)

    # 迭代生成器会先产生样本，然后输出统计结果
    for i, sample in enumerate(gen, 1):
        print(f"样本{i}: {sample}")