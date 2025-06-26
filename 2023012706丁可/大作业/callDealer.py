#!/usr/bin/env python
# coding:utf-8

import sys
from largeXMLDealer import xml_parser_decorator

@xml_parser_decorator(elemTags=["accession", "sequence"])  # 同时处理两种标签
def process_element(elem):
    """处理XML元素的函数"""
    # 这个函数现在只需要定义，实际处理逻辑在装饰器中实现
    pass

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python callDealer.py <xml_file>")
        print("Example:")
        print("  python callDealer.py P00734.xml")
        sys.exit(1)

    fileName = sys.argv[1]

    try:
        print(f"\nParsing results:")
        process_element(fileName)  # 调用被装饰的函数

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        sys.exit(1)