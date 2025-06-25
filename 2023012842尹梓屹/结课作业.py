import xml.etree.ElementTree as ET
from typing import Callable, Dict, Any, TextIO
from functools import wraps
from io import StringIO
import gzip

def xml_file_parser(
    element_path: str,
    encoding: str = 'utf-8',
    gzipped: bool = False,
    buffer_size: int = 1024 * 1024
):
    """
    XML大文件解析修饰器工厂函数
    
    参数:
        element_path: 要解析的XML元素路径，如 'book' 或 'catalog/book'
        encoding: 文件编码，默认为utf-8
        gzipped: 是否处理gzip压缩文件
        buffer_size: 读取缓冲区大小，默认为1MB
        
    返回:
        装饰器函数
    """
    def decorator(print_func: Callable[[Dict[str, Any]], None]):
        @wraps(print_func)
        def wrapper(file_path: str, *args, **kwargs):
            # 打开文件
            opener = gzip.open if gzipped else open
            with opener(file_path, 'rb') as f:
                # 创建迭代器
                context = ET.iterparse(
                    f,
                    events=('start', 'end'),
                    parser=ET.XMLParser(encoding=encoding)
                )
                
                # 获取元素标签列表
                tags = element_path.split('/')
                current_path = []
                element_stack = []
                data = {}
                
                # 解析XML
                for event, elem in context:
                    if event == 'start':
                        current_path.append(elem.tag)
                        element_stack.append(elem)
                        
                        # 如果路径匹配，初始化数据字典
                        if current_path == tags:
                            data = {
                                'tag': elem.tag,
                                'attrib': dict(elem.attrib),
                                'text': '',
                                'children': []
                            }
                    
                    elif event == 'end':
                        # 如果路径匹配，收集数据并调用打印函数
                        if current_path == tags:
                            if elem.text and elem.text.strip():
                                data['text'] = elem.text.strip()
                            
                            # 调用被装饰的打印函数
                            print_func(data, *args, **kwargs)
                            
                            # 清除已处理元素以减少内存占用
                            elem.clear()
                            for ancestor in element_stack[:-1]:
                                ancestor.clear()
                        
                        current_path.pop()
                        element_stack.pop()
        
        return wrapper
    return decorator

# 示例使用
if __name__ == "__main__":
    # 示例XML数据
    sample_xml = """
    <catalog>
        <book id="bk101">
            <author>Gambardella, Matthew</author>
            <title>XML Developer's Guide</title>
            <genre>Computer</genre>
            <price>44.95</price>
            <publish_date>2000-10-01</publish_date>
            <description>An in-depth look at creating applications with XML.</description>
        </book>
        <book id="bk102">
            <author>Ralls, Kim</author>
            <title>Midnight Rain</title>
            <genre>Fantasy</genre>
            <price>5.95</price>
            <publish_date>2000-12-16</publish_date>
            <description>A former architect battles corporate zombies.</description>
        </book>
    </catalog>
    """
    
    # 将示例XML写入临时文件
    with open('sample.xml', 'w', encoding='utf-8') as f:
        f.write(sample_xml)
    
    # 定义打印函数
    def simple_print(book_data: Dict[str, Any]):
        """简单的打印函数"""
        print(f"\nBook ID: {book_data['attrib']['id']}")
        print(f"Title: {book_data['text'] if book_data['text'] else 'N/A'}")
        print("Attributes:", book_data['attrib'])
    
    # 应用修饰器
    @xml_file_parser('catalog/book')
    def print_book(book_data: Dict[str, Any]):
        """带修饰的打印函数"""
        print("\n=== Book Information ===")
        print(f"ID: {book_data['attrib']['id']}")
        for child in book_data['children']:
            print(f"{child['tag']}: {child['text']}")
    
    # 使用原始打印函数
    print("=== 使用简单打印函数 ===")
    simple_print_decorated = xml_file_parser('catalog/book')(simple_print)
    simple_print_decorated('sample.xml')
    
    # 使用带修饰的打印函数
    print("\n=== 使用带修饰的打印函数 ===")
    print_book('sample.xml')
    
    # 更复杂的打印函数示例
    @xml_file_parser('catalog/book', encoding='utf-8')
    def detailed_print(book_data: Dict[str, Any], highlight: bool = False):
        """更复杂的打印函数，带额外参数"""
        if highlight:
            print("\n\033[1;32m=== Highlighted Book ===\033[0m")
        else:
            print("\n=== Book Details ===")
        
        print(f"ID: {book_data['attrib'].get('id', 'N/A')}")
        print(f"Attributes: {book_data['attrib']}")
        if book_data['text']:
            print(f"Content: {book_data['text']}")
    
    print("\n=== 使用带参数的打印函数 ===")
    detailed_print('sample.xml', highlight=True)
