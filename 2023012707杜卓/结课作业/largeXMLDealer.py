#!/usr/bin/env python
# coding:utf-8

from lxml import etree  # type: ignore
from os import path
from optparse import OptionParser


class LargeXMLParser:
    def __init__(self, filename, elemTag):

        self.filename = filename
        self.elemTag = elemTag

    def __call__(self, func):

        def wrapper(*args, **kwargs):
            count = self.parse(self.filename, self.elemTag, func)
            print(f"Parsed {count} XML elements.")
            return count

        return wrapper

    def parse(self, fileName, elemTag, func4Element=None):

        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError("The input file is not a valid XML file.")

        count = 0
        es = ('end',)
        ns = self._getNamespace(fileName)
        ns = "{%s}" % ns

        context = etree.iterparse(fileName, events=es, tag=ns + elemTag)

        for event, elem in context:
            try:
                if func4Element:
                    func4Element(elem)
            except Exception as e:
                raise Exception("Error in processing element: " + str(e))
            finally:
                elem.clear()
                count += 1
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        del context
        return count

    def _getNamespace(self, fileName):

        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError("The input file is not a valid XML file.")
        result = ''
        es = ('start-ns',)
        context = etree.iterparse(fileName, events=es)
        for event, elem in context:
            prefix, result = elem
            break
        del context
        return result


def dealwithElement(elem):

    if isinstance(elem, object):
        print(elem.text)