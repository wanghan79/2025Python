#!/usr/bin/env python
# coding:utf-8

import sys
from os import path
from lxml import etree
from optparse import OptionParser


class largeXMLDealer:
    """
    A class to deal with large XML files.
    """

    def __init__(self):
        """Constructor"""

    def parse(self, fileName, elemTag, func4Element=None):
        """
        Parse the XML file and apply the given function to each element.
        """
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
        """
        Get the namespace of the XML file.
        """
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
    """
    A function to process each XML element.
    """
    if isinstance(elem, object):
        print(elem.text)


def main():
    """
    Main function to parse command line arguments and process the XML file.
    """
    usage = "usage: %prog [options] <XML file> <element tag>"
    parser = OptionParser(usage)
    parser.add_option("-p", "--print", dest="bPrint", default=False, action="store_true",
                      help="Print results on the screen.")
    parser.add_option("-o", "--output", type="string", dest="outputFile", default=None,
                      help="Output the results to a file.")

    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("You must specify the XML file name and the element tag.")

    filePath = path.normpath(args[0])
    elemTag = args[1]

    if not path.isfile(filePath) or not filePath.endswith("xml"):
        raise Exception("The input file is not a valid XML file.")

    largXML = largeXMLDealer()
    count = largXML.parse(filePath, elemTag, dealwithElement)

    if options.bPrint:
        print("Parsed %10d XML elements." % count)

    if options.outputFile:
        with open(options.outputFile, 'w') as f:
            f.write("Parsed %10d XML elements.\n" % count)


if __name__ == "__main__":
    main()