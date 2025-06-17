#!/usr/bin/env python
# coding:utf-8

from largeXMLDealer import xml_element_processor
import sys


def default_element_handler(element):
    """
    默认元素处理器：打印元素文本内容
    """
    if element.text and element.text.strip():
        print(element.text.strip())


def main():
    if len(sys.argv) < 3:
        print("使用方式: python callDealer.py <filename.xml> <tag_name>")
        print("示例: python callDealer.py P00734.xml accession")
        sys.exit(1)

    file_path = sys.argv[1]
    tag_name = sys.argv[2]

    @xml_element_processor(file_path, tag_name)
    def process_element(elem):
        default_element_handler(elem)

    # 触发解析过程
    process_element()


if __name__ == "__main__":
    main()
