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
from functools import wraps


class largeXMLDealer:
    """
    
    """

    def __init__(self, func):
        """Constructor"""
        self.func = func
        wraps(func)(self)

    def __call__(self, fileName, elemTag,  bPrint=False, outputFile=None):
        """"""
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError("The input file is not a valid XML file.")

        count = 0
        es = ('end',)
        ns = self._getNamespace(fileName)
        ns = "{%s}" % ns

        context = etree.iterparse(fileName, events=es, tag=ns + elemTag)

        if bPrint:
            print(f"Processing elements with tag: {elemTag}")

        for event, elem in context:
            # Call the outside function to deal with the element here
            try:
                self.func(elem, bPrint=bPrint)
                process_nested(elem, bPrint)
                if bPrint:
                    print(f"Processed element {count + 1}: {elem.tag}")
            except Exception as e:
                raise Exception(f"Something wrong in function parameter: {e}")
            finally:
                elem.clear()
                count = count + 1
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        del context
        # Return how many elements had been parsed
        if outputFile:
            with open(outputFile, 'w') as f:
                f.write(f"Parsed {count} XML elements.\n")
        else:
            print(f"Parsed {count} XML elements.")

        return count

    def _getNamespace(self, fileName):
        """"""
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError("The input file is not a valid XML file.")
        result = ''
        es = ('start-ns',)
        context = etree.iterparse(fileName, events=es)
        for event, elem in context:
            prefix, result = elem
            # print("%s, %d"%(elem, len(elem)))
            break
        del context
        return result


@largeXMLDealer
def dealWithElement(elem, bPrint=True, recursive_func=None):
    """处理当前元素，递归由单独函数实现"""
    if bPrint:
        print(f"Current Tag: {elem.tag}, Text: {elem.text}")

def process_nested(elem, bPrint=True):
    """独立递归函数"""
    if bPrint:
        print(f"Processing Tag: {elem.tag}, Text: {elem.text}")
    for child in elem:
        process_nested(child, bPrint)


def main():
    """
    
    """
    # Construct the usage.
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-p", "--print", dest="bPrint", default=True, action="store_true",
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

    # Call the decorated function
    dealWithElement(filePath, options.tag, bPrint=options.bPrint, outputFile=options.outputFile)


if __name__ == "__main__":
    main()
# Linux Command Line Example:
# python3 largeXMLDealer.py -t entry /home/Biodata/OrignalData/Protein/Uniprot/current/uniprot_sprot.xml

#python C:\Users\HUAWEI\PycharmProjects\PythonProject\案例分析\largeXMLDealer.py -t lineage C:\Users\HUAWEI\PycharmProjects\PythonProject\案例分析\P00734.xml
