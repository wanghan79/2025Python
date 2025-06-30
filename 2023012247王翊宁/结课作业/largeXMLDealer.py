import xml.sax
from functools import wraps
from typing import Callable, Dict, List, Optional, Any

class XMLStatsHandler(xml.sax.ContentHandler):
    """SAX处理器用于收集XML统计数据"""
    def __init__(self, target_elements: List[str]):
        self.target_elements = target_elements
        self.stats = {element: [] for element in target_elements}
        self.current_element = None
        self.current_data = ""
        self.total_records = 0
    
    def startElement(self, tag: str, attrs: Dict[str, str]):
        if tag in self.target_elements:
            self.current_element = tag
    
    def characters(self, content: str):
        if self.current_element:
            self.current_data += content.strip()
    
    def endElement(self, tag: str):
        if tag == self.current_element and self.current_data:
            self.stats[tag].append(self.current_data)
            self.total_records += 1
            self.current_element = None
            self.current_data = ""

def xml_parser_decorator(file_path: str, target_elements: List[str]):
    """
    XML大文件解析修饰器工厂
    :param file_path: XML文件路径
    :param target_elements: 需要收集的XML元素标签列表
    """
    def decorator(print_func: Callable):
        @wraps(print_func)
        def wrapper(*args: Any, **kwargs: Any):
            # 创建SAX解析器
            parser = xml.sax.make_parser()
            parser.setFeature(xml.sax.handler.feature_namespaces, 0)
            handler = XMLStatsHandler(target_elements)
            parser.setContentHandler(handler)
            
            try:
                print(f"\n开始解析XML文件: {file_path}")
                parser.parse(file_path)
                print(f"解析完成，共处理 {handler.total_records} 条记录")
                
                # 将统计结果注入被修饰函数
                kwargs['xml_stats'] = handler.stats
                return print_func(*args, **kwargs)
            
            except xml.sax.SAXParseException as e:
                print(f"XML解析错误(行 {e.getLineNumber()}): {e.getMessage()}")
                kwargs['xml_stats'] = None
                return print_func(*args, **kwargs)
            
            except Exception as e:
                print(f"系统错误: {str(e)}")
                kwargs['xml_stats'] = None
                return print_func(*args, **kwargs)
        
        return wrapper
    return decorator
