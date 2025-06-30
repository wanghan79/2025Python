import xml.sax
from functools import wraps
from typing import Callable, Dict, Any

class XMLChunkParser(xml.sax.ContentHandler):
    """SAX解析器处理XML数据块"""
    def __init__(self, target_element: str, callback: Callable):
        self.target = target_element
        self.callback = callback
        self.current_data = {}
        self.current_element = None
        self.buffer = ""

    def startElement(self, name, attrs):
        if name == self.target:
            self.current_data = dict(attrs)
        self.current_element = name

    def characters(self, content):
        if self.current_element and content.strip():
            self.buffer += content.strip()

    def endElement(self, name):
        if name == self.target:
            self.callback(self.current_data)
            self.current_data = {}
        elif self.current_element == name and self.buffer:
            self.current_data[name] = self.buffer
            self.buffer = ""

def xml_stream_parser(file_path: str, target_element: str):
    """
    XML大文件解析装饰器
    :param file_path: XML文件路径
    :param target_element: 需要提取的XML元素名
    """
    def decorator(process_func: Callable[[Dict[str, Any]], None]):
        @wraps(process_func)
        def wrapper(*args, **kwargs):
            parser = xml.sax.make_parser()
            handler = XMLChunkParser(target_element, lambda data: process_func(data, *args, **kwargs))
            parser.setContentHandler(handler)
            parser.parse(file_path)
        return wrapper
    return decorator

# ==================== 使用示例 ====================
if __name__ == "__main__":
    # 示例1：基本使用
    @xml_stream_parser("large_data.xml", "product")
    def print_product(product: dict):
        """被装饰的函数将接收每个product元素的数据"""
        print(f"Processing: {product['id']} - {product.get('name', '')}")

    print_product()  # 自动触发解析

    # 示例2：带参数的处理器
    @xml_stream_parser("transactions.xml", "transaction")
    def analyze_transaction(transaction: dict, currency: str):
        if transaction['currency'] == currency:
            print(f"{transaction['amount']} {currency}")

    analyze_transaction(currency="USD")  # 只处理美元交易

    # 示例3：链式装饰器（组合统计功能）
    @stats_operations('SUM', 'AVG')
    @xml_stream_parser("sales.xml", "sale")
    def process_sale(sale: dict):
        return {
            'amount': float(sale['amount']),
            'quantity': int(sale['quantity'])
        }

    process_sale()  # 自动解析并统计