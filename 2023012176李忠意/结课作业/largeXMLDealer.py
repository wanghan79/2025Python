#!/usr/bin/env python
# coding:utf-8
"""
  Author:  H.Wang --<>
  Purpose: To parse the large XML files more than 500M
  Created: 4/4/2016
"""

from lxml import etree
from os import path

class largeXMLDealer:

    def __init__(self, filename, elemTag):
        self.filename = filename
        self.elemTag = elemTag

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print(f"Parsing file: {self.filename}, Tag: {self.elemTag}")
            count = self.parse(self.filename, self.elemTag, func)
            print(f"Already parsed {count} XML elements.")
        return wrapper
    def parse(self, fileName, elemTag, func4Element=None):
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError(f"Invalid file: {fileName}")

        count = 0
        es = ('end',)
        ns = self._getNamespace(fileName)
        ns = "{%s}" % ns

        context = etree.iterparse(fileName, events=es, tag=ns + elemTag)

        for event, elem in context:
            # Call the outside function to deal with the element here
            try:
                func4Element(elem)
            except Exception:
                raise Exception("Something wrong in function parameter: func4Element")
            finally:
                elem.clear()
                count = count + 1
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        del context
        # Return how many elements had been parsed
        return count

    def _getNamespace(self, fileName):
        """"""
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError(f"Invalid file: {fileName}")
        result = ''
        es = ('start-ns',)
        context = etree.iterparse(fileName, events=es)
        for event, elem in context:
            prefix, result = elem
            # print("%s, %d"%(elem, len(elem)))
            break
        del context
        return result
