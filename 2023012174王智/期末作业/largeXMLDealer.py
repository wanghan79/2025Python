from lxml import etree
from os import path
from optparse import OptionParser
from functools import wraps


class XMLParserDecorator:
    """
    XML Parser Decorator Class
    """

    def __init__(self, func):
        """Constructor"""
        self.func = func
        wraps(func)(self)

    def __call__(self, fileName, elemTag, bPrint=False, outputFile=None):
        """"""
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError("The input file is not a valid XML file.")

        count = 0
        es = ('end',)
        ns = self._getNamespace(fileName)
        ns = "{%s}" % ns

        context = etree.iterparse(fileName, events=es, tag=ns + elemTag)

        for event, elem in context:
            # Call the decorated function to deal with the element here
            try:
                self.func(elem, bPrint=bPrint)
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
            break
        del context
        return result


@XMLParserDecorator
def dealWithElement(elem, bPrint=True):
    """Function to handle the element"""
    if elem.text and bPrint:
        # 输出标签和文本内容
        print(f"Element Text: {elem.text}")


@XMLParserDecorator
def reverse_print(elem, bPrint=True):
    """Function to print element text in reverse order"""
    if elem.text and bPrint:
        # 反转文本内容并输出
        reversed_text = elem.text[::-1]
        print(f"Reversed Text: {reversed_text}")


def main():
    """

    """
    # Construct the usage.
    print("Large XML Dealer is running...")
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

    # Check the correction of users input and call the decorated functions.
    if len(args) != 1:
        parser.error("You have not input the XML file name")

    filePath = path.normpath(args[0])
    if not path.isfile(filePath) or not filePath.endswith("xml"):
        raise Exception("The input file is not exist or a valid XML file.")


if __name__ == "__main__":
    main()
