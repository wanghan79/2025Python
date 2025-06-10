from lxml import etree
from os import path
from optparse import OptionParser


class largeXMLDealer:
    """
    A class to deal with large XML files.
    """

    def __init__(self, func):
        """Constructor"""
        self.func = func

    def __call__(self, fileName, elemTag, bPrint=False, outputFile=None):
        """
        Process the XML file and call the provided function for each element.
        """
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
            try:
                self.func(elem, bPrint)
                if bPrint:
                    print(f"Processed element {count + 1}: {elem.tag}")
            except Exception as e:
                raise Exception(f"Something wrong in function parameter: {e}")
            finally:
                elem.clear()
                count += 1
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        del context

        if outputFile:
            with open(outputFile, 'w') as f:
                f.write(f"Parsed {count} XML elements.\n")
        else:
            print(f"Parsed {count} XML elements.")

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


def dealWithElement(elem, bPrint=True):
    """
    Function to process each XML element and its children recursively.
    """
    if bPrint:
        print(f"Element Tag: {elem.tag}, Text: {elem.text}")

    # Recursively process child elements
    for child in elem:
        dealWithElement(child, bPrint)


def main():
    """
    Main function to parse command-line arguments and call the XML processing function.
    """
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-p", "--print", dest="bPrint", default=True, action="store_true",
                      help="Print results on the screen.")
    parser.add_option("-o", "--output", type="string", dest="outputFile", default=None,
                      help="Output the results to a file.")
    parser.add_option("-t", "--tag", type="string", dest="tag", default="",
                      help="The XML tag interested to parse.")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("You have not input the XML file name")

    filePath = path.normpath(args[0])
    if not path.isfile(filePath) or not filePath.endswith("xml"):
        raise Exception("The input file is not exist or a valid XML file.")

    # Call the decorated function
    largeXMLDealer(dealWithElement)(filePath, options.tag, bPrint=options.bPrint, outputFile=options.outputFile)


if __name__ == "__main__":
    main()