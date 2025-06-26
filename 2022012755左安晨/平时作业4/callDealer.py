"""
  Author:  Zuoanchen--<>
  Created: 6/10/2025
"""

import largeXMLDealer
import sys


def print_element(elem):
    """
    Function to print element text
    """
    if elem.text and elem.text.strip():
        print(elem.text.strip())


if __name__ == "__main__":
    fileName = input("请输入 XML 文件路径: ").strip()
    elemTag = input("请输入要解析的 XML 标签名: ").strip()


    @largeXMLDealer.xml_parser(fileName, elemTag)
    def process_xml(elem):
        print_element(elem)


    process_xml()