import random as rnd
from string import ascii_letters as letters, digits as nums
from functools import wraps

def stats_wrapper(*metrics):
    """带参装饰器工厂，配置需要的统计指标"""
    
    def decorator(original_func):
        @wraps(original_func)
        def wrapped_func(*params, **options):
            # 执行原始函数获取数据集
            dataset = original_func(*params, **options)
            
            # 初始化结果容器
            analysis_results = {m: {} for m in metrics}
            
            # 检查数据集是否为空
            if not dataset:
                print("警告：数据集为空")
                return dataset
            
            # 提取所有数值型字段 - 修复括号问题
            numeric_fields = set()
            for field in dataset[0].keys():
                # 检查该字段在所有样本中是否都是数值类型
                if all(isinstance(sample[field], (int, float)) for sample in dataset):
                    numeric_fields.add(field)
            
            # 按字段进行统计计算
            for field in numeric_fields:
                values = [entry[field] for entry in dataset]
                
                # 动态执行统计计算
                if 'SUM' in metrics:
                    analysis_results['SUM'][field] = sum(values)
                if 'AVG' in metrics:
                    analysis_results['AVG'][field] = sum(values) / len(values)
                if 'MAX' in metrics:
                    analysis_results['MAX'][field] = max(values)
                if 'MIN' in metrics:
                    analysis_results['MIN'][field] = min(values)
            
            # 输出统计报告
            print("数据分析报告：")
            for metric, result in analysis_results.items():
                if result:  # 只输出有结果的统计项
                    print(f"{metric}统计: {result}")
            
            return dataset
        
        return wrapped_func
    
    return decorator

class DataGenerator:
    """数据生成器工厂类"""
    
    TYPE_MAP = {
        "int": lambda: rnd.randint(0, 100),
        "float": lambda: round(rnd.uniform(0, 100), 2),
        "string": lambda: ''.join(rnd.choices(letters + nums, k=10)),
        "bool": lambda: rnd.choice([True, False])
    }
    
    @staticmethod
    def create_entries(entry_count, schema):
        """根据模式生成数据条目"""
        entries = []
        for _ in range(entry_count):
            entry = {}
            for field, data_type in schema.items():
                if data_type in DataGenerator.TYPE_MAP:
                    entry[field] = DataGenerator.TYPE_MAP[data_type]()
            entries.append(entry)
        return entries

# 应用装饰器
@stats_wrapper('SUM', 'AVG', 'MAX', 'MIN')
def generate_data_with_analysis(count, schema):
    """生成数据并执行分析"""
    return DataGenerator.create_entries(count, schema)

# 使用示例
if __name__ == "__main__":
    # 定义数据结构
    data_schema = {
        "id": "int",
        "username": "string",
        "years": "int",
        "rating": "float",
        "is_verified": "bool"
    }

    # 生成10个样本并分析
    generate_data_with_analysis(10, data_schema)