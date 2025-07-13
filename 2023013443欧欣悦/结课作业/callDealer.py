#!/usr/bin/env python
# coding:utf-8

import largeXMLDealer
import sys
from functools import wraps
from datetime import datetime  # 需要补充导入datetime模块


def print_decorator(func):
    @wraps(func)
    def wrapper(elem):
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        formatted_text = f"{timestamp} Element '{elem.tag}': {elem.text.strip()}"
        line_number = getattr(elem, 'sourceline', 'Unknown')
        print(f"{formatted_text} (Line: {line_number})")

    return wrapper


@print_decorator
def dealwithElement(elem):
    pass  # 实际处理逻辑由装饰器完成


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 callDealer.py <xml_file> <element_tag>")
        sys.exit(1)

    fileName = sys.argv[1]
    elemTag = sys.argv[2]

    lxmld = largeXMLDealer.largeXMLDealer()
    count = lxmld.parse(fileName, elemTag, dealwithElement)
    print(f"\nAlready parsed {count} XML elements.")