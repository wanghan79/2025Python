#!/usr/bin/env python
# coding:utf-8

import sys
from largeXMLDealer import xml_dealer


@xml_dealer(elem_tag="accession")
def process_accessions(elem):
    """处理accession标签的函数"""
    if elem.text:
        print(elem.text.strip())


@xml_dealer(elem_tag="sequence")
def process_sequence(elem):
    """处理sequence标签的函数"""
    if elem.text:
        print(elem.text.strip())


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python callDealer.py <xml_file>")
        sys.exit(1)

    file_name = sys.argv[1]

    # 根据需要调用不同的处理函数
    print("\nProcessing accessions:")
    process_accessions(file_name)

    print("\nProcessing sequence:")
    process_sequence(file_name)
