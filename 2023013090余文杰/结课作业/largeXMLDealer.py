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


class largeXMLDealer:
    """

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
            # print("%s, %d"%(elem, len(elem)))
            break
        del context
        return result


class XMLDealerDecorator:
    def __init__(self, wrapped_class):
        self.wrapped_class = wrapped_class

    def __call__(self, *args, **kwargs):
        instance = self.wrapped_class(*args, **kwargs)
        original_parse = instance.parse

        def enhanced_parse(fileName, elemTag, callback):
            elements_text = []

            def capture_element(elem):
                text_content = elem.text.strip() if elem.text else ""
                elements_text.append(text_content)
                if callback:
                    callback(elem)

            result = original_parse(fileName, elemTag, capture_element)

            print("=== XML Parsing Result ===")
            for i, text in enumerate(elements_text, 1):
                print(f"Element {i}: {text}")
            print("=========================")

            return result

        instance.parse = enhanced_parse
        return instance


class XMLParserDecorator:
    """
    装饰器类，用于解析大型 XML 文件并逐个处理指定标签的元素。
    """

    def __init__(self, elem_tag):
        self.elem_tag = elem_tag  # 需要解析的 XML 标签

    def __call__(self, func):
        def wrapped_func(filename, *args, **kwargs):
            if not path.isfile(filename) or not filename.endswith(".xml"):
                raise FileNotFoundError(f"Invalid XML file: {filename}")

            count = 0
            ns = self._get_namespace(filename)
            full_tag = f"{{{ns}}}{self.elem_tag}" if ns else self.elem_tag

            context = etree.iterparse(filename, events=("end",), tag=full_tag)

            for event, elem in context:
                try:
                    func(elem, *args, **kwargs)  # 调用用户定义的函数处理当前元素
                finally:
                    elem.clear()
                    while elem.getprevious() is not None:
                        del elem.getparent()[0]
                    count += 1

            print(f"Already parsed {count} XML elements.")
            return count

        return wrapped_func

    def _get_namespace(self, filename):
        """获取 XML 文件的默认命名空间"""
        context = etree.iterparse(filename, events=("start-ns",))
        for event, elem in context:
            prefix, ns_uri = elem
            return ns_uri
        return ""



def main():
    """

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
# Linux Command Line Example:
# python3 largeXMLDealer.py -t entry /home/Biodata/OrignalData/Protein/Uniprot/current/uniprot_sprot.xml
