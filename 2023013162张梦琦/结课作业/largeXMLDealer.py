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
    """大型XML文件处理修饰器类"""
    
    def __init__(self, elemTag):
        """构造函数，接收元素标签"""
        self.elemTag = elemTag
    
    def __call__(self, func):
        """使实例可调用，实现修饰器功能"""
        
        def wrapped(fileName):
            if not path.isfile(fileName) or not fileName.endswith("xml"):
                raise FileNotFoundError(f"文件 {fileName} 不存在或不是XML文件")
            
            count = 0
            es = ('end',)
            ns = self._getNamespace(fileName)
            ns = "{%s}" % ns
            
            context = etree.iterparse(fileName, events=es, tag=ns + self.elemTag)
            
            for event, elem in context:
                try:
                    # 调用被修饰的函数处理元素
                    func(elem)
                except Exception as e:
                    raise Exception(f"处理元素时出错: {str(e)}")
                finally:
                    elem.clear()
                    count += 1
                    while elem.getprevious() is not None:
                        del elem.getparent()[0]
            del context
            print(f"已解析 {count} 个XML元素。")
            return count
        
        return wrapped
    
    def _getNamespace(self, fileName):
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
