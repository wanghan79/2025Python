from optparse import OptionParser
from os import path
from lxml import etree


class largeXMLDealer:

    def __init__(self, fileName, elemTag):
        """Constructor"""

    def parse(self, fileName, elemTag, func4Element = None):
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
            func4Element(elem)
            try:
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


    def __call__(self,func):
        def wrapper():
            fileName = self.fileName
            elemTag = self.elemTag
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
                    func(elem)
                except Exception:
                    raise Exception("Something wrong in function parameter: func4Element")
                finally:
                    elem.clear()
                    count = count + 1
                    while elem.getprevious() is not None:
                        del elem.getparent()[0]
            del context
            return count
        return wrapper

def main():
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

    # Check the correction of users input and call the functions of class DoSomething.
    if (len(args) != 1):
        parser.error("You have not input the XML file name")

    filePath = path.normpath(args[0])
    if not path.isfile(filePath) or not filePath.endswith("xml"):
        raise Exception("The input file is not exist or a vailable XML file.")


    # Call XML parser
    # largeXML = largeXMLDealer()
    @largeXMLDealer(filePath, options.tag)
    def callDealer(item):
        """"""
        if isinstance(item, object):
            print(item.text)


    # num = largeXML.parse(filePath, options.tag,dealWithElement)
    num = callDealer()
    print("Parsed %10d XML elements." % num)


if __name__ == "__main__":
    main()

# Linux Command Line Example:
# python3 largeXMLDealer.py -t entry /home/Biodata/OrignalData/Protein/Uniprot/current/uniprot_sprot.xml
