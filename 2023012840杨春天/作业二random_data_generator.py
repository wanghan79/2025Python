import random
import string
from typing import Any, Dict, Generator, List, Optional, Tuple, Type, Union

class RandomDataGenerator:
    """随机数据生成器，支持多种数据类型和嵌套结构"""
    
    def __init__(self, struct: Dict[Any, Dict], num: int = 1):
        """
        初始化随机数据生成器
        
        参数:
            struct: 数据结构定义
            num: 生成的数据组数
        """
        self.struct = struct
        self.num = num
        
    def generate(self) -> Generator[Any, None, None]:
        """生成随机数据的生成器"""
        for _ in range(self.num):
            yield self._generate_group(self.struct)
    
    def _generate_group(self, struct: Dict[Any, Dict]) -> Any:
        """根据结构定义生成一组数据"""
        group = {}
        for data_type, config in struct.items():
            if data_type == 'num':
                continue  # 'num' 是特殊关键字，用于指定生成数量
            group[data_type] = self._generate_item(data_type, config)
        
        # 如果结构定义的是元组类型，将结果转换为元组
        if tuple in struct:
            return tuple(group.values())
        return group
    
    def _generate_item(self, data_type: Type, config: Dict) -> Any:
        """生成单个数据项"""
        if data_type == int:
            return self._generate_int(config)
        elif data_type == float:
            return self._generate_float(config)
        elif data_type == str:
            return self._generate_str(config)
        elif data_type == bool:
            return self._generate_bool(config)
        elif data_type == list:
            return self._generate_list(config)
        elif data_type == tuple:
            return self._generate_tuple(config)
        elif data_type == set:
            return self._generate_set(config)
        elif data_type == dict:
            return self._generate_dict(config)
        else:
            raise ValueError(f"不支持的数据类型: {data_type}")
    
    def _generate_int(self, config: Dict) -> int:
        """生成随机整数"""
        data_range = config.get("datarange", (0, 100))
        return random.randint(data_range[0], data_range[1])
    
    def _generate_float(self, config: Dict) -> float:
        """生成随机浮点数"""
        data_range = config.get("datarange", (0.0, 1.0))
        return random.uniform(data_range[0], data_range[1])
    
    def _generate_str(self, config: Dict) -> str:
        """生成随机字符串"""
        data_range = config.get("datarange", string.ascii_letters)
        length = config.get("len", 1)
        return ''.join(random.choices(data_range, k=length))
    
    def _generate_bool(self, config: Dict) -> bool:
        """生成随机布尔值"""
        return random.choice([True, False])
    
    def _generate_list(self, config: Dict) -> List:
        """生成随机列表"""
        list_length = config.get("len", 1)
        item_type = config.get("item_type", int)
        item_config = config.get("item_config", {})
        return [self._generate_item(item_type, item_config) for _ in range(list_length)]
    
    def _generate_tuple(self, config: Dict) -> Tuple:
        """生成随机元组"""
        return tuple(self._generate_list(config))
    
    def _generate_set(self, config: Dict) -> Set:
        """生成随机集合"""
        set_length = config.get("len", 1)
        item_type = config.get("item_type", int)
        item_config = config.get("item_config", {})
        
        # 确保集合元素的唯一性
        elements = set()
        while len(elements) < set_length:
            elements.add(self._generate_item(item_type, item_config))
        return elements
    
    def _generate_dict(self, config: Dict) -> Dict:
        """生成随机字典"""
        sub_struct = config.get("struct", {})
        num_items = config.get("num", 1)
        
        # 创建子生成器并获取结果
        sub_generator = RandomDataGenerator(sub_struct, num_items)
        result = {}
        
        for i, item in enumerate(sub_generator.generate()):
            key = config.get("key_prefix", f"key_{i}")
            result[key] = item
        
        return result

# 使用示例
if __name__ == "__main__":
    # 定义数据结构
    struct = {
        'num': 3,  # 生成3组数据
        tuple: {
            str: {"datarange": string.ascii_uppercase, "len": 4},  # 随机大写字母字符串
            int: {"datarange": (1, 100)},  # 1-100的随机整数
            list: {
                "item_type": float,
                "item_config": {"datarange": (0.0, 1.0)},
                "len": 3  # 长度为3的浮点数列表
            },
            dict: {
                "struct": {
                    'name': {"datarange": string.ascii_lowercase, "len": 5},
                    'age': {"datarange": (18, 60)}
                },
                "num": 2  # 字典包含2个项
            }
        }
    }
    
    # 创建生成器并生成数据
    generator = RandomDataGenerator(struct)
    data = list(generator.generate())
    
    # 打印生成的数据
    for i, item in enumerate(data):
        print(f"数据组 {i+1}: {item}")    