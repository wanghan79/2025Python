#!/usr/bin/env python
# coding:utf-8
"""
  Author:  H.Wang --<>
  Purpose: To parse the large XML files more than 500M
  Created: 4/4/2016
"""

import os
from lxml import etree
from argparse import ArgumentParser
from functools import wraps


# Decorator class to handle XML parsing
class XMLParser:
    def __init__(self, func):
        self.func = func
        wraps(func)(self)

    def __call__(self, file_path, tag, print_output=False, output_file=None):
        if not os.path.isfile(file_path) or not file_path.endswith(".xml"):
            raise FileNotFoundError("The input file is not a valid XML file.")

        count = 0
        namespace = self._get_namespace(file_path)
        full_tag = f"{{{namespace}}}{tag}"

        context = etree.iterparse(file_path, events=("end",), tag=full_tag)

        if print_output:
            print(f"Processing elements with tag: {tag}")

        for _, elem in context:
            try:
                self.func(elem, print_output)
                self._process_nested(elem, print_output)
                if print_output:
                    print(f"Processed element {count + 1}: {elem.tag}")
            except Exception as e:
                raise Exception(f"Error in function parameter: {e}")
            finally:
                elem.clear()
                count += 1
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        del context

        if output_file:
            with open(output_file, "w") as f:
                f.write(f"Parsed {count} XML elements.\n")
        else:
            print(f"Parsed {count} XML elements.")

        return count

    def _get_namespace(self, file_path):
        if not os.path.isfile(file_path) or not file_path.endswith(".xml"):
            raise FileNotFoundError("The input file is not a valid XML file.")
        context = etree.iterparse(file_path, events=("start-ns",))
        for _, (prefix, uri) in context:
            return uri
        return ""

    def _process_nested(self, elem, print_output):
        if print_output:
            print(f"Processing nested Tag: {elem.tag}, Text: {elem.text}")
        for child in elem:
            self._process_nested(child, print_output)


# Function to handle each XML element
@XMLParser
def handle_element(elem, print_output=True):
    if print_output:
        print(f"Current Tag: {elem.tag}, Text: {elem.text}")


def main():
    parser = ArgumentParser(description="Parse large XML files.")
    parser.add_argument("xml_file", help="Path to the XML file.")
    parser.add_argument("-t", "--tag", required=True, help="XML tag to parse.")
    parser.add_argument("-p", "--print", action="store_true", help="Print results to the screen.")
    parser.add_argument("-o", "--output", help="Output file to write the results.")

    args = parser.parse_args()

    handle_element(args.xml_file, args.tag, print_output=args.print, output_file=args.output)


if __name__ == "__main__":
    main()