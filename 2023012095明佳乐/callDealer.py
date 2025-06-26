#!/usr/bin/env python
# coding:utf-8

import largeXMLDealer
import sys

def dealwithElement(elem, tag_name):
    """Function to process each XML element"""
    if isinstance(elem, object):
        if tag_name == "sequence":
            # For sequence tag, print text directly (keep original format)
            print(elem.text)
        else:
            # For other tags (like accession), add tag name prefix
            print(f"{tag_name}: {elem.text}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python callDealer.py <xml_file> <elemTag>")
        sys.exit(1)
    
    fileName = sys.argv[1]
    elemTag = sys.argv[2]
    
    # 使用装饰器包装处理函数
    wrapped_func = largeXMLDealer.largeXMLDealer.parse_decorator(elemTag=elemTag)(lambda elem: dealwithElement(elem, elemTag))
    wrapped_func(fileName)