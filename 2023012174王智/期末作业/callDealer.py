#!/usr/bin/env python
# coding:utf-8

import largeXMLDealer
import sys


def custom_function(elem, bPrint=True):
    """Custom function to handle elements"""
    if bPrint:
        print(f"{elem.text}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python callDealer.py <xml_file> <tag>")
        sys.exit(1)

    fileName = sys.argv[1]
    elemTag = sys.argv[2]

    # Use the decorated function
    decorated_func = largeXMLDealer.XMLParserDecorator(custom_function)
    largeXMLDealer.dealWithElement(fileName, elemTag, bPrint=True)
    largeXMLDealer.reverse_print(fileName, elemTag, bPrint=True)
    count = decorated_func(fileName, elemTag, bPrint=True)
    print(f"Already parsed {count} XML elements.")
  
