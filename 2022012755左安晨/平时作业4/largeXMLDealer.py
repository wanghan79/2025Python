#!/usr/bin/env python
# coding:utf-8
"""
  Author:  Zuoanchen--<>
  Created: 6/10/2025
"""

from lxml import etree
from os import path
from optparse import OptionParser
from functools import wraps


def xml_parser(fileName, elemTag):
    """
    Decorator factory to handle XML parsing and pass elements to the decorated function
    """

    def decorator(func):
        @wraps(func)
        def wrapper():
            if not path.isfile(fileName) or not fileName.endswith("xml"):
                raise FileNotFoundError

            count = 0
            es = ('end',)
            ns = wrapper._getNamespace(fileName)
            ns = "{%s}" % ns

            context = etree.iterparse(fileName, events=es, tag=ns + elemTag)

            for event, elem in context:
                # Call the decorated function with the element
                try:
                    func(elem)
                except Exception:
                    raise Exception("Something wrong in the decorated function")
                finally:
                    elem.clear()
                    count = count + 1
                    while elem.getprevious() is not None:
                        del elem.getparent()[0]
            del context
            # Return how many elements had been parsed
            print(f"Already parsed {count} XML elements.")
            return count

        def _getNamespace(fileName):
            """Helper method to get namespace"""
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

        wrapper._getNamespace = _getNamespace
        return wrapper

    return decorator


class largeXMLDealer:
    """
    Class to handle large XML files
    """

    def __init__(self):
        """Constructor"""
        pass

    def parse(self, fileName, elemTag, func4Element=None):
        """
        Parse XML file and process elements with the given function
        """
        if func4Element:
            @xml_parser(fileName, elemTag)
            def decorated_parser(elem):
                func4Element(elem)

            return decorated_parser()
        else:
            @xml_parser(fileName, elemTag)
            def decorated_parser(elem):
                print(elem.text)

            return decorated_parser()


def main():
    """
    Main function for command line execution
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


if __name__ == "__main__":
    main()