#!/usr/bin/env python
# coding:utf-8
"""
  Author:  H.Wang --<>
  Purpose: To parse the large XML files more than 500M
  Created: 4/4/2016
"""

from lxml import etree
from os import path
from optparse import OptionParser

class XMLDecorator:
    """A decorator class to modify the dealwithElement function for parsing large XML files."""
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, elem):
        """Call the decorated function and handle element processing."""
        self.func(elem)
        self.count += 1
        # Clear the element to save memory
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]

    def get_count(self):
        """Return the number of elements processed."""
        return self.count

class largeXMLDealer:
    """
    A class for dealing with large XML files.
    """
    def __init__(self):
        """Constructor"""

    def parse(self, fileName, elemTag, func4Element=None):
        """"""
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
                if func4Element is not None:
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
            raise FileNotFoundError
        result = ''
        es = ('start-ns',)
        context = etree.iterparse(fileName, events=es)
        for event, elem in context:
            prefix, result = elem
            break
        del context
        return result

def main():
    """
    The main function to parse XML files.
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
        raise Exception("The input file is not exist or a available XML file.")
    # Call XML parser
    largXML = largeXMLDealer()
    count = largXML.parse(filePath, options.tag)
    print("Parsed %10d XML elements." % count)

if __name__ == "__main__":
    main()