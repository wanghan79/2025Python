
"""
    Purpose: To parse the large XML files
    Created: 2025/05/28
"""

from lxml import etree
from os import path
from functools import wraps
from optparse import OptionParser

class largeXMLDealer:
    """A class decorator to parse large XML files and apply a function to each element."""

    def __init__(self, func):
        """Constructor"""
        self.func = func
        wraps(func)(self)

    def __call__(self, fileName, elemTag):
        """Call method to parse the XML file and apply the decorated function."""
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError("The input file is not a valid XML file.")

        count = 0
        es = ('end',)
        ns = self._getNamespace(fileName)
        ns = "{%s}" % ns

        context = etree.iterparse(fileName, events=es, tag=ns + elemTag)

        for event, elem in context:
            try:
                self.func(elem)
            except Exception as e:
                raise Exception(f"Something wrong in function parameter: {e}")
            finally:
                elem.clear()
                count += 1
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        del context
        return count

    def _getNamespace(self, fileName):
        """Get the namespace from the XML file."""
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


def main():
    """
    Main function to parse command line arguments and call the XML parser.
    """
    # Construct the usage.
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-t", "--tag", type="string", dest="tag", default="",
                    help="The XML tag interested to parse.")

    # Parse the options and args input by users.
    (options, args) = parser.parse_args()

    # Check the correction of users input and call the functions of class DoSomething.
    if len(args) != 1:
        parser.error("You have not input the XML file name")

    filePath = path.normpath(args[0])
    if not path.isfile(filePath) or not filePath.endswith("xml"):
        raise Exception("The input file is not exist or a vailable XML file.")

    # Define a function to deal with each element
    def dealwithElement(elem):
        if isinstance(elem, object):
            print(elem.text)

    # Call XML parser
    lxmld = largeXMLDealer(dealwithElement)
    count = lxmld(filePath, options.tag)
    print(f"Parsed {count} XML elements.")


if __name__ == "__main__":
    main()
