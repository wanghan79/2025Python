import xml.sax
from functools import wraps
from typing import Callable, Dict, List, Optional


class XMLStatsHandler(xml.sax.ContentHandler):
    """SAX处理器用于收集XML统计数据"""

    def __init__(self, target_elements: List[str]):
        self.target_elements = target_elements
        self.stats = {element: [] for element in target_elements}
        self.current_element = None
        self.current_data = ""

    def startElement(self, tag, attrs):
        if tag in self.target_elements:
            self.current_element = tag

    def characters(self, content):
        if self.current_element:
            self.current_data += content.strip()

    def endElement(self, tag):
        if tag == self.current_element and self.current_data:
            self.stats[tag].append(self.current_data)
            self.current_element = None
            self.current_data = ""


def xml_parser_decorator(file_path: str, target_elements: List[str]):
    """
    带参修饰器工厂函数，用于解析XML大文件
    :param file_path: XML文件路径
    :param target_elements: 需要统计的XML元素列表
    """

    def decorator(print_func: Callable):
        @wraps(print_func)
        def wrapper(*args, **kwargs):
            # 创建SAX解析器
            parser = xml.sax.make_parser()
            handler = XMLStatsHandler(target_elements)
            parser.setContentHandler(handler)

            try:
                # 解析XML文件
                parser.parse(file_path)
                print(f"成功解析XML文件: {file_path}")

                # 将统计结果作为额外参数传递给打印函数
                kwargs['xml_stats'] = handler.stats
                return print_func(*args, **kwargs)

            except Exception as e:
                print(f"XML解析错误: {str(e)}")
                kwargs['xml_stats'] = None
                return print_func(*args, **kwargs)

        return wrapper

    return decorator


# 应用修饰器的打印函数示例
@xml_parser_decorator(
    file_path="large_data.xml",
    target_elements=["employee", "department", "salary"]
)
def print_data_summary(data: Dict, xml_stats: Optional[Dict] = None):
    """
    打印数据摘要的装饰后函数
    :param data: 原始数据字典
    :param xml_stats: 从修饰器传入的XML统计结果
    """
    print("\n=== 数据摘要 ===")
    print("原始数据:", data)

    if xml_stats:
        print("\nXML统计结果:")
        for element, values in xml_stats.items():
            print(f"{element}数量: {len(values)}")
            if values:
                sample = values[0] if len(values) == 1 else values[:3]
                print(f"示例: {sample}{'...' if len(values) > 3 else ''}")
    else:
        print("\n无有效的XML统计数据")


# 使用示例
if __name__ == "__main__":
    # 测试数据
    test_data = {
        "name": "示例数据集",
        "records": 1000,
        "description": "结合XML数据的测试样例"
    }

    # 调用被装饰的函数
    print_data_summary(test_data)