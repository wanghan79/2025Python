import xml.etree.ElementTree as ET
from functools import wraps
import sys

def xml_parser_decorator(func):
    """XML大文件解析修饰器"""
    @wraps(func)
    def wrapper(xml_path, *args, **kwargs):
        context = ET.iterparse(xml_path, events=('start', 'end'))
        _, root = next(context)  
        
        data_buffer = []
        for event, elem in context:
            if event == 'end' and elem.tag == 'item':  # 假设数据节点为item
                data = {child.tag: child.text for child in elem}
                data_buffer.append(data)
                elem.clear()  # 释放内存
                
                if len(data_buffer) >= 1000:
                    func(data_buffer, *args, **kwargs)
                    data_buffer.clear()

        if data_buffer:
            func(data_buffer, *args, **kwargs)
        root.clear()  
    return wrapper

@xml_parser_decorator
def print_data(data_list):
    """数据打印函数"""
    for idx, data in enumerate(data_list, 1):
        print(f"Item {idx}: {data}")
        if idx % 50 == 0:  # 每50条换行
            print()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parser.py <large_xml_file>")
        sys.exit(1)
    
    xml_file = sys.argv[1]
    print_data(xml_file)  # 调用修饰后的函数
