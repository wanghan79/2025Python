#!/usr/bin/env python
# coding:utf-8
"""
  Author:  H.Wang --<>
  Purpose: To parse the large XML files more than 500M
  Created: 4/4/2016
  Modified: 使用装饰器模式重构
"""

from lxml import etree
from os import path
from optparse import OptionParser
import functools


def largeXMLDealer(func):
    """
    装饰器函数，用于解析大型XML文件
    """
    @functools.wraps(func)
    def wrapper(fileName, elemTag, *args, **kwargs):
        if not path.isfile(fileName) or not fileName.endswith("xml"):
            raise FileNotFoundError("文件不存在或不是XML文件")

        count = 0
        es = ('end',)
        ns = _getNamespace(fileName)
        ns = "{%s}" % ns

        context = etree.iterparse(fileName, events=es, tag=ns + elemTag)

        for event, elem in context:
            # 调用被装饰的函数处理元素
            try:
                func(elem, *args, **kwargs)
            except Exception as e:
                raise Exception(f"处理元素时出错: {str(e)}")
            finally:
                elem.clear()
                count = count + 1
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        del context
        # 返回解析的元素数量
        return count
    
    return wrapper


def _getNamespace(fileName):
    """获取XML命名空间"""
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


def main():
    """
    命令行入口函数
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
    
    # 简单的处理函数示例
    @largeXMLDealer
    def process_element(elem):
        print(elem.text)
    
    # 调用装饰后的函数
    count = process_element(filePath, options.tag)
    print("Parsed %10d XML elements." % count)


if __name__ == "__main__":
    main()
# Linux Command Line Example:
# python3 largeXMLDealer.py -t entry /home/Biodata/OrignalData/Protein/Uniprot/current/uniprot_sprot.xml
