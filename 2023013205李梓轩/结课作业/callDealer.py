#!/usr/bin/env python
# coding:utf-8

import sys
from largeXMLDealer import xml_dealer


def process_element(elem):
    """通用处理函数"""
    if elem.text:
        print(elem.text.strip())


if __name__ == "__main__":
    # 检查参数数量
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python callDealer.py <xml_file> [tag_name]")
        print("Example 1: python callDealer.py example.xml accession")
        print("Example 2: python callDealer.py example.xml sequence")
        sys.exit(1)

    file_name = sys.argv[1]

    # 如果没有提供标签名，默认处理两个标签
    if len(sys.argv) == 2:
        print("\nProcessing accessions:")
        process_accessions = xml_dealer(elem_tag="accession")(process_element)
        process_accessions(file_name)

        print("\nProcessing sequence:")
        process_sequence = xml_dealer(elem_tag="sequence")(process_element)
        process_sequence(file_name)
    else:
        # 处理用户指定的标签
        tag_name = sys.argv[2]
        print(f"\nProcessing {tag_name}:")
        process_tag = xml_dealer(elem_tag=tag_name)(process_element)
        process_tag(file_name)
