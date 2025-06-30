import random
import xml.etree.ElementTree as ET
from functools import wraps
from typing import List, Dict, Any, Tuple, Generator
import statistics
import io

def xml_parser_decorator(chunk_size: int = 1000):
    """
    XML大文件解析修饰器

    参数:
        chunk_size: 处理块大小
    """

    def decorator(print_func):
        @wraps(print_func)
        def wrapper(xml_content: str, *args, **kwargs):
            """
            包装数据打印函数，添加XML解析功能

            参数:
                xml_content: XML内容（字符串或文件路径）
                *args, **kwargs: 传递给原始打印函数的参数
            """

            def parse_xml_iteratively(xml_data):
                """迭代解析XML数据"""
                # 如果是文件路径，读取文件；否则作为XML字符串处理
                if xml_data.endswith('.xml'):
                    try:
                        tree = ET.parse(xml_data)
                        root = tree.getroot()
                    except FileNotFoundError:
                        print(f"警告: 文件 {xml_data} 不存在，创建示例XML数据")
                        root = create_sample_xml()
                else:
                    try:
                        root = ET.fromstring(xml_data)
                    except ET.ParseError:
                        print("XML格式错误，创建示例XML数据")
                        root = create_sample_xml()

                # 迭代处理XML元素
                elements_processed = 0
                current_chunk = []

                for elem in root.iter():
                    # 提取元素信息
                    element_info = {
                        'tag': elem.tag,
                        'text': elem.text.strip() if elem.text else '',
                        'attributes': dict(elem.attrib),
                        'children_count': len(list(elem))
                    }

                    current_chunk.append(element_info)
                    elements_processed += 1

                    # 当达到块大小时，处理这一块
                    if len(current_chunk) >= chunk_size:
                        yield current_chunk, elements_processed
                        current_chunk = []

                # 处理剩余元素
                if current_chunk:
                    yield current_chunk, elements_processed

            def create_sample_xml():
                """创建示例XML数据"""
                xml_string = """<?xml version="1.0" encoding="UTF-8"?>
                <library>
                    <book id="1" category="fiction">
                        <title>小说一</title>
                        <author>作者A</author>
                        <year>2020</year>
                        <price>29.99</price>
                    </book>
                    <book id="2" category="science">
                        <title>科学书籍</title>
                        <author>作者B</author>
                        <year>2021</year>
                        <price>39.99</price>
                    </book>
                    <book id="3" category="history">
                        <title>历史读物</title>
                        <author>作者C</author>
                        <year>2019</year>
                        <price>25.50</price>
                    </book>
                </library>"""
                return ET.fromstring(xml_string)

            print(f"=== XML解析开始 (块大小: {chunk_size}) ===")

            total_elements = 0
            chunk_count = 0

            # 解析XML并分块处理
            for chunk_data, elements_count in parse_xml_iteratively(xml_content):
                chunk_count += 1
                total_elements = elements_count

                print(f"\n--- 处理块 {chunk_count} (已处理 {elements_count} 个元素) ---")

                # 调用原始打印函数处理数据
                print_func(chunk_data, *args, **kwargs)

            print(f"\n=== XML解析完成 ===")
            print(f"总共处理了 {total_elements} 个XML元素，分为 {chunk_count} 个块")

        return wrapper

    return decorator


@xml_parser_decorator(chunk_size=2)
def print_xml_data(data_chunk: List[Dict], show_details: bool = True):
    """被修饰的数据打印函数"""
    for i, element in enumerate(data_chunk):
        print(f"  元素 {i + 1}:")
        print(f"    标签: {element['tag']}")

        if show_details:
            if element['text']:
                print(f"    文本: {element['text']}")
            if element['attributes']:
                print(f"    属性: {element['attributes']}")
            print(f"    子元素数量: {element['children_count']}")
        print()

def test_all_assignments():
    print("\n" + "=" * 60)
    print("结课作业：XML解析修饰器测试")
    print("=" * 60)

    # 测试XML解析修饰器
    sample_xml = """<?xml version="1.0" encoding="UTF-8"?>
    <students>
        <student id="1">
            <name>张三</name>
            <age>20</age>
            <grade>A</grade>
        </student>
        <student id="2">
            <name>李四</name>
            <age>21</age>
            <grade>B</grade>
        </student>
        <student id="3">
            <name>王五</name>
            <age>19</age>
            <grade>A</grade>
        </student>
    </students>"""

    print_xml_data(sample_xml, show_details=True)
    print("\n" + "=" * 60)

test_all_assignments()
