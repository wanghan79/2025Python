import random
import string

class SimpleGenerator:
    """一个简单的随机样本生成器"""
    
    @staticmethod
    def generate_number(min_val=0, max_val=100):
        """生成随机数字"""
        return random.randint(min_val, max_val)
    
    @staticmethod
    def generate_text(length=8):
        """生成随机文本"""
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    @staticmethod
    def generate_from_list(items):
        """从列表中随机选择一项"""
        return random.choice(items)
    
    def generate_samples(self, template, count=1):
        """
        根据模板生成指定数量的样本
        
        参数:
            template: 字典，定义每个字段的生成规则
            count: 要生成的样本数量
            
        示例模板:
        {
            'age': ('number', {'min_val': 18, 'max_val': 6000}),
            'name': ('text', {'length': 6}),
            'city': ('list', {'items': ['北京', '上海', '天津', '深圳']})
        }
        """
        samples = []
        for _ in range(count):
            sample = {}
            for field, (type_, params) in template.items():
                if type_ == 'number':
                    sample[field] = self.generate_number(**params)
                elif type_ == 'text':
                    sample[field] = self.generate_text(**params)
                elif type_ == 'list':
                    sample[field] = self.generate_from_list(params['items'])
            samples.append(sample)
        return samples

# 使用示例
if __name__ == '__main__':
    # 创建生成器实例
    generator = SimpleGenerator()
    
    # 定义数据模板
    template = {
        'id': ('number', {'min_val': 1, 'max_val': 1000}),
        'name': ('text', {'length': 6}),
        'city': ('list', {'items': ['北京', '上海', '广州', '深圳']})
    }
    
    # 生成3个样本
    samples = generator.generate_samples(template, count=3)
    
    # 打印结果
    print("\n生成的随机样本：")
    for sample in samples:
        print(sample) 
