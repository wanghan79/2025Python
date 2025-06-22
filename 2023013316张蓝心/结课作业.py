#!/usr/bin/env python
# coding:utf-8

from lxml import etree
from os import path
from optparse import OptionParser
from functools import wraps
import sys

# 临时模拟命令行参数
sys.argv = ["largeXMLDealerF1.py", "P00734.xml", "-t", "item", "-p"]


def xml_parser_decorator(func):
    """
    装饰器，用于处理XML解析和元素处理
    """

    @wraps(func)
    def wrapper(elem, *args, **kwargs):
        # 这里可以添加解析前的预处理
        result = func(elem, *args, **kwargs)
        # 这里可以添加解析后的后处理
        return result

    return wrapper


class largeXMLDealer:
    def __init__(self):
        pass

    def parse(self, fileName, elemTag, func4Element=None):
        """
        解析大型XML文件
        :param fileName: XML文件路径
        :param elemTag: 需要处理的元素标签
        :param func4Element: 处理元素的函数(将被装饰器装饰)
        """
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError

        count = 0
        es = ('end',)
        ns = self._getNamespace(fileName)
        ns = "{%s}" % ns

        # 装饰用户提供的处理函数
        decorated_func = xml_parser_decorator(func4Element) if func4Element else None

        context = etree.iterparse(fileName, events=es, tag=ns + elemTag)

        for event, elem in context:
            try:
                if decorated_func:
                    decorated_func(elem)
            except Exception:
                raise Exception("Error processing element with decorated function")
            finally:
                elem.clear()
                count += 1
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        del context
        return count

    def _getNamespace(self, fileName):
        """
        获取XML文件的命名空间
        """
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


# 示例处理函数，将被装饰器装饰
@xml_parser_decorator
def print_element(elem):
    """
    打印元素信息的示例函数
    """
    print(etree.tostring(elem, pretty_print=True, encoding='unicode'))


def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-p", "--print", dest="bPrint", default=False, action="store_true",
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
        raise Exception("The input file is not exist or a available XML file.")

    largXML = largeXMLDealer()

    # 根据选项决定使用哪个处理函数
    if options.bPrint:
        # 使用装饰过的打印函数
        count = largXML.parse(filePath, options.tag, print_element)
    else:
        # 如果没有指定处理函数，只计数
        count = largXML.parse(filePath, options.tag)

    print(f"Parsed {count:10d} XML elements.")


if __name__ == "__main__":
    main()