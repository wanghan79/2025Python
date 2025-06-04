#!/usr/bin/env python
# coding:utf-8

import largeXMLDealer
import sys

@largeXMLDealer.XMLDecorator
def dealwithElement(elem):
    """"""
    if isinstance(elem, object):
        print(elem.text)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        fileName = sys.argv[1]
        elemTag = sys.argv[2]

        lxmld = largeXMLDealer.largeXMLDealer()
        decorator = largeXMLDealer.XMLDecorator(dealwithElement)
        count = lxmld.parse(fileName, elemTag, decorator)
        print("Already parsed %d XML elements." % decorator.get_count())
    else:
        print("Usage: python3 callDealer.py <filename> <tag>")