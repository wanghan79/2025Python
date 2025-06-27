#!/usr/bin/env python
# coding:utf-8

import sys
from largeXMLDealer import LargeXMLParser


@LargeXMLParser(sys.argv[1], sys.argv[2])
def dealwithElement(elem):

    if isinstance(elem, object):
        print(elem.text)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python callDealer.py <xml_file> <element_tag>", file=sys.stderr)
        sys.exit(1)

    try:
        dealwithElement()
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)