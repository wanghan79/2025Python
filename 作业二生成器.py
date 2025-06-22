import random
def random_sample_generator(sample_size, num_samples, value_range):
    for _ in range(num_samples):
        sample = [random.randint(value_range[0], value_range[1]) for _ in range(sample_size)]
        yield sample

# 输入参数
sample_size = int(input("请输入每个样本的大小："))
num_samples = int(input("请输入需要生成的样本数量："))
value_range_start = int(input("请输入随机值范围的起始值："))
value_range_end = int(input("请输入随机值范围的结束值："))

generator = random_sample_generator(sample_size, num_samples, (value_range_start, value_range_end))
print("\n生成的随机样本如下：")
for i, sample in enumerate(generator):
    print(f"样本 {i + 1}: {sample}")