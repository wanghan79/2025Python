#!/usr/bin/env python
# coding:utf-8
"""
  Author:  H.Wang --<>
  Purpose: To parse the large XML files more than 500M
  Created: 4/4/2016
  Modified: [修改日期] - 修复了func4Element调用问题
"""

from lxml import etree
from os import path
from optparse import OptionParser
from functools import wraps


class largeXMLDealer:
    """
    A class for parsing large XML files efficiently
    """

    def __init__(self):
        """Constructor"""
        pass

    @staticmethod
    def parse_decorator(elemTag):
        """
        Decorator to parse XML file and process elements with given tag
        Args:
            elemTag: tag name to parse
        """

        def decorator(func):
            @wraps(func)
            def wrapper(fileName, *args, **kwargs):
                if not path.isfile(fileName) or not fileName.endswith("xml"):
                    raise FileNotFoundError("XML file not found or invalid file type")

                count = 0
                es = ('end',)
                dealer = largeXMLDealer()
                ns = dealer._getNamespace(fileName)
                ns = "{%s}" % ns if ns else ""  # Handle case when no namespace found

                context = etree.iterparse(fileName, events=es, tag=ns + elemTag)

                for event, elem in context:
                    try:
                        func(elem, *args, **kwargs)
                    except Exception as e:
                        raise Exception(f"Error processing element: {str(e)}")
                    finally:
                        elem.clear()
                        count += 1
                        # Clean up preceding siblings
                        while elem.getprevious() is not None:
                            del elem.getparent()[0]
                del context
                print(f"Already parsed {count} XML elements.")

            return wrapper

        return decorator

    def parse(self, fileName, elemTag, func4Element=None):
        """
        Parse XML file and process elements with given tag
        Args:
            fileName: path to XML file
            elemTag: tag name to parse
            func4Element: function to process each element
        Returns:
            count of parsed elements
        """
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError("XML file not found or invalid file type")

        count = 0
        es = ('end',)
        ns = self._getNamespace(fileName)
        ns = "{%s}" % ns if ns else ""  # Handle case when no namespace found

        context = etree.iterparse(fileName, events=es, tag=ns + elemTag)

        for event, elem in context:
            try:
                if func4Element:
                    func4Element(elem)
            except Exception as e:
                raise Exception(f"Error processing element: {str(e)}")
            finally:
                elem.clear()
                count += 1
                # Clean up preceding siblings
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        del context
        return count

    def _getNamespace(self, fileName):
        """
        Extract namespace from XML file
        Args:
            fileName: path to XML file
        Returns:
            namespace string or empty string if no namespace
        """
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError("XML file not found or invalid file type")

        result = ''
        es = ('start-ns',)
        context = etree.iterparse(fileName, events=es)
        try:
            for event, elem in context:
                if event == 'start-ns':
                    prefix, result = elem
                    break
        finally:
            del context
        return result


def main():
    """
    Main function to handle command line arguments and initiate parsing
    """
    usage = "usage: %prog [options] xml_file"
    parser = OptionParser(usage)
    parser.add_option("-p", "--print", dest="bPrint", default=False,
                      action="store_true", help="Print results on the screen.")
    parser.add_option("-o", "--output", type="string", dest="outputFile",
                      default=None, help="Output the results to a file.")
    parser.add_option("-t", "--tag", type="string", dest="tag",
                      default="", help="The XML tag to parse (required).")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("You must specify exactly one XML file")

    if not options.tag:
        parser.error("You must specify a tag name with -t/--tag option")

    filePath = path.normpath(args[0])
    if not path.isfile(filePath) or not filePath.endswith("xml"):
        raise Exception("The input file does not exist or is not a valid XML file.")

    # Define element processing function based on options
    def element_handler(elem):
        """Handle XML element based on command line options"""
        elem_str = etree.tostring(elem, encoding="unicode", pretty_print=True)
        if options.bPrint:
            print(elem_str)
        if options.outputFile:
            with open(options.outputFile, "a", encoding="utf-8") as f:
                f.write(elem_str + "\n")

    # Initialize and parse
    xml_dealer = largeXMLDealer()
    try:
        count = xml_dealer.parse(filePath, options.tag,
                                 func4Element=element_handler if (options.bPrint or options.outputFile) else None)
        print(f"Successfully parsed {count} '{options.tag}' elements.")
    except Exception as e:
        print(f"Error occurred: {str(e)}")


if __name__ == "__main__":
    main()