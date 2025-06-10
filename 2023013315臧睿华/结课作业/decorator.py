#!/usr/bin/env python
# coding:utf-8
"""
  Author:  H.Wang --<>
  Purpose: To parse the large XML files more than 500M
  Created: 4/4/2016
  修改： 臧睿华
  时间： 2025/5/27
"""

from lxml import etree
from os import path
from optparse import OptionParser
import sys


class largeXMLDealer:
    """
    
    """

    def __init__(self, func4Element = None):
        self.func4Element = func4Element
        """Constructor"""

    def __call__(self, func4Element):
        self.func4Element = func4Element
        return func4Element
    
    def parse(self, fileName, elemTag):
        """
        
        """
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError

        count = 0
        es = ('end',)
        ns = self._getNamespace(fileName)
        ns = "{%s}" % ns

        context = etree.iterparse(fileName, events=es, tag=ns + elemTag)

        for event, elem in context:
            # Call the outside function to deal with the element here
            try:
                if self.func4Element:
                    self.func4Element(elem)
            finally:
                elem.clear()
                count += 1
                parent = elem.getparent()
                if parent is not None:
                    while elem.getprevious() is not None:
                        del parent[0]
        del context
        # Return how many elements had been parsed
        return count

    def _getNamespace(self, fileName):
        """"""
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError
        result = ''
        es = ('start-ns',)
        context = etree.iterparse(fileName, events=es)
        for event, elem in context:
            prefix, result = elem
            # print("%s, %d"%(elem, len(elem)))
            break
        del context
        return result


def main():
    """
    
    """
    # Construct the usage.
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-p", "--print", dest="bPrint", default=False, action="store_true",
                      help="Print results on the screen.")
    parser.add_option("-o", "--output", type="string", dest="outputFile", default=None,
                      help="Output the results to a file.")
    parser.add_option("-t", "--tag", type="string", dest="tag", default="",
                      help="The XML tag interested to parse.")

    # Parse the options and args input by users.
    (options, args) = parser.parse_args()

    # Check the correction of users input and call the fuctions of class DoSomething.
    if (len(args) != 1):
        parser.error("You have not input the XML file name")

    filePath = path.normpath(args[0])
    if not path.isfile(filePath) or not filePath.endswith("xml"):
        raise Exception("The input file is not exist or a vailable XML file.")
    # Call XML parser
    largXML = largeXMLDealer()
    count = largXML.parse(filePath, options.tag)
    print("Parsed %10d XML elements." % count)


dealer = largeXMLDealer()

@dealer
def dealwithElement(elem):
    """
    
    """
    print(elem.tag, elem.text)


if __name__ == "__main__":
    # if len(sys.argv) == 2:
    fileName = sys.argv[1]
    elemTag = sys.argv[2]

    # print("%s, %s"%(fileName, elemTag))
    # lxmld = largeXMLDealer.largeXMLDealer()
    lxmld = largeXMLDealer(dealwithElement)
    count = lxmld.parse(fileName, elemTag)
    print("Already parsed %d XML elements." % count)