#!/usr/bin/env python
# coding:utf-8

import largeXMLDealer
import sys
import os


def dealwithElement(elem):
    """处理XML元素，打印节点文本（去除首尾空白）"""
    if elem is not None and elem.text:
        print(elem.text.strip())


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("USAGE: python3 callDealer.py <XML_FILE> <ELEMENT_TAG>")
        sys.exit(1)
    
    fileName = sys.argv[1]
    target_tag = sys.argv[2]  
  
    if not os.path.exists(fileName):
        print(f"Error: File '{fileName}' not found.")
        sys.exit(1)
    
    lxmld = largeXMLDealer.largeXMLDealer()
    
    try:

        count = lxmld.parse(fileName, target_tag, dealwithElement)
        print(f"Already parsed {count} XML elements.")
    except Exception as e:
        print(f"Parsing failed: {str(e)}")
        sys.exit(1)
