import random
from string import ascii_letters, ascii_uppercase, ascii_lowercase, digits
from functools import wraps

# 定义支持的统计操作类型
STAT_OPS = {
    'SUM': lambda x: sum(x),
    'AVG': lambda x: sum(x) / len(x),
    'MAX': lambda x: max(x),
    'MIN': lambda x: min(x)
}

def perform_statistical_analysis(*requested_ops):
    """
    装饰器工厂函数，用于为样本生成函数添加统计分析功能
    
    参数:
        *requested_ops: 需要执行的统计操作类型
        
    返回:
        装饰器函数
    """
    # 验证请求的操作是否有效
    invalid_ops = set(requested_ops) - set(STAT_OPS.keys())
    if invalid_ops:
        raise ValueError(f"不支持的操作类型: {invalid_ops}")

    def decorator(original_func):
        @wraps(original_func)
        def wrapped_function(*args, **kwargs):
            # 执行原始函数获取样本数据
            generated_samples = original_func(*args, **kwargs)
            
            if not generated_samples:
                return generated_samples

            # 初始化结果字典
            analysis_results = {}
            
            # 遍历样本中的每个数值字段
            for field in generated_samples[0]:
                if isinstance(generated_samples[0][field], (int, float)):
                    field_values = [s[field] for s in generated_samples]
                    
                    # 执行每个请求的统计操作
                    for operation in requested_ops:
                        result_key = f"{field}_{operation}"
                        analysis_results[result_key] = STAT_OPS[operation](field_values)

            # 输出分析报告
            if analysis_results:
                print("\n统计分析报告:")
                for metric, value in analysis_results.items():
                    print(f"{metric}: {value:.2f}" if isinstance(value, float) else f"{metric}: {value}")

            return generated_samples

        return wrapped_function

    return decorator


class DataSampleGenerator:
    def __init__(self, sample_count, data_schema):
        """
        初始化样本生成器
        
        参数:
            sample_count: 需要生成的样本数量
            data_schema: 定义数据结构模式的字典
        """
        self.sample_count = sample_count
        self.data_schema = data_schema

    def _generate_field(self, field_schema):
        """
        根据字段模式生成随机数据
        
        参数:
            field_schema: 字段定义
            
        返回:
            生成的随机数据
        """
        data_category = field_schema.get('type')
        
        if data_category == 'integer':
            value_range = field_schema.get('range', [0, 100])
            return random.randint(value_range[0], value_range[1])
            
        elif data_category == 'decimal':
            value_range = field_schema.get('range', [0.0, 100.0])
            return round(random.uniform(value_range[0], value_range[1]), 2)
            
        elif data_category == 'text':
            char_set = field_schema.get('charset', ascii_letters)
            length = field_schema.get('length', 8)
            return ''.join(random.choices(char_set, k=length))
            
        elif data_category == 'sequence':
            item_def = field_schema.get('items', [{}])
            size = field_schema.get('size', random.randint(1, 10))
            return [self._generate_field(item_def[0]) for _ in range(size)]
            
        elif data_category == 'mapping':
            fields = field_schema.get('fields', {})
            return {k: self._generate_field(v) for k, v in fields.items()}
            
        elif data_category == 'fixed_sequence':
            elements = field_schema.get('elements', [])
            return tuple(self._generate_field(e) for e in elements)
            
        return None

    def create_samples(self):
        """
        生成样本数据集合
        
        返回:
            包含所有样本的列表
        """
        result_set = []
        for _ in range(self.sample_count):
            sample = {}
            for field_name, field_def in self.data_schema.items():
                sample[field_name] = self._generate_field(field_def)
            result_set.append(sample)
        return result_set

    @classmethod
    def create_with_config(cls, sample_count, data_schema):
        """
        工厂方法，通过配置创建生成器实例
        
        参数:
            sample_count: 样本数量
            data_schema: 数据模式定义
            
        返回:
            DataSampleGenerator实例
        """
        return cls(sample_count, data_schema)


@perform_statistical_analysis('SUM', 'AVG', 'MAX', 'MIN')
def generate_data_with_analysis(sample_count, data_schema):
    """
    生成样本数据并执行统计分析
    
    参数:
        sample_count: 样本数量
        data_schema: 数据模式定义
        
    返回:
        生成的样本列表
    """
    generator = DataSampleGenerator(sample_count, data_schema)
    return generator.create_samples()


if __name__ == "__main__":
    # 定义数据结构模式
    sample_schema = {
        "numeric_value": {"type": "integer", "range": [10, 200]},
        "decimal_value": {"type": "decimal", "range": [5.0, 95.5]},
        "text_value": {"type": "text", "charset": ascii_uppercase, "length": 10},
        "item_list": {
            "type": "sequence",
            "items": [{"count": {"type": "integer", "range": [1, 15]}}],
            "size": 6
        },
        "nested_data": {
            "type": "mapping",
            "fields": {
                "id": {"type": "integer", "range": [1000, 9999]},
                "code": {"type": "text", "charset": ascii_lowercase, "length": 6}
            }
        },
        "fixed_data": {
            "type": "fixed_sequence",
            "elements": [
                {"type": "integer", "range": [5, 50]},
                {"type": "text", "charset": digits, "length": 3}
            ]
        }
    }

    # 生成样本并分析
    data_samples = generate_data_with_analysis(15, sample_schema)

    # 显示生成的样本
    print("\n生成的样本数据:")
    for idx, sample in enumerate(data_samples, 1):
        print(f"样本#{idx}: {sample}")
