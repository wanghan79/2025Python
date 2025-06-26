"""
    Purpose: To parse large XML files
    Created: 2025/05/27
"""

from lxml import etree
from os import path
from functools import wraps
from optparse import OptionParser

class XMLParser:
    """A class decorator to parse large XML files and apply a function to each element."""

    def __init__(self, func):
        """Constructor"""
        self.func = func
        wraps(func)(self)

    def __call__(self, file_name, element_tag):
        """Call method to parse the XML file and apply the decorated function."""
        if not path.isfile(file_name) or not file_name.endswith("xml"):
            raise FileNotFoundError("The input file is not a valid XML file.")

        count = 0
        events = ('end',)
        namespace = self._get_namespace(file_name)
        namespace = "{%s}" % namespace

        context = etree.iterparse(file_name, events=events, tag=namespace + element_tag)

        for event, element in context:
            try:
                self.func(element)
            except Exception as e:
                raise Exception(f"Error in function parameter: {e}")
            finally:
                element.clear()
                count += 1
                while element.getprevious() is not None:
                    del element.getparent()[0]
        del context
        return count

    def _get_namespace(self, file_name):
        """Get the namespace from the XML file."""
        if not path.isfile(file_name) or not file_name.endswith("xml"):
            raise FileNotFoundError("The input file is not a valid XML file.")
        result = ''
        events = ('start-ns',)
        context = etree.iterparse(file_name, events=events)
        for event, elem in context:
            prefix, result = elem
            break
        del context
        return result


def main():
    """
    Main function to parse command line arguments and call the XML parser.
    """
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-t", "--tag", type="string", dest="tag", default="",
                      help="The XML tag to parse.")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("You have not input the XML file name")

    file_path = path.normpath(args[0])
    if not path.isfile(file_path) or not file_path.endswith("xml"):
        raise Exception("The input file does not exist or is not a valid XML file.")

    def process_element(element):
        if isinstance(element, object):
            print(element.text)

    xml_parser = XMLParser(process_element)
    count = xml_parser(file_path, options.tag)
    print(f"Parsed {count} XML elements.")


if __name__ == "__main__":
    main()