#!/usr/bin/env python
# coding:utf-8
"""
  Author:  H.Wang --<>
  Purpose: To parse the large XML files more than 500M
  Created: 4/4/2016
"""

from lxml import etree
from os import path

class XMLDealer:
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, fileName, elemTag):
        self.parse(fileName, elemTag)
        print(f"Already parsed {self.count} XML elements.")

    def parse(self, fileName, elemTag):
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError

        es = ('end',)
        ns = self._getNamespace(fileName)
        ns = "{%s}" % ns

        context = etree.iterparse(fileName, events=es, tag=ns + elemTag)

        for event, elem in context:
            try:
                self.func(elem)
            except Exception as e:
                raise Exception("Something wrong in function parameter: func") from e
            finally:
                elem.clear()
                self.count += 1
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        del context

    def _getNamespace(self, fileName):
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

# 导出修饰器类
__all__ = ['XMLDealer']

def main():
    """
    主函数，处理命令行参数并调用XML解析器
    """
    # Construct the usage.
    usage = "usage: %prog [options] <xml_file>"
    parser = OptionParser(usage)
    parser.add_option("-p", "--print", dest="bPrint", default=False, action="store_true",
                      help="Print results on the screen.")
    parser.add_option("-o", "--output", type="string", dest="outputFile", default=None,
                      help="Output the results to a file.")
    parser.add_option("-t", "--tag", type="string", dest="tag", default="",
                      help="The XML tag interested to parse.")

    # Parse the options and args input by users.
    (options, args) = parser.parse_args()

    # Check the correction of users input
    if len(args) != 1:
        parser.error("请提供XML文件路径作为参数")

    filePath = path.normpath(args[0])
    if not path.isfile(filePath) or not filePath.endswith("xml"):
        parser.error(f"文件不存在或不是有效的XML文件: {filePath}")

    if not options.tag:
        parser.error("请使用 -t 选项指定要解析的XML标签")

    # 添加处理元素的函数
    def process_element(elem):
        # 这里可以写对元素的处理逻辑，比如打印元素标签等
        print(elem.tag)
        # 如果tag是'sequence'，你可能想获取序列内容
        if elem.tag.endswith('sequence'):
            print(f"序列内容: {elem.text}")

    # Call XML parser，注意这里添加了第三个参数
    largXML = largeXMLDealer()
    count = largXML.parse(filePath, options.tag, process_element)
    print("Parsed %10d XML elements." % count)


if __name__ == "__main__":
    main()
# Linux Command Line Example:
# python3 largeXMLDealer.py -t entry /home/Biodata/OrignalData/Protein/Uniprot/current/uniprot_sprot.xml
