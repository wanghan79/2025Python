"""
2023012373赵浚彤
2025春季学期python
结课作业
"""
from functools import wraps
from lxml import etree
from largeXMLDealer import LargeXMLHandler
import os

# 定义常量
xml_file = os.path.join(os.path.dirname(__file__), "P00734.xml")
target_tag = 'accession'

# 定义装饰器函数
def xml_parser_decorator(file_path, tag):
    """
    一个装饰器，使用 LargeXMLHandler 来解析 XML 文件。
    它根据 tag 筛选元素（如果提供了特定标签），并将匹配的元素传递给被修饰的函数。
    如果 tag 为 None，则处理所有元素。
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"xml_parser_decorator: 已为文件 '{file_path}' 和标签 '{tag}' 初始化")
            handler = LargeXMLHandler()

            def element_processor(elem):
                raw_tag = elem.tag
                tag_name = raw_tag
                if '}' in tag_name:
                    tag_name = tag_name.split('}', 1)[1]

                if tag is None or tag_name == tag:
                    print(
                        f"  标签匹配 (条件: target_tag='{tag}', actual_raw_tag='{raw_tag}', extracted_tag='{tag_name}')。正在调用被修饰的函数。")
                    func(elem, *args, **kwargs)

            handler.process_xml(file_path, element_processor)

        return wrapper

    return decorator

# 定义被装饰的函数
@xml_parser_decorator(file_path=xml_file, tag=target_tag)
def print_element(elem):
    """
    此函数由 xml_parser_decorator 装饰器修饰。
    它接收一个 XML 元素，并打印该元素，同时保持其原有的层级结构。
    """
    print(f"--- 找到元素 ({elem.tag}) ---")
    try:
        print(etree.tostring(elem, pretty_print=True, encoding='unicode').strip())
    except Exception as e:
        print(f"将元素 {elem.tag if elem is not None else 'None'} 转换成字符串时出错: {e}")
    print("------------------------\n")

# 主程序入口
if __name__ == "__main__":
    print(f"开始处理 XML 文件 '{xml_file}'\n目标标签: '{target_tag}'\n")
    print_element()
    print("XML 处理完成。")
