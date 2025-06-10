#!/usr/bin/env python
# coding:utf-8

import sys
from largeXMLDealer import parse_large_xml


def dealwithElement(elem):

    print(elem.text)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python callDealer.py <xml_file> <tag>")
        sys.exit(1)

    fileName = sys.argv[1]
    elemTag = sys.argv[2]

    try:
        @parse_large_xml(fileName, elemTag)
        def process_element(elem):
            dealwithElement(elem)

        count = process_element()
        print(f"Already parsed {count} XML elements.")
    except Exception as e:
        print(f"[ERROR] {e}")