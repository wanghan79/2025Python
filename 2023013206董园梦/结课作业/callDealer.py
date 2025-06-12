#!/usr/bin/env python
# coding:utf-8

import largeXMLDealer
import sys


def process_element(element):
    if isinstance(element, object):
        print(element.text)


if __name__ == "__main__":
    file_name = sys.argv[1]
    element_tag = sys.argv[2]

    xml_parser = largeXMLDealer.XMLParser()
    count = xml_parser.parse(file_name, element_tag, process_element)
    print(f"Already parsed {count} XML elements.")