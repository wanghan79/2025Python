import random
from typing import Any, Dict, List, Union, Callable


class RandomSampleGenerator:
    """随机样本生成器，支持多种数据类型和嵌套结构的随机样本生成"""
    
    def __init__(self):
        """初始化生成器，注册基本类型生成器"""
        self.type_generators = {
            'int': self._generate_int,
            'float': self._generate_float,
            'str': self._generate_str,
            'bool': self._generate_bool,
            'list': self._generate_list,
            'dict': self._generate_dict,
            'tuple': self._generate_tuple
        }
    
    def generate_sample(self, config: Dict[str, Any]) -> Any:
        """
        根据配置生成单个随机样本
        
        参数:
            config: 样本配置字典，必须包含'type'字段指定类型
            
        返回:
            生成的随机样本
            
        异常:
            ValueError: 当遇到不支持的类型时抛出
        """
        sample_type = config.get('type')
        if sample_type not in self.type_generators:
            raise ValueError(f"不支持的类型: {sample_type}")
            
        return self.type_generators[sample_type](config)
    
    def generate_samples(self, count: int, config: Dict[str, Any]) -> List[Any]:
        """
        生成多个随机样本
        
        参数:
            count: 要生成的样本数量
            config: 单个样本的配置
            
        返回:
            包含所有生成样本的列表
        """
        return [self.generate_sample(config) for _ in range(count)]
    
    # 基本类型生成器
    def _generate_int(self, config: Dict[str, Any]) -> int:
        """生成随机整数"""
        min_val = config.get('min', 0)
        max_val = config.get('max', 100)
        return random.randint(min_val, max_val)
    
    def _generate_float(self, config: Dict[str, Any]) -> float:
        """生成随机浮点数"""
        min_val = config.get('min', 0.0)
        max_val = config.get('max', 100.0)
        decimal = config.get('decimal', 2)
        return round(random.uniform(min_val, max_val), decimal)
    
    def _generate_str(self, config: Dict[str, Any]) -> str:
        """生成随机字符串"""
        chars = config.get('chars', 'abcdefghijklmnopqrstuvwxyz0123456789')
        length = config.get('length', 8)
        return ''.join(random.choices(chars, k=length))
    
    def _generate_bool(self, config: Dict[str, Any]) -> bool:
        """生成随机布尔值"""
        return random.choice([True, False])
    
    # 容器类型生成器
    def _generate_list(self, config: Dict[str, Any]) -> List[Any]:
        """生成随机列表"""
        element_config = config.get('element', {'type': 'int'})
        length = config.get('length', random.randint(1, 5))
        return [self.generate_sample(element_config) for _ in range(length)]
    
    def _generate_dict(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """生成随机字典"""
        fields = config.get('fields', {})
        return {key: self.generate_sample(value_config) for key, value_config in fields.items()}
    
    def _generate_tuple(self, config: Dict[str, Any]) -> tuple:
        """生成随机元组"""
        elements = config.get('elements', [{'type': 'int'}])
        return tuple(self.generate_sample(element) for element in elements)


def interactive_generator_demo():
    """交互式生成器演示，通过命令行获取用户输入并生成样本"""
    generator = RandomSampleGenerator()
    print("随机样本生成器演示")
    print("=" * 50)
    
    while True:
        print("\n请选择操作:")
        print("1: 生成简单类型样本")
        print("2: 生成列表样本")
        print("3: 生成字典样本")
        print("4: 生成嵌套结构样本")
        print("5: 退出演示")
        
        choice = input("请输入选项 (1-5): ")
        
        if choice == '5':
            print("\n演示结束!")
            break
            
        count = int(input("请输入要生成的样本数量: "))
        
        if choice == '1':
            # 简单类型生成
            print("\n选择简单类型:")
            print("1: 整数")
            print("2: 浮点数")
            print("3: 字符串")
            print("4: 布尔值")
            
            type_choice = input("请输入类型选项 (1-4): ")
            config = {}
            
            if type_choice == '1':
                config = {
                    'type': 'int',
                    'min': int(input("最小值: ")),
                    'max': int(input("最大值: "))
                }
            elif type_choice == '2':
                config = {
                    'type': 'float',
                    'min': float(input("最小值: ")),
                    'max': float(input("最大值: ")),
                    'decimal': int(input("小数位数 (默认2): ") or 2)
                }
            elif type_choice == '3':
                chars = input("字符集 (默认为a-z0-9): ") or 'abcdefghijklmnopqrstuvwxyz0123456789'
                config = {
                    'type': 'str',
                    'chars': chars,
                    'length': int(input("长度 (默认8): ") or 8)
                }
            elif type_choice == '4':
                config = {'type': 'bool'}
            else:
                print("无效选项!")
                continue
                
        elif choice == '2':
            # 列表生成
            print("\n配置列表:")
            element_type = input("元素类型 (int/float/str/bool): ")
            element_config = {}
            
            if element_type == 'int':
                element_config = {
                    'type': 'int',
                    'min': int(input("最小值: ")),
                    'max': int(input("最大值: "))
                }
            elif element_type == 'float':
                element_config = {
                    'type': 'float',
                    'min': float(input("最小值: ")),
                    'max': float(input("最大值: "))
                }
            elif element_type == 'str':
                chars = input("字符集 (默认a-z0-9): ") or 'abcdefghijklmnopqrstuvwxyz0123456789'
                element_config = {
                    'type': 'str',
                    'chars': chars,
                    'length': int(input("长度 (默认8): ") or 8)
                }
            elif element_type == 'bool':
                element_config = {'type': 'bool'}
            else:
                print("无效类型!")
                continue
                
            length = int(input("列表长度 (默认随机1-5): ") or random.randint(1, 5))
            config = {
                'type': 'list',
                'element': element_config,
                'length': length
            }
            
        elif choice == '3':
            # 字典生成
            fields = {}
            print("\n配置字典字段 (输入q结束添加):")
            
            while True:
                key = input("字段名称: ")
                if key == 'q':
                    break
                    
                field_type = input(f"{key} 类型 (int/float/str/bool): ")
                field_config = {}
                
                if field_type == 'int':
                    field_config = {
                        'type': 'int',
                        'min': int(input(f"{key} 最小值: ")),
                        'max': int(input(f"{key} 最大值: "))
                    }
                elif field_type == 'float':
                    field_config = {
                        'type': 'float',
                        'min': float(input(f"{key} 最小值: ")),
                        'max': float(input(f"{key} 最大值: "))
                    }
                elif field_type == 'str':
                    chars = input(f"{key} 字符集 (默认a-z0-9): ") or 'abcdefghijklmnopqrstuvwxyz0123456789'
                    field_config = {
                        'type': 'str',
                        'chars': chars,
                        'length': int(input(f"{key} 长度 (默认8): ") or 8)
                    }
                elif field_type == 'bool':
                    field_config = {'type': 'bool'}
                else:
                    print("无效类型!")
                    continue
                    
                fields[key] = field_config
                
            config = {
                'type': 'dict',
                'fields': fields
            }
            
        elif choice == '4':
            # 嵌套结构生成
            print("\n使用预定义的嵌套结构: 用户订单信息")
            config = {
                'type': 'dict',
                'fields': {
                    'order_id': {'type': 'str', 'chars': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', 'length': 10},
                    'customer': {
                        'type': 'dict',
                        'fields': {
                            'name': {'type': 'str', 'chars': 'abcdefghijklmnopqrstuvwxyz', 'length': 8},
                            'age': {'type': 'int', 'min': 18, 'max': 65},
                            'is_vip': {'type': 'bool'}
                        }
                    },
                    'items': {
                        'type': 'list',
                        'element': {
                            'type': 'dict',
                            'fields': {
                                'product_id': {'type': 'int', 'min': 100, 'max': 999},
                                'quantity': {'type': 'int', 'min': 1, 'max': 10},
                                'price': {'type': 'float', 'min': 10.0, 'max': 1000.0, 'decimal': 2}
                            }
                        },
                        'length': random.randint(1, 5)
                    },
                    'total_amount': {'type': 'float', 'min': 50.0, 'max': 5000.0, 'decimal': 2},
                    'created_at': {'type': 'str', 'chars': '0123456789-', 'length': 10}
                }
            }
        else:
            print("无效选项!")
            continue
            
        # 生成并显示样本
        try:
            samples = generator.generate_samples(count, config)
            _print_samples(samples)
        except ValueError as e:
            print(f"生成样本时出错: {e}")


def _print_samples(samples: List[Any], max_display: int = 5) -> None:
    """打印样本列表"""
    print(f"\n生成了 {len(samples)} 个样本:")
    
    if len(samples) <= max_display:
        for i, sample in enumerate(samples):
            print(f"样本 {i+1}: {sample}")
    else:
        for i in range(max_display):
            print(f"样本 {i+1}: {samples[i]}")
        print(f"... 和另外 {len(samples) - max_display} 个样本")


# 使用范例 - 非交互式API使用示例
def api_usage_examples():
    """生成器API使用范例，展示如何通过代码直接调用生成器"""
    generator = RandomSampleGenerator()
    
    print("=" * 50)
    print("随机样本生成器API使用范例")
    print("=" * 50)
    
    # 范例1: 生成随机整数
    int_samples = generator.generate_samples(3, {'type': 'int', 'min': 1, 'max': 100})
    print("\n范例1: 生成随机整数")
    print(int_samples)
    
    # 范例2: 生成随机浮点数
    float_samples = generator.generate_samples(3, {'type': 'float', 'min': 0.0, 'max': 1.0, 'decimal': 4})
    print("\n范例2: 生成随机浮点数")
    print(float_samples)
    
    # 范例3: 生成随机字符串
    str_samples = generator.generate_samples(3, {'type': 'str', 'chars': 'ABCDEFG', 'length': 5})
    print("\n范例3: 生成随机字符串")
    print(str_samples)
    
    # 范例4: 生成随机列表
    list_samples = generator.generate_samples(2, {
        'type': 'list',
        'element': {'type': 'float', 'min': 0, 'max': 100},
        'length': 4
    })
    print("\n范例4: 生成随机列表")
    print(list_samples)
    
    # 范例5: 生成随机字典
    dict_samples = generator.generate_samples(2, {
        'type': 'dict',
        'fields': {
            'name': {'type': 'str', 'length': 6},
            'age': {'type': 'int', 'min': 18, 'max': 60},
            'is_student': {'type': 'bool'}
        }
    })
    print("\n范例5: 生成随机字典")
    print(dict_samples)
    
    # 范例6: 生成复杂嵌套结构
    nested_config = {
        'type': 'dict',
        'fields': {
            'id': {'type': 'str', 'length': 8, 'chars': '0123456789'},
            'data': {
                'type': 'list',
                'element': {
                    'type': 'dict',
                    'fields': {
                        'value': {'type': 'float', 'min': 0, 'max': 100},
                        'details': {
                            'type': 'tuple',
                            'elements': [
                                {'type': 'str', 'length': 4},
                                {'type': 'int', 'min': 1, 'max': 10}
                            ]
                        }
                    }
                },
                'length': 3
            }
        }
    }
    
    nested_samples = generator.generate_samples(2, nested_config)
    print("\n范例6: 生成复杂嵌套结构")
    print(nested_samples)


if __name__ == '__main__':
    # 选择运行交互式演示或API使用范例
    print("选择运行模式:")
    print("1: 交互式生成器演示")
    print("2: API使用范例")
    
    mode = input("请输入选项 (1-2): ")
    if mode == '1':
        interactive_generator_demo()
    else:
        api_usage_examples()